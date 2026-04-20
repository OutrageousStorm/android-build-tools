#!/usr/bin/env python3
"""
sign_apk.py -- Sign Android APKs with automatic keystore generation
Usage: python3 sign_apk.py --apk app.apk [--keystore keystore.jks] [--password pass] [--output signed.apk]
"""
import subprocess, sys, os, argparse, shutil
from pathlib import Path
from datetime import datetime, timedelta

def run(cmd, check=True):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"Error: {r.stderr}")
        sys.exit(1)
    return r.stdout + r.stderr

def create_keystore(ks_path, password="android", validity=10000):
    """Generate a debug keystore (one-time)"""
    if Path(ks_path).exists():
        return
    print(f"  Generating {ks_path}...")
    run(
        f'keytool -genkeypair -v -keystore "{ks_path}" '
        f'-storepass {password} -alias androiddebugkey '
        f'-keypass {password} -keyalg RSA -keysize 2048 '
        f'-validity {validity} '
        f'-dname "CN=Android Debug,O=Android,C=US"'
    )

def zipalign(apk_path, aligned_path):
    """4-byte align APK"""
    if not shutil.which("zipalign"):
        print("Warning: zipalign not found in PATH")
        return apk_path
    run(f'zipalign -f 4 "{apk_path}" "{aligned_path}"')
    return aligned_path

def sign_with_apksigner(apk_path, ks_path, password, out_path):
    """Sign using apksigner (recommended)"""
    if not shutil.which("apksigner"):
        return False
    run(
        f'apksigner sign --ks "{ks_path}" '
        f'--ks-pass pass:{password} '
        f'--key-pass pass:{password} '
        f'--out "{out_path}" "{apk_path}"'
    )
    return True

def sign_with_jarsigner(apk_path, ks_path, password, out_path):
    """Fallback: use jarsigner"""
    run(
        f'jarsigner -keystore "{ks_path}" '
        f'-storepass {password} -keypass {password} '
        f'-signedjar "{out_path}" "{apk_path}" androiddebugkey'
    )
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apk", required=True)
    parser.add_argument("--keystore", default=str(Path.home() / ".android" / "debug.keystore"))
    parser.add_argument("--password", default="android")
    parser.add_argument("--output")
    parser.add_argument("--validity", type=int, default=10000)
    args = parser.parse_args()

    apk = Path(args.apk)
    if not apk.exists():
        print(f"APK not found: {apk}")
        sys.exit(1)

    ks = args.keystore
    pwd = args.password
    out = args.output or f"{apk.stem}_signed.apk"

    print(f"\n🔨 APK Signer")
    print(f"  APK: {apk.name}")
    print(f"  Keystore: {ks}")

    # Create keystore if needed
    if not Path(ks).exists():
        Path(ks).parent.mkdir(parents=True, exist_ok=True)
        create_keystore(ks, pwd, args.validity)

    # Zipalign
    aligned = f"/tmp/{apk.stem}_aligned.apk"
    zipalign(str(apk), aligned)

    # Sign
    print(f"  Signing...")
    ok = sign_with_apksigner(aligned, ks, pwd, out) or sign_with_jarsigner(aligned, ks, pwd, out)

    if ok:
        size = Path(out).stat().st_size / (1024 * 1024)
        print(f"\n✅ Signed: {out} ({size:.1f} MB)")
    else:
        print("❌ Signing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
