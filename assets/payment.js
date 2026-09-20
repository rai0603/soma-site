/**
 * Soma 行銷站 — 匯款 / ATM / PayPal 購買流程（線上刷卡停用期間）。
 *
 * 五個語系首頁共用這一支，所以收款資訊只有這裡一份，改一次全站生效。
 *
 * ⚠️ 帳號採「拆段存放、前端組合」：原始 HTML/JS 不含完整帳號字串，
 *    降低被爬蟲收錄、被冒用於詐騙話術的機會。這不是加密，只是提高門檻。
 *
 * 填寫方式：改下面 PAYMENT 裡標了 TODO(rai) 的值即可。
 * 銀行資料沒填完時，頁面會自動退回「來信索取匯款資訊」，不會顯示空欄位。
 */
(function () {
  'use strict';

  /** 銀行帳號分段，每段 3–5 碼。例：['0123','456','789012'] */
  var ACCOUNT_PARTS = []; // TODO(rai): 填銀行帳號分段

  var PAYMENT = {
    bankName:     '', // TODO(rai) 例：'玉山銀行'
    bankCode:     '', // TODO(rai) 例：'808'
    branch:       '', // TODO(rai) 例：'台中分行'
    accountName:  '', // TODO(rai) 例：'水行者國際有限公司'
    swift:        '', // TODO(rai) 海外電匯用；留空則海外只顯示 PayPal
    paypalUrl:    '', // TODO(rai) 例：'https://paypal.me/xxxx'
    supportEmail: 'support@soma-agent.com',
  };

  /** 可用匯款購買的方案（原本 Paddle 賣得動的那幾個）。金額為 TWD。 */
  var SKUS = {
    buyout_basic:  { twd: 599,  key: 'basic'   },
    buyout_pro:    { twd: 899,  key: 'pro'     },
    addon_podcast: { twd: 399,  key: 'podcast' },
  };

  var BANK_OK = ACCOUNT_PARTS.length > 0 && PAYMENT.bankName !== '' && PAYMENT.accountName !== '';

  var T = {
    'zh-Hant': {
      btn: '線上支付申請中', btnSub: '改用匯款 / ATM 購買 →',
      title: '線上支付申請中',
      intro: '我們正在更換金流服務商，線上刷卡暫時停用。這段期間可以用銀行匯款、ATM 轉帳或 PayPal 購買，我們確認款項後會把序號寄到你的信箱，通常在 1 個工作天內完成。',
      plan: { basic: '限量買斷・基礎', pro: '限量買斷・進階', podcast: 'Podcast 雙角色對話（加購）' },
      bankTitle: '匯款 / ATM 轉帳（台灣）', bank: '銀行', branch: '分行', holder: '戶名', acct: '帳號', amount: '金額',
      swift: 'SWIFT', copy: '複製', copied: '已複製',
      askMail: '請來信 {email} 索取匯款帳號，我們會在 1 個工作天內回覆。',
      paypalTitle: '海外買家 — PayPal', paypalDesc: '沒有台灣銀行帳戶的話用這個，可刷卡。金額以 PayPal 當日匯率換算。',
      paypalBtn: 'PayPal 付款',
      reportTitle: '付款後請回報', reportDesc: '我們沒辦法自動比對匯款，需要你告訴我們一聲才能發序號。',
      reportBtn: '寄出付款回報',
      reportHint: '無法開啟郵件軟體的話，請直接寄到 {email}，註明方案、付款後五碼（或 PayPal 交易編號）、日期、收序號的信箱。',
      fraudTitle: '防詐騙提醒',
      fraud: ['我們只有這一組收款帳戶，也只會在本頁公布。', '我們絕不會用電話、簡訊或通訊軟體通知你「帳號變更」「分期設定錯誤」「需要操作 ATM 更正」。接到這類訊息一律是詐騙。', '有疑問請寄信到 {email} 向我們確認，不要照對方指示操作。'],
      close: '關閉', keyLabel: '你的序號', mailSubject: '付款回報 — {plan}',
      mailLines: ['（請填寫以下資訊，我們收到後會盡快處理）', '', '方案：{plan} NT${amount}', '付款方式（匯款／ATM／PayPal）：', '付款帳號後五碼或 PayPal 交易編號：', '付款日期：', '收序號的 Email：'],
    },
    'zh-Hans': {
      btn: '在线支付申请中', btnSub: '改用汇款 / ATM 购买 →',
      title: '在线支付申请中',
      intro: '我们正在更换支付服务商，在线刷卡暂时停用。这段期间可以用银行汇款、ATM 转账或 PayPal 购买，我们确认款项后会把序号寄到你的邮箱，通常在 1 个工作日内完成。',
      plan: { basic: '限量买断・基础', pro: '限量买断・进阶', podcast: 'Podcast 双角色对话（加购）' },
      bankTitle: '汇款 / ATM 转账（台湾）', bank: '银行', branch: '分行', holder: '户名', acct: '账号', amount: '金额',
      swift: 'SWIFT', copy: '复制', copied: '已复制',
      askMail: '请来信 {email} 索取汇款账号，我们会在 1 个工作日内回覆。',
      paypalTitle: '海外买家 — PayPal', paypalDesc: '没有台湾银行账户的话用这个，可刷卡。金额以 PayPal 当日汇率换算。',
      paypalBtn: 'PayPal 付款',
      reportTitle: '付款后请回报', reportDesc: '我们没办法自动比对汇款，需要你告诉我们一声才能发序号。',
      reportBtn: '寄出付款回报',
      reportHint: '无法打开邮件软件的话，请直接寄到 {email}，注明方案、付款后五码（或 PayPal 交易编号）、日期、收序号的邮箱。',
      fraudTitle: '防诈骗提醒',
      fraud: ['我们只有这一组收款账户，也只会在本页公布。', '我们绝不会用电话、短信或通讯软件通知你「账号变更」「分期设定错误」「需要操作 ATM 更正」。接到这类讯息一律是诈骗。', '有疑问请寄信到 {email} 向我们确认，不要照对方指示操作。'],
      close: '关闭', keyLabel: '你的序号', mailSubject: '付款回报 — {plan}',
      mailLines: ['（请填写以下资讯，我们收到后会尽快处理）', '', '方案：{plan} NT${amount}', '付款方式（汇款／ATM／PayPal）：', '付款账号后五码或 PayPal 交易编号：', '付款日期：', '收序号的 Email：'],
    },
    en: {
      btn: 'Online payment under review', btnSub: 'Pay by transfer / PayPal →',
      title: 'Online payment under review',
      intro: 'We are switching payment providers, so card checkout is temporarily unavailable. You can still buy by PayPal or bank transfer — we will email your license key once payment clears, usually within one business day.',
      plan: { basic: 'Perpetual — Basic', pro: 'Perpetual — Advanced', podcast: 'Podcast two-character mode (add-on)' },
      bankTitle: 'Bank transfer (Taiwan)', bank: 'Bank', branch: 'Branch', holder: 'Account name', acct: 'Account no.', amount: 'Amount',
      swift: 'SWIFT', copy: 'Copy', copied: 'Copied',
      askMail: 'Email {email} for our bank details and we will reply within one business day.',
      paypalTitle: 'PayPal', paypalDesc: 'Easiest option outside Taiwan — pay by card through PayPal. Converted at PayPal’s rate.',
      paypalBtn: 'Pay with PayPal',
      reportTitle: 'Tell us after you pay', reportDesc: 'We cannot match payments automatically, so we need a quick note from you before we can issue the key.',
      reportBtn: 'Send payment confirmation',
      reportHint: 'If your mail app will not open, email {email} directly with the plan, the PayPal transaction ID or last five digits of your transfer, the date, and the address to send the key to.',
      fraudTitle: 'Fraud warning',
      fraud: ['We have only one receiving account, and we only publish it here.', 'We will never call, text or message you about a "changed account number", an "incorrect instalment setting", or ask you to operate an ATM to fix anything. Any such message is a scam.', 'If in doubt, email {email} to confirm with us. Do not follow the other party’s instructions.'],
      close: 'Close', keyLabel: 'Your license key', mailSubject: 'Payment confirmation — {plan}',
      mailLines: ['(Please fill this in — we will process it as soon as we receive it)', '', 'Plan: {plan} NT${amount}', 'Payment method (bank transfer / PayPal):', 'PayPal transaction ID or last 5 digits of transfer:', 'Payment date:', 'Email to send the license key to:'],
    },
    ja: {
      btn: 'オンライン決済は申請中', btnSub: '振込 / PayPal で購入 →',
      title: 'オンライン決済は申請中',
      intro: '決済代行会社の切り替え中のため、カード決済を一時停止しています。その間は PayPal または銀行振込でご購入いただけます。入金確認後、通常 1 営業日以内にライセンスキーをメールでお送りします。',
      plan: { basic: '買い切り・ベーシック', pro: '買い切り・アドバンス', podcast: 'Podcast 2キャラ会話（追加購入）' },
      bankTitle: '銀行振込（台湾）', bank: '銀行', branch: '支店', holder: '口座名義', acct: '口座番号', amount: '金額',
      swift: 'SWIFT', copy: 'コピー', copied: 'コピーしました',
      askMail: '{email} までご連絡いただければ、1 営業日以内に振込先をお送りします。',
      paypalTitle: 'PayPal', paypalDesc: '台湾の銀行口座をお持ちでない方はこちら。カード決済が使えます。金額は PayPal のレートで換算されます。',
      paypalBtn: 'PayPal で支払う',
      reportTitle: 'お支払い後にご連絡ください', reportDesc: '入金の自動照合ができないため、ご連絡をいただいてからキーを発行します。',
      reportBtn: '支払い報告を送る',
      reportHint: 'メールソフトが開かない場合は {email} 宛に、プラン・PayPal 取引 ID または振込口座の下 5 桁・日付・キーの送り先メールをお送りください。',
      fraudTitle: '詐欺にご注意',
      fraud: ['当方の入金口座はこの 1 つだけで、公開もこのページのみです。', '「口座変更」「分割設定の誤り」「ATM での訂正操作」などを電話・SMS・メッセージアプリでご案内することは一切ありません。そうした連絡はすべて詐欺です。', 'ご不明な点は {email} までご確認ください。相手の指示には従わないでください。'],
      close: '閉じる', keyLabel: 'ライセンスキー', mailSubject: '支払い報告 — {plan}',
      mailLines: ['（ご記入ください。確認後すぐに対応します）', '', 'プラン：{plan} NT${amount}', 'お支払い方法（振込 / PayPal）：', 'PayPal 取引 ID または振込口座の下 5 桁：', 'お支払い日：', 'キーの送付先メール：'],
    },
    ko: {
      btn: '온라인 결제 신청 중', btnSub: '계좌이체 / PayPal 로 구매 →',
      title: '온라인 결제 신청 중',
      intro: '결제 대행사를 변경하는 중이라 카드 결제가 일시 중단되었습니다. 그동안 PayPal 또는 계좌이체로 구매하실 수 있으며, 입금 확인 후 보통 1 영업일 이내에 라이선스 키를 메일로 보내 드립니다.',
      plan: { basic: '평생 이용・베이직', pro: '평생 이용・어드밴스', podcast: 'Podcast 2인 대화 (추가 구매)' },
      bankTitle: '계좌이체 (대만)', bank: '은행', branch: '지점', holder: '예금주', acct: '계좌번호', amount: '금액',
      swift: 'SWIFT', copy: '복사', copied: '복사됨',
      askMail: '{email} 로 메일 주시면 1 영업일 이내에 입금 계좌를 보내 드립니다.',
      paypalTitle: 'PayPal', paypalDesc: '대만 계좌가 없으시면 이 방법을 이용하세요. 카드 결제가 가능하며 금액은 PayPal 환율로 환산됩니다.',
      paypalBtn: 'PayPal 로 결제',
      reportTitle: '결제 후 알려 주세요', reportDesc: '입금을 자동으로 대조할 수 없어서, 알려 주셔야 키를 발급해 드릴 수 있습니다.',
      reportBtn: '결제 내역 보내기',
      reportHint: '메일 앱이 열리지 않으면 {email} 로 플랜, PayPal 거래 ID 또는 이체 계좌 뒤 5 자리, 날짜, 키를 받을 메일 주소를 보내 주세요.',
      fraudTitle: '사기 주의',
      fraud: ['입금 계좌는 이 하나뿐이며, 이 페이지에서만 공개합니다.', '「계좌 변경」「할부 설정 오류」「ATM 조작 필요」 등을 전화·문자·메신저로 안내하는 일은 절대 없습니다. 그런 연락은 모두 사기입니다.', '의심되면 {email} 로 저희에게 직접 확인하시고, 상대방 지시를 따르지 마세요.'],
      close: '닫기', keyLabel: '라이선스 키', mailSubject: '결제 내역 — {plan}',
      mailLines: ['(작성해 주시면 확인 후 바로 처리해 드립니다)', '', '플랜: {plan} NT${amount}', '결제 수단 (계좌이체 / PayPal):', 'PayPal 거래 ID 또는 이체 계좌 뒤 5 자리:', '결제일:', '키를 받을 이메일:'],
    },
  };

  var CSS = [
    '.sp-ov{position:fixed;inset:0;background:rgba(11,42,48,.55);z-index:9999;display:flex;align-items:flex-start;justify-content:center;overflow-y:auto;padding:24px 16px;}',
    '.sp-box{background:#fff;color:#12262B;max-width:520px;width:100%;border-radius:14px;box-shadow:0 20px 60px rgba(0,0,0,.28);padding:26px 24px;margin:auto;}',
    '.sp-h{font-weight:900;font-size:19px;margin:0 0 10px;}',
    '.sp-p{font-size:14px;line-height:1.75;margin:0 0 16px;color:#33474D;}',
    '.sp-sec{border:1px solid #DCE4E6;border-radius:11px;padding:15px 16px;margin-bottom:13px;}',
    '.sp-sec h4{margin:0 0 9px;font-size:14.5px;font-weight:800;}',
    '.sp-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #EDF1F2;}',
    '.sp-row:last-child{border-bottom:0;}',
    '.sp-k{font-size:12.5px;color:#5A6D72;width:82px;flex:0 0 auto;}',
    '.sp-v{font-size:14px;font-weight:700;flex:1;word-break:break-all;}',
    '.sp-cp{flex:0 0 auto;font-size:11.5px;border:1px solid #CBD6D9;background:#F5F8F8;border-radius:7px;padding:4px 9px;cursor:pointer;color:#12262B;}',
    '.sp-cp:hover{background:#E9EFF0;}',
    '.sp-btn{display:block;width:100%;box-sizing:border-box;text-align:center;padding:13px;border-radius:9px;font-weight:800;font-size:14.5px;text-decoration:none;cursor:pointer;border:0;}',
    '.sp-btn-1{background:#0E7C86;color:#fff;} .sp-btn-1:hover{background:#0B656D;}',
    '.sp-btn-2{background:#F5F8F8;color:#12262B;border:1px solid #CBD6D9;} .sp-btn-2:hover{background:#E9EFF0;}',
    '.sp-note{font-size:12px;line-height:1.7;color:#5A6D72;margin:9px 0 0;}',
    '.sp-fraud{background:#FFF7ED;border-color:#F3D3AE;}',
    '.sp-fraud ul{margin:0;padding-left:18px;} .sp-fraud li{font-size:12.5px;line-height:1.75;margin-bottom:6px;color:#4A3520;}',
    '.sp-x{float:right;background:0;border:0;font-size:22px;line-height:1;cursor:pointer;color:#5A6D72;padding:0 2px;}',
    '@media(max-width:420px){.sp-box{padding:20px 16px;} .sp-k{width:70px;}}',
  ].join('');

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function fill(s, vars) {
    return String(s).replace(/\{(\w+)\}/g, function (_, k) { return vars[k] != null ? vars[k] : ''; });
  }
  function row(k, v, copyable, t) {
    return '<div class="sp-row"><span class="sp-k">' + esc(k) + '</span><span class="sp-v">' + esc(v) + '</span>' +
      (copyable ? '<button type="button" class="sp-cp" data-copy="' + esc(v) + '">' + esc(t.copy) + '</button>' : '') + '</div>';
  }

  var SomaPayment = {
    /** 這個 SKU 現在買得到嗎（匯款管道）。買不到的（訂閱、創始款）維持「即將開放」。 */
    sellable: function (sku) { return Object.prototype.hasOwnProperty.call(SKUS, sku); },

    labels: function (lang) {
      var t = T[lang] || T.en;
      return { btn: t.btn, btnSub: t.btnSub };
    },

    /** 開啟付款說明。extra.licenseKey 給 Podcast 加購用。 */
    open: function (sku, lang, extra) {
      var t = T[lang] || T.en;
      var s = SKUS[sku];
      if (!s) return;
      var planName = t.plan[s.key] || s.key;
      var amount = s.twd.toLocaleString('en-US');
      var email = PAYMENT.supportEmail;
      var key = extra && extra.licenseKey ? extra.licenseKey : '';

      var lines = t.mailLines.map(function (l) { return fill(l, { plan: planName, amount: amount }); });
      if (key) lines.push(t.keyLabel + '：' + key);
      var mailto = 'mailto:' + email +
        '?subject=' + encodeURIComponent(fill(t.mailSubject, { plan: planName })) +
        '&body=' + encodeURIComponent(lines.join('\n') + '\n');

      var bankBlock = BANK_OK
        ? '<div class="sp-sec"><h4>' + esc(t.bankTitle) + '</h4>' +
            row(t.bank, PAYMENT.bankName + (PAYMENT.bankCode ? '（' + PAYMENT.bankCode + '）' : ''), false, t) +
            (PAYMENT.branch ? row(t.branch, PAYMENT.branch, false, t) : '') +
            row(t.holder, PAYMENT.accountName, false, t) +
            row(t.acct, ACCOUNT_PARTS.join(''), true, t) +
            (PAYMENT.swift ? row(t.swift, PAYMENT.swift, true, t) : '') +
            row(t.amount, 'NT$' + amount, true, t) +
          '</div>'
        : '<div class="sp-sec"><h4>' + esc(t.bankTitle) + '</h4><p class="sp-p" style="margin:0;">' +
            fill(esc(t.askMail), { email: esc(email) }) + '</p></div>';

      var paypalBlock = PAYMENT.paypalUrl
        ? '<div class="sp-sec"><h4>' + esc(t.paypalTitle) + '</h4><p class="sp-note" style="margin:0 0 11px;">' + esc(t.paypalDesc) + '</p>' +
            '<a class="sp-btn sp-btn-2" href="' + esc(PAYMENT.paypalUrl) + '" target="_blank" rel="noopener noreferrer">' +
            esc(t.paypalBtn) + ' · NT$' + amount + '</a></div>'
        : '';

      /* 台灣買家看匯款優先；其他語系 PayPal 在前，台灣帳戶留在後面備用。 */
      var payBlocks = (lang === 'zh-Hant') ? bankBlock + paypalBlock : paypalBlock + bankBlock;

      var fraud = '<div class="sp-sec sp-fraud"><h4>' + esc(t.fraudTitle) + '</h4><ul>' +
        t.fraud.map(function (f) { return '<li>' + fill(esc(f), { email: esc(email) }) + '</li>'; }).join('') +
        '</ul></div>';

      var html =
        '<div class="sp-box" role="dialog" aria-modal="true" aria-label="' + esc(t.title) + '">' +
          '<button type="button" class="sp-x" data-sp-close aria-label="' + esc(t.close) + '">&times;</button>' +
          '<h3 class="sp-h">' + esc(t.title) + '</h3>' +
          '<p class="sp-p">' + esc(t.intro) + '</p>' +
          '<div class="sp-sec"><div class="sp-row"><span class="sp-k"></span>' +
            '<span class="sp-v">' + esc(planName) + '</span><span class="sp-v" style="text-align:right;flex:0 0 auto;">NT$' + amount + '</span></div>' +
            (key ? row(t.keyLabel, key, false, t) : '') + '</div>' +
          payBlocks +
          '<div class="sp-sec"><h4>' + esc(t.reportTitle) + '</h4>' +
            '<p class="sp-note" style="margin:0 0 11px;">' + esc(t.reportDesc) + '</p>' +
            '<a class="sp-btn sp-btn-1" href="' + mailto + '">' + esc(t.reportBtn) + '</a>' +
            '<p class="sp-note">' + fill(esc(t.reportHint), { email: esc(email) }) + '</p></div>' +
          fraud +
        '</div>';

      var ov = document.createElement('div');
      ov.className = 'sp-ov';
      ov.innerHTML = html;

      function close() {
        ov.remove();
        document.removeEventListener('keydown', onKey);
        document.body.style.overflow = prevOverflow;
      }
      function onKey(e) { if (e.key === 'Escape') close(); }

      /* backdrop 用 overlay 本身接點擊，不包住內容 —— 包住會吃掉內部 input/button 的互動 */
      ov.addEventListener('click', function (e) {
        if (e.target === ov || e.target.hasAttribute('data-sp-close')) close();
        var cp = e.target.closest && e.target.closest('[data-copy]');
        if (cp && navigator.clipboard) {
          navigator.clipboard.writeText(cp.getAttribute('data-copy'));
          cp.textContent = t.copied;
          setTimeout(function () { cp.textContent = t.copy; }, 1800);
        }
      });
      document.addEventListener('keydown', onKey);

      var prevOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      document.body.appendChild(ov);
    },
  };

  var style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  window.SomaPayment = SomaPayment;
})();
