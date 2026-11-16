"""Minimal Keyfern license check for a Python desktop app (PyQt, PySide, Tkinter) or CLI tool.

First run: asks for the license key and activates this machine online (/v1/activate).
Next runs: checks online again; with no internet, falls back to the Ed25519-signed cache,
but only while the product's offline lease is valid (lease_days > 0 in the dashboard).
"""
import os
import sys
import time
from pathlib import Path

from keyfern import Keyfern, KeyfernError, KeyfernNetworkError

HERE = Path(__file__).resolve().parent
# A real app keeps these two files in the user's data folder (%APPDATA%\YourApp, ~/.config/yourapp...).
CACHE = HERE / "license.cache"   # last signed server answer, verified again on every offline start
KEY_FILE = HERE / "license.key"  # the key the user typed, so they are asked only once
REVOKED = ("blocked", "expired", "invalid_key", "machine_limit")


def load_env(path):
    """Read KEY=value lines from .env without an extra dependency. Real environment variables win."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip().strip("\"'"))


def when(ts):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))


def get_license(kf):
    """Return (license, mode). Exits when there is no valid license."""
    key = KEY_FILE.read_text(encoding="utf-8").strip() if KEY_FILE.exists() else ""
    while True:
        if not key:
            try:
                key = input("License key: ").strip()
            except EOFError:  # no console attached (e.g. started from a GUI launcher)
                key = ""
            if not key:
                sys.exit("No license key entered.")
        try:
            lic, mode = kf.activate(key), "Online"
        except KeyfernNetworkError:
            try:
                # signature, machine, expiry, lease and clock rollback are all checked here
                lic, mode = kf.cached(), "Offline Lease"
            except KeyfernError as e:
                sys.exit(f"Offline and no valid license cache ({e.code}): {e}\n"
                         "Connect to the internet and start again. Offline starts work only if the product "
                         "has a lease duration (e.g. 30 days) in its Keyfern dashboard settings.")
        except KeyfernError as e:
            print(f"License refused ({e.code}): {e}")
            if e.code in REVOKED:
                kf.clear_cache()
            KEY_FILE.unlink(missing_ok=True)
            key = ""
            continue
        KEY_FILE.write_text(lic.key, encoding="utf-8")
        return lic, mode


def main():
    load_env(HERE / ".env")
    product = os.environ.get("KEYFERN_PRODUCT_ID", "").strip()
    public_key = os.environ.get("KEYFERN_PUBLIC_KEY", "").strip()
    if not product or not public_key:
        sys.exit("Set KEYFERN_PRODUCT_ID and KEYFERN_PUBLIC_KEY in .env (copy .env.example).")

    kf = Keyfern(product=product, public_key=public_key, cache_path=str(CACHE))
    lic, mode = get_license(kf)

    if lic.lease_until is None:
        offline = "allowed, no time limit"
    elif lic.lease_until <= lic.issued_at:
        offline = "off (lease_days = 0: set a lease duration in the product settings)"
    else:
        offline = f"allowed until {when(lic.lease_until)}"

    print(f"Licensed ({mode})")
    print(f"  Key:      {lic.key}")
    print(f"  Expires:  {'never' if lic.expires is None else when(lic.expires)}")
    print(f"  Offline:  {offline}")
    print(f"  Features: {', '.join(map(str, lic.features)) or 'none'}")
    # Your app starts here. Gate paid parts with a feature number, e.g.: if lic.has(1): enable_pro()


if __name__ == "__main__":
    main()
