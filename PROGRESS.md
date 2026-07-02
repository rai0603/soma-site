# PROGRESS — Soma 行銷站（soma-site）

## Verified facts（已驗證事實）
- **（2026-07-02）全站已換皮 P-3 白域科技 × 攻殻融合風，且五語版全數上線 repo**：`index.html`（繁中）+ `en/` `cn/` `ja/` `ko/` 各含 index.html + success.html。DOM 驗證（繁中活頁全項 + 日文版活頁抽查 + 四語 DOMParser 結構比對）：12 sections / 5 SKU / 6 FAQ / 4 pillars / 6 features / 3 chars / hreflang 6 條 / 語言切換器 on 標記正確 / asset 相對路徑正確 / paddleLocale 分語言 / successUrl 分語言。
- 背景分頁的 CSS transition 不會推進 → `getComputedStyle` 量 max-height/opacity 會卡在起始值（與截圖搶拍同族）。驗證要嘛把 transition 設 none 量終值，要嘛聚焦分頁。
- `index.html` 全站重建完成，本地 server 驗證通過（`python3 -m http.server 8753`）。
- 以 DOM 量測驗證（非靠截圖）：
  - 定價三卡完整渲染（424–441px、opacity:1、子元素齊全），無壓扁、無裁切。
  - 角色切換：點頭像 → 主圖/姓名/描述/選中外框正確切換並可切回。
  - 雙角色對話：模式 pill 切換更新說明文字 + `aria-pressed`；舞台每 2.6s 輪流高亮發言。
  - 結帳按鈕：Paddle token 未設定時正確 fallback 顯示 toast「結帳即將開放」，不報錯。
  - FAQ：6 題單開手風琴，`maxHeight` 取 `scrollHeight` 無裁切；切題互斥收合正常。
  - 募資/批次數字目前皆誠實 0（raised=0, pct=0, batch left=100）。
- ⚠️ 截圖工具在「捲動後立即擷取」會搶在合成器重繪前 → 出現假空白；DOM 才是權威。viewport 實高 676px（screenshot 1512×785 是 DPR 縮放）。

## General rules（通則，先查這裡）
- **正式產品名＝「Soma Agent」**（2026-06-28 定案；slogan 仍「Agent in the Shell」，兩者不相鄰擺放避免 Agent 重複）。全站身份字樣（nav/title/og/footer/hero eyebrow/Demo 標題）用 Soma Agent。
- **平台發行三階段**：① 首波 macOS（Intel x64 + Apple Silicon M 系列）→ ② Mac App Store 上架 → ③ Windows / Linux。已做成「平台藍圖」專區（#platform，技術協力與定價之間）+ FAQ + Hero 系統需求小字。
- 站型＝**群募框架**（非單純直購），招牌賣點＝**雙角色對話**做成專屬區塊（決策 2026-06-26）。
- 公開 repo：禁 commit secrets / Paddle live key / 內部成本毛利數字。
- ~~設計 token 沿用 Lumi design：薄荷 `#16E0D0` / 深夜藍 `#211A33` / 奶油白 `#FFF7EF`，字體 Zen Maru Gothic + Noto Sans TC + Baloo 2。~~ **（2026-07-02 起被攻殻融合風取代，見下條；index.html 仍是舊風格待改版）**
- **品牌視覺定案（2026-07-02）＝「攻殻官網 × CD-3」融合風**：近黑底 `#0a0a0c`、白字大字距、磷光青 `#7cf5d8` 與琥珀 `#e6b357` 只當針點色（一個字母/一個游標的面積）、日英混排小標、切角框＋DotGothic16 角落記號。字標三件套：G-1 切殻大字（Six Caps + 橫切 mask，hero 專用）／G-2 一覧體（Michroma，正式標準字）／G-3 **「SOMA_」工作 logo**（Orbitron 拉字距＋青游標，nav/favicon/頭像）。**純文字字標，不用圖形 glyph**（Rai 明確否決雙波紋 S）。提案頁：`docs/logo-gits-fusion.html`、mock：`docs/brand-hero-mock.html`。
- **品牌主軸定案（2026-07-02）**：「打造個人專屬 AI 桌面助理——完全客製化」，四支柱映射攻殻詞彙：**外觀=SHELL／大腦(LLM)=GHOST／語音=VOICE／功能=MODULE**（BYOK 敘事：你的 AI=ghost、Soma=殼）。
- 深底區次要文字用 `--on-dark-muted (#C4BFD6)` 提亮，避免「深底配淡字」。
- 設定全集中在 `index.html` 底部 `SOMA` 物件（paddle token/prices + campaign 數字）。
- 設計原始稿在 `docs/_design_src/`（已 gitignore，本機參考用，含 Lumi 原型唯一規格來源）。

## Open failures（待調查/待辦）
- [ ] Paddle：填 client token + 5 個 price ID（buyout_basic/pro、founder、sub_basic_year、sub_pro_year），先 sandbox 驗證 Overlay + successUrl→success.html。
- [ ] 募資數字接後端 API / CMS（goal/raised/backers/batch/countdown），**上線前切勿用假數字**。
- [ ] Demo 9:16 影片（目前佔位，點擊顯示 toast）。
- [ ] 新 Soma logo（現為 gradient 方塊 + "S" 暫代；舊 Lumi「ル」已棄用）。
- [ ] 各家官方品牌 logo（Claude/ChatGPT/Gemini/Azure/Live2D/VRoid 現為自繪近似 SVG）。
- [ ] 角色圖為開發測試示範（サクラ/ユメ/レイ），正式版替換。
- [ ] i18n 5 語言（繁中已成，簡中/英/日/韓待翻；計畫每語言獨立 HTML/URL 利 SEO）。
- [ ] footer 聯絡信箱 `hello@soma.app` 為佔位，待換正式。
- [ ] 部署 Cloudflare 子網域（如 soma.waterman-sports.com）。
- [ ] 行動版導覽：≤980px 隱藏錨點連結只留 CTA，尚未做漢堡選單。

## Lessons learned（教訓）
- 視覺驗證用 DOM 量測（getBoundingClientRect/computedStyle/手動觸發 handler）比「捲動後截圖」可靠——本環境截圖會搶在重繪前。
- dc.html 設計稿含設計工具 runtime（support.js / x-dc / sc-if / {{ }}），handoff 明示不可移植，須當規格來源純手重建。

## Last session（續跑指標）
- 做了什麼（2026-07-02）：① logo 三輪提案 → 攻殻融合定案（`docs/logo-gits-fusion.html`），配色五套提案（`docs/palette-concepts.html`）→ **Rai 拍板 P-3 白域科技**。② `index.html` + `success.html` 全站換皮 P-3 × GITS（原內容 100% 保留，新增 CUSTOMIZE_ 四支柱 index 區 + 各卡 pillar 代號），③ 4 個 subagent 平行產出 en/cn/ja/ko 完整獨立 HTML（i18n 策略＝每語言獨立檔，無 build step），④ DOM 驗證五語全綠。
- 在地化備註：Demo 例句「播周杰倫」ja 版改「YOASOBI をかけて」、ko 版改「아이유(IU) 틀어 줘」；ja/ko 定價區各加一句「價格為台灣元」註記。若 Demo 影片實拍是周杰倫要改回。
- 下一步：填 Paddle sandbox token + 5 price ID 跑真實 Overlay；Demo 影片；正式 logo 資產（文字轉外框 SVG + favicon 全尺寸，字標=G-3 SOMA_）；未來文案改動需同步五個檔（改繁中後可再叫 subagent 重翻）。
- 舊提案頁：`docs/logo-concepts.html`（粉彩，棄）、`docs/logo-concepts-cd3.html`（glyph，棄）、`docs/logo-wordmark.html`（初版）、`docs/brand-hero-mock.html`（hero mock，已落地）。
- 本地預覽：`python3 -m http.server 8753` → http://localhost:8753/index.html（+ /en/ /cn/ /ja/ /ko/）
