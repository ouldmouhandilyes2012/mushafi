# Mushafi

Mushafi is an offline-first Arabic Quran memorization and revision application built with Python and Kivy.

## Current status

The project is structured in a modular way and includes:

- SQLite database layer
- Offline-first data import schema for Quran, tafsir, and local audio
- Home screen and core screen structure
- Arabic RTL UI layout
- Heart screen for memorization status
- Profile and settings screens
- Review and statistics placeholders backed by local database

## Important note

This repository intentionally does not include fake Quran text or invented tafsir data. The app is designed to work with verified local import files stored under:

- `assets/quran/hafs/`
- `assets/quran/warsh/`
- `assets/quran/qalun/`
- `assets/tafsir/`
- `assets/audio/`

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Android build

```bash
buildozer android debug
```

Note: actual APK generation requires a valid Android SDK, NDK, and Buildozer environment on the machine used for the build.
