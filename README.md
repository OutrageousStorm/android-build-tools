# 🔨 Android Build Tools

Python utilities for automating Android app build tasks — APK signing, alignment, configuration.

## Tools

| Script | What it does |
|--------|-------------|
| `sign_apk.py` | Sign APKs with keystore, auto-generate debug key |
| `align_apks.py` | Zipalign multiple APKs in batch |
| `build_config.py` | Generate BuildConfig.java from JSON |
| `manifest_editor.py` | Edit AndroidManifest.xml programmatically |

## Requirements
```bash
pip install lxml
# Also needs: apksigner, zipalign (Android SDK build-tools)
```
