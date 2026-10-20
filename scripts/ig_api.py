#!/usr/bin/env python3
"""Instagram API helper for @tonepair.studio.

Usage:
  python3 scripts/ig_api.py check     # verify the token and account
  python3 scripts/ig_api.py limit     # check the content publishing quota (needs publish permission)
  python3 scripts/ig_api.py refresh   # refresh the long-lived token (token must be 24h+ old and unexpired)

Secrets are read from .env and never printed.
"""
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
GRAPH = "https://graph.instagram.com"
API_VERSION = "v24.0"


def load_env() -> dict:
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def save_env(updates: dict) -> None:
    env = load_env()
    env.update(updates)
    ENV_PATH.write_text("".join(f"{k}={v}\n" for k, v in env.items()))
    os.chmod(ENV_PATH, 0o600)


def call(path: str, params: dict) -> dict:
    url = f"{GRAPH}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as err:
        body = err.read().decode(errors="replace")
        token = params.get("access_token", "")
        if token:
            body = body.replace(token, "<TOKEN>")
        sys.exit(f"HTTP {err.code}: {body[:500]}")


def check(env: dict) -> None:
    me = call(f"{API_VERSION}/me", {
        "fields": "user_id,username,account_type,media_count",
        "access_token": env["IG_ACCESS_TOKEN"],
    })
    print(json.dumps(me, ensure_ascii=False, indent=2))


def limit(env: dict) -> None:
    res = call(f"{API_VERSION}/{env['IG_USER_ID']}/content_publishing_limit", {
        "fields": "config,quota_usage",
        "access_token": env["IG_ACCESS_TOKEN"],
    })
    print(json.dumps(res, ensure_ascii=False, indent=2))


def refresh(env: dict) -> None:
    res = call("refresh_access_token", {
        "grant_type": "ig_refresh_token",
        "access_token": env["IG_ACCESS_TOKEN"],
    })
    expires = dt.date.today() + dt.timedelta(seconds=int(res.get("expires_in", 0)))
    save_env({
        "IG_ACCESS_TOKEN": res["access_token"],
        "IG_TOKEN_ISSUED_AT": dt.date.today().isoformat(),
        "IG_TOKEN_EXPIRES_ON": expires.isoformat(),
    })
    print(f"refreshed; expires on {expires.isoformat()}")


if __name__ == "__main__":
    commands = {"check": check, "limit": limit, "refresh": refresh}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    commands[sys.argv[1]](load_env())

