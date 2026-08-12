#!/usr/bin/env node
/**
 * 客戶自助頁產生器：`/account`（我的帳號）與 `/recover`（找回序號），五語。
 *
 * 這兩頁是純靜態 HTML + fetch，資料全部來自授權後端 license.soma-agent.com：
 *   /auth/request → magic link 登入信（不做密碼）
 *   /me           → 授權與裝置（要 credentials，origin 必須在後端白名單）
 *   /me/devices/:id/deactivate → 遠端解綁
 *   /recover      → 重寄序號（公開端點，回應一律不分歧）
 *
 * account 產生成 `account/index.html`：後端 /auth/verify 導回的是不帶副檔名的
 * `SITE_BASE_URL/account`，目錄形式才接得住。
 *
 * 用法：node scripts/build-portal.mjs
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const API = 'https://license.soma-agent.com';
const SITE = 'https://soma-agent.com';

const LANGS = [
  { code: 'zh-Hant', dir: '', htmlLang: 'zh-Hant', locale: 'zh-TW', label: '繁' },
  { code: 'zh-Hans', dir: 'cn', htmlLang: 'zh-Hans', locale: 'zh-CN', label: '简' },
  { code: 'en', dir: 'en', htmlLang: 'en', locale: 'en-US', label: 'EN' },
  { code: 'ja', dir: 'ja', htmlLang: 'ja', locale: 'ja-JP', label: '日' },
  { code: 'ko', dir: 'ko', htmlLang: 'ko', locale: 'ko-KR', label: '한' },
];

/* ---------- 文案 ---------- */

const S = {
  'zh-Hant': {
    home: '回首頁', guide: '使用教學', account: '我的帳號', recover: '找回序號',
    emailPh: '購買時使用的 Email', invalidEmail: '請輸入有效的 Email 位址。',
    tooMany: '嘗試太頻繁了，請過一分鐘再試。', netError: '暫時連不上授權伺服器，請稍後再試。',
    loading: '載入中…', support: '寄信給客服',
    rcTitle: '找回序號', rcDesc: 'Soma Agent 找回序號｜把名下所有授權序號重寄到你的信箱。',
    rcLead: '輸入購買時使用的 Email，我們會把這個信箱名下的所有序號重新寄一次。',
    rcSubmit: '重寄序號',
    rcSent: '如果這個信箱有授權，序號已經寄出了。請檢查收件匣與垃圾信件匣。',
    acTitle: '我的帳號', acDesc: 'Soma Agent 我的帳號｜查看授權、序號與已綁定的裝置，並可遠端解除綁定。',
    acLead: '輸入購買時使用的 Email，我們會寄一條登入連結給你——不需要設密碼。',
    acSubmit: '寄送登入連結',
    acSent: '如果這個信箱有授權，登入連結已經寄出。連結 15 分鐘內有效，而且只能用一次。',
    acInvalidLink: '這條登入連結無效或已經用過了，請重新索取一次。',
    logout: '登出', noLicense: '這個帳號名下還沒有授權。買了之後用同一個 Email 登入就會自動接上。',
    key: '序號', copy: '複製', copied: '已複製', purchasedAt: '購買日', seats: '席次',
    devices: '已綁定的裝置', noDevices: '尚未綁定任何裝置。',
    activatedAt: '啟用', lastSeen: '最後使用', unbind: '解除綁定',
    unbindConfirm: '確定要解除「{name}」的綁定嗎？該裝置下次開啟 Soma Agent 時會回到未授權狀態，席次會立刻釋放。',
    unnamed: '未命名裝置',
    tier: { basic: '基礎版', advanced: '進階版' }, podcast: 'Podcast 加購',
    type: { perpetual: '買斷', subscription: '訂閱', trial: '7 天試用' },
    status: { active: '使用中', suspended: '已暫停', refunded: '已退款' },
    expiresAt: '到期日', neverExpires: '永久有效',
  },
  'zh-Hans': {
    home: '回首页', guide: '使用教程', account: '我的账号', recover: '找回序号',
    emailPh: '购买时使用的 Email', invalidEmail: '请输入有效的 Email 地址。',
    tooMany: '尝试太频繁了，请过一分钟再试。', netError: '暂时连不上授权服务器，请稍后再试。',
    loading: '加载中…', support: '寄信给客服',
    rcTitle: '找回序号', rcDesc: 'Soma Agent 找回序号｜把名下所有授权序号重寄到你的邮箱。',
    rcLead: '输入购买时使用的 Email，我们会把这个邮箱名下的所有序号重新寄一次。',
    rcSubmit: '重寄序号',
    rcSent: '如果这个邮箱有授权，序号已经寄出了。请检查收件箱与垃圾邮件箱。',
    acTitle: '我的账号', acDesc: 'Soma Agent 我的账号｜查看授权、序号与已绑定的设备，并可远程解除绑定。',
    acLead: '输入购买时使用的 Email，我们会寄一条登录链接给你——不需要设密码。',
    acSubmit: '寄送登录链接',
    acSent: '如果这个邮箱有授权，登录链接已经寄出。链接 15 分钟内有效，而且只能用一次。',
    acInvalidLink: '这条登录链接无效或已经用过了，请重新索取一次。',
    logout: '登出', noLicense: '这个账号名下还没有授权。买了之后用同一个 Email 登录就会自动接上。',
    key: '序号', copy: '复制', copied: '已复制', purchasedAt: '购买日', seats: '席位',
    devices: '已绑定的设备', noDevices: '尚未绑定任何设备。',
    activatedAt: '激活', lastSeen: '最后使用', unbind: '解除绑定',
    unbindConfirm: '确定要解除「{name}」的绑定吗？该设备下次打开 Soma Agent 时会回到未授权状态，席位会立刻释放。',
    unnamed: '未命名设备',
    tier: { basic: '基础版', advanced: '进阶版' }, podcast: 'Podcast 加购',
    type: { perpetual: '买断', subscription: '订阅', trial: '7 天试用' },
    status: { active: '使用中', suspended: '已暂停', refunded: '已退款' },
    expiresAt: '到期日', neverExpires: '永久有效',
  },
  en: {
    home: 'Home', guide: 'Guide', account: 'My account', recover: 'Recover key',
    emailPh: 'The email you bought with', invalidEmail: 'Please enter a valid email address.',
    tooMany: 'Too many attempts. Try again in a minute.', netError: 'Cannot reach the licence server right now. Please try again shortly.',
    loading: 'Loading…', support: 'Email support',
    rcTitle: 'Recover your key', rcDesc: 'Soma Agent — resend every licence key registered to your email address.',
    rcLead: 'Enter the email you bought with and we will resend every licence key registered to it.',
    rcSubmit: 'Resend my keys',
    rcSent: 'If that address has a licence, the keys are on their way. Check your inbox and spam folder.',
    acTitle: 'My account', acDesc: 'Soma Agent — view your licences, keys and bound machines, and unbind remotely.',
    acLead: 'Enter the email you bought with and we will send you a sign-in link. No password needed.',
    acSubmit: 'Send sign-in link',
    acSent: 'If that address has a licence, the sign-in link is on its way. It is valid for 15 minutes and works once.',
    acInvalidLink: 'That sign-in link is invalid or has already been used. Please request a new one.',
    logout: 'Sign out', noLicense: 'No licence on this account yet. Buy one with this same email and it will attach automatically.',
    key: 'Licence key', copy: 'Copy', copied: 'Copied', purchasedAt: 'Purchased', seats: 'Seats',
    devices: 'Bound machines', noDevices: 'No machine bound yet.',
    activatedAt: 'Activated', lastSeen: 'Last seen', unbind: 'Unbind',
    unbindConfirm: 'Unbind “{name}”? That machine drops back to unlicensed next time Soma Agent starts, and the seat is freed immediately.',
    unnamed: 'Unnamed machine',
    tier: { basic: 'Basic', advanced: 'Advanced' }, podcast: 'Podcast add-on',
    type: { perpetual: 'One-time', subscription: 'Subscription', trial: '7-day trial' },
    status: { active: 'Active', suspended: 'Suspended', refunded: 'Refunded' },
    expiresAt: 'Expires', neverExpires: 'Never expires',
  },
  ja: {
    home: 'トップへ', guide: '使い方ガイド', account: 'マイアカウント', recover: 'キーの再送',
    emailPh: '購入時のメールアドレス', invalidEmail: '有効なメールアドレスを入力してください。',
    tooMany: '試行が多すぎます。1 分ほど待って再度お試しください。', netError: 'ライセンスサーバーに接続できません。しばらくしてからお試しください。',
    loading: '読み込み中…', support: 'サポートに問い合わせる',
    rcTitle: 'キーの再送', rcDesc: 'Soma Agent — 登録済みのライセンスキーをメールで再送します。',
    rcLead: '購入時のメールアドレスを入力すると、そのアドレスに紐づくライセンスキーをすべて再送します。',
    rcSubmit: 'キーを再送する',
    rcSent: 'そのアドレスにライセンスがあれば、キーを送信しました。受信トレイと迷惑メールフォルダをご確認ください。',
    acTitle: 'マイアカウント', acDesc: 'Soma Agent — ライセンス・キー・認証済み端末の確認と、リモートでの認証解除。',
    acLead: '購入時のメールアドレスを入力してください。ログインリンクをお送りします（パスワードは不要です）。',
    acSubmit: 'ログインリンクを送る',
    acSent: 'そのアドレスにライセンスがあれば、ログインリンクを送信しました。有効期限は 15 分、使用は 1 回限りです。',
    acInvalidLink: 'このログインリンクは無効か、すでに使用されています。もう一度お試しください。',
    logout: 'ログアウト', noLicense: 'このアカウントにはまだライセンスがありません。同じアドレスで購入すると自動的に紐づきます。',
    key: 'ライセンスキー', copy: 'コピー', copied: 'コピーしました', purchasedAt: '購入日', seats: 'ライセンス数',
    devices: '認証済みの端末', noDevices: 'まだ端末は登録されていません。',
    activatedAt: '認証日', lastSeen: '最終使用', unbind: '認証を解除',
    unbindConfirm: '「{name}」の認証を解除しますか？次回 Soma Agent を起動したときに未認証の状態に戻り、枠はすぐに解放されます。',
    unnamed: '名称未設定の端末',
    tier: { basic: 'ベーシック', advanced: 'アドバンス' }, podcast: 'Podcast 追加',
    type: { perpetual: '買い切り', subscription: 'サブスク', trial: '7 日間の試用' },
    status: { active: '有効', suspended: '停止中', refunded: '返金済み' },
    expiresAt: '有効期限', neverExpires: '無期限',
  },
  ko: {
    home: '홈으로', guide: '사용 가이드', account: '내 계정', recover: '일련번호 찾기',
    emailPh: '구매 시 사용한 이메일', invalidEmail: '올바른 이메일 주소를 입력해 주세요.',
    tooMany: '시도가 너무 잦습니다. 1분 후에 다시 시도해 주세요.', netError: '라이선스 서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.',
    loading: '불러오는 중…', support: '고객지원에 메일 보내기',
    rcTitle: '일련번호 찾기', rcDesc: 'Soma Agent — 등록된 라이선스 키를 메일로 다시 보내 드립니다.',
    rcLead: '구매 시 사용한 이메일을 입력하시면 그 주소에 등록된 모든 라이선스 키를 다시 보내 드립니다.',
    rcSubmit: '키 다시 받기',
    rcSent: '해당 주소에 라이선스가 있다면 키를 보냈습니다. 받은편지함과 스팸함을 확인해 주세요.',
    acTitle: '내 계정', acDesc: 'Soma Agent — 라이선스와 키, 인증된 기기를 확인하고 원격으로 인증을 해제합니다.',
    acLead: '구매 시 사용한 이메일을 입력해 주세요. 로그인 링크를 보내 드립니다(비밀번호 불필요).',
    acSubmit: '로그인 링크 받기',
    acSent: '해당 주소에 라이선스가 있다면 로그인 링크를 보냈습니다. 15분간 유효하며 한 번만 사용할 수 있습니다.',
    acInvalidLink: '이 로그인 링크는 유효하지 않거나 이미 사용되었습니다. 다시 요청해 주세요.',
    logout: '로그아웃', noLicense: '이 계정에는 아직 라이선스가 없습니다. 같은 이메일로 구매하면 자동으로 연결됩니다.',
    key: '라이선스 키', copy: '복사', copied: '복사됨', purchasedAt: '구매일', seats: '좌석',
    devices: '인증된 기기', noDevices: '아직 등록된 기기가 없습니다.',
    activatedAt: '인증일', lastSeen: '최근 사용', unbind: '인증 해제',
    unbindConfirm: '「{name}」의 인증을 해제할까요? 다음에 Soma Agent를 실행하면 미인증 상태로 돌아가고 좌석은 즉시 반환됩니다.',
    unnamed: '이름 없는 기기',
    tier: { basic: '베이직', advanced: '어드밴스' }, podcast: 'Podcast 추가',
    type: { perpetual: '단품 구매', subscription: '구독', trial: '7일 체험' },
    status: { active: '사용 중', suspended: '일시 중지', refunded: '환불됨' },
    expiresAt: '만료일', neverExpires: '무기한',
  },
};

/* ---------- 共用 ---------- */

const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const CSS = `
  :root{
    --bg:#F2F4F7; --panel:#FFFFFF; --ink:#14161D; --muted:#5A6172; --dim:#9AA2B3; --line:#D8DCE4;
    --acc:#0091AD; --acc-soft:#E3F4F8; --amber:#E0771C; --amber-soft:#FBEEDF; --bad:#B0264A; --bad-soft:#FBE7EC;
    --d-line:#2A2E3A; --d-fg:#F2F3F7; --d-muted:#A6ACBD; --d-dim:#6A7183; --d-acc:#66E0F2;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{background:var(--bg);color:var(--ink);font-family:'Noto Sans TC',sans-serif;line-height:1.7;}
  a{color:inherit;}
  .wrap{max-width:760px;margin:0 auto;padding:0 24px;}
  header{border-bottom:1px solid var(--line);background:rgba(242,244,247,.92);}
  nav{max-width:760px;margin:0 auto;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;}
  .logo{font-family:'Orbitron',sans-serif;font-weight:800;font-size:18px;letter-spacing:.22em;text-decoration:none;}
  .logo i{color:var(--acc);font-style:normal;}
  .navright{display:flex;align-items:center;gap:14px;}
  .lang{display:flex;gap:2px;font-size:12px;}
  .lang a{padding:4px 7px;text-decoration:none;color:var(--dim);border:1px solid transparent;border-radius:3px;}
  .lang a.on{color:var(--acc);border-color:var(--acc);}
  .navlink{font-size:13px;color:var(--muted);text-decoration:none;}
  .navlink:hover{color:var(--acc);}

  main{padding:48px 0 72px;}
  .eyebrow{font-family:'DotGothic16',monospace;font-size:11px;letter-spacing:.2em;color:var(--dim);margin-bottom:10px;}
  h1{font-size:33px;font-weight:900;margin:0 0 12px;letter-spacing:.02em;}
  .lead{color:var(--muted);margin:0 0 28px;max-width:56ch;}

  form{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 12px;}
  input[type=email]{flex:1;min-width:240px;padding:12px 14px;border:1px solid var(--line);border-radius:5px;background:var(--panel);font:inherit;font-size:15px;color:var(--ink);}
  input[type=email]:focus{outline:2px solid var(--acc);outline-offset:-1px;border-color:var(--acc);}
  button{font:inherit;font-weight:700;font-size:14.5px;border:0;border-radius:5px;padding:12px 22px;background:var(--acc);color:#fff;cursor:pointer;}
  button:hover{filter:brightness(1.08);}
  button[disabled]{opacity:.5;cursor:not-allowed;}
  button.ghost{background:var(--panel);color:var(--muted);border:1px solid var(--line);font-weight:500;padding:7px 14px;font-size:13px;}
  button.ghost:hover{color:var(--bad);border-color:var(--bad);filter:none;}

  .msg{padding:13px 16px;border-radius:5px;font-size:14.5px;margin:0 0 20px;}
  .msg.ok{background:var(--acc-soft);border-left:3px solid var(--acc);color:#0d3d47;}
  .msg.bad{background:var(--bad-soft);border-left:3px solid var(--bad);color:#7a1730;}
  .msg.wait{background:var(--panel);border:1px solid var(--line);color:var(--muted);}
  [hidden]{display:none !important;}

  .who{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding-bottom:16px;border-bottom:1px solid var(--line);margin-bottom:26px;}
  .who .mail{font-weight:700;overflow-wrap:anywhere;}

  .lic{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:22px;margin-bottom:18px;}
  .lic-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:16px;}
  .lic-plan{font-size:19px;font-weight:800;}
  .tag{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.06em;padding:3px 9px;border-radius:3px;margin-left:8px;vertical-align:2px;}
  .tag.t-active{background:var(--acc-soft);color:#0d3d47;}
  .tag.t-suspended{background:var(--amber-soft);color:#7a4410;}
  .tag.t-refunded{background:var(--bad-soft);color:#7a1730;}
  .tag.t-addon{background:#EDE7FB;color:#4a2f8f;}
  .meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px 20px;font-size:13.5px;color:var(--muted);margin-bottom:16px;}
  .meta b{display:block;color:var(--dim);font-size:11.5px;letter-spacing:.08em;font-weight:700;text-transform:uppercase;margin-bottom:1px;}
  .keyrow{display:flex;align-items:center;gap:10px;background:var(--bg);border:1px solid var(--line);border-radius:5px;padding:10px 14px;margin-bottom:18px;flex-wrap:wrap;}
  .keyrow code{font-family:ui-monospace,Menlo,monospace;font-size:15px;letter-spacing:.5px;overflow-wrap:anywhere;flex:1;}
  .devs h4{font-size:12px;letter-spacing:.1em;color:var(--dim);text-transform:uppercase;margin:0 0 8px;}
  .dev{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:11px 0;border-top:1px solid var(--line);flex-wrap:wrap;}
  .dev-name{font-weight:700;font-size:14.5px;}
  .dev-when{font-size:12.5px;color:var(--dim);}
  .empty{color:var(--muted);font-size:14px;padding:11px 0;border-top:1px solid var(--line);}

  footer{background:#0e1015;color:var(--d-muted);padding:24px 0;font-size:12.5px;margin-top:40px;}
  footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;}
  footer a{color:inherit;}
  @media(max-width:560px){h1{font-size:27px;} button{width:100%;} input[type=email]{min-width:0;}}
`;

/** 同一頁在其他語系的相對路徑。account 是目錄、recover 是檔案。 */
function altHref(from, to, page) {
  const up = from.dir ? '../' : '';
  const base = `${up}${to.dir ? `${to.dir}/` : ''}`;
  return page === 'account' ? `${base}account/` : `${base}recover.html`;
}

/** account 在子目錄底下多一層，站內連結要多退一級。 */
function shell({ lang, page, bodyHtml, script }) {
  const t = S[lang.code];
  // account 產在 <lang>/account/ 底下，比 recover 多一層，站內連結要多退一級
  const up = page === 'account' ? '../' : '';
  const title = page === 'account' ? t.acTitle : t.rcTitle;
  const desc = page === 'account' ? t.acDesc : t.rcDesc;
  const canonical = `${SITE}/${lang.dir ? `${lang.dir}/` : ''}${page === 'account' ? 'account' : 'recover'}`;

  const langBar = LANGS.map(
    (l) => `<a${l.code === lang.code ? ' class="on"' : ''} href="${altHref(lang, l, page)}" lang="${l.htmlLang}">${l.label}</a>`,
  ).join('');
  const hreflang = LANGS.map(
    (l) => `<link rel="alternate" hreflang="${l.htmlLang}" href="${SITE}/${l.dir ? `${l.dir}/` : ''}${page === 'account' ? 'account' : 'recover'}">`,
  ).join('\n');
  const other = page === 'account'
    ? `<a class="navlink" href="${up}recover.html">${esc(t.recover)}</a>`
    : `<a class="navlink" href="${up}account/">${esc(t.account)}</a>`;

  return `<!DOCTYPE html>
<html lang="${lang.htmlLang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} — Soma Agent</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#F2F4F7">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="${canonical}">
${hreflang}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Chakra+Petch:wght@400;700&family=DotGothic16&family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Sans+JP:wght@500;700&display=swap" rel="stylesheet">
<style>${CSS}</style>
</head>
<body>

<header>
  <nav>
    <a class="logo" href="${up}index.html">SOMA<i>_</i></a>
    <div class="navright">
      <div class="lang">${langBar}</div>
      ${other}
      <a class="navlink" href="${up}help.html">${esc(t.guide)}</a>
      <a class="navlink" href="${up}index.html">${esc(t.home)}</a>
    </div>
  </nav>
</header>

<main>
  <div class="wrap">
${bodyHtml}
  </div>
</main>

<footer>
  <div class="wrap">
    <span>© 2026 Soma Agent</span>
    <span><a href="mailto:support@soma-agent.com">support@soma-agent.com</a></span>
  </div>
</footer>

<script>
const API = ${JSON.stringify(API)};
const T = ${JSON.stringify(S[lang.code])};
const LOCALE = ${JSON.stringify(lang.locale)};
const $ = (id) => document.getElementById(id);
const looksLikeEmail = (v) => /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v.trim());
function show(el, cls, text){ el.className = 'msg ' + cls; el.textContent = text; el.hidden = false; }
${script}
</script>
</body>
</html>
`;
}

/* ---------- recover ---------- */

function recoverPage(lang) {
  const t = S[lang.code];
  const body = `    <div class="eyebrow">SEC.RC / RECOVER</div>
    <h1>${esc(t.rcTitle)}</h1>
    <p class="lead">${esc(t.rcLead)}</p>
    <form id="f" novalidate>
      <input id="email" type="email" autocomplete="email" placeholder="${esc(t.emailPh)}" aria-label="${esc(t.emailPh)}">
      <button id="btn" type="submit">${esc(t.rcSubmit)}</button>
    </form>
    <p id="msg" class="msg" hidden></p>`;

  const script = `
$('f').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = $('email').value.trim();
  const msg = $('msg'), btn = $('btn');
  if (!looksLikeEmail(email)) return show(msg, 'bad', T.invalidEmail);

  btn.disabled = true;
  try {
    const res = await fetch(API + '/recover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    // 後端對「查到／查不到」一律回同一個回應，前端也不要多說什麼
    if (res.status === 429) show(msg, 'bad', T.tooMany);
    else if (!res.ok) show(msg, 'bad', T.netError);
    else show(msg, 'ok', T.rcSent);
  } catch { show(msg, 'bad', T.netError); }
  btn.disabled = false;
});`;

  return shell({ lang, page: 'recover', bodyHtml: body, script });
}

/* ---------- account ---------- */

function accountPage(lang) {
  const t = S[lang.code];
  const body = `    <div class="eyebrow">SEC.AC / ACCOUNT</div>
    <h1>${esc(t.acTitle)}</h1>

    <p id="msg" class="msg" hidden></p>

    <section id="signin" hidden>
      <p class="lead">${esc(t.acLead)}</p>
      <form id="f" novalidate>
        <input id="email" type="email" autocomplete="email" placeholder="${esc(t.emailPh)}" aria-label="${esc(t.emailPh)}">
        <button id="btn" type="submit">${esc(t.acSubmit)}</button>
      </form>
    </section>

    <section id="dash" hidden>
      <div class="who">
        <span class="mail" id="who-mail"></span>
        <button class="ghost" id="btn-logout" type="button">${esc(t.logout)}</button>
      </div>
      <div id="licenses"></div>
    </section>`;

  const script = `
const fmtDate = (s) => s ? new Date(s).toLocaleDateString(LOCALE, { year:'numeric', month:'long', day:'numeric' }) : '';

function planName(lic){
  const base = T.tier[lic.tier] || lic.tier;
  return base + '（' + (T.type[lic.licenseType] || lic.licenseType) + '）';
}

function licenseCard(lic){
  const card = document.createElement('div');
  card.className = 'lic';

  const top = document.createElement('div');
  top.className = 'lic-top';
  const plan = document.createElement('div');
  plan.className = 'lic-plan';
  plan.textContent = planName(lic);
  if (lic.addons && lic.addons.includes('podcast')) {
    const a = document.createElement('span');
    a.className = 'tag t-addon';
    a.textContent = T.podcast;
    plan.appendChild(a);
  }
  const st = document.createElement('span');
  st.className = 'tag t-' + lic.status;
  st.textContent = T.status[lic.status] || lic.status;
  top.appendChild(plan); top.appendChild(st);
  card.appendChild(top);

  const keyrow = document.createElement('div');
  keyrow.className = 'keyrow';
  const code = document.createElement('code');
  code.textContent = lic.key;
  const copyBtn = document.createElement('button');
  copyBtn.className = 'ghost'; copyBtn.type = 'button'; copyBtn.textContent = T.copy;
  copyBtn.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(lic.key); copyBtn.textContent = T.copied; }
    catch { /* 沒有剪貼簿權限就讓使用者自己選取 */ }
  });
  keyrow.appendChild(code); keyrow.appendChild(copyBtn);
  card.appendChild(keyrow);

  const meta = document.createElement('div');
  meta.className = 'meta';
  const cells = [
    [T.purchasedAt, fmtDate(lic.purchasedAt)],
    [T.seats, (lic.devices ? lic.devices.length : 0) + ' / ' + lic.seatLimit],
    [T.expiresAt, lic.expiresAt ? fmtDate(lic.expiresAt) : T.neverExpires],
  ];
  for (const [label, value] of cells) {
    const d = document.createElement('div');
    const b = document.createElement('b'); b.textContent = label;
    d.appendChild(b); d.appendChild(document.createTextNode(value));
    meta.appendChild(d);
  }
  card.appendChild(meta);

  const devs = document.createElement('div');
  devs.className = 'devs';
  const h4 = document.createElement('h4'); h4.textContent = T.devices;
  devs.appendChild(h4);

  if (!lic.devices || lic.devices.length === 0) {
    const e = document.createElement('div'); e.className = 'empty'; e.textContent = T.noDevices;
    devs.appendChild(e);
  } else {
    for (const d of lic.devices) {
      const row = document.createElement('div');
      row.className = 'dev';
      const left = document.createElement('div');
      const name = document.createElement('div');
      name.className = 'dev-name';
      name.textContent = d.name || T.unnamed;
      const when = document.createElement('div');
      when.className = 'dev-when';
      when.textContent = T.activatedAt + ' ' + fmtDate(d.activatedAt) + ' ・ ' + T.lastSeen + ' ' + fmtDate(d.lastSeenAt);
      left.appendChild(name); left.appendChild(when);
      const btn = document.createElement('button');
      btn.className = 'ghost'; btn.type = 'button'; btn.textContent = T.unbind;
      btn.addEventListener('click', () => unbind(d.id, d.name || T.unnamed, btn));
      row.appendChild(left); row.appendChild(btn);
      devs.appendChild(row);
    }
  }
  card.appendChild(devs);
  return card;
}

async function unbind(id, name, btn){
  if (!confirm(T.unbindConfirm.replace('{name}', name))) return;
  btn.disabled = true;
  try {
    const res = await fetch(API + '/me/devices/' + encodeURIComponent(id) + '/deactivate', {
      method: 'POST', credentials: 'include',
    });
    if (!res.ok) { show($('msg'), 'bad', res.status === 429 ? T.tooMany : T.netError); btn.disabled = false; return; }
    await load();                    // 重讀，席次數字才不會停在舊值
  } catch { show($('msg'), 'bad', T.netError); btn.disabled = false; }
}

function renderDash(data){
  $('who-mail').textContent = data.email;
  const box = $('licenses');
  box.textContent = '';
  if (!data.licenses || data.licenses.length === 0) {
    const e = document.createElement('p'); e.className = 'msg wait'; e.textContent = T.noLicense;
    box.appendChild(e);
  } else {
    for (const lic of data.licenses) box.appendChild(licenseCard(lic));
  }
  $('signin').hidden = true;
  $('dash').hidden = false;
}

async function load(){
  const msg = $('msg');
  try {
    const res = await fetch(API + '/me', { credentials: 'include' });
    if (res.status === 401) { $('dash').hidden = true; $('signin').hidden = false; return; }
    if (!res.ok) { show(msg, 'bad', T.netError); $('signin').hidden = false; return; }
    renderDash(await res.json());
  } catch {
    show(msg, 'bad', T.netError);
    $('signin').hidden = false;
  }
}

$('f').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = $('email').value.trim();
  const msg = $('msg'), btn = $('btn');
  if (!looksLikeEmail(email)) return show(msg, 'bad', T.invalidEmail);
  btn.disabled = true;
  try {
    const res = await fetch(API + '/auth/request', {
      method: 'POST', credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    if (res.status === 429) show(msg, 'bad', T.tooMany);
    else if (!res.ok) show(msg, 'bad', T.netError);
    else show(msg, 'ok', T.acSent);
  } catch { show(msg, 'bad', T.netError); }
  btn.disabled = false;
});

$('btn-logout').addEventListener('click', async () => {
  try { await fetch(API + '/auth/logout', { method: 'POST', credentials: 'include' }); } catch {}
  location.href = location.pathname;   // 清掉可能殘留的 ?error=
});

// /auth/verify 兌換失敗會把人導回 ?error=invalid_link
if (new URLSearchParams(location.search).get('error') === 'invalid_link') {
  show($('msg'), 'bad', T.acInvalidLink);
}
show($('msg'), 'wait', T.loading);
load().finally(() => {
  const m = $('msg');
  if (m.className === 'msg wait') m.hidden = true;   // 只清掉「載入中」，別蓋掉錯誤訊息
});`;

  return shell({ lang, page: 'account', bodyHtml: body, script });
}

/* ---------- 輸出 ---------- */

for (const lang of LANGS) {
  const accDir = join(ROOT, lang.dir, 'account');
  mkdirSync(accDir, { recursive: true });
  writeFileSync(join(accDir, 'index.html'), accountPage(lang), 'utf8');

  const recFile = join(ROOT, lang.dir, 'recover.html');
  writeFileSync(recFile, recoverPage(lang), 'utf8');

  console.log(`  ✓ ${lang.dir ? lang.dir + '/' : ''}account/index.html + ${lang.dir ? lang.dir + '/' : ''}recover.html`);
}
console.log(`\n${LANGS.length} 個語系 × 2 頁 → ${ROOT}`);
