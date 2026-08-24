#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "aiohttp>=3.9.0",
# ]
# ///

"""CLI PoC for Keenetic router management."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import contextlib
import ipaddress
import posixpath
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import md5, sha256
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, quote, unquote, urlparse

import aiohttp

MAC_RE = re.compile(r"^[0-9a-f]{2}(?::[0-9a-f]{2}){5}$")
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_FILE = ".env"
# Keychain item holding the router password: service `keenetic`, account = the router
# username. Create it with:
#   security add-generic-password -U -s keenetic -a <router-user> -w
# Giving `-w` no value makes `security` prompt instead of taking the password through
# argv, where the process list can see it.
KEYCHAIN_SERVICE = "keenetic"
KEYCHAIN_TIMEOUT = 10
REDACTED = "<redacted>"
# Substring match: any key containing one of these is sensitive.
SENSITIVE_KEY_PARTS = (
    "password",
    "passwd",  # `interface chilli macpasswd` (03_commands_interface.md).
    "passphrase",
    "secret",
    "token",
    "psk",
)
# Suffix/exact match, so that "private-key" and "preshared_key" are redacted while
# incidental matches such as "keyword", "monkey", and "key-length" are not.
SENSITIVE_KEY_SUFFIXES = ("-key", "_key")
# "pin" is exact-match only: as a substring it would eat "spin" and "mapping".
# `show defaults` (06_commands_show.md, "3.166.17") returns the factory service
# password, Wi-Fi key and WPS PIN under names that match none of the rules above --
# "servicepass" does not contain "password", and "wlankey"/"wlanwps" end in neither
# "-key" nor "_key". The reference masks exactly these three plus "servicetag", and
# `show defaults` is a bare GET that needs no --unsafe, so without them the tool
# prints the router's factory credentials straight into the agent's transcript.
SENSITIVE_KEY_EXACT = frozenset(
    {"key", "keys", "pin", "servicepass", "wlankey", "wlanwps"}
)
# Secrets also arrive as free text (for example a line of `show running-config`), where
# the key name is part of the value rather than a JSON key.
# Keywords that only ever introduce a secret, and the two that are also ordinary
# English words -- "token" and "secret" appear in client names and descriptions.
# Split further by how safe they are to match mid-line: a compound keyword is never
# ordinary English, while a bare "password" is (see SENSITIVE_DIRECTIVE_RE below).
# "authtoken" belongs here rather than with the ambiguous "token": it is one word, so
# the \b in front of "token" never fires inside it, and `nextdns authtoken <authtoken>`
# (05_commands_mws_ndns_opkg_services.md) would otherwise leak a NextDNS account token.
# "servicepass", "wlankey" and "wlanwps" belong here for the same reason "authtoken"
# does: they are single words, so the \b in front of "password"/"key" never fires
# inside them, and a text/* rendering of `show defaults` would leak what the JSON
# path now redacts.
SENSITIVE_COMPOUND_KEYWORDS = (
    r"(?:private|preshared|public|obfs)-key|passphrase|xauth-password|authtoken"
    r"|servicepass|wlankey|wlanwps"
)
SENSITIVE_SECRET_KEYWORDS = (
    rf"{SENSITIVE_COMPOUND_KEYWORDS}|password|psk"
)
SENSITIVE_AMBIGUOUS_KEYWORDS = r"secret|token"
SENSITIVE_FREE_TEXT_KEYWORDS = (
    rf"{SENSITIVE_SECRET_KEYWORDS}|{SENSITIVE_AMBIGUOUS_KEYWORDS}"
)
# `secret: 123e45ed`, `token=1f3a36` (06_commands_show.md). The value runs to end of
# line: a secret may contain spaces, and redacting only the next token would leak the
# tail.
# The separator is [ \t] rather than \s: \s matches a newline, so a line ending in
# `token:` would consume the *next* line as its value and replace router state the
# agent parses with <redacted>.
SENSITIVE_ASSIGNMENT_RE = re.compile(
    rf"(?i)\b({SENSITIVE_FREE_TEXT_KEYWORDS})([ \t]*[:=][ \t]*)(\S.*)"
)
# A running-config directive: an indented `password md5 <hash>`, `private-key <key>`,
# `psk <key>`. `password md5 <hash>` stores the md5 that auth() hashes the challenge
# against, so the hash *is* the authenticator -- redacting only the algorithm keyword
# would leak it.
# The *indent* is what tells a directive apart from prose, and it is required rather
# than optional. Every secret-bearing directive in `show running-config`
# (06_commands_show.md, "3.166.102") is nested under a section -- `interface X`,
# `user admin`, `system` -- so it is always indented; only section headers sit at
# column zero, and none of them starts with a secret keyword. Anchoring to the first
# word alone is not enough, because redact_text also runs over *scalar values*, where
# there is no `ident:` prefix and no indent: extract_log_entries hands over the bare
# message ("password authentication failed for user bob"), and `list clients` hands
# over a client name ("Password Manager Pro"). Both begin with the keyword, and
# redacting them destroys router state the agent parses as truth -- on `show log`,
# the tool's main diagnostic path, with no --no-redact escape hatch on `list clients`.
# This is the same discriminator SENSITIVE_NEXTDNS_AUTH_RE below already relies on.
SENSITIVE_DIRECTIVE_RE = re.compile(
    rf"(?im)^([ \t]+)({SENSITIVE_SECRET_KEYWORDS})([ \t]+)(\S.*)$"
)
# The same directive form for "secret" and "token", which need the value to look like
# one before they are believed: a client named "Token Ring PC" is not a secret, and
# mangling it would corrupt output the agent parses as router state.
SENSITIVE_AMBIGUOUS_DIRECTIVE_RE = re.compile(
    rf"(?im)^([ \t]+)({SENSITIVE_AMBIGUOUS_KEYWORDS})([ \t]+)([^\s]{{8,}}.*)$"
)
# Secret-bearing directives whose keyword is not the first word: `crypto ike key`
# (02_commands_core_access_storage_components_crypto.md) and `wpa-eap radius secret`
# (03_commands_interface.md). Everything after the keyword goes, because in
# `crypto ike key <name> <psk> <peer>` the secret is not the first argument.
SENSITIVE_DIRECTIVE_PREFIX_RE = re.compile(
    r"(?i)\b("
    r"crypto ike key|wpa-eap radius secret|macpasswd|sim pin"
    # `show running-config` renders these with the secret keyword behind one or two
    # command words, so neither the first-word anchor nor a compound-keyword match
    # reaches them: `iapp key ns3 <key>` (06_commands_show.md),
    # `authentication password <password>` and `chilli login <server> username <u>
    # password <p>` (03_commands_interface.md), `chilli radiussecret <secret>` and
    # `chilli uamsecret <secret>` (03_commands_interface.md), `web-api password
    # <password>` (07_commands_..._system_tools_users_vpn.md) and the WPS pins
    # (03_commands_interface.md). Everything after the keyword goes: in
    # `wps peer <mac> <pin>` and `iapp key <name> <key>` the secret is not the
    # first argument.
    r"|iapp key|authentication password|web-api password"
    r"|chilli radiussecret|chilli uamsecret|chilli login"
    r"|wps self-pin|wps peer"
    r")([ \t]+)(\S.*)"
)
# `encryption key <id> ( <value> [default] | default)` (03_commands_interface.md) is
# the WEP key, and a WEP key is all hex digits, so the key-shaped-token guard used for
# `psk` would miss it. The documented key id is what tells the directive apart from
# prose such as "encryption key mismatch" in a log line.
SENSITIVE_WEP_KEY_RE = re.compile(r"(?i)\b(encryption key)([ \t]+)(\d\S*.*)")
# `show running-config` prints a directive with its command words in front, so the
# secret keyword is usually *not* the first word of the line
# (06_commands_show.md renders `authentication wpa-psk ns3 <psk>`, and
# 03_commands_interface.md documents `interface wireguard private-key <key>` and
# `interface ipsec preshared-key <psk>`). Anchoring to the first word would leak all
# three. These keywords are compound and never ordinary English, so they can be
# matched anywhere in the line without mangling prose the way a bare "password" would.
SENSITIVE_COMPOUND_DIRECTIVE_RE = re.compile(
    rf"(?i)\b({SENSITIVE_COMPOUND_KEYWORDS})([ \t]+)(\S.*)"
)
# A token that looks like a key rather than a word: eight or more non-space characters
# mixing letters with digits, or one carrying base64 punctuation. This is a weak
# signal on its own and is only ever used *in addition to* the indent anchor below --
# a Keenetic interface name ("WifiMaster0/AccessPoint0") and a MAC address both
# satisfy it, so nothing may rely on it to tell a secret from prose.
SECRET_LIKE_TOKEN = r"(?:(?=\S*[0-9])(?=\S*[A-Za-z])\S{8,}|\S*[+/=]\S*)"
# `psk` is the one secret keyword that also turns up in log prose ("wpa-psk handshake
# failed"), and unlike the compound keywords it sits behind command words in
# `show running-config` (06_commands_show.md renders `authentication wpa-psk ns3
# <psk>`), so it can be anchored to neither the first word nor the whole line.
# It is anchored to the running-config *indent* instead, for the reason spelled out
# above SENSITIVE_DIRECTIVE_RE: matching `psk` anywhere on any line meant that
# "wpa-psk handshake failed on WifiMaster0/AccessPoint0" -- an ordinary `show log`
# line -- had its failure reason and client MAC replaced with <redacted>, because the
# key-shaped-token guard alone accepts an interface name and a MAC as "key-shaped".
# The guard is kept as a second condition, not as the discriminator.
# The guard is applied by searching the matched value separately rather than by
# embedding SECRET_LIKE_TOKEN in this pattern. Inlining it nests two lazy quantifiers
# inside a third, which backtracks quadratically: a 20k-character single-line text/*
# body took 8s of CPU *after* the response completed, where ClientTimeout no longer
# covers it. Split this way every quantifier scans the line once.
SENSITIVE_PSK_DIRECTIVE_RE = re.compile(r"(?im)^([ \t]+[^\n]*?)\b(psk)([ \t]+)(\S[^\n]*)$")
SECRET_LIKE_TOKEN_RE = re.compile(rf"(?:\A|\s){SECRET_LIKE_TOKEN}")
# `nextdns authenticate <login> <password> [<pin>]`
# (05_commands_mws_ndns_opkg_services.md) is the one documented directive that carries
# a credential with no secret keyword anywhere on the line, and `show running-config`
# renders it nested under the `nextdns` section, so the `nextdns` prefix that would
# disambiguate it is gone and the first word is a plain English verb. "authenticate"
# is not a word any other command in the reference starts with, and requiring both the
# indent and a second argument is what keeps a message such as "authenticate failed"
# intact. The login stays visible -- it is an account name, not a credential -- and
# everything after it goes, because the optional pin trails the password.
SENSITIVE_NEXTDNS_AUTH_RE = re.compile(
    r"(?im)^([ \t]+)(authenticate)([ \t]+)(\S+)([ \t]+)(\S.*)$"
)
# Control characters would let router-supplied text (a DHCP hostname, a log message)
# forge rows in table output that an agent parses as router state.
CONTROL_CHARS_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")
ERROR_LABELS = {"E", "C", "F"}
ERROR_LEVELS = {"error", "critical", "fatal"}
ERROR_MESSAGE_PATTERNS = (
    "error",
    "failed",
    "failure",
    "timeout",
    "refused",
    "denied",
    "unreachable",
    "did not complete",
    "stopped hearing back",
    "retrying handshake",
)


class CliError(Exception):
    """Expected CLI error."""


@dataclass
class RouterConfig:
    host: str
    port: int
    username: str
    # repr=False keeps the router password out of the dataclass's generated repr. The
    # value never reaches the wire in the clear -- auth() only hashes it into the
    # challenge response -- so the realistic way it escapes is someone printing the
    # config while debugging, or tooling that renders a frame's locals. Both put it
    # straight into an agent transcript. Keep any new credential field out of the repr
    # for the same reason.
    password: str = field(repr=False)
    ssl: bool
    timeout: int


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    try:
        # A directory or an unreadable file raises OSError, which main() reports as a
        # transport failure ("HTTP error", exit 3) -- the agent would conclude the
        # router is down when the actual problem is the --env-file path.
        raw_text = path.read_text(encoding="utf-8")
    except OSError as err:
        raise CliError(f"Cannot read env file {path}: {err}") from err
    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        value = value.strip()
        # Strip one matched surrounding pair only: str.strip(chars) removes every
        # leading and trailing occurrence, which silently truncates a password that
        # ends in a quote character.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key] = value
    return data


def resolve_env_path(env_file_arg: str) -> Path:
    env_path = Path(env_file_arg)
    if env_path.is_absolute():
        return env_path
    return SCRIPT_DIR / env_path


def resolve_env_file_arg(env_file_arg: str | None) -> tuple[str, bool]:
    """Split the --env-file option into the path to load and whether it was given.

    Whether the operator named the file is what decides both that the file must exist
    and that it outvotes the process environment, so `--env-file .env` must not be
    mistaken for the default. Defaulting the argparse option to DEFAULT_ENV_FILE loses
    exactly that distinction, hence the None sentinel.
    """
    if env_file_arg is None:
        return DEFAULT_ENV_FILE, False
    return env_file_arg, True


def require_env_path(env_file_arg: str, resolved: Path, *, explicit: bool) -> Path:
    """Fail loudly when the operator named an --env-file that is not there.

    The default .env is allowed to be absent (settings may come from the process
    environment), but a typo in an explicit --env-file must not degrade into a
    confusing "Missing required settings".
    """
    if explicit and not resolved.exists():
        raise CliError(f"--env-file not found: {resolved} (from '{env_file_arg}').")
    return resolved


def build_base_url(host: str, port: int, use_ssl: bool) -> str:
    """Build the router base URL.

    KEENETIC_HOST may be a bare host or a full URL. When it carries a scheme, that
    scheme wins over KEENETIC_SSL and an explicit port in the URL wins over
    KEENETIC_PORT; any path component is rejected rather than silently mangled.
    """
    host = host.strip().rstrip("/")
    if "://" not in host:
        # Prepend the scheme and fall through to the same validation: a bare
        # "192.168.1.1/rci" is just as wrong as "http://192.168.1.1/rci", and a bare
        # "fe80::1" or "host:notaport" must fail as a CliError rather than as a yarl
        # ValueError traceback later.
        host = f"{'https' if use_ssl else 'http'}://{host}"

    parsed = urlparse(host)
    if not parsed.scheme or not parsed.netloc:
        raise CliError(f"Invalid KEENETIC_HOST value: {host}")
    if parsed.scheme not in {"http", "https"}:
        raise CliError(
            f"Invalid KEENETIC_HOST value: {host}. Scheme must be http or https."
        )
    if parsed.path or parsed.query or parsed.fragment:
        raise CliError(
            f"Invalid KEENETIC_HOST value: {host}. "
            "Provide only a host (optionally with scheme and port), without a path."
        )
    try:
        explicit_port = parsed.port
    except ValueError as err:
        raise CliError(f"Invalid port in KEENETIC_HOST value: {host}") from err
    if explicit_port is not None:
        return f"{parsed.scheme}://{parsed.netloc}"
    return f"{parsed.scheme}://{parsed.netloc}:{port}"


def password_from_keychain(username: str) -> str | None:
    """The router password for `username` from the macOS keychain, or None.

    Keyed on the *router* username, not on the local user: pointing `--env-file` at a
    second router looks up that router's own item instead of silently reusing this
    one's password.

    Reading is all this does. Nothing writes the item, because the router password
    only ever changes when the operator changes it -- an automatic cache refresh would
    serve an event that never happens on its own, and `security add-generic-password`
    can only take the value through argv, where the process list can see it.

    Never raises. A missing item, a locked keychain, a non-macOS host and an absent
    `security` binary are all just "no password here"; load_router_config reports the
    whole chain at once rather than leaking which link failed.
    """
    try:
        proc = subprocess.run(
            ["security", "find-generic-password",
             "-s", KEYCHAIN_SERVICE, "-a", username, "-w"],
            capture_output=True,
            text=True,
            timeout=KEYCHAIN_TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    # `-w` prints the value and a trailing newline, and nothing else goes to stdout.
    # Only the trailing newline is stripped: a password may legitimately end in spaces.
    return proc.stdout.rstrip("\n") or None


def load_router_config(env_file: Path, *, file_wins: bool) -> RouterConfig:
    """Merge the env file with the process environment into a router config.

    By default the process environment wins, which is the convention every dotenv
    loader follows and what the consuming skill relies on. An explicit `--env-file`
    inverts that: naming a file is an operator choosing *which router* to talk to, and
    an exported KEENETIC_HOST that quietly outvoted it would send that file's
    credentials to a host the operator did not select -- on `set policy`, it would
    reconfigure the wrong device.
    """
    env_data = load_env_file(env_file)
    merged = {**os.environ, **env_data} if file_wins else {**env_data, **os.environ}

    # KEENETIC_PASSWORD is deliberately not required here: it has one more source
    # below, and demanding it now would reject a working keychain-only setup.
    required = ("KEENETIC_HOST", "KEENETIC_USERNAME")
    missing = [name for name in required if not merged.get(name)]
    if missing:
        raise CliError(
            f"Missing required settings: {', '.join(missing)}. "
            f"Provide them in {env_file} or environment variables."
        )

    username = merged["KEENETIC_USERNAME"]
    # The keychain is the intended home for the password, and the env file the escape
    # hatch: this is a tool for diagnosing a broken network, so it must not need a
    # working keychain to run. The env/file half honours the same `file_wins` rule as
    # every other setting, so naming a file still selects that router's credentials.
    password = merged.get("KEENETIC_PASSWORD") or password_from_keychain(username)
    if not password:
        # Naming every source keeps this actionable without saying which one was
        # tried last -- the operator needs the whole chain to know where to put it.
        raise CliError(
            f"No password for router user '{username}'. Looked in $KEENETIC_PASSWORD, "
            f"in {env_file}, and in the keychain "
            f"(security find-generic-password -s {KEYCHAIN_SERVICE} -a {username} -w)."
        )

    try:
        port = int(merged.get("KEENETIC_PORT", "80"))
    except ValueError as err:
        raise CliError("KEENETIC_PORT must be an integer.") from err
    # An out-of-range port reaches yarl as a ValueError from inside session.request,
    # which the catch-all in main() reports as "unexpected failure" (exit 1) -- the
    # agent reads that as an unforeseen router response rather than a typo in .env.
    # build_base_url already rejects a bad port spelled inside KEENETIC_HOST.
    if not 1 <= port <= 65535:
        raise CliError(f"KEENETIC_PORT must be between 1 and 65535, got {port}.")

    try:
        timeout = int(merged.get("KEENETIC_TIMEOUT", "30"))
    except ValueError as err:
        raise CliError("KEENETIC_TIMEOUT must be an integer.") from err
    # aiohttp arms no timer at all for a non-positive total, so KEENETIC_TIMEOUT=0 --
    # a plausible spelling of "no limit" -- silently removes the only protection
    # against an unresponsive router and hangs the agent with no output and no exit
    # code. A negative value expires every request instantly instead, which is
    # indistinguishable from the router being unreachable.
    if timeout < 1:
        raise CliError(f"KEENETIC_TIMEOUT must be a positive integer, got {timeout}.")

    return RouterConfig(
        host=merged["KEENETIC_HOST"],
        port=port,
        username=username,
        password=password,
        ssl=parse_bool(merged.get("KEENETIC_SSL", "false")),
        timeout=timeout,
    )


def normalize_mac(value: str) -> str:
    return value.strip().lower().replace("-", ":")


def parse_json_payload(value: str | None) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as err:
        raise CliError(f"Invalid --data-json: {err}") from err


def is_sensitive_key(key: str) -> bool:
    normalized = key.strip().casefold()
    return (
        normalized in SENSITIVE_KEY_EXACT
        or normalized.endswith(SENSITIVE_KEY_SUFFIXES)
        or any(part in normalized for part in SENSITIVE_KEY_PARTS)
    )


def redact_text(text: str) -> str:
    """Redact secrets that appear inside a string value rather than as a JSON key."""

    def hide(match: re.Match[str]) -> str:
        # Every group but the last is the keyword and its separator; the last is the
        # value, which is replaced wholesale.
        return f"{''.join(match.groups()[:-1])}{REDACTED}"

    def hide_if_key_shaped(match: re.Match[str]) -> str:
        # `psk` alone is not enough to believe the rest of the line is a secret, so
        # the value has to carry something key-shaped as well. Checked here rather
        # than in the pattern: see SENSITIVE_PSK_DIRECTIVE_RE.
        if not SECRET_LIKE_TOKEN_RE.search(match.groups()[-1]):
            return match.group(0)
        return hide(match)

    text = SENSITIVE_ASSIGNMENT_RE.sub(hide, text)
    text = SENSITIVE_DIRECTIVE_PREFIX_RE.sub(hide, text)
    text = SENSITIVE_WEP_KEY_RE.sub(hide, text)
    text = SENSITIVE_COMPOUND_DIRECTIVE_RE.sub(hide, text)
    text = SENSITIVE_PSK_DIRECTIVE_RE.sub(hide_if_key_shaped, text)
    text = SENSITIVE_NEXTDNS_AUTH_RE.sub(hide, text)
    text = SENSITIVE_DIRECTIVE_RE.sub(hide, text)
    return SENSITIVE_AMBIGUOUS_DIRECTIVE_RE.sub(hide, text)


def sanitize_text(text: str) -> str:
    """Neutralise control characters in router-supplied text."""
    return CONTROL_CHARS_RE.sub(" ", text)


def redact_sensitive(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: REDACTED if is_sensitive_key(str(key)) else redact_sensitive(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def output_json(value: Any, *, raw: bool = False, redact: bool = True) -> None:
    data = redact_sensitive(value) if redact else value
    if isinstance(data, str):
        # A non-JSON router response (text/*) still has to leave here as JSON, and
        # still has to be stripped of control characters -- printing it raw would let
        # router-supplied text forge structure in output the agent parses.
        data = sanitize_text(data)
    if raw:
        print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
        return
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


MAX_ERROR_BODY_CHARS = 500


def describe_response_body(body: Any) -> str:
    """Render a response body for an error message: redacted and length-bounded.

    Error paths are printed to stderr and land in the consuming agent's transcript,
    so an unredacted body here would defeat redaction everywhere else.
    """
    redacted = redact_sensitive(body)
    if isinstance(redacted, str):
        text = sanitize_text(redacted)
    else:
        try:
            text = json.dumps(redacted, ensure_ascii=False, sort_keys=True)
        except (TypeError, ValueError):
            text = sanitize_text(str(redacted))
    if len(text) > MAX_ERROR_BODY_CHARS:
        return f"{text[:MAX_ERROR_BODY_CHARS]}... (truncated)"
    return text


def collect_rci_status_messages(response: Any, severities: frozenset[str]) -> list[str]:
    """Extract RCI status messages of the given severities from an HTTP 200 body.

    The router reports command failure in a "status" array rather than via the HTTP
    status code, so a write that never happened otherwise looks like a success. A
    single status object appears in place of the array as well; treating it as an
    ordinary subtree would drop the message entirely.
    """
    messages: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return
        raw_status = node.get("status")
        if isinstance(raw_status, list):
            entries: list[Any] = raw_status
        elif isinstance(raw_status, dict) and isinstance(raw_status.get("status"), str):
            entries = [raw_status]
        else:
            entries = []
        for item in entries:
            if not isinstance(item, dict):
                continue
            if str(item.get("status", "")).casefold() in severities:
                text = str(item.get("message") or item.get("ident") or item).strip()
                # These messages are printed to stderr and land in the consuming
                # agent's transcript, and the router echoes the rejected value back
                # ("bad value for private-key: ..."), so redact them like any other
                # router-supplied text.
                messages.append(sanitize_text(redact_text(text)))
        for key, value in node.items():
            # Only skip the key that was consumed as a status report; a "status"
            # subtree that is not one still has to be walked.
            if key == "status" and entries:
                continue
            walk(value)

    walk(response)
    return messages


def collect_rci_errors(response: Any) -> list[str]:
    """Messages that mean the command failed."""
    return collect_rci_status_messages(response, frozenset({"error"}))


def collect_rci_warnings(response: Any) -> list[str]:
    """Messages that accompany a command that may still have succeeded.

    A warning must not abort a write before its state is read back -- the read-back is
    what actually answers whether the change landed.
    """
    return collect_rci_status_messages(response, frozenset({"warning"}))


# Path segments that name an action rather than a settings subtree. Per the RCI spec
# (keenetic_api_docs/full_reference_chapters/01_http_api_basics.md, "B.1.2 Methods") GET
# retrieves settings and is "not applicable" to actions other than /rci/show, so GET should
# never execute a command. These are still gated behind --unsafe as defence in depth,
# because executing one of them by accident is unrecoverable.
ACTION_PATH_SEGMENTS = frozenset(
    {
        "save",
        "reboot",
        "restart",
        "reset",
        "shutdown",
        "erase",
        "upgrade",
        "factory-reset",
        # Component and firmware management (02_commands_core_..._components_crypto.md).
        "commit",
        "install",
        "remove",
        "copy",
        # Interface state changes (03_commands_interface.md, "interface up/down",
        # "interface connect", "interface traffic-counter action disconnect",
        # "interface ip dhcp client release/renew").
        "up",
        "down",
        "connect",
        "disconnect",
        "release",
        "renew",
        "logout",
        # System and storage actions (07_commands_..._system_tools_users_vpn.md:
        # "system log clear", "system eject", "system mount", "system swap",
        # "sms delete").
        "clear",
        "eject",
        "mount",
        "unmount",
        "swap",
        "format",
        "mkdir",
        "delete",
        # Configuration rollback and certificate revocation are as irreversible as a
        # reset: "system configuration fail-safe rollback"
        # (07_commands_..._system_tools_users_vpn.md) and "ip http ssl acme revoke"
        # (04_commands_ip_ipv6_network.md).
        "rollback",
        "revoke",
        # Mesh, mobile and messaging actions: "mws update start/stop", "mws acquire"
        # (05_commands_mws_ndns_opkg_services.md), "interface mobile scan"
        # (03_commands_interface.md), "sms send" / "ussd send"
        # (07_commands_..._system_tools_users_vpn.md).
        "start",
        "stop",
        "acquire",
        "scan",
        "send",
        # "user password generate" replaces a user's password
        # (07_commands_..._system_tools_users_vpn.md).
        "generate",
        # Actions with an external effect that no read shares a name with:
        # "ip ssh keygen" replaces the host key and "ip hotspot wake" sends a
        # Wake-on-LAN packet (04_commands_ip_ipv6_network.md); "interface usb
        # power-cycle" and "ping-check profile power-cycle" cut power to a port
        # (03_commands_interface.md, 05_commands_mws_ndns_opkg_services.md);
        # "<vpn> session-logout" drops live sessions (02_..._crypto.md,
        # 05_commands_mws_ndns_opkg_services.md, 07_..._vpn.md); "dns-proxy srr-reset"
        # and "interface ip dhcp client displace" reset runtime state
        # (02_..._crypto.md, 03_commands_interface.md); "dlna rescan",
        # "interface channel auto-rescan" and "components check-update" start a scan
        # (02_..._crypto.md, 03_commands_interface.md).
        "keygen",
        "wake",
        "power-cycle",
        "session-logout",
        "srr-reset",
        "displace",
        "rescan",
        "auto-rescan",
        "check-update",
        # "interface mac clone" overwrites an interface's MAC with the operator PC's
        # (03_commands_interface.md, "3.29.147") and "ndns drop-name" releases the
        # KeenDNS hostname allocation, as irreversible as "revoke"
        # (05_commands_mws_ndns_opkg_services.md, "3.120.3"). Both are documented
        # "Change settings: Yes" and neither shares a name with any read.
        "clone",
        "drop-name",
        # "interface wps self-pin" starts WPS pairing -- "Process takes 2 minutes or
        # until the first connection occured" (03_commands_interface.md, "3.29.251")
        # -- so it opens the Wi-Fi to an unauthenticated join. The segment is exact,
        # so this does not touch the "wps auto-self-pin" settings toggle
        # ("3.29.248"), which is a distinct segment.
        "self-pin",
        # Deliberately absent alongside it: "button" and "peer", the other two WPS
        # actions ("3.29.249", "3.29.250"). Both collide with reads -- "system button"
        # and "show button" (07_..._vpn.md "3.175.1", 06_commands_show.md "3.166.5"),
        # and "crypto ike peer" and the WireGuard peer subtree -- and gating the pair
        # would mean ordering segments the canonicalisation deliberately keeps as an
        # unordered candidate set. Same trade-off as "get"/"update" below.
        # Deliberately absent: "get", "update", "ping" and "traceroute". They name
        # actions under some parents ("ip http ssl acme get") but read settings under
        # others, and blocking a legitimate read pushes the agent towards --unsafe,
        # which is worse than the residual risk of a GET the RCI spec says will not
        # execute.
    }
)

# A method that is not a bare HTTP token would be rejected deep inside aiohttp with a
# ValueError, which surfaces to the agent as a traceback rather than an "Error:" line.
HTTP_METHOD_RE = re.compile(r"^[A-Za-z]+$")

# Surrounding whitespace and dots, stripped in a single pass so that a mixture of the
# two cannot leave one kind behind (see canonical_forms).
SURROUNDING_DECORATION_RE = re.compile(r"^[\s.]+|[\s.]+$")

# Separators the router may still find inside an already-decoded query parameter name.
QUERY_SEPARATORS_RE = re.compile(r"[/&=]")


def split_endpoint(endpoint: str) -> tuple[str, str]:
    """Split an endpoint into (path, query), discarding any fragment.

    A fragment is never meaningful for RCI and is dropped by the HTTP client before
    the request goes out, so it must not be allowed to hide a path segment from the
    gate below.
    """
    without_fragment = endpoint.split("#", 1)[0]
    path, separator, query = without_fragment.partition("?")
    return path, f"{separator}{query}"


def canonical_forms(raw: str) -> set[str]:
    """Every form of one path segment or query name the router might act on.

    Candidates may only ever be *added*, never removed -- the same doctrine the `..`
    handling below follows. Two ways a segment can mean less here than it does on the
    wire:

    - Deleting a control character splices the halves either side of it together, so
      `save%00x` would canonicalise to `savex` and miss the check. The RCI engine is
      native code and a C string stops at the NUL, so it sees `save`. Keep the
      truncated prefix alongside the spliced form.
    - `;` is a separator the router may still honour: parse_qsl stopped splitting on
      it in 3.10, and RFC 3986 path parameters use it, so `reboot;x` may reach the
      router as `reboot`.

    Trailing decoration such as `save%20` or `save%2e` is stripped for the same
    reason: whether the router's parser trims it is not something this side can
    verify, so strip it here rather than let it decide. Whitespace and dots are
    stripped together in one pass, because stripping them in sequence stops at the
    first character of the other kind: `save%20%2e` (`save .`) survived a
    `.strip().strip(".")` as `save `, and `%2e%20save` as ` save`.
    """
    forms = {CONTROL_CHARS_RE.sub("", raw), CONTROL_CHARS_RE.split(raw)[0]}
    forms |= {form.split(";", 1)[0] for form in tuple(forms)}
    cleaned = {SURROUNDING_DECORATION_RE.sub("", form).casefold() for form in forms}
    return {form for form in cleaned if form}


def canonical_path_segments(path: str) -> set[str]:
    """Path segments as the router will see them.

    The HTTP client percent-decodes and resolves dot-segments before putting the path
    on the wire, so matching the raw string would let `/rci/system/configuration/%73ave`
    or `/rci/system/configuration/SAVE` slip past a check for `save`.
    """
    decoded = unquote(path).replace("\\", "/")
    # Resolving `..` may only ever *add* candidates. An encoded separator is not a
    # separator on the wire -- yarl leaves `%2F` encoded, so `/rci/system/reboot%2F..`
    # is sent with `reboot` still in it -- yet it becomes one here after decoding, and
    # `..` then cancels the action segment in front of it. Inspecting the decoded path
    # *and* its normalised form keeps the action visible whichever way the router
    # splits the string it receives.
    candidates = [decoded, posixpath.normpath(decoded)] if decoded else []
    segments = set()
    for candidate in candidates:
        for segment in candidate.split("/"):
            segments |= canonical_forms(segment)
    return segments


def canonical_query_keys(query: str) -> set[str]:
    """Query parameter names as the router will see them.

    Per the RCI spec (01_http_api_basics.md, "B.1.1") a query parameter is an argument
    to the command named by the path, so `/rci/system/configuration?save` reaches the
    router as the same action as `/rci/system/configuration/save`. Checking only the
    path would gate one spelling of an action and wave through the other.
    """
    keys: set[str] = set()
    raw = query.lstrip("?")
    # parse_qsl stopped treating `;` as a parameter separator in 3.10, so parse both
    # spellings and keep every name either one yields: `?x=1;save` names only `x`
    # under the modern rules but may name `save` to a router that still splits on it.
    for source in {raw, raw.replace(";", "&")}:
        for name, _ in parse_qsl(source, keep_blank_values=True):
            # parse_qsl percent-decodes the name, so a name may still contain what the
            # router could read as a separator; split on it rather than let `save%2f..`
            # hide the action inside one opaque key. `&` and `=` are split for the
            # same reason and are the separators the RCI spec actually names for the
            # query channel (01_http_api_basics.md, "B.1.1"): `?a%26save=1` decodes to
            # the single name `a&save` here, but reaches the router as a string it may
            # re-split into `a` and `save`.
            for part in QUERY_SEPARATORS_RE.split(name.replace("\\", "/")):
                keys |= canonical_forms(part)
    return keys


def ensure_safe_router_request(
    method: str,
    endpoint: str,
    unsafe: bool,
    *,
    has_body: bool = False,
) -> str:
    """Gate router requests that can change state and return the endpoint to send.

    Allowed without --unsafe: a GET with no request body, which the RCI spec defines
    as read-only (settings are retrieved, actions are not executed). Everything else
    -- any non-GET method, a GET on an action path such as
    /rci/system/configuration/save, and a GET carrying a body -- requires the caller
    to opt in explicitly.

    The returned endpoint has any fragment stripped, so that the string this function
    inspected is the string that is actually sent.
    """
    normalized_method = method.strip().upper()
    if not HTTP_METHOD_RE.match(normalized_method):
        raise CliError(f"Invalid HTTP method: {method!r}. Use a plain verb such as GET.")
    path, query = split_endpoint(endpoint.strip())
    sanitized_endpoint = f"{path}{query}"
    # The endpoint is concatenated onto the router base URL, so anything other than a
    # single-slash-rooted path can move the request to a different host entirely:
    # "@evil.example/rci/show/version" turns the router's host:port into URL userinfo
    # and sends the request -- and any --unsafe body -- to evil.example. This check is
    # about *which machine* is contacted, so --unsafe does not waive it.
    if not path.startswith("/") or path.startswith("//"):
        raise CliError(
            f"Blocked: endpoint must be a router path starting with a single '/', "
            f"got {endpoint!r}. It is joined to the router URL, so any other form "
            "can redirect the request to another host."
        )
    if unsafe:
        return sanitized_endpoint
    if normalized_method != "GET":
        raise CliError(
            f"Blocked: {normalized_method} {sanitized_endpoint} can modify the router. "
            "Only GET is allowed by default. Re-read the current state first, confirm "
            "the blast radius of any removal, then add --unsafe to proceed."
        )
    offending = (
        canonical_path_segments(path) | canonical_query_keys(query)
    ) & ACTION_PATH_SEGMENTS
    if offending:
        raise CliError(
            f"Blocked: GET {sanitized_endpoint} names the action "
            f"'{min(offending)}'. Reads are allowed by default, but this path could "
            "execute something irreversible. Add --unsafe only if you intend to run it."
        )
    if has_body:
        # Per the RCI spec a GET returns data that was previously POSTed and has no
        # legitimate body, so a body on a GET is an attempt to express a mutation in
        # a form the path-based check above cannot see.
        raise CliError(
            f"Blocked: GET {sanitized_endpoint} carries a request body. A read has no "
            "body; a nested command sent this way would bypass the endpoint check. "
            "Use --unsafe if you intend to run it."
        )
    return sanitized_endpoint


def as_router_flag(value: Any) -> bool:
    """Coerce a router boolean.

    RCI mixes real JSON booleans with "yes"/"no" strings for the same kind of field
    (01_http_api_basics.md renders `"connected": "yes"` next to `"global": false`), and
    bool("no") is True -- which would report every offline client as active.
    """
    if isinstance(value, bool):
        return value
    return str(value).strip().casefold() in {"yes", "true", "1"}


def value_as_text(value: Any) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return sanitize_text(str(value))


def parse_since(value: str) -> datetime:
    # Every datetime here is deliberately naive (hence the DTZ noqas below). `show log`
    # emits `Jan 05 11:00:00` -- no zone, no year -- which is the router's local wall
    # clock, and --since is the operator typing their own local wall clock. Both are
    # compared against datetime.now(); attaching UTC would silently shift every
    # comparison by the local offset, and there is no zone on the wire to attach
    # instead.
    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)  # noqa: DTZ007 - naive by design
        except ValueError:
            continue
    raise CliError(
        "Invalid --since value. Use 'YYYY-MM-DD HH:MM:SS' "
        "or 'YYYY-MM-DD HH:MM'."
    )


def parse_log_timestamp(value: str, now: datetime | None = None) -> datetime | None:
    now = now or datetime.now()  # noqa: DTZ005 - naive by design, see parse_since
    match = re.fullmatch(r"([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})", value.strip())
    if not match:
        return None
    month, day, time_part = match.groups()
    try:
        parsed = datetime.strptime(  # noqa: DTZ007 - naive by design, see parse_since
            f"{now.year} {month} {int(day):02d} {time_part}", "%Y %b %d %H:%M:%S"
        )
    except ValueError:
        return None
    if parsed > now + timedelta(days=1):
        try:
            parsed = parsed.replace(year=now.year - 1)
        except ValueError:
            # Feb 29 in a leap year has no counterpart in the previous year.
            return None
    return parsed


def extract_log_entries(response: Any) -> list[dict[str, Any]]:
    # The router reports a rejected command inside a 200 body, so a missing `log` key
    # may mean "the command failed and said why" rather than "this shape is
    # unexpected". Checking the status array first keeps the router's own explanation
    # instead of replacing it with a generic shape complaint.
    errors = collect_rci_errors(response)
    if errors:
        raise CliError(f"Router rejected show log: {'; '.join(errors)}")
    try:
        raw_log = response[0]["show"]["log"]["log"]
    except (KeyError, IndexError, TypeError) as err:
        raise CliError("Unexpected response for show log.") from err

    # The router normally answers with a mapping of key -> row, but RCI renders a
    # repeated element as a list and a lone entry as the row object itself
    # (01_http_api_basics.md, "B.1.3.3"), and an empty log has no entries at all.
    # `show log` is the agent's main diagnostic path, so a shape difference must not
    # fail it outright the way it would elsewhere.
    if raw_log is None:
        rows: list[tuple[Any, Any]] = []
    elif isinstance(raw_log, list):
        rows = list(enumerate(raw_log))
    elif isinstance(raw_log, dict):
        # A row carries "message"/"timestamp"; a mapping is keyed by entry id.
        if "message" in raw_log or "timestamp" in raw_log:
            rows = [(raw_log.get("id", 0), raw_log)]
        else:
            rows = list(raw_log.items())
    else:
        raise CliError("Unexpected log shape for show log.")

    entries: list[dict[str, Any]] = []
    for key, row in rows:
        if not isinstance(row, dict):
            continue
        message_data = row.get("message") if isinstance(row.get("message"), dict) else {}
        message_text = str(message_data.get("message") or "")
        entry = {
            "id": row.get("id", key),
            "timestamp": row.get("timestamp", ""),
            "ident": row.get("ident", ""),
            "label": message_data.get("label", ""),
            "level": message_data.get("level", ""),
            "message": message_text,
        }
        if "repeated" in message_data:
            entry["repeated"] = message_data["repeated"]
        entries.append(entry)

    def sort_key(entry: dict[str, Any]) -> int:
        try:
            return int(entry["id"])
        except (TypeError, ValueError):
            return 0

    return sorted(entries, key=sort_key)


def is_error_log_entry(entry: dict[str, Any]) -> bool:
    label = str(entry.get("label", "")).upper()
    level = str(entry.get("level", "")).casefold()
    message = str(entry.get("message", "")).casefold()
    return (
        label in ERROR_LABELS
        or level in ERROR_LEVELS
        or any(pattern in message for pattern in ERROR_MESSAGE_PATTERNS)
    )


def filter_log_entries(
    entries: list[dict[str, Any]],
    *,
    since: datetime | None = None,
    errors_only: bool = False,
    grep: str | None = None,
) -> list[dict[str, Any]]:
    filtered = entries
    if since is not None:
        kept: list[dict[str, Any]] = []
        unparsed = 0
        for entry in filtered:
            parsed = parse_log_timestamp(str(entry.get("timestamp", "")))
            if parsed is None:
                unparsed += 1
                continue
            if parsed >= since:
                kept.append(entry)
        if unparsed:
            # Silently dropping these would turn a timestamp-format change into a
            # confident "no errors in the last N minutes".
            print(
                f"Warning: {unparsed} log entr{'y' if unparsed == 1 else 'ies'} had an "
                "unrecognised timestamp and were excluded by the time filter.",
                file=sys.stderr,
            )
        filtered = kept
    if errors_only:
        filtered = [entry for entry in filtered if is_error_log_entry(entry)]
    if grep:
        needle = grep.casefold()
        filtered = [
            entry
            for entry in filtered
            if needle
            in " ".join(
                str(entry.get(field, ""))
                for field in ("timestamp", "ident", "label", "level", "message")
            ).casefold()
        ]
    return filtered


def raise_rci_errors(data: Any, endpoint: str) -> None:
    """Fail a read whose HTTP 200 body carries an RCI error status.

    The router reports command failure inside a 200 body, so a read that the router
    refused arrives here as a body with no data key and a "status" array explaining
    why. Normalising that to "no rows" would report `show interfaces` as
    "No interfaces found." and `list clients` as "No active clients found." -- the
    agent would conclude the router has no interfaces rather than that the read
    failed, and would act on it. extract_log_entries already checks this first; these
    are the paths that did not.
    """
    errors = collect_rci_errors(data)
    if errors:
        raise CliError(f"Router rejected {endpoint}: {'; '.join(errors)}")


def normalize_rci_rows(data: Any, endpoint: str) -> list[dict[str, Any]]:
    """Normalise a "multiple input" RCI subtree into a list of rows.

    Such a subtree normally comes back as a list, but with no entries the router
    answers with an empty object and with a single entry it may answer with the object
    itself. Raising on those would break `list clients` on a router that has no host
    rules; returning [] for a genuinely unparseable shape would render every client's
    policy as "-", which is indistinguishable from "no client has a policy".

    Rows of the wrong type are dropped rather than raising: they reach here from a live
    response, and one bad row must not turn a read into a traceback.
    """
    raise_rci_errors(data, endpoint)
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if data is None:
        return []
    if isinstance(data, dict):
        return [data] if data else []
    raise CliError(f"Unexpected response for {endpoint}.")


def dict_values_only(data: Any, endpoint: str) -> dict[str, dict[str, Any]]:
    """An RCI mapping response, with entries of an unexpected type dropped."""
    raise_rci_errors(data, endpoint)
    if not isinstance(data, dict):
        raise CliError(f"Unexpected response for {endpoint}.")
    return {key: value for key, value in data.items() if isinstance(value, dict)}


class KeeneticApiClient:
    """Minimal Keenetic API client for CLI operations."""

    def __init__(self, session: aiohttp.ClientSession, cfg: RouterConfig) -> None:
        self._session = session
        self._cfg = cfg
        self._base_url = build_base_url(cfg.host, cfg.port, cfg.ssl)
        self._authenticated = False

    @property
    def router_host(self) -> str:
        """The configured router address. Exposed instead of the whole config so that
        a caller needing the host cannot reach the password through the same handle."""
        return self._cfg.host

    async def _request_raw(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | list[Any] | None = None,
    ) -> tuple[int, Mapping[str, str], Any]:
        url = f"{self._base_url}{endpoint}"
        # Defence in depth behind ensure_safe_router_request: whatever string arrives
        # here, the request must go to the configured router and nowhere else.
        target = urlparse(url)
        base = urlparse(self._base_url)
        if (target.scheme, target.netloc) != (base.scheme, base.netloc):
            raise CliError(
                f"Blocked: endpoint {endpoint!r} would send the request to "
                f"{target.netloc!r} instead of the configured router."
            )
        # The check above pins only the first hop. aiohttp follows redirects by
        # default, and a 307/308 replays the method and body -- including the /auth
        # credentials and any --data-json -- at whatever host the Location names, so
        # a compromised router or an on-path attacker on the default plaintext
        # transport could move the request off-box after the check has passed. RCI
        # does not redirect; let a 3xx fall through to the status handling below.
        async with self._session.request(
            method=method, url=url, json=payload, allow_redirects=False
        ) as response:
            # `.copy()` keeps aiohttp's CIMultiDict rather than flattening it into a
            # plain dict: HTTP header names are case-insensitive and nothing
            # guarantees the router (or a proxy in front of it, or an HTTP/2 hop)
            # spells `X-NDM-Challenge` the way auth() looks it up. A plain-dict copy
            # would turn any other casing into "missing challenge data" and take
            # every command down.
            headers = response.headers.copy()
            if response.content_type == "application/json":
                try:
                    body: Any = await response.json()
                except (json.JSONDecodeError, aiohttp.ContentTypeError) as err:
                    raise CliError(
                        f"Router returned malformed JSON for {method} {endpoint}: {err}"
                    ) from err
            elif response.content_type == "application/javascript":
                body = self._parse_javascript_response(await response.text())
            else:
                body = await response.text()
            return response.status, headers, body

    async def auth(self) -> None:
        """Authenticate once per process; the cookie jar carries the session after that."""
        if self._authenticated:
            return
        status, headers, _ = await self._request_raw("GET", "/auth")
        if status == 200:
            self._authenticated = True
            return
        if status != 401:
            raise CliError(f"Auth request failed with HTTP {status}.")

        realm = headers.get("X-NDM-Realm")
        challenge = headers.get("X-NDM-Challenge")
        if not realm or not challenge:
            raise CliError("Router auth headers are missing challenge data.")

        password = f"{self._cfg.username}:{realm}:{self._cfg.password}"
        pass_md5 = md5(password.encode("utf-8")).hexdigest()
        pass_sha = sha256(f"{challenge}{pass_md5}".encode()).hexdigest()

        status, _, body = await self._request_raw(
            "POST",
            "/auth",
            {"login": self._cfg.username, "password": pass_sha},
        )
        if status != 200:
            raise CliError(
                f"Authentication failed with HTTP {status}: {describe_response_body(body)}"
            )
        self._authenticated = True

    async def api(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | list[Any] | None = None,
    ) -> Any:
        await self.auth()
        # ensure_safe_router_request validates the *normalised* method, so the padded
        # form it accepts has to be normalised here too: aiohttp rejects " GET " with a
        # ValueError that reaches the agent as a traceback instead of an "Error:" line.
        method = method.strip().upper()
        status, _, body = await self._request_raw(method, endpoint, payload)
        if status != 200:
            raise CliError(
                f"Request {method} {endpoint} failed with HTTP {status}: "
                f"{describe_response_body(body)}"
            )
        return body

    @staticmethod
    def _parse_javascript_response(data: str) -> dict[str, str]:
        parsed: dict[str, str] = {}
        prepared = data.replace("\n\t", "").replace("\n", "")
        for row in prepared.split(";"):
            if not row.strip() or "=" not in row:
                continue
            key, value = row.split("=", 1)
            key = key.strip()
            value = value.lstrip()
            if "{" not in value:
                value = value.replace('"', "")
            parsed[key] = value
        return parsed

    async def show_ip_hotspot(self) -> list[dict[str, Any]]:
        endpoint = "/rci/show/ip/hotspot/host"
        return normalize_rci_rows(await self.api("GET", endpoint), endpoint)

    async def show_rc_ip_hotspot_host(self) -> list[dict[str, Any]]:
        endpoint = "/rci/show/rc/ip/hotspot/host"
        return normalize_rci_rows(await self.api("GET", endpoint), endpoint)

    async def show_interface(self) -> dict[str, dict[str, Any]]:
        return dict_values_only(
            await self.api("GET", "/rci/show/interface"), "/rci/show/interface"
        )

    async def show_interface_stat(self, interface: str) -> dict[str, Any]:
        data = await self.api("GET", f"/rci/show/interface/stat?name={quote(interface, safe='')}")
        if not isinstance(data, dict):
            raise CliError("Unexpected response for /rci/show/interface/stat.")
        return data

    async def show_log(self, max_lines: int) -> list[dict[str, Any]]:
        payload = [{"show": {"log": {"max-lines": max_lines}}}]
        data = await self.api("POST", "/rci/", payload)
        return extract_log_entries(data)

    async def show_ip_dhcp_pool(self) -> dict[str, dict[str, Any]]:
        endpoint = "/rci/show/ip/dhcp/pool"
        return dict_values_only(await self.api("GET", endpoint), endpoint)

    async def show_ip_dhcp_bindings(self) -> list[dict[str, Any]]:
        # Both reservations and running leases come back under one `lease` key; they
        # differ by `expires` ("infinity" for a reservation), not by which key holds them.
        endpoint = "/rci/show/ip/dhcp/bindings"
        data = await self.api("GET", endpoint)
        if isinstance(data, dict):
            rows = data.get("lease", [])
            return [row for row in rows if isinstance(row, dict)]
        return normalize_rci_rows(data, endpoint)

    async def ip_policy_list(self) -> dict[str, dict[str, Any]]:
        return dict_values_only(await self.api("GET", "/rci/ip/policy"), "/rci/ip/policy")

    async def ip_hotspot_host_policy(
        self,
        mac: str,
        access: str,
        policy: str | dict[str, bool],
    ) -> Any:
        # Per 04_commands_ip_ipv6_network.md ("ip hotspot host", Change settings: Yes)
        # this writes the running configuration only; without the batched
        # `system configuration save` (07_commands_..._system_tools_users_vpn.md,
        # "system configuration save") the policy is lost on reboot.
        payload = [
            {"ip": {"hotspot": {"host": {"mac": mac, access: True, "policy": policy}}}},
            {"system": {"configuration": {"save": {}}}},
        ]
        return await self.api("POST", "/rci/", payload)

def split_batched_policy_response(response: Any) -> tuple[Any, Any]:
    """Split the `[host rule, configuration save]` batch response into its two halves.

    RCI reproduces the request array element for element (01_http_api_basics.md,
    "B.1.3.4"), so element 0 reports on the policy write and element 1 on the save.
    Reading errors from the whole body blames the policy write for a flash-write
    failure on the save -- and aborts before the read-back that says whether the
    policy actually changed, which is the one inversion the read-back exists to
    prevent. An unexpected shape falls back to treating the whole body as the policy
    result: over-reporting a failure is safer than missing one.
    """
    if isinstance(response, list) and len(response) == 2:
        return response[0], response[1]
    return response, None


def select_dhcp_pool(
    pools: dict[str, dict[str, Any]],
    router_host: str,
    requested: str | None,
) -> tuple[str, dict[str, Any]]:
    """Pick the DHCP pool to report on, by name or by the router address in use.

    Defaulting to "the pool whose network contains the router we are talking to" keeps
    this portable: a Keenetic serves a pool per bridge (a guest network is its own
    pool with its own subnet), and the one the operator means is the LAN they reached
    the router through. Hard-coding a subnet would tie the tool to one household.
    """
    if requested:
        pool = pools.get(requested)
        if not isinstance(pool, dict):
            available = sanitize_text(", ".join(sorted(pools)))
            raise CliError(f"Unknown DHCP pool '{requested}'. Available: {available}.")
        return requested, pool

    try:
        router_ip = ipaddress.ip_address(router_host)
    except ValueError:
        available = sanitize_text(", ".join(sorted(pools)))
        raise CliError(
            f"KEENETIC_HOST is '{router_host}', not a plain address, so the pool cannot "
            f"be chosen automatically. Name one with --pool. Available: {available}."
        ) from None

    for name, pool in sorted(pools.items()):
        if not isinstance(pool, dict):
            continue
        try:
            network = ipaddress.ip_network(str(pool.get("network", "")), strict=False)
        except ValueError:
            continue
        if router_ip in network:
            return name, pool

    available = sanitize_text(", ".join(sorted(pools)))
    raise CliError(
        f"No DHCP pool covers the router address {router_ip}. Name one with --pool. "
        f"Available: {available}."
    )


def collect_address_usage(
    bindings: list[dict[str, Any]],
    hotspot_rows: list[dict[str, Any]],
    network: Any,
) -> dict[str, dict[str, Any]]:
    """Addresses inside `network` that the router knows are in use, and on what evidence.

    Filtering by network is not cosmetic. A Keenetic serves several subnets at once, so
    both sources carry rows for every bridge; counting them all would report the guest
    network's leases as occupying the LAN. Rows also arrive with placeholder addresses
    (`0.0.0.0` for a client seen without a lease), which belong in no network's count.

    Three kinds, because they answer different questions:
      - `reservation` — a DHCP binding that never expires; the address belongs to that
        host and handing it to anything else collides.
      - `lease` — a running DHCP lease; free once it expires, but taken right now.
      - `seen` — a host the router sees at an address DHCP never handed out, i.e. one
        configured on the device itself. These are invisible to /rci/show/ip/dhcp/*,
        and a "free" address chosen without them is the classic silent collision.
    """
    usage: dict[str, dict[str, Any]] = {}

    def inside(raw: str) -> bool:
        try:
            return ipaddress.ip_address(raw) in network
        except ValueError:
            return False

    for row in bindings:
        ip = str(row.get("ip", "")).strip()
        if not inside(ip):
            continue
        usage[ip] = {
            "ip": ip,
            "kind": "reservation" if row.get("expires") == "infinity" else "lease",
            "mac": row.get("mac") or row.get("via"),
            "name": row.get("name") or row.get("hostname"),
            "expires": row.get("expires"),
        }

    for row in hotspot_rows:
        ip = str(row.get("ip", "")).strip()
        if ip in usage or not inside(ip):
            continue
        usage[ip] = {
            "ip": ip,
            "kind": "seen",
            "mac": row.get("mac"),
            "name": row.get("name") or row.get("hostname"),
            "expires": None,
        }

    return usage


def group_into_ranges(addresses: list[Any]) -> list[tuple[Any, Any]]:
    """Collapse a sorted address list into inclusive (first, last) runs."""
    ranges: list[tuple[Any, Any]] = []
    for address in addresses:
        if ranges and int(address) == int(ranges[-1][1]) + 1:
            ranges[-1] = (ranges[-1][0], address)
        else:
            ranges.append((address, address))
    return ranges


def render_ranges(ranges: list[tuple[Any, Any]]) -> str:
    return ", ".join(
        str(first) if first == last else f"{first}-{last}" for first, last in ranges
    ) or "-"


def free_addresses(
    network: Any,
    pool_begin: Any,
    pool_end: Any,
    taken: set[str],
    router_ip: Any | None,
) -> tuple[list[Any], list[Any]]:
    """Free addresses, split into (outside the DHCP pool, inside it).

    The split is the whole point. Only the outside half is safe to configure statically
    on a device: an address inside the pool is free *this second*, and the router may
    hand it to the next machine that asks. Reporting one list would invite exactly the
    collision the command exists to prevent.
    """
    outside: list[Any] = []
    inside: list[Any] = []
    for address in network.hosts():
        if str(address) in taken or address == router_ip:
            continue
        if pool_begin <= address <= pool_end:
            inside.append(address)
        else:
            outside.append(address)
    return outside, inside


def policy_identity(row: dict[str, Any] | None) -> str | None:
    """The policy id a hotspot-host row denotes, in the vocabulary of `set policy`.

    Returns the same strings resolve_policy produces, so a write can be compared
    against the state read back afterwards. None means "no rule" or "unrecognised
    rule" -- never assume unrestricted access from an unreadable row.
    """
    if not isinstance(row, dict):
        return None
    access = str(row.get("access", "")).casefold()
    # `access` and `policy` are independent settings on the same host, not two
    # spellings of one (04_commands_ip_ipv6_network.md, "3.52.7 ip hotspot host":
    # the synopsis applies one of access/schedule/policy per invocation, and
    # `no host <mac> <which>` removes each separately), so a host can carry a policy
    # *and* be denied. `deny` is documented as "Deny access to the internet", which
    # outranks a policy: a policy only selects a routing profile for traffic allowed
    # out at all. Checking `policy` first would report a cut-off client as merely
    # routed somewhere -- the same inversion render_policy refuses to make for an
    # unreadable row. This CLI never writes that pair (it clears the policy when
    # denying), but the router's own CLI and web UI can.
    if access == "deny":
        return "not_internet"
    policy_name = row.get("policy")
    if policy_name:
        return str(policy_name)
    if access == "permit":
        return "default"
    return None


def render_policy(
    row: dict[str, Any] | None,
    available_policies: dict[str, dict[str, Any]],
) -> str:
    if not row:
        return "-"
    identity = policy_identity(row)
    if identity is None:
        # Reporting an unrecognised row as "default" would claim a restricted client
        # is unrestricted; say so instead.
        return "unknown"
    if identity in {"default", "not_internet"}:
        return identity
    policy_data = available_policies.get(identity)
    description = (
        str(policy_data.get("description", "")).strip()
        if isinstance(policy_data, dict)
        else ""
    )
    # Both halves are router-supplied text that ends up interpolated into single-line
    # output the agent parses as router state; a newline in a policy description would
    # forge lines there.
    identity = sanitize_text(identity)
    description = sanitize_text(description)
    return f"{identity} ({description})" if description else identity


def print_table(
    headers: tuple[str, ...],
    rows: list[tuple[str, ...]],
    *,
    empty_message: str,
) -> None:
    """Render a fixed-width table.

    The column layout is a de-facto output contract for the consuming agent, so the
    padding rule (two spaces between columns, every column left-justified) is shared
    by all callers rather than reimplemented per command.
    """
    if not rows:
        print(empty_message)
        return

    widths = [len(header) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))

    def format_row(values: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(widths[idx]) for idx, value in enumerate(values))

    print(format_row(headers))
    print(format_row(tuple("-" * width for width in widths)))
    for row in rows:
        print(format_row(row))


def build_client_records(
    clients: list[dict[str, Any]],
    policy_by_mac: dict[str, dict[str, Any]],
    available_policies: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Normalise router client rows into the records both output modes render.

    Rows are collapsed by MAC. `show ip hotspot` returns one row per interface a host
    is reachable through (06_commands_show.md, "3.166.56"), so a single client on two
    interfaces arrives as two rows carrying the same MAC -- which is exactly why
    resolve_client_mac_by_name de-duplicates before calling a name ambiguous. Emitting
    both rows here would contradict that: `list clients --json` would report one
    device twice, and an agent counting clients or diffing the list across a
    `set policy` would see a phantom device appear or vanish with the interface.

    Merging prefers the active row -- a host may be stale on one interface and current
    on another -- and otherwise fills each field from the first row that carries it.
    """
    records: dict[str, dict[str, Any]] = {}
    for client in clients:
        if not isinstance(client, dict):
            # A row of an unexpected shape carries no client identity, so there is
            # nothing to report about it; dropping it beats a traceback.
            continue
        mac = normalize_mac(str(client.get("mac", "")))
        record = {
            "mac": mac,
            "name": client.get("name") or None,
            "hostname": client.get("hostname") or None,
            "ip": client.get("ip") or None,
            "active": as_router_flag(client.get("active")),
            "policy": render_policy(policy_by_mac.get(mac), available_policies),
        }
        previous = records.get(mac)
        if previous is None:
            records[mac] = record
            continue
        if record["active"] and not previous["active"]:
            # The active row wins outright, but must not lose a field only the
            # inactive row carried.
            for field in ("name", "hostname", "ip"):
                if record[field] is None:
                    record[field] = previous[field]
            records[mac] = record
        else:
            for field in ("name", "hostname", "ip"):
                if previous[field] is None:
                    previous[field] = record[field]
            previous["active"] = previous["active"] or record["active"]
    return sorted(
        records.values(),
        key=lambda record: (str(record["name"] or "").casefold(), record["mac"]),
    )


def print_clients_table(
    records: list[dict[str, Any]],
    empty_message: str = "No clients found.",
) -> None:
    headers = ("MAC", "Name", "Hostname", "IP", "Active", "Policy")
    rows = [
        (
            value_as_text(record["mac"]),
            value_as_text(record["name"]),
            value_as_text(record["hostname"]),
            value_as_text(record["ip"]),
            "yes" if record["active"] else "no",
            value_as_text(record["policy"]),
        )
        for record in records
    ]
    print_table(headers, rows, empty_message=empty_message)


def build_policy_records(
    available_policies: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = [
        {"policy": "default", "description": "Allow internet access without explicit policy"},
        {"policy": "not_internet", "description": "Deny internet access"},
    ]
    for policy_id in sorted(available_policies):
        data = available_policies[policy_id]
        records.append(
            {
                "policy": policy_id,
                "description": (data.get("description") if isinstance(data, dict) else None)
                or None,
            }
        )
    return records


def print_policies_table(records: list[dict[str, Any]]) -> None:
    rows = [
        (value_as_text(record["policy"]), value_as_text(record["description"]))
        for record in records
    ]
    print_table(("Policy", "Description"), rows, empty_message="No policies found.")


def print_interfaces_table(interfaces: dict[str, dict[str, Any]]) -> None:
    headers = ("Name", "Type", "Connected", "Link", "Address", "Description")
    rows = [
        (
            value_as_text(name),
            value_as_text(data.get("type")),
            value_as_text(data.get("connected")),
            value_as_text(data.get("link")),
            value_as_text(data.get("address")),
            value_as_text(data.get("description")),
        )
        for name, data in sorted(interfaces.items(), key=lambda item: item[0].casefold())
    ]
    print_table(headers, rows, empty_message="No interfaces found.")


def print_log_entries(entries: list[dict[str, Any]]) -> None:
    if not entries:
        print("No log entries found.")
        return
    for entry in entries:
        repeated = f" repeated={entry['repeated']}" if "repeated" in entry else ""
        print(
            f"{value_as_text(entry.get('timestamp'))} "
            f"{value_as_text(entry.get('label')):<1} "
            f"{value_as_text(entry.get('level')):<8} "
            f"{value_as_text(entry.get('ident')):<10} "
            f"#{value_as_text(entry.get('id'))}{repeated} "
            f"{value_as_text(entry.get('message'))}"
        )


async def resolve_client_mac_by_mac(client: KeeneticApiClient, mac_ref: str) -> str:
    target_mac = normalize_mac(mac_ref)
    if not MAC_RE.fullmatch(target_mac):
        raise CliError(f"Invalid MAC address format: {mac_ref}")

    clients = await client.show_ip_hotspot()
    if any(normalize_mac(str(row.get("mac", ""))) == target_mac for row in clients):
        return target_mac
    raise CliError(f"Client with MAC {mac_ref} was not found in router client list.")


async def resolve_client_mac_by_name(client: KeeneticApiClient, name_ref: str) -> str:
    clients = await client.show_ip_hotspot()
    matches: list[str] = []
    wanted_cf = name_ref.strip().casefold()
    for row in clients:
        name = str(row.get("name") or "")
        hostname = str(row.get("hostname") or "")
        if name.casefold() == wanted_cf or hostname.casefold() == wanted_cf:
            matches.append(normalize_mac(str(row.get("mac", ""))))

    if not matches:
        raise CliError(f"Client '{name_ref}' not found. Use exact name/hostname or MAC address.")
    # De-duplicated before counting: `show ip hotspot` returns one row per interface a
    # host is reachable through (06_commands_show.md, "3.166.56"), so a single client
    # on two interfaces yields two rows with the same MAC. That is not an ambiguity,
    # and "use the MAC instead" would be advice the agent cannot act on -- there is
    # only one. Two *different* MACs still raise.
    unique = set(matches)
    if len(unique) > 1:
        raise CliError(f"Client name '{name_ref}' is ambiguous. Use MAC address instead.")
    return matches[0]


async def resolve_policy(
    client: KeeneticApiClient,
    policy_name: str,
) -> tuple[str, str | dict[str, bool], str]:
    policy_raw = policy_name.strip()
    policy_cf = policy_raw.casefold()

    if policy_cf in {"default", "permit"}:
        return "permit", {"no": True}, "default"
    if policy_cf in {"not_internet", "deny"}:
        return "deny", {"no": True}, "not_internet"

    policies = await client.ip_policy_list()

    if policy_raw in policies:
        return "permit", policy_raw, policy_raw

    by_description = [
        policy_id
        for policy_id, data in policies.items()
        if str(data.get("description", "")).casefold() == policy_cf
    ]
    if len(by_description) == 1:
        # Returned raw: the middle element goes on the wire as the policy to set, and
        # the last is compared against the id read back. Sanitizing happens where the
        # value is interpolated into text output instead (see cmd_set_policy).
        policy_id = by_description[0]
        return "permit", policy_id, policy_id
    if len(by_description) > 1:
        raise CliError(f"Policy description '{policy_name}' is ambiguous. Use policy id.")

    # Policy ids come from the router, so sanitize before joining them into a
    # single-line error the agent reads.
    available = ["default", "not_internet", *sorted(policies.keys())]
    joined = sanitize_text(", ".join(str(name) for name in available))
    raise CliError(f"Unknown policy '{policy_name}'. Available policies: {joined}")


async def cmd_list_clients(
    client: KeeneticApiClient,
    include_inactive: bool,
    as_json: bool = False,
) -> None:
    clients = await client.show_ip_hotspot()
    if not include_inactive:
        clients = [row for row in clients if as_router_flag(row.get("active"))]

    policy_rows = await client.show_rc_ip_hotspot_host()
    available_policies = await client.ip_policy_list()
    policy_by_mac = {
        normalize_mac(str(row.get("mac", ""))): row
        for row in policy_rows
        if row.get("mac")
    }
    records = build_client_records(clients, policy_by_mac, available_policies)
    if as_json:
        output_json(records)
        return
    # Redaction applies in every output mode; neither list command has --no-redact, so
    # the table must not be the one way around it.
    print_clients_table(
        redact_sensitive(records),
        empty_message="No active clients found." if not include_inactive else "No clients found.",
    )


async def cmd_show_dhcp(
    client: KeeneticApiClient,
    pool_name: str | None = None,
    occupied: bool = False,
    as_json: bool = False,
) -> None:
    pools = await client.show_ip_dhcp_pool()
    name, pool = select_dhcp_pool(pools, client.router_host, pool_name)

    try:
        network = ipaddress.ip_network(str(pool["network"]), strict=False)
        pool_begin = ipaddress.ip_address(str(pool["begin"]))
        pool_end = ipaddress.ip_address(str(pool["end"]))
    except (KeyError, ValueError) as err:
        raise CliError(f"DHCP pool '{name}' has no usable network/begin/end.") from err

    router_ip = None
    router_field = pool.get("router")
    if isinstance(router_field, dict):
        with contextlib.suppress(ValueError):
            router_ip = ipaddress.ip_address(str(router_field.get("router", "")))

    # Both sources are needed: /rci/show/ip/dhcp/bindings misses an address configured
    # on the device itself, and the hotspot registry misses a reservation for a host
    # that is currently offline.
    usage = collect_address_usage(
        await client.show_ip_dhcp_bindings(),
        await client.show_ip_hotspot(),
        network,
    )
    outside, inside = free_addresses(network, pool_begin, pool_end, set(usage), router_ip)
    counts = Counter(record["kind"] for record in usage.values())

    if as_json:
        output_json(
            {
                "pool": name,
                "network": str(network),
                "router": str(router_ip) if router_ip else None,
                "pool_begin": str(pool_begin),
                "pool_end": str(pool_end),
                "occupied_total": len(usage),
                "occupied_by_kind": dict(counts),
                # Only `free_outside_pool` is safe to configure on a device; the router
                # can hand out anything in `free_inside_pool` at any moment.
                "free_outside_pool": [str(a) for a in outside],
                "free_inside_pool": [str(a) for a in inside],
                "occupied": sorted(
                    redact_sensitive(list(usage.values())),
                    key=lambda r: ipaddress.ip_address(r["ip"]),
                ),
            }
        )
        return

    print(f"Pool {name}: {pool_begin}-{pool_end} on {network}")
    if router_ip:
        print(f"Router: {router_ip}")
    print(
        f"Occupied: {len(usage)} "
        f"({counts['reservation']} reservations, {counts['lease']} leases, "
        f"{counts['seen']} seen only)"
    )
    print()
    print(f"Free outside the pool ({len(outside)}) - safe to assign statically:")
    print(f"  {render_ranges(group_into_ranges(outside))}")
    print()
    print(f"Free inside the pool ({len(inside)}) - the router may hand these out:")
    print(f"  {render_ranges(group_into_ranges(inside))}")

    if occupied:
        print()
        records = redact_sensitive(
            sorted(usage.values(), key=lambda r: ipaddress.ip_address(r["ip"]))
        )
        print_table(
            ("IP", "Kind", "MAC", "Name"),
            [
                (
                    value_as_text(r["ip"]),
                    value_as_text(r["kind"]),
                    value_as_text(r.get("mac")),
                    value_as_text(r.get("name")),
                )
                for r in records
            ],
            empty_message="No occupied addresses found.",
        )


async def cmd_list_policies(client: KeeneticApiClient, as_json: bool = False) -> None:
    records = build_policy_records(await client.ip_policy_list())
    if as_json:
        output_json(records)
        return
    print_policies_table(redact_sensitive(records))


async def cmd_set_policy(
    client: KeeneticApiClient,
    mac_ref: str | None,
    name_ref: str | None,
    policy_name: str,
    as_json: bool = False,
) -> None:
    if mac_ref:
        mac = await resolve_client_mac_by_mac(client, mac_ref)
    elif name_ref:
        mac = await resolve_client_mac_by_name(client, name_ref)
    else:
        raise CliError("Specify either --mac or --name.")

    access, policy_payload, resolved_policy = await resolve_policy(client, policy_name)
    response = await client.ip_hotspot_host_policy(
        mac=mac, access=access, policy=policy_payload
    )
    policy_response, save_response = split_batched_policy_response(response)
    errors = collect_rci_errors(policy_response)
    if errors:
        raise CliError(
            f"Router rejected policy change for {mac}: {'; '.join(errors)}"
        )
    # Neither a warning nor a failure of the batched `system configuration save` may
    # abort before the read-back below, which is what determines whether the policy
    # actually changed. A save that failed means the change is live but will not
    # survive a reboot -- reported separately, after the read-back has spoken.
    warnings = collect_rci_warnings(policy_response) + collect_rci_warnings(save_response)
    persist_errors = collect_rci_errors(save_response)
    # An absent save half means split_batched_policy_response did not recognise the
    # response shape, so nothing here ever saw the `system configuration save` report.
    # "No errors came back" is not the same claim as "the save succeeded", and only
    # the second one may be published as `persisted`: an agent that reads `true` here
    # stops worrying about the change surviving a reboot.
    if save_response is None:
        warnings.append(
            "Router did not report on the batched `system configuration save`; "
            "whether the change survives a reboot is unknown."
        )
    persisted = save_response is not None and not persist_errors

    # The write reports success in a 200 body, so confirm it by reading the state back.
    observed_row = next(
        (
            row
            for row in await client.show_rc_ip_hotspot_host()
            if isinstance(row, dict) and normalize_mac(str(row.get("mac", ""))) == mac
        ),
        None,
    )
    observed_policy = policy_identity(observed_row)
    observed_label = render_policy(observed_row, await client.ip_policy_list())
    confirmed = observed_policy == resolved_policy

    if as_json:
        output_json(
            {
                "mac": mac,
                "requested_policy": resolved_policy,
                # The bare id, comparable to requested_policy; the human-readable
                # "Policy0 (Guests)" form lives in observed_policy_description.
                "observed_policy": observed_policy,
                "observed_policy_description": observed_label,
                "confirmed": confirmed,
                # False means the change is in the running configuration but the
                # batched `system configuration save` failed, so a reboot loses it.
                "persisted": persisted,
                "warnings": warnings,
            }
        )

    # Warnings go out before the `not confirmed` check below, not after it. A write
    # that was accepted but did not land is exactly the case a router warning is most
    # likely to explain, and raising first would discard them in table mode -- JSON
    # mode already emitted them above.
    if not as_json:
        for warning in warnings:
            print(f"Router warning: {warning}", file=sys.stderr)

    # The policy id is router-supplied, so neutralise control characters before it
    # goes into single-line output the agent parses as router state.
    requested_label = sanitize_text(resolved_policy)
    if not confirmed:
        # The router accepted the request without reporting an error, yet the state
        # read back does not match. Reporting success here would be a lie the agent
        # has no way to detect.
        raise CliError(
            f"Policy change for {mac} was accepted but not applied: requested "
            f"{requested_label}, router reports {observed_label}."
        )
    if not as_json:
        print(f"Policy updated: {mac} -> {requested_label} (router now reports: {observed_label})")
    if persist_errors:
        raise CliError(
            f"Policy change for {mac} was applied but not saved: "
            f"{'; '.join(persist_errors)}. It is active now and will be lost on reboot."
        )


async def cmd_api_request(
    client: KeeneticApiClient,
    method: str,
    endpoint: str,
    data_json: str | None,
    unsafe: bool,
    raw: bool,
    no_redact: bool,
) -> None:
    payload = parse_json_payload(data_json)
    safe_endpoint = ensure_safe_router_request(
        method, endpoint, unsafe, has_body=data_json is not None
    )
    response = await client.api(method, safe_endpoint, payload)
    output_json(response, raw=raw, redact=not no_redact)


async def cmd_show_interfaces(
    client: KeeneticApiClient,
    name: str | None,
    interface_type: str | None,
    connected: bool,
    as_json: bool,
    no_redact: bool,
) -> None:
    interfaces = await client.show_interface()

    if name:
        if name not in interfaces:
            raise CliError(f"Interface '{name}' was not found.")
        interfaces = {name: interfaces[name]}

    if interface_type:
        wanted_type = interface_type.casefold()
        interfaces = {
            interface_name: data
            for interface_name, data in interfaces.items()
            if str(data.get("type", "")).casefold() == wanted_type
        }

    if connected:
        interfaces = {
            interface_name: data
            for interface_name, data in interfaces.items()
            if as_router_flag(data.get("connected"))
        }

    if as_json:
        output_json(interfaces, redact=not no_redact)
        return

    print_interfaces_table(redact_sensitive(interfaces) if not no_redact else interfaces)


async def cmd_show_interface_stat(
    client: KeeneticApiClient,
    name: str,
    no_redact: bool,
) -> None:
    # This command has one output mode: JSON. There is no table form to switch to.
    stat = await client.show_interface_stat(name)
    output_json(stat, redact=not no_redact)


async def cmd_show_log(
    client: KeeneticApiClient,
    lines: int,
    since_minutes: int | None,
    since: str | None,
    errors_only: bool,
    grep: str | None,
    as_json: bool,
    no_redact: bool,
) -> None:
    if lines < 1:
        raise CliError("--lines must be a positive integer.")
    if since_minutes is not None and since_minutes < 1:
        raise CliError("--since-minutes must be a positive integer.")
    if since_minutes is not None and since:
        raise CliError("Use either --since-minutes or --since, not both.")

    since_dt: datetime | None = None
    if since_minutes is not None:
        # Naive by design, see parse_since.
        since_dt = datetime.now() - timedelta(minutes=since_minutes)  # noqa: DTZ005
    elif since:
        since_dt = parse_since(since)

    entries = await client.show_log(lines)
    entries = filter_log_entries(
        entries,
        since=since_dt,
        errors_only=errors_only,
        grep=grep,
    )

    if as_json:
        output_json(entries, redact=not no_redact)
        return
    print_log_entries(redact_sensitive(entries) if not no_redact else entries)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="keenetic-cli",
        description="Proof-of-concept CLI for Keenetic API integration commands.",
    )
    parser.add_argument(
        "--env-file",
        # The default is a None sentinel, not DEFAULT_ENV_FILE: `--env-file .env` has
        # to be distinguishable from omitting the option (see resolve_env_file_arg).
        default=None,
        help=(
            "Path to .env with Keenetic credentials (relative paths are resolved from "
            "script directory). An explicitly named file takes precedence over "
            "KEENETIC_* variables already in the environment; the default .env does not."
        ),
    )

    root_subparsers = parser.add_subparsers(dest="command_group", required=True)

    list_parser = root_subparsers.add_parser("list", help="List entities.")
    list_subparsers = list_parser.add_subparsers(dest="list_command", required=True)
    list_clients_parser = list_subparsers.add_parser("clients", help="List router clients.")
    list_clients_parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include inactive clients in output.",
    )
    list_clients_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON records instead of a table.",
    )
    list_clients_parser.set_defaults(
        handler=lambda client, args: cmd_list_clients(
            client, args.include_inactive, args.json
        )
    )
    list_policies_parser = list_subparsers.add_parser(
        "policies", help="List available router policies."
    )
    list_policies_parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON records instead of a table.",
    )
    list_policies_parser.set_defaults(
        handler=lambda client, args: cmd_list_policies(client, args.json)
    )

    set_parser = root_subparsers.add_parser("set", help="Set router options.")
    set_subparsers = set_parser.add_subparsers(dest="set_command", required=True)
    set_policy_parser = set_subparsers.add_parser("policy", help="Set policy for a client.")
    target_group = set_policy_parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--mac", help="Client MAC address.")
    target_group.add_argument("--name", help="Exact client name or hostname.")
    set_policy_parser.add_argument(
        "--policy",
        required=True,
        help=(
            "Policy name: default (alias: permit), not_internet (alias: deny), "
            "policy id, or exact description."
        ),
    )
    set_policy_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the requested and observed policy as JSON.",
    )
    set_policy_parser.set_defaults(
        handler=lambda client, args: cmd_set_policy(
            client, args.mac, args.name, args.policy, args.json
        )
    )

    api_parser = root_subparsers.add_parser("api", help="Run raw Keenetic API requests.")
    api_subparsers = api_parser.add_subparsers(dest="api_command", required=True)
    api_request_parser = api_subparsers.add_parser(
        "request",
        help="Call a Keenetic API endpoint. Any body-less GET is allowed by default.",
    )
    api_request_parser.add_argument(
        "--method",
        default="GET",
        help="HTTP method to use (default: GET).",
    )
    api_request_parser.add_argument(
        "--endpoint",
        required=True,
        help="API endpoint, for example /rci/show/interface.",
    )
    api_request_parser.add_argument(
        "--data-json",
        help="Inline JSON request body.",
    )
    api_request_parser.add_argument(
        "--unsafe",
        action="store_true",
        help=(
            "Allow requests the read-only guard blocks: any non-GET method, a GET whose "
            "path or query names an action ("
            + ", ".join(sorted(ACTION_PATH_SEGMENTS))
            + "), and a GET carrying --data-json."
        ),
    )
    api_request_parser.add_argument(
        "--raw",
        action="store_true",
        help="Print compact JSON instead of pretty JSON.",
    )
    api_request_parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Print sensitive fields without redaction.",
    )
    api_request_parser.set_defaults(
        handler=lambda client, args: cmd_api_request(
            client,
            args.method,
            args.endpoint,
            args.data_json,
            args.unsafe,
            args.raw,
            args.no_redact,
        )
    )

    show_parser = root_subparsers.add_parser("show", help="Show router state.")
    show_subparsers = show_parser.add_subparsers(dest="show_command", required=True)
    show_interfaces_parser = show_subparsers.add_parser(
        "interfaces",
        help="Show router interfaces from /rci/show/interface.",
    )
    show_interfaces_parser.add_argument("--name", help="Show one interface by exact name.")
    show_interfaces_parser.add_argument(
        "--type",
        dest="interface_type",
        help="Filter by interface type, case-insensitive (for example: wireguard).",
    )
    show_interfaces_parser.add_argument(
        "--connected",
        action="store_true",
        help="Show only connected interfaces.",
    )
    show_interfaces_parser.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON instead of a table.",
    )
    show_interfaces_parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Print sensitive fields without redaction.",
    )
    show_interfaces_parser.set_defaults(
        handler=lambda client, args: cmd_show_interfaces(
            client,
            args.name,
            args.interface_type,
            args.connected,
            args.json,
            args.no_redact,
        )
    )

    show_stat_parser = show_subparsers.add_parser(
        "interface-stat",
        help="Show interface statistics from /rci/show/interface/stat.",
    )
    show_stat_parser.add_argument("--name", required=True, help="Interface name.")
    show_stat_parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Print sensitive fields without redaction.",
    )
    show_stat_parser.set_defaults(
        handler=lambda client, args: cmd_show_interface_stat(
            client, args.name, args.no_redact
        )
    )

    show_dhcp_parser = show_subparsers.add_parser(
        "dhcp",
        help="Show the DHCP pool, occupied addresses, and which addresses are free.",
    )
    show_dhcp_parser.add_argument(
        "--pool",
        help=(
            "DHCP pool name. Defaults to the pool whose network contains the configured "
            "router address, which is the LAN this CLI is talking to."
        ),
    )
    show_dhcp_parser.add_argument(
        "--occupied",
        action="store_true",
        help="Also print a table of the occupied addresses and what holds each one.",
    )
    show_dhcp_parser.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON instead of a summary.",
    )
    show_dhcp_parser.set_defaults(
        handler=lambda client, args: cmd_show_dhcp(
            client, args.pool, args.occupied, args.json
        )
    )

    show_log_parser = show_subparsers.add_parser(
        "log",
        help="Show router system log with optional time, error, and text filters.",
    )
    show_log_parser.add_argument(
        "--lines",
        type=int,
        default=200,
        help="Number of recent log entries to request from the router (default: 200).",
    )
    show_log_parser.add_argument(
        "--since-minutes",
        type=int,
        help="Show entries from the last N minutes.",
    )
    show_log_parser.add_argument(
        "--since",
        help="Show entries since local time 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD HH:MM'.",
    )
    show_log_parser.add_argument(
        "--errors",
        action="store_true",
        help="Show errors and problem-like network messages only.",
    )
    show_log_parser.add_argument(
        "--grep",
        help="Case-insensitive text filter across timestamp, ident, level, and message.",
    )
    show_log_parser.add_argument(
        "--json",
        action="store_true",
        help="Print normalized JSON log entries instead of text lines.",
    )
    show_log_parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Print sensitive fields without redaction.",
    )
    show_log_parser.set_defaults(
        handler=lambda client, args: cmd_show_log(
            client,
            args.lines,
            args.since_minutes,
            args.since,
            args.errors,
            args.grep,
            args.json,
            args.no_redact,
        )
    )

    return parser


async def run_cli(args: argparse.Namespace) -> None:
    env_file_arg, explicit_env_file = resolve_env_file_arg(args.env_file)
    env_path = require_env_path(
        env_file_arg,
        resolve_env_path(env_file_arg),
        explicit=explicit_env_file,
    )
    cfg = load_router_config(env_path, file_wins=explicit_env_file)
    timeout = aiohttp.ClientTimeout(total=cfg.timeout)
    cookie_jar = aiohttp.CookieJar(unsafe=True)

    async with aiohttp.ClientSession(timeout=timeout, cookie_jar=cookie_jar) as session:
        client = KeeneticApiClient(session, cfg)
        await args.handler(client, args)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        asyncio.run(run_cli(args))
    except CliError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 2
    except aiohttp.ClientError as err:
        # ClientConnectorError is also an OSError, so this must precede the arms below.
        print(f"HTTP error: {err}", file=sys.stderr)
        return 3
    except TimeoutError:
        # aiohttp raises a bare TimeoutError on ClientTimeout expiry; it is not a
        # ClientError, and an unreachable router is the most likely real failure.
        print(
            "HTTP error: the router did not respond within the configured "
            "KEENETIC_TIMEOUT.",
            file=sys.stderr,
        )
        return 3
    except OSError as err:
        print(f"HTTP error: {err}", file=sys.stderr)
        return 3
    except KeyboardInterrupt:
        return 130
    except Exception as err:  # noqa: BLE001 - see below
        # The consumer is an agent parsing stdout/stderr. A traceback from an
        # unforeseen response shape is far harder for it to act on than one line, so
        # nothing is allowed to escape as a traceback.
        print(f"Error: unexpected failure: {type(err).__name__}: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
