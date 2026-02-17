#!/usr/bin/env python3
"""
Google Workspace OAuth2 token helper.
Uses OAuth 2.0 Client ID with a stored refresh token to get access tokens.

Setup (one-time):
  1. Create OAuth 2.0 Client ID (Desktop app) in Google Cloud Console
  2. Download the client secret JSON
  3. Run: python3 gw-auth.py --setup --client-secret /path/to/client_secret.json
  4. Open the printed URL in a browser, consent, copy the code= from the redirect URL
  5. Run: python3 gw-auth.py --exchange --client-secret /path/to/client_secret.json --code CODE

Usage (after setup):
  python3 gw-auth.py --scopes gmail,calendar,drive
  python3 gw-auth.py --scopes gmail --json

No external dependencies — uses only Python stdlib.
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

SCOPE_MAP = {
    "gmail": [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.labels",
    ],
    "gmail.readonly": [
        "https://www.googleapis.com/auth/gmail.readonly",
    ],
    "calendar": [
        "https://www.googleapis.com/auth/calendar",
    ],
    "calendar.readonly": [
        "https://www.googleapis.com/auth/calendar.readonly",
    ],
    "drive": [
        "https://www.googleapis.com/auth/drive",
    ],
    "drive.readonly": [
        "https://www.googleapis.com/auth/drive.readonly",
    ],
    "sheets": [
        "https://www.googleapis.com/auth/spreadsheets",
    ],
    "docs": [
        "https://www.googleapis.com/auth/documents",
    ],
    "slides": [
        "https://www.googleapis.com/auth/presentations",
    ],
}

# All scopes for initial consent (request broad access once)
ALL_SCOPES = sorted({s for v in SCOPE_MAP.values() for s in v})

TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
REDIRECT_URI = "http://localhost:8085"

CREDENTIALS_DIR = "/data/openclaw-data/secrets"
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, "google-oauth-credentials.json")


def load_credentials():
    """Load OAuth credentials from env vars or file.

    Env vars (preferred):
      GOOGLE_CLIENT_ID
      GOOGLE_CLIENT_SECRET
      GOOGLE_REFRESH_TOKEN
    Fallback: credentials JSON file.
    """
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")

    if client_id and client_secret and refresh_token:
        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }

    if os.path.isfile(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE) as f:
            return json.load(f)

    return None


def save_credentials(data):
    """Save OAuth credentials to file."""
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    os.chmod(CREDENTIALS_FILE, 0o600)


def load_client_secret(path):
    """Load client_id and client_secret from Google's JSON format."""
    with open(path) as f:
        cs = json.load(f)
    for key in ("installed", "web"):
        if key in cs:
            return cs[key]["client_id"], cs[key]["client_secret"]
    print("ERROR: Unrecognized client secret format", file=sys.stderr)
    sys.exit(1)


def exchange_code(client_id, client_secret, code):
    """Exchange authorization code for tokens."""
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(TOKEN_ENDPOINT, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def refresh_access_token(client_id, client_secret, refresh_token):
    """Use refresh token to get a new access token."""
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(TOKEN_ENDPOINT, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def cmd_setup(client_secret_path):
    """Print the authorization URL for the user to open."""
    client_id, _ = load_client_secret(client_secret_path)

    auth_params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(ALL_SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "login_hint": "hello@thehappylab.com",
    }
    auth_url = f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(auth_params)}"

    print(f"\nOpen this URL in your browser:\n\n{auth_url}\n")
    print("After consent, copy the code= value from the redirect URL, then run:")
    print(f"  python3 gw-auth.py --exchange --client-secret {client_secret_path} --code YOUR_CODE\n")


def cmd_exchange(client_secret_path, code):
    """Exchange the authorization code for tokens and save credentials."""
    client_id, client_secret = load_client_secret(client_secret_path)

    tokens = exchange_code(client_id, client_secret, code)

    if "refresh_token" not in tokens:
        print("ERROR: No refresh token returned. Revoke app access and try again.", file=sys.stderr)
        sys.exit(1)

    creds = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": tokens["refresh_token"],
    }
    save_credentials(creds)

    print(f"✅ Credentials saved to {CREDENTIALS_FILE}")
    print(f"\n   To use env vars instead:")
    print(f"     GOOGLE_CLIENT_ID={client_id}")
    print(f"     GOOGLE_CLIENT_SECRET={client_secret}")
    print(f"     GOOGLE_REFRESH_TOKEN={tokens['refresh_token']}")


def get_token(scope_names: list[str]) -> str:
    """Get a fresh access token for the requested scopes."""
    creds = load_credentials()
    if not creds:
        print(
            "ERROR: No credentials found. Run setup first:\n"
            "  python3 gw-auth.py --setup --client-secret /path/to/client_secret.json",
            file=sys.stderr,
        )
        sys.exit(1)

    result = refresh_access_token(
        creds["client_id"],
        creds["client_secret"],
        creds["refresh_token"],
    )
    return result["access_token"]


def main():
    parser = argparse.ArgumentParser(description="Google Workspace OAuth2 token helper")
    parser.add_argument("--setup", action="store_true", help="Print auth URL for consent flow")
    parser.add_argument("--exchange", action="store_true", help="Exchange auth code for tokens")
    parser.add_argument("--client-secret", help="Path to client_secret.json")
    parser.add_argument("--code", help="Authorization code (for --exchange)")
    parser.add_argument("--scopes", "-s", help="Comma-separated: gmail, calendar, drive, sheets, docs, slides")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.setup:
        if not args.client_secret:
            print("ERROR: --client-secret required", file=sys.stderr)
            sys.exit(1)
        cmd_setup(args.client_secret)
        return

    if args.exchange:
        if not args.client_secret or not args.code:
            print("ERROR: --client-secret and --code required", file=sys.stderr)
            sys.exit(1)
        cmd_exchange(args.client_secret, args.code)
        return

    if not args.scopes:
        parser.print_help()
        sys.exit(1)

    token = get_token([s.strip() for s in args.scopes.split(",")])

    if args.json:
        print(json.dumps({"access_token": token}))
    else:
        print(token, end="")


if __name__ == "__main__":
    main()
