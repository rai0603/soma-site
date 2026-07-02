# CLAUDE.md — Soma 行銷網站（soma-site）

> 搭配 `~/.claude/CLAUDE.md` 全域宣言。這是 **Soma** 桌面虛擬夥伴的官方行銷站。
> ⚠️ 本 repo **公開**（利 SEO）：絕不 commit secrets、Paddle live key、或內部成本/毛利數字。

## 這是什麼
靜態行銷網站，採 **群眾募資（群募）框架**上市：募資儀表板 + 早鳥倒數 + 限量批次飢餓條 + Stretch Goals。結帳走 **Paddle.js Overlay Checkout**（購買在本站做）。賣 Soma 桌面 App。
> 決策（2026-06-26）：站型確定走「群募框架」而非單純直購；招牌賣點「雙桌寵對話」做成專屬區塊。

## 產品一句話
**Soma — Agent in the Shell.** Bring your own AI; Soma gives it a face, a voice, and a memory.
（玩《Ghost in the Shell》梗：你的 AI＝ghost、Soma＝軀殼。Soma＝希臘文「身體」。）

## 網站區塊（已實作於 index.html）
Nav → Hero（Soma / Agent in the Shell + 主視覺 + 募資進度）→ Pain→Solution → 功能（6 卡）→ **⭐ 雙角色對話（招牌專屬區，podcast/三方切換）** → 角色切換器（多角色人設+記憶）→ Demo（9:16 佔位）→ 技術協力 Powered by → 定價/群募（募資儀表板 + 限量買斷 + 早鳥訂閱 + Stretch Goals）→ FAQ → Footer CTA → Footer。
成功頁：`success.html`（序號將寄到信箱）。

## 做法
- 使用者會貼一份 design 當基底 → 存成 `index.html`、改名 Soma、套標語、對齊 `docs/`。
- 購買：**Paddle.js Overlay Checkout**（先接 sandbox price ID，live 之後換）。各方案：月費基礎/進階、買斷基礎/進階、加購點數、外觀商店。
- 成功頁：說明「序號將寄到信箱，到 Soma App 貼上啟用」。
- i18n：5 語言（繁中/簡中/英/日/韓），每語言獨立 HTML/URL 利 SEO；內容定稿後再翻。英文為主（CJK+英市場中性）。

## 部署
**Cloudflare 子網域**（如 `soma.waterman-sports.com`）或 Soma 專屬網域——固網 HiNet 擋 `github.io`（見全域 memory `feedback_hinet_github_io_block`）。

## 設計紀律（沿用全域 feedback）
- 不要深底配灰字/淡字（`feedback_no_dark_bg_dim_text`）。
- 按鈕 disabled 要講原因。文案 5 語言可擴展。

## 相關檔案（本機可讀，未 commit 進本公開 repo）
- 完整商業化計畫：`~/.claude/plans/cached-hugging-mitten.md`
- App 主 repo（私有）：`~/Developer/live2d-desktop-agent/`（功能細節、`docs/pricing-plan.md` 內部版含成本、`LICENSING_BACKEND_SPEC.md`）
- 授權後端（私有，之後建）：`~/Developer/soma-license/`
- 品牌/文案來源：`docs/brand.md`；公開定價：`docs/pricing.md`

## 金流串接（本站只負責「開 checkout」）
購買 → Paddle.js Overlay → 付款完成 → Paddle webhook 打到 `soma-license` 後端發序號 → email 客戶 → 客戶到 App 啟用。本站不碰序號/驗證，只放 Paddle 按鈕 + 成功頁說明。
