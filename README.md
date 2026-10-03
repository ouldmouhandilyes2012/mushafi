# Mushafi

Offline-first Arabic Quran memorization and revision app built in Python with Kivy.

## Project layout

- `main.py` – application entry point
- `database/` – SQLite connection and migrations
- `models/` – data models
- `screens/` – app screens
- `services/` – Quran, audio, review, and offline utilities
- `widgets/` – reusable widgets
- `assets/` – local Quran, tafsir, audio, and font import folders

## Notes

This repository intentionally does not bundle fake Quran text, invented tafsir, or fake audio. The app is structured to support local verified data imports from `assets/quran/*`, `assets/tafsir/*`, and `assets/audio/*`.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Build Android with Buildozer

```bash
buildozer android debug
```

If the build environment does not have Android SDK/NDK, the script is prepared but the actual APK build must be run on a machine that has the required Android toolchain.
