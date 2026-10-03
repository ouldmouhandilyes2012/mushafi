# Mushafi - مصحفي

Offline-first Arabic Quran memorization and revision application built with Python and Kivy.

## Features

### ✅ Implemented

- **Heart Screen (قلب القرآن)**: Visual 114-surah grid with status tracking
  - 🟢 Memorized (محفوظ)
  - 🟡 Needs Review (يحتاج مراجعة)
  - 🔴 Not Memorized (غير محفوظ)
  - Status persists in SQLite

- **Quran Screen (القرآن)**:
  - Local JSON-based Quran text import
  - Navigate between surahs (1-114)
  - Switch between riwayat (hafs, warsh, qalun)
  - Adjust font size locally

- **Review Engine (المراجعة)**:
  - Automatic interval scheduling
  - Review dashboard with due/upcoming/overdue tracking
  - Mark reviews as complete
  - Success/failure-based interval adjustment

- **Tafsir System (التفسير)**:
  - Local JSON-based tafsir import
  - Search by surah and ayah
  - Display tafsir with source attribution

- **Profile Management (الملف الشخصي)**:
  - Editable user display name
  - Memorization goal (number of surahs)
  - Review goal (number of sessions)
  - Data persists in SQLite

- **Settings (الإعدادات)**:
  - Select preferred riwayah
  - Adjust font size (18-26)
  - Toggle night mode
  - Control local notifications
  - All settings save to SQLite

- **Statistics (الإحصائيات)**:
  - Track memorized/unmemorized/review-needed surahs
  - Progress percentage
  - User goals display
  - Real-time data from SQLite

- **Database**:
  - Full SQLite schema with 14 tables
  - Proper foreign keys and constraints
  - Default settings initialization
  - Profile and statistics aggregation

### 📦 Data Import

The app supports offline local data in JSON format:

**Quran Format** (`assets/quran/hafs/hafs.json`):
```json
[
  {
    "surah_number": 1,
    "surah_name": "الفاتحة",
    "ayah_number": 1,
    "text": "بسم الله الرحمن الرحيم"
  }
]
```

**Tafsir Format** (`assets/tafsir/tafsir.json`):
```json
[
  {
    "surah_number": 1,
    "ayah_number": 1,
    "tafsir": "تفسير الآية",
    "source": "اسم التفسير"
  }
]
```

**Sample files** are included in `assets/sample_data/`.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Android Build

Requires Android SDK, NDK, and Buildozer:

```bash
buildozer android debug
```

## Important Notes

1. **No Fake Data**: This project does not include invented Quran text or tafsir. It uses a verified local import schema instead.
2. **Fully Offline**: Once data is imported, the app works completely offline.
3. **SQLite Persistence**: All user data (progress, settings, profile) is stored locally in SQLite.
4. **Extensible**: The architecture supports easy addition of new tafsir sources, riwayat, and readers.

## Project Structure

```
mushafi/
├── main.py
├── requirements.txt
├── buildozer.spec
├── database/
│   ├── database.py
│   └── migrations.py
├── models/
│   ├── surah.py
│   ├── verse.py
│   ├── riwayah.py
│   ├── reader.py
│   ├── review.py
│   └── profile.py
├── screens/
│   ├── base.py
│   ├── home.py
│   ├── quran.py
│   ├── heart.py
│   ├── review.py
│   ├── tafsir.py
│   ├── recitation.py
│   ├── statistics.py
│   ├── profile.py
│   └── settings.py
├── services/
│   ├── quran_service.py
│   ├── audio_service.py
│   ├── recitation_engine.py
│   ├── review_engine.py
│   ├── tafsir_service.py
│   └── offline_manager.py
├── widgets/
│   ├── heart_grid.py
│   ├── verse_widget.py
│   └── audio_player.py
└── assets/
    ├── quran/
    │   ├── hafs/
    │   ├── warsh/
    │   └── qalun/
    ├── tafsir/
    ├── audio/
    ├── fonts/
    └── sample_data/
```

## Limitations

- **APK Status**: No actual Android APK has been built in this environment. Real APK requires Android SDK/NDK toolchain.
- **Audio**: Placeholder implementation; actual audio playback requires local .mp3 files in `assets/audio/`.
- **Recitation Recording**: UI present but backend recording features require platform-specific implementations.

## License

MIT
