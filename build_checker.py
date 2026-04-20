#!/usr/bin/env python3
"""
build_checker.py -- Check Android build info, compile time, SDK version, etc.
Usage: python3 build_checker.py
"""
import subprocess, re

def adb(cmd):
    r = subprocess.run(f"adb shell getprop {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

props = {
    "Build ID": "ro.build.id",
    "Build Time": "ro.build.date.utc",
    "Build Version": "ro.build.version.release",
    "SDK Version": "ro.build.version.sdk",
    "Compilation Date": "ro.build.date",
    "Git Commit": "ro.build.version.incremental",
    "Security Patch": "ro.build.version.security_patch",
    "Product": "ro.product.model",
    "Brand": "ro.product.brand",
    "Bootloader": "ro.bootloader",
    "Radio/Modem": "ro.baseband",
}

print("\n📦 Android Build Info\n")
for label, prop in props.items():
    val = adb(prop)
    print(f"  {label:<20} {val}")
print()
