# Mushafi - مصحفي

## Summary

**Mushafi** is a complete offline-first Arabic Quran memorization and revision application built with Python and Kivy. All features work locally without internet connection.

## Current Features (v1.0)

### 🔖 Core Functionality

1. **Quran Reading Screen** (القرآان)
   - Navigate between all 114 surahs
   - Switch between riwayat: Hafs, Warsh, Qalun
   - Adjustable font size (18-26px)
   - Local JSON-based text import
   - No internet required

2. **Heart Screen - Memorization Tracker** (قلب القرآان)
   - Visual 6x19 grid of all 114 surahs
   - Three status levels:
     - 🟢 **Memorized** (Green)
     - 🟡 **Needs Review** (Yellow)
     - 🔴 **Not Memorized** (Red)
   - Tap to toggle status
   - Persistent SQLite storage
   - Status persists across app restarts

3. **Review System** (المراجعة)
   - Intelligent spaced-repetition scheduling
   - Dashboard with due/upcoming/overdue counts
   - Automatic interval adjustment based on success/failure
   - Mark reviews as complete
   - Track mistake count and success count

4. **Tafsir System** (التفسير)
   - Search tafsir by surah and ayah
   - Local JSON-based tafsir import
   - Display with source attribution
   - Multiple tafsir sources supported

5. **Profile Management** (الملف الشخصي)
   - Editable user name
   - Memorization goal (target number of surahs)
   - Review goal (target sessions per week)
   - All data persists in SQLite

6. **Settings** (الإعدادات)
   - Select preferred riwayah
   - Adjust font size globally
   - Toggle night mode
   - Enable/disable local notifications
   - All settings saved locally

7. **Statistics Dashboard** (الإحصائيات)
   - Surahs memorized / total
   - Surahs needing review
   - Progress percentage
   - User's memorization and review goals
   - Real-time data from SQLite

8. **Bookmarks & Notes** (العلامات والملاحظات)
   - Bookmark specific ayahs
   - Add/edit/delete notes on surahs and ayahs
   - View all bookmarks and notes
   - Organized tabbed interface

9. **Recitation Recording** (التسميع)
   - Record personal recitations locally
   - Save recordings with metadata
   - View saved recordings
   - Delete recordings
   - No uploads to any server

### 📦 Data & Persistence

- **SQLite Database** with 14 tables
- **Local JSON Imports** for Quran, Tafsir, Riwayat, Readers
- **User Data Storage**: Progress, settings, profile, notes, bookmarks, recordings
- **Sample Data** included in `assets/sample_data/`

### 🔽 UI/UX

- **Arabic RTL Layout** throughout
- **Warm Color Palette**: Ivory backgrounds, gold accents
- **Simple Card-based Design**
- **Status Color-coding**: Green/Yellow/Red for memorization states
- **Responsive Layout** for different phone sizes
- **Clear Navigation** with back button on every screen

## Data Import Format

### Quran Format

Place in `assets/quran/hafs/hafs.json`, `assets/quran/warsh/warsh.json`, etc.:

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

### Tafsir Format

Place in `assets/tafsir/tafsir.json`:

```json
[
  {
    "surah_number": 1,
    "ayah_number": 1,
    "tafsir": "تفسير الآية هنا",
    "source": "اسم التفسير إربايته"
  }
]
```

## Installation & Running

```bash
# Clone the repository
git clone https://github.com/ouldmouhandilyes2012/mushafi.git
cd mushafi

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Building for Android

Requires: Android SDK, NDK, and Buildozer

```bash
buildozer android debug
# APK will be in bin/
```

## Project Structure

```
mushafi/
├── main.py                 # App entry point
├── requirements.txt         # Python dependencies
├── buildozer.spec           # Android build config
├── database/
│   ├── database.py          # SQLite wrapper
│   └── migrations.py        # Schema & initialization
├── models/                 # Data classes
├── screens/                # UI screens (9 screens)
├── services/               # Business logic
├── widgets/                # Reusable components
└── assets/
    ├── quran/               # Quran JSON imports (hafs, warsh, qalun)
    ├── tafsir/              # Tafsir JSON imports
    ├── audio/               # Local audio files
    ├── fonts/               # Custom fonts
    └── sample_data/         # Example JSON files
```

## Design Philosophy

1. **No Internet Required**: All features work completely offline
2. **No Fake Data**: The app uses verified local data imports only
3. **User Privacy**: All data is stored locally; no tracking or uploads
4. **Simple & Fast**: Lightweight, efficient database queries
5. **Extensible**: Easy to add new riwayat, tafsir sources, readers
6. **Quranic Focus**: Designed specifically for Quran memorization and revision

## Notes

- **APK Status**: This is source code. Building to Android requires a machine with Android SDK, NDK, and Buildozer installed.
- **Sample Data**: Includes example Quran and Tafsir JSON in `assets/sample_data/` for reference.
- **Database Location**: `database/mushafi.db` (created automatically on first run)
- **Settings & Profile**: Stored in SQLite, not in config files

## Future Enhancements

- Audio playback for recorded recitations
- Export user progress as backup
- Multiple user profiles
- Hadith integration
- Night mode refinement
- Gesture-based navigation

## License

MIT

## Support

For issues or feature requests, use GitHub Issues.
