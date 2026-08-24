#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "aiohttp>=3.9.0",
# ]
# ///

"""Offline tests for keenetic_cli.py.

Run with `uv run tests/test_keenetic_cli.py`. Nothing here contacts the router:
every case exercises a pure function or a hand-written fake client.

keenetic_cli.py is deliberately a single script rather than a package, so it is
loaded by path. It must be registered in sys.modules before exec_module, because
the @dataclass decorator on RouterConfig resolves annotations through the module.
"""

from __future__ import annotations

import asyncio
import contextlib
import importlib.util
import io
import os
import sys
from datetime import datetime
from pathlib import Path

# multidict ships with aiohttp; the auth-header test needs the real
# case-insensitive mapping the router response actually carries.
from multidict import CIMultiDict

SCRIPT = Path(__file__).resolve().parent.parent / "keenetic_cli.py"
_spec = importlib.util.spec_from_file_location("keenetic_cli", SCRIPT)
assert _spec and _spec.loader
kc = importlib.util.module_from_spec(_spec)
sys.modules["keenetic_cli"] = kc
_spec.loader.exec_module(kc)


FAILURES: list[str] = []
TESTS: list = []


def test(func):
    TESTS.append(func)
    return func


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_blocked(method: str, endpoint: str, **kwargs) -> None:
    try:
        kc.ensure_safe_router_request(method, endpoint, False, **kwargs)
    except kc.CliError:
        return
    raise AssertionError(f"{method} {endpoint!r} should require --unsafe but was allowed")


def assert_allowed(method: str, endpoint: str, **kwargs) -> None:
    try:
        kc.ensure_safe_router_request(method, endpoint, False, **kwargs)
    except kc.CliError as err:
        raise AssertionError(f"{method} {endpoint!r} should be allowed but was blocked: {err}")


# --------------------------------------------------------------------------
# The unsafe-request gate. A bypass here means an agent can reboot or
# reconfigure a live router while the operator only asked it to look at
# something, so the allow-list is asserted as tightly as the deny-list.
# --------------------------------------------------------------------------


@test
def plain_reads_are_allowed_without_unsafe():
    for endpoint in (
        "/rci/show/interface",
        "/rci/show/interface/stat?name=Wireguard0",
        "/rci/show/ip/hotspot/host",
        "/rci/ip/policy",
        "/rci/show/version",
    ):
        assert_allowed("GET", endpoint)


@test
def action_paths_require_unsafe():
    for endpoint in (
        "/rci/system/configuration/save",
        "/rci/system/reboot",
        "/rci/system/configuration/factory-reset",
        "/rci/components/commit",
        "/rci/interface/Wireguard0/down",
        "/rci/copy",
    ):
        assert_blocked("GET", endpoint)


@test
def action_paths_are_matched_after_percent_decoding():
    # yarl percent-decodes before the request goes on the wire, so matching the
    # raw string would let this through as the literal segment "%73ave".
    assert_blocked("GET", "/rci/system/configuration/%73ave")
    assert_blocked("GET", "/rci/system/sa%76e")
    assert_blocked("GET", "/rci/system/re%62oot")


@test
def action_paths_are_matched_case_insensitively():
    assert_blocked("GET", "/rci/system/configuration/SAVE")
    assert_blocked("GET", "/rci/system/configuration/Save")
    assert_blocked("GET", "/rci/system/REBOOT")


@test
def a_fragment_cannot_hide_an_action_segment():
    # The HTTP client drops the fragment, so "save#" reaches the router as "save".
    assert_blocked("GET", "/rci/system/configuration/save#")
    assert_blocked("GET", "/rci/system/reboot#anything")


@test
def dot_segments_are_resolved_before_matching():
    assert_blocked("GET", "/rci/show/../system/configuration/save")


@test
def a_dot_segment_cannot_cancel_an_action_segment():
    # An encoded separator is not a separator on the wire -- yarl leaves %2F alone, so
    # the router still receives a path naming the action -- but decoding it here made
    # `..` cancel the segment in front of it, and the gate then judged a path the
    # router will never see. Resolving `..` may only ever add candidates.
    assert_blocked("GET", "/rci/system/reboot%2F..")
    assert_blocked("GET", "/rci/system/configuration/save%2f..")
    assert_blocked("GET", "/rci/system/configuration/save/..")
    assert_blocked("GET", "/rci/system/configuration?save%2f..")
    # A trailing dot is decoration the router's parser may well trim.
    assert_blocked("GET", "/rci/system/configuration/save%2e")
    # Ordinary reads keep working.
    assert_allowed("GET", "/rci/show/interface")
    assert_allowed("GET", "/rci/show/ip/hotspot/../hotspot")


@test
def the_returned_endpoint_is_what_gets_sent():
    check(
        kc.ensure_safe_router_request("GET", "/rci/show/interface#frag", False)
        == "/rci/show/interface",
        "gate must strip the fragment from the endpoint it returns",
    )
    check(
        kc.ensure_safe_router_request("GET", "/rci/show/interface/stat?name=X", False)
        == "/rci/show/interface/stat?name=X",
        "gate must preserve the query string",
    )


@test
def non_get_methods_require_unsafe():
    for method in ("POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "post"):
        assert_blocked(method, "/rci/show/interface")


@test
def a_get_carrying_a_body_requires_unsafe():
    # A nested command expressed as a GET body is invisible to the path check.
    assert_blocked("GET", "/rci/", has_body=True)
    assert_allowed("GET", "/rci/", has_body=False)


@test
def unsafe_permits_everything_and_still_sanitizes():
    check(
        kc.ensure_safe_router_request("POST", "/rci/system/reboot#x", True)
        == "/rci/system/reboot",
        "--unsafe must still return a fragment-free endpoint",
    )


@test
def an_endpoint_may_not_retarget_the_host():
    # The endpoint is concatenated onto the router base URL, so "@host/..." turns the
    # router's host:port into userinfo and sends the request somewhere else entirely.
    for endpoint in (
        "@evil.example/rci/show/version",
        "//evil.example/rci/show/version",
        "http://evil.example/rci/show/version",
        "rci/show/version",
        "",
    ):
        assert_blocked("GET", endpoint)


@test
def host_retargeting_is_blocked_even_with_unsafe():
    # This check is about which machine is contacted, not about what is run there,
    # so opting in to a write must not waive it.
    for endpoint in ("@evil.example/rci/", "//evil.example/rci/"):
        try:
            kc.ensure_safe_router_request("POST", endpoint, True)
        except kc.CliError:
            continue
        raise AssertionError(f"--unsafe must not permit retargeting to {endpoint!r}")


@test
def documented_action_verbs_require_unsafe():
    # Every one of these is a documented command in keenetic_api_docs/ whose effect
    # is not a read: clearing the log destroys the diagnostics `show log` exists for.
    for endpoint in (
        "/rci/system/log/clear",
        "/rci/system/eject",
        "/rci/interface/connect",
        "/rci/interface/traffic-counter/action/disconnect",
        "/rci/interface/ip/dhcp/client/release",
        "/rci/interface/ip/dhcp/client/renew",
        "/rci/sms/delete",
        "/rci/interface/chilli/logout",
    ):
        assert_blocked("GET", endpoint)


@test
def trailing_decoration_does_not_hide_an_action_segment():
    # `save%00` and `save%20` reach the router verbatim; whether its parser trims
    # them is not verifiable from this side, so the gate trims before matching.
    for endpoint in (
        "/rci/system/configuration/save%00",
        "/rci/system/configuration/save%20",
        "/rci/system/configuration/%09save",
    ):
        assert_blocked("GET", endpoint)


@test
def an_embedded_control_character_does_not_splice_an_action_segment_away():
    # Deleting the control character joins the halves either side of it, turning
    # `save%00x` into `savex` -- which is in no deny-list. The RCI engine is native
    # code and a C string stops at the NUL, so the router still sees `save`.
    for endpoint in (
        "/rci/system/configuration/save%00x",
        "/rci/system/reboot%00zzz",
        "/rci/system/reboot%01a",
        "/rci/system/configuration?save%00x",
        "/rci/system/configuration?reboot%1fy=1",
    ):
        assert_blocked("GET", endpoint)
    # Splicing must still be checked too: a control character *inside* a word does
    # not make that word an action.
    assert_allowed("GET", "/rci/show/ver%00sion")


@test
def a_semicolon_does_not_hide_an_action_segment():
    # parse_qsl stopped splitting on `;` in 3.10 and RFC 3986 path parameters use it,
    # so the router may read `reboot;x` as `reboot` where this side reads one opaque
    # token.
    for endpoint in (
        "/rci/system/reboot;x",
        "/rci/system/configuration?save;x",
        "/rci/system/configuration?x=1;save",
    ):
        assert_blocked("GET", endpoint)
    # A semicolon in a value that names no action stays allowed.
    assert_allowed("GET", "/rci/show/interface?name=Home;Guest")


@test
def a_malformed_method_is_a_cli_error_not_a_traceback():
    # aiohttp raises ValueError deep in the stack for a non-token method, which the
    # consuming agent would see as a traceback rather than an "Error:" line.
    for method in (" ge t ", "GET\r\nX-Injected: 1", "", "G3T"):
        try:
            kc.ensure_safe_router_request(method, "/rci/show/version", False)
        except kc.CliError:
            continue
        raise AssertionError(f"method {method!r} should be rejected")
    # Surrounding whitespace and case alone stay acceptable.
    assert_allowed(" get ", "/rci/show/version")


# --------------------------------------------------------------------------
# Redaction
# --------------------------------------------------------------------------


@test
def secret_keys_are_redacted():
    for key in ("private-key", "preshared_key", "password", "api-token", "psk", "key"):
        result = kc.redact_sensitive({key: "s3cret"})
        check(result[key] == kc.REDACTED, f"{key!r} should be redacted, got {result[key]!r}")


@test
def incidental_key_matches_are_not_redacted():
    # Substring matching on "key" destroyed ordinary diagnostic fields.
    for key in ("keyword", "monkey", "key-length", "keepalive"):
        result = kc.redact_sensitive({key: "visible"})
        check(result[key] == "visible", f"{key!r} should not be redacted, got {result[key]!r}")


@test
def secrets_inside_string_values_are_redacted():
    # `show running-config` returns configuration as plain text lines.
    config = ["interface Wireguard0", "    private-key AAAABBBBCCCC"]
    result = kc.redact_sensitive({"message": config})
    check(
        kc.REDACTED in result["message"][1] and "AAAABBBBCCCC" not in result["message"][1],
        f"private-key value should be redacted, got {result['message'][1]!r}",
    )


@test
def running_config_directives_are_redacted_when_the_keyword_is_not_first():
    # `show running-config` prints the command words in front of the keyword
    # (06_commands_show.md renders `authentication wpa-psk ns3 <psk>`), so anchoring
    # to the first word of the line leaked the Wi-Fi PSK, the WireGuard private key
    # and the IPsec PSK -- all reachable as a plain GET with no --unsafe.
    secrets = {
        "                 authentication wpa-psk ns3 BMc1we4ZX9/fbJtDiM": "BMc1we4ZX9/fbJtDiM",
        "                 wireguard private-key UshaeghezaiJ7reo8X5uo=": "UshaeghezaiJ7reo8X5uo=",
        "                 ipsec preshared-key gbp1gW3pBQK.g=": "gbp1gW3pBQK.g=",
        "                 macpasswd s3cretvalue": "s3cretvalue",
    }
    for line, secret in secrets.items():
        result = kc.redact_text(line)
        check(secret not in result, f"secret leaked from {line!r}: {result!r}")
        check(kc.REDACTED in result, f"{line!r} should be redacted, got {result!r}")


@test
def secret_bearing_directives_behind_command_words_are_redacted():
    # The keyword-first anchor and the compound-keyword list between them missed a
    # whole family of documented directives whose secret sits behind one or two
    # command words. Every one of these is reachable through a read-only
    # `show running-config`, so a miss leaks the credential with redaction still on.
    secrets = {
        "     iapp key ns3 4k/XpM98jF123131NK9eur5Jk7Cgq4PpBm4M6U": "4k/XpM98jF123131NK9eur5Jk7Cgq4PpBm4M6U",
        "     encryption key 1 1231231234": "1231231234",
        "     wireguard obfs-key 5(-3*3RA{2&kay)_BbQs5a": "5(-3*3RA{2&kay)_BbQs5a",
        "     obfs-key 5(-3*3RA{2&kay)_BbQs5a": "5(-3*3RA{2&kay)_BbQs5a",
        "     xauth-password Aihoi2cha1": "Aihoi2cha1",
        "     authentication password Aihoi2cha1": "Aihoi2cha1",
        "     web-api password hunter2": "hunter2",
        "     chilli radiussecret sharedvalue": "sharedvalue",
        "     chilli uamsecret sharedvalue": "sharedvalue",
        "     chilli login 1.2.3.4 username bob password s3cretvalue": "s3cretvalue",
        "     wps self-pin 12345670": "12345670",
        "     wps peer aa:bb:cc:dd:ee:ff 12345670": "12345670",
    }
    for line, secret in secrets.items():
        result = kc.redact_text(line)
        check(secret not in result, f"secret leaked from {line!r}: {result!r}")
        check(kc.REDACTED in result, f"{line!r} should be redacted, got {result!r}")


@test
def nextdns_account_credentials_are_redacted():
    # `nextdns authtoken <authtoken>` and `nextdns authenticate <login> <password>
    # [<pin>]` (05_commands_mws_ndns_opkg_services.md) both carry NextDNS account
    # credentials through `show running-config`, nested under the `nextdns` section so
    # the command word is gone. "authtoken" is one word, so the \b in front of the
    # ambiguous "token" never fired inside it, and "authenticate" carries no secret
    # keyword at all.
    secrets = {
        "    authtoken 1f2a36": "1f2a36",
        "    nextdns authtoken 1f2a36": "1f2a36",
        "authtoken: 1f2a36": "1f2a36",
        "    authenticate account@gmail.com 123456789 1234": "123456789",
    }
    for line, secret in secrets.items():
        result = kc.redact_text(line)
        check(secret not in result, f"secret leaked from {line!r}: {result!r}")
        check(kc.REDACTED in result, f"{line!r} should be redacted, got {result!r}")
    # The account name is not a credential and stays readable.
    check(
        "account@gmail.com" in kc.redact_text("    authenticate account@gmail.com 123456789 1234"),
        "the login should survive redaction",
    )
    # "authenticate" is an ordinary verb, so an unindented log line stays intact.
    prose = "ndm: Core::Session: authenticate failed for user bob."
    check(kc.redact_text(prose) == prose, f"log prose was mangled: {kc.redact_text(prose)!r}")


@test
def an_explicitly_named_default_env_file_is_still_explicit():
    # argparse defaulting --env-file to ".env" could not tell omission apart from
    # `--env-file .env`, so the named file silently lost to exported KEENETIC_*
    # variables and a missing one was tolerated.
    check(kc.resolve_env_file_arg(None) == (kc.DEFAULT_ENV_FILE, False), "omission must not be explicit")
    check(kc.resolve_env_file_arg(".env") == (".env", True), "`--env-file .env` must be explicit")
    check(kc.resolve_env_file_arg("other.env") == ("other.env", True), "a named file must be explicit")
    parser = kc.build_parser()
    omitted = parser.parse_args(["show", "interfaces"])
    check(omitted.env_file is None, f"the default must be the None sentinel, got {omitted.env_file!r}")
    named = parser.parse_args(["--env-file", ".env", "show", "interfaces"])
    check(named.env_file == ".env", f"an explicit .env was lost: {named.env_file!r}")


@test
def the_wep_key_id_is_what_tells_the_directive_from_prose():
    # A WEP key is all hex digits, so the key-shaped-token guard used for `psk` would
    # miss it; the documented `encryption key <id>` argument is the guard instead.
    prose = "wmond: encryption key mismatch on WifiMaster0"
    check(kc.redact_text(prose) == prose, f"log prose was mangled: {kc.redact_text(prose)!r}")
    directive = kc.redact_text("     encryption key 2 abcd1234ef")
    check("abcd1234ef" not in directive, f"WEP key leaked: {directive!r}")


@test
def log_prose_is_not_mistaken_for_a_secret_directive():
    # The output is parsed by an agent as router state, so redaction must not eat
    # ordinary words. "psk" is the risky one: it is compound enough to appear
    # mid-line, and common enough to appear in log prose.
    intact = (
        "ppp: password authentication failed",
        "wpa-psk handshake completed for aa:bb:cc:dd:ee:ff",
        "Token Ring PC",
        "key-length 2048",
    )
    for line in intact:
        check(kc.redact_text(line) == line, f"{line!r} was mangled into {kc.redact_text(line)!r}")


@test
def router_status_messages_are_redacted():
    # Status messages are printed to stderr and land in the agent's transcript, and
    # the router echoes the rejected value back.
    body = [{"status": [
        {"status": "error", "message": "bad value for private-key: UshaeghezaiJ7reo8iK6=="}]}]
    messages = kc.collect_rci_errors(body)
    check("UshaeghezaiJ7reo8iK6==" not in messages[0], f"secret leaked: {messages[0]!r}")
    check(kc.REDACTED in messages[0], f"expected a redaction marker, got {messages[0]!r}")


@test
def redaction_recurses_into_nested_structures():
    result = kc.redact_sensitive({"peer": [{"public-key": "abc", "endpoint": "1.2.3.4"}]})
    check(result["peer"][0]["public-key"] == kc.REDACTED, "nested key not redacted")
    check(result["peer"][0]["endpoint"] == "1.2.3.4", "non-secret sibling was altered")


@test
def error_bodies_are_redacted_and_truncated():
    described = kc.describe_response_body({"password": "hunter2"})
    check("hunter2" not in described, f"secret leaked into error text: {described}")
    long_body = kc.describe_response_body("x" * 5000)
    check(len(long_body) < 600, "long error body should be truncated")


# --------------------------------------------------------------------------
# Router-supplied text reaches agent-parsed output
# --------------------------------------------------------------------------


@test
def control_characters_cannot_forge_table_rows():
    # A DHCP hostname is chosen by the client device.
    hostile = "evil\naa:bb:cc:dd:ee:ff  fake  fake"
    rendered = kc.value_as_text(hostile)
    check("\n" not in rendered, f"newline survived into table output: {rendered!r}")


# --------------------------------------------------------------------------
# Log handling
# --------------------------------------------------------------------------


@test
def leap_day_rollover_returns_none_instead_of_raising():
    # Feb 29 has no counterpart in the previous year.
    check(
        kc.parse_log_timestamp("Feb 29 10:00:00", now=datetime(2024, 1, 5, 12, 0, 0)) is None,  # noqa: DTZ001
        "leap-day rollover should return None",
    )


@test
def log_timestamps_parse_and_roll_back_a_year():
    now = datetime(2026, 1, 5, 12, 0, 0)  # noqa: DTZ001 - router log times are naive
    check(kc.parse_log_timestamp("Jan 05 11:00:00", now=now) == datetime(2026, 1, 5, 11, 0, 0),  # noqa: DTZ001
          "same-year timestamp misparsed")
    check(kc.parse_log_timestamp("Dec 31 23:00:00", now=now).year == 2025,
          "future-looking timestamp should roll back to the previous year")
    check(kc.parse_log_timestamp("not a timestamp", now=now) is None,
          "unparseable timestamp should return None")


@test
def unparseable_timestamps_are_reported_not_silently_dropped():
    entries = [{"id": 1, "timestamp": "2026-08-24T10:00:00", "message": "error boom"}]
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        result = kc.filter_log_entries(entries, since=datetime(2020, 1, 1))  # noqa: DTZ001
    check(result == [], "entry with unparseable timestamp is still excluded")
    check("unrecognised timestamp" in stderr.getvalue(),
          f"a warning must be emitted, got {stderr.getvalue()!r}")


@test
def error_entries_are_detected_by_label_level_and_message():
    check(kc.is_error_log_entry({"label": "E"}), "label E is an error")
    check(kc.is_error_log_entry({"level": "critical"}), "level critical is an error")
    check(kc.is_error_log_entry({"message": "connection refused"}), "refused is an error")
    check(not kc.is_error_log_entry({"label": "I", "message": "link up"}), "info is not an error")


@test
def malformed_log_responses_raise_clierror():
    for bad in ([], [{}], [{"show": {}}], "nonsense", None):
        try:
            kc.extract_log_entries(bad)
        except kc.CliError:
            continue
        raise AssertionError(f"extract_log_entries({bad!r}) should raise CliError")


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------


@test
def base_url_is_built_from_host_port_and_ssl():
    check(kc.build_base_url("192.168.1.1", 80, False) == "http://192.168.1.1:80", "plain host")
    check(kc.build_base_url("192.168.1.1", 443, True) == "https://192.168.1.1:443", "ssl host")
    check(kc.build_base_url("https://router.lan", 80, False) == "https://router.lan:80",
          "scheme in host should win over the ssl flag")
    check(kc.build_base_url("https://router.lan:8443", 80, False) == "https://router.lan:8443",
          "explicit port in host should win over the port argument")


@test
def malformed_hosts_raise_clierror_not_valueerror():
    for host in ("http://router.lan:abc", "http://192.168.1.1/foo", "ftp://router.lan", "://x"):
        try:
            result = kc.build_base_url(host, 80, False)
        except kc.CliError:
            continue
        except Exception as err:  # noqa: BLE001 - the point is that this must not happen
            raise AssertionError(f"build_base_url({host!r}) raised {type(err).__name__}: {err}")
        raise AssertionError(f"build_base_url({host!r}) should raise CliError, got {result!r}")


@test
def missing_explicit_env_file_is_an_error():
    try:
        kc.require_env_path("nope.env", Path("/nonexistent/nope.env"), explicit=True)
    except kc.CliError:
        pass
    else:
        raise AssertionError("an explicit --env-file that does not exist must raise")
    # The default .env may legitimately be absent.
    kc.require_env_path(".env", Path("/nonexistent/.env"), explicit=False)


@test
def parse_bool_accepts_documented_truthy_values():
    for value in ("1", "true", "TRUE", "yes", "y", "on"):
        check(kc.parse_bool(value) is True, f"{value!r} should be true")
    for value in ("0", "false", "no", "", "maybe"):
        check(kc.parse_bool(value) is False, f"{value!r} should be false")


# --------------------------------------------------------------------------
# RCI success/failure reporting
# --------------------------------------------------------------------------


@test
def rci_errors_inside_a_200_body_are_detected():
    body = {"status": [{"status": "error", "code": 7405998, "message": "host is not registered"}]}
    check(kc.collect_rci_errors(body) == ["host is not registered"], "flat error not collected")
    nested = [{"ip": {"hotspot": {"host": {"status": [
        {"status": "error", "message": "already set"}]}}}}]
    check(kc.collect_rci_errors(nested) == ["already set"], "nested error not collected")
    ok = {"status": [{"status": "message", "message": "done"}]}
    check(kc.collect_rci_errors(ok) == [], "informational status must not be treated as an error")
    # A single status object in place of the array must not be walked past.
    single = {"status": {"status": "error", "message": "solo"}}
    check(kc.collect_rci_errors(single) == ["solo"], "object-shaped status was dropped")


@test
def warnings_are_reported_but_are_not_failures():
    # A warning on the batched `system configuration save` must not abort set policy
    # before the read-back, which is what determines whether the change landed.
    body = {"status": [{"status": "warning", "message": "already set"}]}
    check(kc.collect_rci_errors(body) == [], "a warning must not read as an error")
    check(kc.collect_rci_warnings(body) == ["already set"], "warning not collected")


@test
def log_entries_are_read_from_every_shape_rci_uses():
    # RCI renders a repeated element as an array and a lone entry as the object itself
    # (01_http_api_basics.md, "B.1.3.3"); an empty log has no entries at all. show log
    # is the agent's main diagnostic path, so a shape difference must not fail it.
    row = {"id": 7, "timestamp": "Aug 24 10:00:00", "ident": "ndm",
           "message": {"message": "hello", "level": "info", "label": "I"}}

    def entries(raw):
        return kc.extract_log_entries([{"show": {"log": {"log": raw}}}])

    check([e["message"] for e in entries({"0": row})] == ["hello"], "mapping shape")
    check([e["message"] for e in entries([row])] == ["hello"], "array shape")
    check([e["id"] for e in entries(row)] == [7], "single-object shape")
    check(entries({}) == [], "an empty log is not an error")
    check(entries(None) == [], "a null log is not an error")
    try:
        entries("nonsense")
    except kc.CliError:
        pass
    else:
        raise AssertionError("a genuinely unparseable log shape must still raise")


@test
def javascript_responses_tolerate_malformed_rows():
    parse = kc.KeeneticApiClient._parse_javascript_response
    check(parse('a="1"; ') == {"a": "1"}, "trailing whitespace row")
    check(parse('a="1";window.reload()') == {"a": "1"}, "row without '='")


# --------------------------------------------------------------------------
# Client records and policy rendering
# --------------------------------------------------------------------------


@test
def unknown_policy_rows_are_not_reported_as_default():
    check(kc.render_policy({"access": "permit"}, {}) == "default", "permit is default")
    check(kc.render_policy({"access": "deny"}, {}) == "not_internet", "deny is not_internet")
    check(kc.render_policy({"mac": "aa:bb:cc:dd:ee:ff"}, {}) == "unknown",
          "a row we do not understand must not claim the client is unrestricted")
    check(kc.render_policy(None, {}) == "-", "absent row renders as -")
    check(kc.render_policy({}, {}) == "-", "empty row renders as -")
    check(kc.render_policy({"policy": "Policy0"}, {"Policy0": {"description": "Home"}})
          == "Policy0 (Home)", "named policy should include its description")


@test
def a_policy_label_cannot_forge_lines_in_agent_parsed_output():
    # The label is interpolated into single-line output ("Policy updated: ... (router
    # now reports: X)") that the consuming agent parses as router state, so a newline
    # in a router-supplied description must not survive into it.
    label = kc.render_policy(
        {"policy": "Policy0"},
        {"Policy0": {"description": "Guests\nPolicy updated: aa:bb -> default"}},
    )
    check("\n" not in label, f"newline survived into a policy label: {label!r}")
    check("\r" not in label, f"carriage return survived into a policy label: {label!r}")
    identity_label = kc.render_policy({"policy": "Pol\ricy0"}, {})
    check("\r" not in identity_label,
          f"control character survived into a policy id: {identity_label!r}")


@test
def client_records_carry_the_fields_the_table_shows():
    clients = [{"mac": "AA-BB-CC-DD-EE-FF", "name": "TV", "ip": "1.2.3.4", "active": True}]
    policies = {"aa:bb:cc:dd:ee:ff": {"access": "deny"}}
    records = kc.build_client_records(clients, policies, {})
    check(records[0]["mac"] == "aa:bb:cc:dd:ee:ff", "MAC should be normalised")
    check(records[0]["policy"] == "not_internet", "policy should be resolved")
    check(records[0]["hostname"] is None, "absent hostname should be None, not ''")


@test
def set_policy_fails_loudly_when_the_router_rejects_the_write():
    class FakeClient:
        async def ip_hotspot_host_policy(self, mac, access, policy):
            return {"status": [{"status": "error", "message": "host is not registered"}]}

        async def show_rc_ip_hotspot_host(self):
            return []

        async def ip_policy_list(self):
            return {}

    # Client resolution needs a live router; the acceptance check is what matters here.
    fake = FakeClient()
    response = asyncio.run(fake.ip_hotspot_host_policy("aa:bb:cc:dd:ee:ff", "permit", {"no": True}))
    check(kc.collect_rci_errors(response) == ["host is not registered"],
          "a rejected write must surface the router's message")


class PolicyFakeClient:
    """A router that accepts the write and reports `observed` on the read-back."""

    def __init__(self, observed: str | None, write_response=None):
        self.observed = observed
        self.write_response = write_response if write_response is not None else [{}, {}]

    async def ip_policy_list(self):
        return {"Policy0": {"description": "Guests"}}

    async def show_ip_hotspot(self):
        return [{"mac": "aa:bb:cc:dd:ee:ff", "name": "TV"}]

    async def ip_hotspot_host_policy(self, mac, access, policy):
        return self.write_response

    async def show_rc_ip_hotspot_host(self):
        if self.observed is None:
            return []
        if self.observed == "default":
            return [{"mac": "aa:bb:cc:dd:ee:ff", "access": "permit"}]
        return [{"mac": "aa:bb:cc:dd:ee:ff", "access": "permit", "policy": self.observed}]


def run_set_policy(client, policy: str) -> tuple[str, str | None]:
    """Run cmd_set_policy --json, returning (stdout, CliError message or None)."""
    stdout = io.StringIO()
    error: str | None = None
    with contextlib.redirect_stdout(stdout):
        try:
            asyncio.run(
                kc.cmd_set_policy(client, "aa:bb:cc:dd:ee:ff", None, policy, as_json=True)
            )
        except kc.CliError as err:
            error = str(err)
    return stdout.getvalue(), error


@test
def set_policy_confirms_the_write_by_reading_the_state_back():
    # The read-back is what decides whether the write landed; a mismatch must fail
    # loudly rather than report the requested value back to the agent.
    out, error = run_set_policy(PolicyFakeClient("Policy0"), "Policy0")
    check(error is None, f"a matching read-back must succeed, got {error!r}")
    check('"confirmed": true' in out, f"confirmed flag missing from {out!r}")

    out, error = run_set_policy(PolicyFakeClient("default"), "Policy0")
    check(error is not None and "not applied" in error,
          f"a mismatched read-back must raise, got {error!r}")
    check('"confirmed": false' in out,
          "the JSON payload must still be printed when the read-back disagrees")


@test
def a_failed_configuration_save_does_not_masquerade_as_a_rejected_write():
    # ip_hotspot_host_policy batches the host rule with `system configuration save`,
    # and RCI mirrors the request array element for element. Reading errors from the
    # whole body blamed the policy write for a flash failure -- and aborted before the
    # read-back that shows the policy did change.
    response = [
        {"ip": {"hotspot": {"host": {"status": [{"status": "message", "message": "ok"}]}}}},
        {"system": {"configuration": {"save": {
            "status": [{"status": "error", "message": "flash write failed"}]}}}},
    ]
    out, error = run_set_policy(PolicyFakeClient("Policy0", response), "Policy0")
    check('"confirmed": true' in out, f"the read-back must still run, got {out!r}")
    check('"persisted": false' in out, f"a failed save must be reported, got {out!r}")
    check(error is not None and "not saved" in error and "rejected" not in error,
          f"a save failure must not read as a rejected write, got {error!r}")


@test
def a_rejected_policy_write_still_aborts_before_the_read_back():
    response = [
        {"ip": {"hotspot": {"host": {"status": [
            {"status": "error", "message": "host is not registered"}]}}}},
        {"system": {"configuration": {"save": {}}}},
    ]
    out, error = run_set_policy(PolicyFakeClient("Policy0", response), "Policy0")
    check(error is not None and "Router rejected" in error, f"got {error!r}")
    check(out == "", "nothing should be printed once the write itself was rejected")


# --------------------------------------------------------------------------
# Policy identity: the write must be comparable to the state read back.
# --------------------------------------------------------------------------


@test
def policy_identity_matches_the_vocabulary_of_resolve_policy():
    check(kc.policy_identity({"policy": "Policy0"}) == "Policy0", "named policy id")
    check(kc.policy_identity({"access": "deny"}) == "not_internet", "deny -> not_internet")
    check(kc.policy_identity({"access": "permit"}) == "default", "permit -> default")
    check(kc.policy_identity(None) is None, "absent row has no identity")
    check(kc.policy_identity({"mac": "aa"}) is None, "unrecognised row has no identity")
    # A row of the wrong type must not raise: it reaches here from a live response.
    check(kc.policy_identity("Policy0") is None, "non-dict row has no identity")


def _config_without_password(keychain_stub):
    """load_router_config against a file that carries everything but the password."""
    import tempfile

    saved_lookup = kc.password_from_keychain
    kc.password_from_keychain = keychain_stub
    saved_env = {
        key: os.environ.get(key)
        for key in ("KEENETIC_HOST", "KEENETIC_USERNAME", "KEENETIC_PASSWORD")
    }
    for key in saved_env:
        os.environ.pop(key, None)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text(
                "KEENETIC_HOST=192.168.1.1\nKEENETIC_USERNAME=keenetic-cli\n",
                encoding="utf-8",
            )
            return kc.load_router_config(path, file_wins=False)
    finally:
        kc.password_from_keychain = saved_lookup
        for key, value in saved_env.items():
            if value is not None:
                os.environ[key] = value


@test
def the_password_falls_back_to_the_keychain_when_no_file_or_env_has_one():
    # The whole point of the keychain path: a .env carrying only non-secret settings
    # must still produce a usable config.
    asked_for = []

    def stub(username):
        asked_for.append(username)
        return "from-keychain"

    cfg = _config_without_password(stub)
    check(cfg.password == "from-keychain", f"keychain value not used: {cfg.password!r}")
    # Keyed on the *router* user, so a second router's --env-file looks up its own item
    # instead of silently reusing this one's password.
    check(asked_for == ["keenetic-cli"], f"looked up the wrong account: {asked_for!r}")


@test
def a_password_in_the_environment_does_not_reach_for_the_keychain():
    # The env file and $KEENETIC_PASSWORD stay the escape hatch for a broken keychain,
    # so they must win without the lookup even running.
    import tempfile

    def stub(username):
        raise AssertionError("the keychain must not be consulted when a password is set")

    saved_lookup = kc.password_from_keychain
    kc.password_from_keychain = stub
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text(
                "KEENETIC_HOST=192.168.1.1\n"
                "KEENETIC_USERNAME=keenetic-cli\n"
                "KEENETIC_PASSWORD=fromfile\n",
                encoding="utf-8",
            )
            cfg = kc.load_router_config(path, file_wins=True)
    finally:
        kc.password_from_keychain = saved_lookup
    check(cfg.password == "fromfile", f"the file password must win: {cfg.password!r}")


@test
def an_empty_keychain_reports_every_source_it_tried():
    # The operator needs the whole chain to know where to put the value; naming only
    # the last link tried would send them to the wrong place.
    try:
        _config_without_password(lambda username: None)
    except kc.CliError as err:
        message = str(err)
    else:
        raise AssertionError("a config with no password anywhere must not load")
    for expected in ("KEENETIC_PASSWORD", "keychain", "keenetic-cli", "find-generic-password"):
        check(expected in message, f"{expected!r} missing from {message!r}")


@test
def a_failed_keychain_lookup_is_not_an_error():
    # A locked keychain, a missing item and a non-macOS host all mean "no password
    # here": raising would take out the env-file escape hatch along with them.
    class _Proc:
        returncode = 44
        stdout = ""

    saved_run = kc.subprocess.run
    kc.subprocess.run = lambda *a, **k: _Proc()
    try:
        check(kc.password_from_keychain("nobody") is None, "non-zero exit must give None")
        kc.subprocess.run = lambda *a, **k: (_ for _ in ()).throw(OSError("no security binary"))
        check(kc.password_from_keychain("nobody") is None, "a missing binary must give None")
    finally:
        kc.subprocess.run = saved_run


@test
def address_usage_ignores_every_network_but_the_one_asked_for():
    # A Keenetic serves several subnets at once, so both sources carry rows for every
    # bridge. Counting them all reported the guest network's leases as occupying the
    # LAN, and a placeholder 0.0.0.0 as occupying something.
    import ipaddress

    network = ipaddress.ip_network("192.168.1.0/24")
    usage = kc.collect_address_usage(
        [
            {"ip": "192.168.1.2", "expires": "infinity", "mac": "aa", "name": "fixed"},
            {"ip": "192.168.1.50", "expires": 1200, "mac": "bb", "name": "leased"},
            {"ip": "10.1.30.100", "expires": 1200, "mac": "cc", "name": "guest"},
        ],
        [
            {"ip": "192.168.1.200", "mac": "dd", "name": "self-configured"},
            {"ip": "0.0.0.0", "mac": "ee", "name": "no-lease-yet"},
            {"ip": "192.168.1.2", "mac": "aa", "name": "already-known"},
        ],
        network,
    )
    check(set(usage) == {"192.168.1.2", "192.168.1.50", "192.168.1.200"},
          f"wrong address set: {sorted(usage)}")
    check(usage["192.168.1.2"]["kind"] == "reservation", "infinity must be a reservation")
    check(usage["192.168.1.50"]["kind"] == "lease", "a numeric expiry must be a lease")
    # An address configured on the device itself is invisible to /rci/show/ip/dhcp/*,
    # and treating it as free is the classic silent collision.
    check(usage["192.168.1.200"]["kind"] == "seen", "hotspot-only must be 'seen'")


@test
def free_addresses_separate_what_dhcp_can_hand_out_from_what_it_cannot():
    # Only the outside-the-pool half is safe to configure on a device: an address
    # inside the pool is free this second and may be leased to the next machine.
    import ipaddress

    network = ipaddress.ip_network("192.168.1.0/24")
    outside, inside = kc.free_addresses(
        network,
        ipaddress.ip_address("192.168.1.33"),
        ipaddress.ip_address("192.168.1.35"),
        {"192.168.1.34", "192.168.1.200"},
        ipaddress.ip_address("192.168.1.1"),
    )
    check(ipaddress.ip_address("192.168.1.35") in inside, "free pool address missing")
    check(ipaddress.ip_address("192.168.1.34") not in inside, "taken address offered")
    check(ipaddress.ip_address("192.168.1.200") not in outside, "taken address offered")
    check(ipaddress.ip_address("192.168.1.1") not in outside, "the router was offered")
    check(ipaddress.ip_address("192.168.1.33") not in outside, "pool address leaked outside")
    check(ipaddress.ip_address("192.168.1.2") in outside, "free non-pool address missing")


@test
def free_address_runs_collapse_into_ranges():
    import ipaddress

    addresses = [ipaddress.ip_address(a) for a in
                 ("192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.9", "192.168.1.11")]
    check(kc.render_ranges(kc.group_into_ranges(addresses))
          == "192.168.1.2-192.168.1.4, 192.168.1.9, 192.168.1.11",
          f"bad rendering: {kc.render_ranges(kc.group_into_ranges(addresses))!r}")
    check(kc.render_ranges(kc.group_into_ranges([])) == "-", "empty must render as '-'")


@test
def the_dhcp_pool_defaults_to_the_lan_the_cli_is_talking_to():
    # A household has more than one pool; the one the operator means is the network
    # they reached the router through. Hard-coding a subnet would not travel.
    pools = {
        "_WEBADMIN": {"network": "192.168.1.0/24", "begin": "192.168.1.33", "end": "192.168.1.152"},
        "_GUEST": {"network": "10.1.30.0/24", "begin": "10.1.30.33", "end": "10.1.30.152"},
    }
    name, _ = kc.select_dhcp_pool(pools, "192.168.1.1", None)
    check(name == "_WEBADMIN", f"picked the wrong pool: {name}")
    name, _ = kc.select_dhcp_pool(pools, "10.1.30.1", None)
    check(name == "_GUEST", f"picked the wrong pool: {name}")
    name, _ = kc.select_dhcp_pool(pools, "192.168.1.1", "_GUEST")
    check(name == "_GUEST", "an explicit --pool must win")

    for host, requested, expected in (
        ("192.168.1.1", "NOSUCH", "Unknown DHCP pool"),
        ("router.lan", None, "not a plain address"),
        ("172.16.0.1", None, "No DHCP pool covers"),
    ):
        try:
            kc.select_dhcp_pool(pools, host, requested)
        except kc.CliError as err:
            check(expected in str(err), f"{expected!r} missing from {str(err)!r}")
            # Every failure has to name the alternatives, or the operator is stuck.
            check("_WEBADMIN" in str(err), f"available pools missing from {str(err)!r}")
        else:
            raise AssertionError(f"{host}/{requested} should not have resolved")


@test
def the_router_password_never_appears_in_a_config_repr():
    # The plaintext password never reaches the wire -- auth() only hashes it into the
    # challenge response -- so the realistic leak is someone printing the config while
    # debugging, straight into an agent transcript.
    cfg = kc.RouterConfig(
        host="192.168.1.1", port=80, username="admin",
        password="SUPERSECRET", ssl=False, timeout=30,
    )
    for rendering in (repr(cfg), str(cfg), f"{cfg}"):
        check("SUPERSECRET" not in rendering, f"password leaked into {rendering!r}")
    check(cfg.password == "SUPERSECRET", "the value itself must still be readable")


@test
def denied_access_outranks_a_policy_on_the_same_host():
    # `access` and `policy` are separate settings on one host, so the router's own CLI
    # and web UI can leave both set. Reporting "Policy2" for a host that is denied the
    # internet would claim a cut-off client is merely routed somewhere.
    row = {"mac": "aa:bb:cc:dd:ee:ff", "access": "deny", "policy": "Policy2"}
    check(kc.policy_identity(row) == "not_internet", "deny outranks the policy")
    check(kc.render_policy(row, {"Policy2": {"description": "VPS"}}) == "not_internet",
          "the human form must not name the policy either")
    # The permit pairing keeps reporting the policy, which is the common live shape.
    permitted = {"mac": "aa:bb:cc:dd:ee:ff", "access": "permit", "policy": "Policy2"}
    check(kc.policy_identity(permitted) == "Policy2", "permit + policy -> the policy")


@test
def a_named_policy_read_back_compares_equal_to_what_was_requested():
    # render_policy formats "Policy0 (Guests)" for humans; comparing that to the
    # requested "Policy0" would report every named-policy write as failed.
    row = {"mac": "aa:bb:cc:dd:ee:ff", "policy": "Policy0"}
    policies = {"Policy0": {"description": "Guests"}}
    check(kc.render_policy(row, policies) == "Policy0 (Guests)", "human form unchanged")
    check(kc.policy_identity(row) == "Policy0", "machine form must match the request")


@test
def an_unreadable_policy_row_is_never_reported_as_unrestricted():
    check(kc.render_policy({"mac": "aa"}, {}) == "unknown", "unrecognised row")
    check(kc.render_policy(None, {}) == "-", "absent row")


@test
def the_policy_write_is_persisted_to_the_stored_configuration():
    sent: list = []

    class FakeClient(kc.KeeneticApiClient):
        def __init__(self):
            pass

        async def api(self, method, endpoint, payload=None):
            sent.append((method, endpoint, payload))
            return {}

    asyncio.run(FakeClient().ip_hotspot_host_policy("aa:bb:cc:dd:ee:ff", "permit", "Policy0"))
    check(len(sent) == 1, f"expected one batched request, got {sent}")
    method, endpoint, payload = sent[0]
    check((method, endpoint) == ("POST", "/rci/"), f"unexpected target {method} {endpoint}")
    check(
        any("save" in str(item) and "configuration" in str(item) for item in payload),
        f"policy write must batch a configuration save, got {payload}",
    )


@test
def a_text_response_leaves_output_json_as_sanitized_json():
    # api request on a text/* response used to print the body raw, so router text
    # could forge table rows in output the agent parses as router state.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        kc.output_json("line1\nMAC  Name\naa:bb  forged")
    printed = buffer.getvalue().strip()
    check("\n" not in printed, f"a forged row survived as a real line: {printed!r}")
    check("\\n" not in printed, f"the newline survived as an escape: {printed!r}")
    check(printed.startswith('"') and printed.endswith('"'),
          f"a str body must leave as a JSON string, got {printed!r}")
    check("forged" in printed, f"the body itself must still be there: {printed!r}")


# --------------------------------------------------------------------------


@test
def documented_actions_added_this_pass_require_unsafe():
    # Every one of these is a documented command whose last path segment names an
    # irreversible action; each used to pass as an ordinary read.
    for endpoint in (
        "/rci/system/configuration/fail-safe/rollback",
        "/rci/ip/http/ssl/acme/revoke",
        "/rci/mws/update/start",
        "/rci/mws/update/stop",
        "/rci/mws/acquire",
        "/rci/interface/mobile/scan",
        "/rci/sms/send",
        "/rci/user/password/generate",
    ):
        assert_blocked("GET", endpoint)


@test
def an_action_named_in_the_query_requires_unsafe():
    # Per the RCI spec a query parameter is an argument to the command named by the
    # path, so gating only the path gates one spelling of an action and not the other.
    assert_blocked("GET", "/rci/system/configuration?save")
    assert_blocked("GET", "/rci/interface?name=Wireguard0&down=")
    assert_blocked("GET", "/rci/system/configuration?%73ave")
    # An ordinary read argument is still a read.
    assert_allowed("GET", "/rci/show/interface/stat?name=Wireguard0")


@test
def a_password_hash_in_running_config_is_redacted():
    # `password md5 <hash>` stores the value auth() hashes the challenge against, so
    # the hash is the authenticator; redacting only "md5" leaked it verbatim.
    for line in (
        "    password md5 5d505c920ed64c8ff3dc4bfefd4dc262",
        "    password nt-hash 209c6174da490caeb422f3fa5a7ae634",
    ):
        result = kc.redact_text(line)
        check(kc.REDACTED in result, f"nothing redacted in {result!r}")
        check(
            "5d505c920ed64c8ff3dc4bfefd4dc262" not in result
            and "209c6174da490caeb422f3fa5a7ae634" not in result,
            f"password hash leaked: {result!r}",
        )
    psk = kc.redact_text("crypto ike key VirtualIPServer mysecretpsk any")
    check("mysecretpsk" not in psk, f"IKE pre-shared key leaked: {psk!r}")
    radius = kc.redact_text("    wpa-eap radius secret sharedvalue")
    check("sharedvalue" not in radius, f"RADIUS secret leaked: {radius!r}")


@test
def ordinary_text_is_not_mangled_by_free_text_redaction():
    # Redaction runs over every string, including client names and log messages the
    # agent reads for diagnosis; swallowing the next word destroyed both.
    check(
        kc.redact_sensitive({"name": "Token Ring PC"})["name"] == "Token Ring PC",
        "a client name was mangled",
    )
    line = "I ppp: password authentication failed for user bob"
    check(kc.redact_text(line) == line, f"a log message was mangled: {kc.redact_text(line)!r}")
    check(
        kc.redact_text("key length is 44 characters") == "key length is 44 characters",
        "an incidental 'key' mention was mangled",
    )


@test
def router_booleans_arrive_as_yes_no_text():
    # bool("no") is True, which reported every offline client as active.
    check(kc.as_router_flag("no") is False, "'no' must not be truthy")
    check(kc.as_router_flag("yes") is True, "'yes' must be truthy")
    check(kc.as_router_flag(False) is False, "a real bool must pass through")
    records = kc.build_client_records([{"mac": "aa:bb:cc:dd:ee:ff", "active": "no"}], {}, {})
    check(records[0]["active"] is False, f"active='no' read as {records[0]['active']!r}")


@test
def multiple_input_subtrees_tolerate_object_shapes():
    endpoint = "/rci/show/rc/ip/hotspot/host"
    check(kc.normalize_rci_rows({}, endpoint) == [], "an empty object means no rows")
    check(kc.normalize_rci_rows(None, endpoint) == [], "null means no rows")
    single = {"mac": "aa:bb:cc:dd:ee:ff", "policy": "Policy0"}
    check(kc.normalize_rci_rows(single, endpoint) == [single], "a single row was dropped")
    check(
        kc.normalize_rci_rows([single, "junk"], endpoint) == [single],
        "a row of the wrong type must be dropped, not raise",
    )
    try:
        kc.normalize_rci_rows("nonsense", endpoint)
    except kc.CliError:
        pass
    else:
        raise AssertionError("an unparseable shape must still raise")


@test
def an_unreadable_policy_map_does_not_raise():
    # The map comes from a live response; a value of the wrong type must not turn a
    # read into a traceback.
    check(kc.render_policy({"policy": "P0"}, {"P0": "Guests"}) == "P0", "non-dict policy entry")


@test
def bare_hosts_are_validated_like_url_hosts():
    check(kc.build_base_url("192.168.1.1:8080", 80, False) == "http://192.168.1.1:8080",
          "an explicit port in a bare host must win over KEENETIC_PORT")
    for host in ("192.168.1.1/rci", "fe80::1", "192.168.1.1:notaport"):
        try:
            result = kc.build_base_url(host, 80, False)
        except kc.CliError:
            continue
        except Exception as err:  # noqa: BLE001
            raise AssertionError(f"build_base_url({host!r}) raised {type(err).__name__}: {err}")
        raise AssertionError(f"build_base_url({host!r}) should raise CliError, got {result!r}")


@test
def env_values_keep_a_trailing_quote_character():
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / ".env"
        path.write_text(
            "KEENETIC_PASSWORD=\"pa55'word\"\n"
            "KEENETIC_USER=admin'\n"
            "export KEENETIC_HOST=192.168.1.1\n",
            encoding="utf-8",
        )
        data = kc.load_env_file(path)
    check(data["KEENETIC_PASSWORD"] == "pa55'word", f"quoted value mangled: {data!r}")
    check(data["KEENETIC_USER"] == "admin'", f"trailing quote truncated: {data!r}")
    check(data["KEENETIC_HOST"] == "192.168.1.1", f"export prefix not handled: {data!r}")
    try:
        kc.load_env_file(Path(__file__).resolve().parent)
    except kc.CliError:
        pass
    except OSError as err:
        raise AssertionError(f"an unreadable env file must be a CliError, got {err!r}")


@test
def an_explicit_env_file_outvotes_the_process_environment():
    # Naming an --env-file is an operator choosing which router to talk to. If an
    # exported KEENETIC_HOST outvoted it, `set policy` would send that file's
    # credentials to a host the operator did not select. The default .env keeps the
    # usual dotenv precedence, because the consuming skill relies on it.
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "router-b.env"
        path.write_text(
            "KEENETIC_HOST=192.168.2.1\n"
            "KEENETIC_USERNAME=admin\n"
            "KEENETIC_PASSWORD=frompassfile\n",
            encoding="utf-8",
        )
        saved = {
            key: os.environ.get(key)
            for key in ("KEENETIC_HOST", "KEENETIC_USERNAME", "KEENETIC_PASSWORD")
        }
        os.environ["KEENETIC_HOST"] = "192.168.9.9"
        os.environ["KEENETIC_USERNAME"] = "admin"
        os.environ["KEENETIC_PASSWORD"] = "fromenv"
        try:
            explicit = kc.load_router_config(path, file_wins=True)
            default = kc.load_router_config(path, file_wins=False)
        finally:
            for key, value in saved.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    check(explicit.host == "192.168.2.1", f"explicit --env-file lost the host: {explicit.host!r}")
    check(explicit.password == "frompassfile", "explicit --env-file lost the password")
    check(default.host == "192.168.9.9", f"the default .env must not outvote the environment: {default.host!r}")
    check(default.password == "fromenv", "the default .env must not outvote the environment")


@test
def an_unobserved_configuration_save_is_not_reported_as_persisted():
    # split_batched_policy_response yields None for the save half whenever the
    # response shape is not the documented element-for-element mirror. "No errors
    # came back" is not "the save succeeded", and an agent reading `persisted: true`
    # stops worrying about the change surviving a reboot.
    out, error = run_set_policy(PolicyFakeClient("Policy0", [{}]), "Policy0")
    check(error is None, f"an unobserved save must not abort a confirmed write, got {error!r}")
    check('"confirmed": true' in out, f"the read-back must still run, got {out!r}")
    check('"persisted": false' in out, f"an unobserved save must not read as persisted: {out!r}")
    check("did not report" in out, f"the reason must reach the agent as a warning: {out!r}")


@test
def a_padded_method_reaches_aiohttp_normalized():
    # The gate accepts " get " because it validates the normalised form; aiohttp
    # rejects a non-token method with a ValueError the agent sees as a traceback.
    seen: list[str] = []

    class FakeClient(kc.KeeneticApiClient):
        def __init__(self):
            pass

        async def auth(self):
            return None

        async def _request_raw(self, method, endpoint, payload=None):
            seen.append(method)
            return 200, {}, {}

    asyncio.run(FakeClient().api(" get ", "/rci/show/version"))
    check(seen == ["GET"], f"method reached the request layer as {seen!r}")


@test
def mixed_trailing_decoration_does_not_hide_an_action_segment():
    # Stripping whitespace and dots in sequence stops at the first character of the
    # other kind: `.strip().strip(".")` left `save%20%2e` (`save .`) as `save ` and
    # `%2e%20save` (`. save`) as ` save`, neither of which is in the deny-list, while
    # `save%2e%20` was correctly trimmed. They are stripped together in one pass now.
    for endpoint in (
        "/rci/system/configuration/save%2e%20",
        "/rci/system/configuration/save%20%2e",
        "/rci/system/configuration/%2e%20save",
        "/rci/system/configuration/%20%2esave%2e%20",
    ):
        assert_blocked("GET", endpoint)
    # A dot inside a word still does not make that word an action.
    assert_allowed("GET", "/rci/show/ver.sion")


@test
def a_query_separator_inside_a_decoded_name_does_not_hide_an_action():
    # parse_qsl percent-decodes the name, so `?a%26save=1` arrives here as the single
    # opaque name `a&save`. `&` is the separator the RCI spec names for the query
    # channel, so the router may re-split it and see `save`.
    for endpoint in (
        "/rci/system/configuration?a%26save=1",
        "/rci/system/configuration?x%3dreboot",
        "/rci/system/configuration?a%26b%26save",
    ):
        assert_blocked("GET", endpoint)
    # An ordinary read argument whose value merely contains a separator is a read.
    assert_allowed("GET", "/rci/show/interface?name=Home%26Guest")


@test
def mac_clone_and_ndns_drop_name_require_unsafe():
    # Both are documented "Change settings: Yes" and share a name with no read:
    # `interface mac clone` (03_commands_interface.md) overwrites an interface MAC,
    # `ndns drop-name` (05_commands_mws_ndns_opkg_services.md) releases the hostname.
    assert_blocked("GET", "/rci/interface/ISP/mac/clone")
    assert_blocked("GET", "/rci/ndns/drop-name")


@test
def factory_defaults_secrets_are_redacted():
    # `show defaults` (06_commands_show.md, "3.166.17") returns the factory service
    # password, Wi-Fi key and WPS PIN. None matched a redaction rule: "servicepass"
    # does not contain "password" and "wlankey" ends in neither "-key" nor "_key",
    # so a bare GET printed them into the agent transcript in cleartext.
    for key in ("servicepass", "wlankey", "wlanwps"):
        check(kc.is_sensitive_key(key), f"{key} is not treated as sensitive")
    redacted = kc.redact_sensitive(
        {"servicepass": "hunter2", "wlankey": "abc123", "wlanwps": "55512345",
         "wlanssid": "Keenetic-0000", "ndmhwid": "KN-1011"}
    )
    check(
        redacted["servicepass"] == kc.REDACTED
        and redacted["wlankey"] == kc.REDACTED
        and redacted["wlanwps"] == kc.REDACTED,
        f"factory secrets survived redaction: {redacted!r}",
    )
    # Non-secret fields of the same response stay readable.
    check(redacted["wlanssid"] == "Keenetic-0000", "the SSID was redacted")
    check(redacted["ndmhwid"] == "KN-1011", "the hardware id was redacted")
    # The same values in a text/* rendering are caught too.
    text = kc.redact_text("   wlankey: abc123\n   servicepass: hunter2")
    check(
        "abc123" not in text and "hunter2" not in text,
        f"factory secrets survived text redaction: {text!r}",
    )


@test
def a_dangling_keyword_does_not_redact_the_following_line():
    # The separator group was `\s*`, and `\s` matches a newline, so a line ending in
    # `token:` consumed the *next* line as its value -- replacing router state the
    # agent parses with <redacted>.
    result = kc.redact_text("token:\nGigabitEthernet1 up\nnext line")
    check(
        "GigabitEthernet1 up" in result,
        f"the line after a dangling keyword was eaten: {result!r}",
    )
    # A real assignment on one line is still redacted.
    check(kc.REDACTED in kc.redact_text("token: 1f3a36"), "a real assignment leaked")


@test
def one_client_on_two_interfaces_is_not_ambiguous():
    # `show ip hotspot` returns one row per interface a host is reachable through
    # (06_commands_show.md, "3.166.56"), so a single client yields two rows with the
    # same MAC. That is not an ambiguity, and "use the MAC instead" would be advice
    # the agent cannot act on -- there is only one.
    class TwoRowsOneHost:
        async def show_ip_hotspot(self):
            return [
                {"name": "NAS", "mac": "AA:BB:CC:DD:EE:FF", "via": "Home"},
                {"name": "NAS", "mac": "aa-bb-cc-dd-ee-ff", "via": "Guest"},
            ]

    resolved = asyncio.run(kc.resolve_client_mac_by_name(TwoRowsOneHost(), "NAS"))
    check(resolved == "aa:bb:cc:dd:ee:ff", f"resolved to {resolved!r}")

    class TwoHosts:
        async def show_ip_hotspot(self):
            return [
                {"name": "NAS", "mac": "AA:BB:CC:DD:EE:FF"},
                {"name": "NAS", "mac": "11:22:33:44:55:66"},
            ]

    try:
        asyncio.run(kc.resolve_client_mac_by_name(TwoHosts(), "NAS"))
    except kc.CliError:
        pass
    else:
        raise AssertionError("two different MACs were not reported as ambiguous")


@test
def show_log_keeps_the_routers_own_error_message():
    # The router reports a rejected command inside a 200 body. Reaching straight for
    # the `log` key turned that into a generic shape complaint, leaving the agent
    # unable to tell "the command was rejected" from "this tool cannot parse it".
    try:
        kc.extract_log_entries(
            [{"show": {"log": {"status": [{"status": "error", "message": "log unavailable"}]}}}]
        )
    except kc.CliError as err:
        check("log unavailable" in str(err), f"the router message was lost: {err}")
    else:
        raise AssertionError("an RCI error in the body was not raised")


@test
def out_of_range_port_and_timeout_are_cli_errors():
    # A non-positive timeout arms no timer in aiohttp at all, so KEENETIC_TIMEOUT=0
    # silently removes the only protection against an unresponsive router; an
    # out-of-range port surfaces as "unexpected failure" (exit 1), which tells the
    # agent the router misbehaved when the cause is a typo in .env.
    base = {
        "KEENETIC_HOST": "192.168.1.1",
        "KEENETIC_USERNAME": "u",
        "KEENETIC_PASSWORD": "p",
    }

    def load(**overrides):
        env = {**base, **overrides}
        saved = dict(os.environ)
        try:
            os.environ.update(env)
            return kc.load_router_config(Path("/nonexistent/.env"), file_wins=False)
        finally:
            os.environ.clear()
            os.environ.update(saved)

    for overrides in (
        {"KEENETIC_TIMEOUT": "0"},
        {"KEENETIC_TIMEOUT": "-5"},
        {"KEENETIC_PORT": "0"},
        {"KEENETIC_PORT": "99999"},
        {"KEENETIC_PORT": "-1"},
    ):
        try:
            load(**overrides)
        except kc.CliError:
            continue
        raise AssertionError(f"{overrides} was accepted")

    cfg = load(KEENETIC_PORT="65535", KEENETIC_TIMEOUT="1")
    check(cfg.port == 65535 and cfg.timeout == 1, "a valid boundary value was rejected")


@test
def auth_challenge_headers_are_read_case_insensitively():
    # response.headers is a CIMultiDict; flattening it into a plain dict made the
    # X-NDM-Realm / X-NDM-Challenge lookups case-sensitive, so any other casing from
    # the router or a proxy took every command down with "missing challenge data".
    captured: list[str] = []

    class LowercaseHeaders(kc.KeeneticApiClient):
        def __init__(self):
            self._authenticated = False
            self._cfg = kc.RouterConfig(
                host="192.168.1.1", port=80, username="u", password="p",
                ssl=False, timeout=30,
            )

        async def _request_raw(self, method, endpoint, payload=None):
            if payload is None:
                return 401, CIMultiDict(
                    [("x-ndm-realm", "ndm"), ("x-ndm-challenge", "abc123")]
                ), ""
            captured.append(payload["login"])
            return 200, CIMultiDict(), ""

    asyncio.run(LowercaseHeaders().auth())
    check(captured == ["u"], f"auth did not complete against lowercased headers: {captured!r}")


@test
def bare_log_messages_and_client_names_survive_redaction():
    # redact_text runs over scalar *values*, not just running-config blobs:
    # extract_log_entries hands over the bare message (the "ppp:" ident is its own
    # field by then) and list clients hands over a client name. Anchoring the
    # directive patterns to the first word alone was not enough -- in a bare value
    # the keyword *is* the first word, so an auth-failure message and a client named
    # "Password Manager Pro" were replaced with "<redacted>", on the agent's main
    # diagnostic path and with no --no-redact escape hatch on list clients.
    intact = (
        "password authentication failed for user bob",
        "password change requested by admin",
        "psk rekey ok",
        "Password Manager Pro",
        "secret handshake completed",
    )
    for line in intact:
        check(kc.redact_text(line) == line, f"{line!r} was mangled into {kc.redact_text(line)!r}")
    entry = [{"id": 1, "timestamp": "t", "ident": "ppp", "label": "E", "level": "error",
              "message": "password authentication failed for user bob"}]
    result = kc.redact_sensitive(entry)
    check(
        result[0]["message"] == entry[0]["message"],
        f"log entry message was mangled: {result[0]['message']!r}",
    )


@test
def interface_names_are_not_treated_as_key_shaped_tokens():
    # SECRET_LIKE_TOKEN accepts anything carrying "/" or mixing 8+ letters and
    # digits, which every Keenetic interface name and every MAC address does. It is a
    # second condition, never the discriminator: matching `psk` anywhere on any line
    # meant an ordinary wmond log line lost its failure reason and client MAC.
    intact = (
        "wpa-psk handshake failed on WifiMaster0/AccessPoint0",
        "psk mismatch on WifiMaster0/AccessPoint0",
        "wmond: psk failure on WifiMaster0/AccessPoint0",
        "ndm: WPA-PSK group rekey for Bridge0/1",
        "wpa-psk authentication failed for d8:b3:77:36:05:c1.",
    )
    for line in intact:
        check(kc.redact_text(line) == line, f"{line!r} was mangled into {kc.redact_text(line)!r}")
    # The documented running-config rendering still loses its key.
    directive = kc.redact_text("                 authentication wpa-psk ns3 BMc1we4ZX9/fbJtDiM")
    check("BMc1we4ZX9/fbJtDiM" not in directive, f"psk leaked: {directive!r}")


@test
def redaction_is_linear_in_line_length():
    # Inlining SECRET_LIKE_TOKEN into SENSITIVE_PSK_DIRECTIVE_RE nested two lazy
    # quantifiers inside a third and backtracked quadratically: a long single-line
    # text/* body burned seconds of CPU after the response completed, where
    # ClientTimeout no longer covers it.
    import time

    line = "    psk " + ("a" * 20000)
    started = time.monotonic()
    kc.redact_text(line)
    elapsed = time.monotonic() - started
    check(elapsed < 1.0, f"redaction took {elapsed:.2f}s on a 20k-char line")


@test
def one_client_on_two_interfaces_yields_one_record():
    # `show ip hotspot` returns one row per interface a host is reachable through
    # (06_commands_show.md, "3.166.56"), which is why resolve_client_mac_by_name
    # de-duplicates before calling a name ambiguous. Emitting both rows would report
    # one device twice and make an agent counting clients see a phantom.
    rows = [
        {"name": "NAS", "mac": "AA:BB:CC:DD:EE:FF", "ip": "192.168.1.5", "active": "no"},
        {"name": "NAS", "mac": "aa-bb-cc-dd-ee-ff", "hostname": "nas.local", "active": "yes"},
    ]
    records = kc.build_client_records(rows, {}, {})
    check(len(records) == 1, f"expected one record, got {len(records)}: {records!r}")
    record = records[0]
    # The active row wins, but must not drop a field only the inactive row carried.
    check(record["active"] is True, f"merged record should be active: {record!r}")
    check(record["ip"] == "192.168.1.5", f"ip lost in merge: {record!r}")
    check(record["hostname"] == "nas.local", f"hostname lost in merge: {record!r}")
    # Two genuinely different MACs stay two records.
    distinct = kc.build_client_records(
        [{"name": "A", "mac": "AA:BB:CC:DD:EE:FF"}, {"name": "B", "mac": "11:22:33:44:55:66"}],
        {},
        {},
    )
    check(len(distinct) == 2, f"distinct MACs were collapsed: {distinct!r}")


@test
def a_read_rejected_inside_an_http_200_body_raises():
    # The router reports failure in a 200 body, so a refused read arrives with no
    # data key and a "status" array saying why. Normalising that to "no rows" made
    # show interfaces print "No interfaces found." -- the agent would conclude the
    # router has no interfaces rather than that the read failed.
    body = {"status": [{"status": "error", "message": "component not installed"}]}
    for func in (kc.dict_values_only, kc.normalize_rci_rows):
        try:
            func(body, "/rci/show/interface")
        except kc.CliError as err:
            check(
                "component not installed" in str(err),
                f"{func.__name__} dropped the router's message: {err}",
            )
        else:
            check(False, f"{func.__name__} silently swallowed an RCI error")
    # An empty result is still an empty result, not an error.
    check(kc.dict_values_only({}, "/x") == {}, "empty mapping should not raise")
    check(kc.normalize_rci_rows([], "/x") == [], "empty list should not raise")


@test
def wps_self_pin_is_gated_without_unsafe():
    # "interface wps self-pin" starts WPS pairing for two minutes
    # (03_commands_interface.md, "3.29.251"), opening the Wi-Fi to an unauthenticated
    # join, so it is an action rather than a settings read.
    try:
        kc.ensure_safe_router_request("GET", "/rci/interface/wps/self-pin", False)
    except kc.CliError:
        pass
    else:
        check(False, "GET /rci/interface/wps/self-pin was allowed without --unsafe")
    # The settings toggle is a distinct segment and must stay readable, as must the
    # reads that "button" and "peer" would have collided with.
    for endpoint in (
        "/rci/interface/wps/auto-self-pin",
        "/rci/show/button",
        "/rci/system/button",
    ):
        kc.ensure_safe_router_request("GET", endpoint, False)



def run() -> int:
    for func in TESTS:
        try:
            func()
        except AssertionError as err:
            FAILURES.append(f"{func.__name__}: {err}")
        except Exception as err:  # noqa: BLE001
            FAILURES.append(f"{func.__name__}: unexpected {type(err).__name__}: {err}")
    for failure in FAILURES:
        print(f"FAIL  {failure}")
    print(f"\n{len(TESTS) - len(FAILURES)}/{len(TESTS)} passed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(run())
