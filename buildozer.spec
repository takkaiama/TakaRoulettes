[app]

title = TakaRouletteS
package.name = evolutionroulettes
package.domain = org.taka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0

#
# ANDROID CONFIGURAÇÃO CORRETA
#

android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.skip_update = False

android.allow_backup = True
android.debug_artifact = apk

#
# BUILD CONFIG
#

[buildozer]
log_level = 2
warn_on_root = 1
