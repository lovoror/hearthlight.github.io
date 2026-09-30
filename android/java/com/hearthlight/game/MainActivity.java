package com.hearthlight.game;

import android.app.Activity;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.IOException;
import java.io.InputStream;

/**
 * The whole app: a WebView showing the game that ships in assets/.
 *
 * The game is a set of ES modules, and a module script loaded over file:// is a
 * cross-origin request that every modern WebView refuses — so instead the page
 * is loaded from an https origin and every request for it is answered locally,
 * out of the APK. That keeps a real secure origin (localStorage, WebAudio,
 * WebRTC and the online relay all behave exactly as on the web) while the game
 * itself never touches the network.
 *
 * Which origin that is comes out of the packaged config.js: the host of the relay
 * the build points at (`android/build.ps1 -Relay`, or the public one by default).
 * It matters because the relay checks the Origin header of every socket and only
 * knows the sites it serves (server/relay.mjs, ORIGINS): the app has to speak from
 * an origin that relay accepts, and reading it from config.js means pointing a
 * build at another server moves the origin with it instead of stranding it on one
 * hard-coded host. A request we have no asset for is left alone and goes to the
 * network, which is how the relay, the phone page and the online saves stay
 * reachable.
 */
public class MainActivity extends Activity {

  private static final String TAG = "Hearthlight";
  // fallback only: config.js is expected to name a relay, and normally does
  private static final String FALLBACK_HOST = "vps-ec093ef6.vps.ovh.ca";

  private String host = FALLBACK_HOST;
  private String start;
  private WebView web;
  private long lastBack;

  @Override protected void onCreate(Bundle state) {
    super.onCreate(state);
    host = relayHost();
    start = "https://" + host + "/index.html";
    getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

    web = new WebView(this);
    web.setBackgroundColor(0xFF14121C);
    WebSettings s = web.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true);
    s.setMediaPlaybackRequiresUserGesture(false);
    s.setAllowFileAccess(false);
    s.setAllowContentAccess(false);
    s.setSupportZoom(false);
    s.setBuiltInZoomControls(false);
    s.setDisplayZoomControls(false);
    s.setUseWideViewPort(false);
    s.setLoadWithOverviewMode(false);
    s.setCacheMode(WebSettings.LOAD_DEFAULT);
    // (the page is served from a https origin; a party on the local network is ws:// — a
    // WebView blocks that as mixed content unless it is told not to)
    s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
    web.setVerticalScrollBarEnabled(false);
    web.setHorizontalScrollBarEnabled(false);
    web.setOverScrollMode(View.OVER_SCROLL_NEVER);
    web.setWebChromeClient(new Chrome());
    web.setWebViewClient(new Local());
    setContentView(web);
    hideBars();

    if (state == null) web.loadUrl(start);
    else web.restoreState(state);
  }

  /**
   * The host of the relay this build was packaged against, read out of assets/config.js
   * (the online relay first, then the plain one). Only a fallback is compiled in.
   */
  private String relayHost() {
    String cfg = "";
    try (InputStream in = getAssets().open("config.js")) {
      java.io.ByteArrayOutputStream all = new java.io.ByteArrayOutputStream();
      byte[] buf = new byte[4096];
      int n;
      while ((n = in.read(buf)) > 0) all.write(buf, 0, n);
      cfg = all.toString("UTF-8");
    } catch (IOException e) {
      Log.w(TAG, "no config.js in assets, using " + FALLBACK_HOST);
      return FALLBACK_HOST;
    }
    java.util.regex.Matcher m = java.util.regex.Pattern
        .compile("(?:onlineRelay|relay)\\s*:\\s*['\"](wss?|https?)://([^/'\"\\s]+)").matcher(cfg);
    while (m.find()) {
      String h = m.group(2);
      if (h != null && !h.isEmpty()) {
        Log.i(TAG, "origin " + h + " (from config.js " + m.group() + ")");
        return h;
      }
    }
    Log.w(TAG, "config.js names no relay, using " + FALLBACK_HOST);
    return FALLBACK_HOST;
  }

  /** Full screen, no status or navigation bar, and it stays that way. */
  private void hideBars() {
    View d = getWindow().getDecorView();
    if (Build.VERSION.SDK_INT >= 30) {
      getWindow().setDecorFitsSystemWindows(false);
      android.view.WindowInsetsController c = getWindow().getInsetsController();
      if (c != null) {
        c.hide(android.view.WindowInsets.Type.systemBars());
        c.setSystemBarsBehavior(android.view.WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
      }
    } else {
      d.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE
          | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
          | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
          | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
          | View.SYSTEM_UI_FLAG_FULLSCREEN
          | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }
  }

  @Override public void onWindowFocusChanged(boolean focused) {
    super.onWindowFocusChanged(focused);
    if (focused) hideBars();
  }

  @Override public void onConfigurationChanged(Configuration c) {
    super.onConfigurationChanged(c);
    hideBars();
  }

  @Override protected void onSaveInstanceState(Bundle out) {
    super.onSaveInstanceState(out);
    web.saveState(out);
  }

  @Override protected void onPause() {
    super.onPause();
    web.onPause();
  }

  @Override protected void onResume() {
    super.onResume();
    web.onResume();
  }

  /** Back hands the game its own menu (Esc); pressed again, it leaves. */
  @Override public void onBackPressed() {
    long now = System.currentTimeMillis();
    if (now - lastBack < 2500) { super.onBackPressed(); return; }
    lastBack = now;
    web.evaluateJavascript(
        "window.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',code:'Escape',keyCode:27,which:27,bubbles:true}))",
        null);
  }

  /** Everything under https://<host>/ that ships in the APK comes from assets/ — the rest is the network's. */
  private class Local extends WebViewClient {
    @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req) {
      Uri u = req.getUrl();
      if (u == null || !host.equals(u.getHost())) return null;
      String path = u.getPath();
      if (path == null || path.length() == 0 || "/".equals(path)) path = "/index.html";
      while (path.startsWith("/")) path = path.substring(1);
      InputStream in;
      try {
        in = getAssets().open(path);
      } catch (IOException e) {
        // not one of ours: the relay's socket, the counters' hello, an online
        // save — let the WebView ask the real server, exactly as a browser would
        return null;
      }
      String type = mime(path);
      return new WebResourceResponse(type, type.startsWith("text/") || type.contains("javascript") ? "utf-8" : null, 200, "OK", null, in);
    }

    @Override public void onPageFinished(WebView view, String url) {
      Log.i(TAG, "page ready: " + url);
    }
  }

  private class Chrome extends WebChromeClient {
    @Override public boolean onConsoleMessage(ConsoleMessage m) {
      Log.i(TAG, m.message() + "  (" + m.sourceId() + ":" + m.lineNumber() + ")");
      return true;
    }
  }

  private static String mime(String p) {
    if (p.endsWith(".js") || p.endsWith(".mjs")) return "text/javascript";
    if (p.endsWith(".html") || p.endsWith(".htm")) return "text/html";
    if (p.endsWith(".css")) return "text/css";
    if (p.endsWith(".json") || p.endsWith(".webmanifest")) return "application/json";
    if (p.endsWith(".png")) return "image/png";
    if (p.endsWith(".svg")) return "image/svg+xml";
    if (p.endsWith(".woff2")) return "font/woff2";
    if (p.endsWith(".txt") || p.endsWith(".md")) return "text/plain";
    return "application/octet-stream";
  }
}
