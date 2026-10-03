[app]

# Application metadata
Title = Mushafi
Package.name = mushafi
Package.domain = org.mushafi

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db,sqlite3,ttf

version = 1.0.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

# Android config
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 30
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,RECORD_AUDIO,VIBRATE
android.private_storage = True
android.archs = arm64-v8a

p4a.branch = master
