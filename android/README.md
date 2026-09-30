# Hearthlight for Android

The whole game, wrapped in a `WebView`, as a single 3 MB APK. Party Mode works:
the phone joins the same relay rooms the browser build does, and the lobby's QR
code points at the hosted `pad.html`, so a phone with the APK can play with
friends on any network — no Wi-Fi pairing, no devserver.

## Build it

```powershell
powershell -ExecutionPolicy Bypass -File android/build.ps1
```

Needs the Android SDK's own tools and a JDK — **no Gradle, no Android Studio
project, no npm, no network**:

| what | where |
| --- | --- |
| `build-tools;35.0.0` (`aapt2`, `d8`, `zipalign`, `apksigner`) | `D:\sdk\build-tools\35.0.0` (override with `-Sdk`) |
| `platforms;android-35` (`android.jar`) | `D:\sdk\platforms\android-35` |
| JDK 11+ (`javac`, `keytool`) | any; pass `-JavaHome` |

`JAVA_HOME` on this machine points at a broken JDK, so the script checks each
candidate for a real `bin/java.exe` and only then uses it:

```powershell
# this is the JDK that works here (openjdk 25, ships with Rider)
powershell -ExecutionPolicy Bypass -File android/build.ps1 `
  -JavaHome "D:\Program Files\JetBrains Rider 2026.1.0.1\jbr"
```

Output: `android/Hearthlight.apk`. The first build also makes
`android/hearthlight.keystore` (alias/key/store password all `hearthlight`) and
reuses it afterwards, so successive builds upgrade in place.

## What the eight steps do

1. **assets** — `robocopy` the game straight out of the repository root (the very
   files the website serves) into `build/assets`, then rewrite `config.js` so the
   relay points at the public server. `tools/android-icon.py` draws the launcher
   icon first; dot-files and dot-directories never make it into the APK.
2. **aapt2 compile** — `res/` → `build/res.zip`.
3. **aapt2 link** — resources + assets + `AndroidManifest.xml` → `app-unsigned.apk`,
   and generates the `R` class into `build/gen`.
4. **javac** — `java/**/*.java` plus that generated `R.java`, against `android.jar`
   as bootclasspath, target/source 8.
5. **d8** — the `.class` files → `classes.dex`, desugared to `--min-api 24`.
6. **package** — `tools/apkzip.py` folds `classes.dex` into the APK while keeping
   every entry's own compression type (assets stay stored, as the WebView wants).
7. **zipalign** — 4-byte aligned, page-aligned uncompressed `.so`/assets.
8. **sign** — `apksigner` with the keystore, then `verify --print-certs`.

## Why the WebView loads from `https://vps-ec093ef6.vps.ovh.ca`

`MainActivity` doesn't use `file:///android_asset/`: ES modules are
cross-origin under `file://` and modern WebViews refuse them outright. It serves
the bundled game from a **real https origin instead**, and that origin is not a
free choice —

`server/relay.mjs` checks the WebSocket handshake's `Origin` header. Only
`https://vps-ec093ef6.vps.ovh.ca` and `https://hearthlight.github.io` are let
through (anything else gets `403 Forbidden`):

```
Origin: https://vps-ec093ef6.vps.ovh.ca    -> 101 Switching Protocols
Origin: https://hearthlight.github.io      -> 101
Origin: https://hearthlight.local          -> 403
Origin: http://localhost:8765              -> 403
Origin: null                               -> 403
```

So `HOST = "vps-ec093ef6.vps.ovh.ca"` in `MainActivity.java`, which both puts the
game in a secure context (localStorage, WebAudio, WebRTC all behave as on the
web) and produces an `Origin` the relay trusts. `shouldInterceptRequest` serves
anything it finds in `assets/` from the APK and returns `null` for everything
else, so `/ws`, `/saves/*` and `/hello` still reach the real server.

Party Mode on the phone is therefore server-based: the lobby shows a QR code
pointing at `https://vps-ec093ef6.vps.ovh.ca/pad.html`, and controllers are
phones with a browser (or the APK) joined to the same room code.

## Options

| parameter | default | meaning |
| --- | --- | --- |
| `-Sdk` | `%ANDROID_HOME%`, else `D:\sdk` | SDK root |
| `-JavaHome` | `%JAVA_HOME%`, Android Studio's `jbr` | JDK to use |
| `-Relay` | `wss://vps-ec093ef6.vps.ovh.ca/ws` | relay baked into `config.js` |
| `-Pad` | `https://vps-ec093ef6.vps.ovh.ca/pad.html` | what the lobby QR code opens |
| `-Stats` | *(empty)* | set to `https://…/hello` to ping the stats counter on boot |
| `-Out` | `android/Hearthlight.apk` | where the signed APK goes |

The two party parameters are only a default: the app itself asks for the server in
**Settings · Party server**, and one address gives both the relay and the page the phones
open (`192.168.1.20:8765` → `ws://192.168.1.20:8765/ws` + `http://192.168.1.20:8765/pad.html`),
so a LAN party needs no rebuild. `-Relay`/`-Pad` just preconfigure `config.js` (the address
already filled in); the `ws://` a LAN relay uses is fine because the WebView allows mixed
content. On a machine that hosts the party itself the row is already filled with that
machine's own LAN address — the local server reports it at `/__lan` — but a phone has no LAN
server to ask, so there it reads `默认`/`Default` until an address is typed in.

## Checking a build without a device

There is no emulator or phone attached here, so the APK's payload is verified by
serving exactly what it ships:

```powershell
python tools/apkcheck.py android/Hearthlight.apk            # contents + baked config
python tools/apkcheck.py android/Hearthlight.apk --extract J:\tmp\apkassets
$env:HEARTHLIGHT_ROOT='J:\tmp\apkassets'; python tools/devserver.py 8777
```

Then point a browser at `http://localhost:8777/?debug=1&lang=zh`. `devserver.py`
is required — it is the only thing around that serves `.mjs` as
`text/javascript`, which the browser insists on for ES modules.

```powershell
# headless Chrome + tools/cdp.mjs drive it from the command line
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' --headless=new `
  --remote-debugging-port=9222 --user-data-dir="$env:TEMP\hl-chrome" `
  --window-size=1280,720 --enable-unsafe-swiftshader --hide-scrollbars `
  "http://localhost:8777/?debug=1&lang=zh"
node tools/cdp.mjs eval "game.settings.lang"
node tools/cdp.mjs shot J:\tmp\apk-title.png
```

Keep Chrome's `--user-data-dir` **outside the repository** — a profile folder in
the checkout gets copied into `assets/` by step 1.

## Files

| file | what it is |
| --- | --- |
| `AndroidManifest.xml` | one activity, `sensorLandscape`, minSdk 24 / targetSdk 35, `INTERNET` + `ACCESS_NETWORK_STATE` |
| `java/com/hearthlight/game/MainActivity.java` | the WebView shell: asset interception, immersive fullscreen, console → logcat, double-back-to-exit |
| `res/values/strings.xml`, `res/values/styles.xml` | app name and the fullscreen theme |
| `res/mipmap-*/ic_launcher*.png` | launcher icons, drawn by `tools/android-icon.py` |
| `build/` | scratch (git-ignored) |
| `Hearthlight.apk`, `hearthlight.keystore` | the deliverable and its signing key (git-ignored) |
