[app]

# (str) Title of your application
title = Better Lyrics

# (str) Package name
package.name = betterlyrics

# (str) Package domain (needed for android/ios packaging)
package.domain = com.betterlyrics

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,md,txt

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,flet==0.28.3,pyperclip,certifi,charset-normalizer,idna,urllib3,websockets,watchdog,pathspec,packaging

# (str) Presplash of the application
presplash.filename = betterlyrics3.png

# (str) Icon of the application
icon.filename = betterlyrics3.png

# (str) Supported orientation (portrait or landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (int) Android SDK version to use
android.sdk = 33

# (str) python-for-android fork to use, defaults to upstream (kivy)
# p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android git clone recursive
# p4a.clone_recursive = 1

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes = ./p4a-recipes

# (str) Filename to the hook for p4a
# p4a.hook =

# (str) Bootstrap to use for android builds
p4a.bootstrap = webview

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
# p4a.port =

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK

# (int) Target Android API, should be as high as possible.
# android.api = 27

# (int) Minimum API your APK / AAB will support.
# android.minapi = 21

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
# android.whitelist =

# (str) Path to a custom whitelist file
# android.whitelist_src =

# (str) Path to a custom blacklist file
# android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_src =

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
# android.gradle_dependencies =

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# android.gradle_repositories =

# (list) packaging options to add 
# android.add_packaging_options =

# (list) Java classes to add as activities to the manifest.
# android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
# android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
# android.manifest.intent_filters =

# (str) launchMode to set for the main activity
# android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7/*.so
# android.add_libs_arm64_v8a = libs/android-v8/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_mips = libs/android-mips/*.so

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
