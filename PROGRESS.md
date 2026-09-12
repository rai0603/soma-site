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

- **Stretch Goals（2026-07-03 三修定案）**：舊目標「韓語聲線／一鍵語音輸入」App 端已完成故下架；「主題皮膚」吸引力低已砍；角色與功能**合併成單一金額階梯**（Rai 指示，不分兩區）。現行 `.goal-ladder` 垂直階梯 8 階：200k✓ 基本 → 300k UNIT-04 機甲型 → 450k 外觀商店 → 650k UNIT-05 ??? → 800k 雙桌寵直播 → 1,000k UNIT-06 ??? → 1.3M Windows 提前啟動 → 2M 語音克隆・會議聽寫。角色列帶「?」機密縮圖（`data-unit-img` 預留概念圖位）＋琥珀空心節點；**UNIT-04 已公開＝機甲型 STRIKER-E2**（Rai 提供概念規格圖，縮圖+點擊看完整圖在 `assets/concepts/`），**UNIT-05 已公開＝浮游型 SENTINEL**（hover bot 場景圖），UNIT-06 仍為 ? teaser；已達成列＝實心青節點＋✓。文案紀律：大工程寫「啟動開發」不承諾時程；角色造型命名「與支持者社群共創」。五語已同步。
- ⚠️ **fal 餘額已耗盡**（ai-video-platform 的 FAL_KEY，2026-07-03 確認）：VRM 角色概念示意圖（機甲型等 3 款，flux/dev 生圖腳本已寫好在 scratchpad gen.py 邏輯）待 Rai 儲值後生成，換進 `data-unit-img` 卡位。

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

## Last session（2026-09-13 — 切到 0.5.4）

0.5.4 修的是 0.5.3 自己造成的破口：角色載入失敗時，錯誤訊息會被啟動進度顯示蓋成
「準備中… (6/6)」，使用者看到「還在準備」而不是失敗原因。根因與修法在
live2d-desktop-agent repo，這邊只做上線。

- Release v0.5.4：SHA256 `57db5b70…ba456`、273,819,708 bytes，公證 Accepted、Gatekeeper 通過
- 五語首頁（連結／版本／SHA256）、五語 success 頁、version.json 全部切換並線上驗證

## Last session（2026-09-12 — 0.5.3 上線 + 下載區明確標示系統需求）

起因：客戶（MacBook 2015 / macOS 11、Safari 16.6.1）回報 app 開啟後永遠停在「準備中…」。
根因與修復在 live2d-desktop-agent repo，這邊做的是上線與說明。

- **Release v0.5.3**（`rai0603/soma-site`）：dmg 261MB／273,820,248 bytes，
  SHA256 `497eb0fa…bd1092`，公證 Accepted、staple OK、Gatekeeper accepted
- **五語首頁**：下載區規格表最上面新增「系統需求」列（排在版本號之前——那是決定要不要
  下載之前就該看到的事）；FAQ「支援哪些作業系統」補上為什麼跟 Safari 有關、怎麼查版本、
  太舊請自行升級（直說 2015 年前後或更早的機種可能升不上去）
- 五語 success 頁下載連結、version.json latest → 0.5.3

### 這次踩到的
- **規格表的 `word-break:break-all` 會把英文單字硬切**（它本來是為了 SHA256 能斷行）：
  英文版需求字串被切成「Safari 15 or lat/er」。長句子那列要改用 `overflow-wrap:break-word`
- **CF Pages 的線上路徑沒有 `.html`**：驗證要打 `/success`、`/ja/success`，
  打 `/success.html` 拿到空白不代表沒部署成功
- 驗證五語頁面時 `data-reveal` 進場動畫會讓截圖一片空白，
  截圖前要先 `document.querySelectorAll('[data-reveal]').forEach(el=>el.classList.add('in'))`

### 順手發現（未處理）
- 右下角「線上客服」的按鈕文字在 en/ja/ko 頁面仍是繁體中文「線上客服」，沒有跟著語言切換

## Last session（2026-09-09 — 儀表板假 0、流量追蹤、0.5.1／0.5.2 上線）

- **儀表板顯示假的 0 已修。** 成因三層：`liveStats` 只在載入時抓一次（長時間開著的分頁永遠停在舊數字）、`.catch(() => {})` 靜默吞掉失敗、靜態 fallback 寫「剩 0 份」讀起來像售完。改成沒資料顯示 `--`、失敗重試三次、localStorage 墊上次成功值、`visibilitychange` 回前景重抓。五語同步。
- **流量追蹤接上 AICMS**（`assets/track.js`，15 頁共用）。先前完全沒裝任何 beacon，所以後台是空的。除 pageview 外送 `download_click`（漏斗最關鍵那格）與 `pageleave`。端點指向 `waterman-sports.cc/api/track`（AICMS public-site 本體；`ai-cms.cc` 是另一個服務，回 405）。
- **`build-help.mjs` 產生器同步**加了追蹤器與雙 Meta Pixel，重建 help 頁不會掉。
- **0.5.1 / 0.5.2 兩次發版**：下載連結、下載面板的版本標示與 **SHA256**、`version.json` 四處都要同步——SHA256 沒換的話，照官網比對雜湊的人會得到 mismatch，看起來像檔案被動過手腳。

### ⚠️ 下一步要知道的
- AICMS 那側的 `is_internal` 要維持 `true`，否則事件會被靜默丟棄。後台分析頁看的時候要開「含外站」。
- Cloudflare Web Analytics 仍未安裝；AICMS 追蹤已在收（9/9 收到 128 筆），可能不需要了。

## Last session（2026-08-14 — 發售鏈路補完）

- **新增頁面**：`help.html` ×5 語（由 app repo `scripts/build-help.mjs` 產生，與 app 內說明面板共用同一份 content.json + i18n）、`account/index.html` ×5 語、`recover.html` ×5 語（由本 repo `scripts/build-portal.mjs` 產生）、`version.json` + `_headers`、`assets/quickstart-{zh-TW,en}.pdf`。
- **定價區改為首發批次敘事**：未填 price id 的方案自動停用並寫明原因（單一真相＝`SOMA.paddle.prices`，之後填了就自動恢復可買）；儀表板主視覺由金額改成份數；假倒數（`Date.now()+18天`）關掉，`countdownDays: null` 時整塊隱藏。
- **五語 nav 加教學入口、footer 加我的帳號／找回序號**；success.html 加教學指路。
- **法務頁**補日／韓／簡中收合摘要，並載明英文為 governing version。
- ⚠️ **這個 repo 現在有兩支產生器**：`scripts/build-portal.mjs`（本 repo）與 app repo 的 `scripts/build-help.mjs`（輸出到這裡）。改文案要回對應的來源改，不要直接編產出的 HTML。

### 這輪踩到的（會再踩）
- **Cloudflare Pages 對不存在的路徑回首頁 HTML**，HTTP 200 不代表頁面存在。驗證一律比對 `<title>`（與首頁不同才算數），JSON 比對 content-type。
- **CF Pages 會裁掉 `.html`**：`/help.html` → 308 → `/help`。canonical / hreflang 用裁掉後的形式，站內相對連結留 `.html` 沒問題。
- `_headers` 對 `/version.json` 放行 CORS `*`，桌面 app 才讀得到版本公告。

## Last session（續跑指標）
- 做了什麼（2026-07-03）：盤點 App repo 功能完成度 → 發現舊 Stretch Goals 兩項已出貨 → 重排六階新目標（見 General rules）→ 五語檔 Python 一次替換 + DOM 驗證（7 tiles、4+3 排版、無溢出）→ commit+push。
- 前一日（2026-07-02）：① logo 三輪提案 → 攻殻融合定案（`docs/logo-gits-fusion.html`），配色五套提案（`docs/palette-concepts.html`）→ **Rai 拍板 P-3 白域科技**。② `index.html` + `success.html` 全站換皮 P-3 × GITS（原內容 100% 保留，新增 CUSTOMIZE_ 四支柱 index 區 + 各卡 pillar 代號），③ 4 個 subagent 平行產出 en/cn/ja/ko 完整獨立 HTML（i18n 策略＝每語言獨立檔，無 build step），④ DOM 驗證五語全綠。
- 在地化備註：Demo 例句「播周杰倫」ja 版改「YOASOBI をかけて」、ko 版改「아이유(IU) 틀어 줘」；ja/ko 定價區各加一句「價格為台灣元」註記。若 Demo 影片實拍是周杰倫要改回。
- 下一步：填 Paddle sandbox token + 5 price ID 跑真實 Overlay；Demo 影片；正式 logo 資產（文字轉外框 SVG + favicon 全尺寸，字標=G-3 SOMA_）；未來文案改動需同步五個檔（改繁中後可再叫 subagent 重翻）。
- 舊提案頁：`docs/logo-concepts.html`（粉彩，棄）、`docs/logo-concepts-cd3.html`（glyph，棄）、`docs/logo-wordmark.html`（初版）、`docs/brand-hero-mock.html`（hero mock，已落地）。
- 本地預覽：`python3 -m http.server 8753` → http://localhost:8753/index.html（+ /en/ /cn/ /ja/ /ko/）
