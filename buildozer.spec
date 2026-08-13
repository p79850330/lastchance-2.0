[app]

title = Last Chance
package.name = lastchance
package.domain = org.lastchance

version = 2.1
requirements = python3,kivy,cryptography,openssl

source.dir = .

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK,REQUEST_INSTALL_PACKAGES

android.minapi = 21
android.api = 33

orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1
