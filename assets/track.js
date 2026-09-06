/**
 * AICMS 流量追蹤 — soma-agent.com（靜態站版）
 *
 * 官網是 Cloudflare Pages 的靜態站，不是 AICMS 託管的頁面，所以走 /api/track
 * 內建的「外站追蹤」路徑：body 帶 tenant_slug，後端驗 tenant.is_internal
 * 且 Origin 必須在該 tenant 的 domains 白名單內，兩者皆過才寫入。
 *
 * 端點指向 waterman-sports.cc 是因為它就是 AICMS public-site 本體
 * （官網客服 widget.js 也是從這裡載的）；ai-cms.cc 是另一個服務，/api/track 回 405。
 *
 * 隱私：不送任何個資。visitor_id 由後端用 sha256(ip+ua+日鹽) 算，24 小時換一次。
 */
(function () {
  var ENDPOINT = 'https://waterman-sports.cc/api/track';
  var TENANT = 'soma-agent';
  var SESSION_KEY = '_aicms_sid';

  function sessionId() {
    try {
      var sid = sessionStorage.getItem(SESSION_KEY);
      if (!sid) {
        sid = 's_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 10);
        sessionStorage.setItem(SESSION_KEY, sid);
      }
      return sid;
    } catch (e) {
      return null; // 無痕模式 sessionStorage 會丟例外，不能讓追蹤弄壞頁面
    }
  }

  function send(payload) {
    payload.tenant_slug = TENANT;
    payload.session_id = sessionId();
    try {
      var body = JSON.stringify(payload);
      // sendBeacon 在頁面關閉時仍保證送出；不支援才退回 fetch keepalive
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: 'application/json' }));
      } else {
        fetch(ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: body,
          keepalive: true,
        }).catch(function () {});
      }
    } catch (e) {
      /* 追蹤失敗一律吞掉，絕不影響使用者 */
    }
  }

  var p = new URLSearchParams(location.search);
  // fbclid 代表來自 Meta 廣告但沒帶 utm_source；後端再用 UA 分辨 FB / IG
  var utmSource = p.get('utm_source') || (p.get('fbclid') ? 'facebook' : null);

  send({
    type: 'pageview',
    path: location.pathname,
    referer: document.referrer || null,
    utm_source: utmSource,
    utm_medium: p.get('utm_medium'),
    utm_campaign: p.get('utm_campaign'),
    utm_content: p.get('utm_content'),
    utm_term: p.get('utm_term'),
    screen_w: screen.width,
    screen_h: screen.height,
  });

  // 下載點擊 — 這是漏斗最關鍵的一格：進站的人裡有多少真的去抓 dmg
  document.addEventListener(
    'click',
    function (e) {
      var a = e.target.closest && e.target.closest('a[href*="releases/download"]');
      if (a) send({ type: 'download_click', path: location.pathname });
    },
    true
  );

  // 停留時間 — pagehide 比 unload 可靠（bfcache 下 unload 不會觸發）
  var enter = Date.now();
  var sent = false;
  function leave() {
    if (sent) return;
    sent = true;
    send({ type: 'pageleave', path: location.pathname, duration_ms: Date.now() - enter });
  }
  addEventListener('pagehide', leave);
  addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') leave();
  });
})();
