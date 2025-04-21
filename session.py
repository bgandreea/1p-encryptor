import os
import subprocess
from constants import ACCOUNT_SHORTHAND, SESSION_CACHE_FILE

SESSION_VAR = f"OP_SESSION_{ACCOUNT_SHORTHAND}"

def is_session_valid(token):
    print("🔎 Validating cached session token...")

    try:
        result = subprocess.run(
            ["op", "user", "get", "--me", "--session", token],
            capture_output=True, text=True, shell=True,
            timeout=5  # ⏱ Timeout after 5 seconds
        )
        print("📣 Validation result:", result.returncode)
        if result.stderr:
            print("❗ STDERR:", result.stderr.strip())
        if result.stdout:
            print("📄 STDOUT:", result.stdout.strip())
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Validation timed out! Token check unresponsive.")
        return False



def load_cached_session():
    if not os.path.exists(SESSION_CACHE_FILE):
        return None
    with open(SESSION_CACHE_FILE, "r") as f:
        token = f.read().strip()
    return token if token else None

def save_session(token):
    with open(SESSION_CACHE_FILE, "w") as f:
        f.write(token)
    os.environ[SESSION_VAR] = token

def refresh_session():
    print("🔁 Refreshing 1Password session token...")
    result = subprocess.run(
        ["op", "signin", "--raw"],
        capture_output=True, text=True, shell=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"❌ Failed to refresh session:\n{result.stderr}")

    token = result.stdout.strip()
    save_session(token)
    print("✅ Session refreshed and ready.")
    return token


def get_or_refresh_session():
    print(f"📂 Checking for cached session file: {SESSION_CACHE_FILE}")

    cached_token = load_cached_session()
    if cached_token:
        print(f"🐍 Cached token found: {cached_token[:8]}...")
        os.environ[SESSION_VAR] = cached_token
        print("✅ Using cached token without validation.")
        return cached_token

    print("🔁 No cached token found. Attempting to refresh...")
    return refresh_session()


