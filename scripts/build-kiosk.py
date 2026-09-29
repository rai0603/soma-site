#!/usr/bin/env python3
"""/kiosk（SOMA AI 導覽機台介紹頁）五語產生器。改文案改這裡，不要直接編產出的 HTML：

    python3 scripts/build-kiosk.py

產出：kiosk.html（繁中）、cn/ en/ ja/ ko/ 各一份 kiosk.html。
樣式在 scripts/kiosk/style.css，圖片在 assets/kiosk/。
頁面不含任何價格——報價由業務現場提供。
"""

import html
import pathlib
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://soma-agent.com"
CSS = (ROOT / "scripts/kiosk/style.css").read_text()
EMAIL = "support@soma-agent.com"

# 語言順序＝切換列順序。dir 是網址子目錄（繁中在根目錄）。
LANGS = [
    ("zh-Hant", "", "繁"),
    ("zh-Hans", "cn", "简"),
    ("en", "en", "EN"),
    ("ja", "ja", "日"),
    ("ko", "ko", "한"),
]

FONTS = {
    "zh-Hant": ("Noto+Sans+TC", '"Noto Sans TC", "PingFang TC", "Heiti TC", "Microsoft JhengHei", sans-serif'),
    "zh-Hans": ("Noto+Sans+SC", '"Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif'),
    "en": ("Noto+Sans", '"Noto Sans", "Helvetica Neue", Arial, sans-serif'),
    "ja": ("Noto+Sans+JP", '"Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif'),
    "ko": ("Noto+Sans+KR", '"Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif'),
}

# 特色的線條圖示（五語共用）
ICONS = [
    '<path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h6"/>',
    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    '<circle cx="12" cy="7" r="3.5"/><path d="M5 21c1-5 3.5-7 7-7s6 2 7 7"/>',
    '<rect x="2" y="4" width="14" height="10" rx="1"/><rect x="16" y="10" width="6" height="10" rx="1"/><path d="M7 18h4"/>',
    '<path d="M4 20h16"/><path d="M14 4l6 6-9 9H5v-6z"/>',
    '<path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/>',
]

T = {
    # ───────────────────────── 繁體中文 ─────────────────────────
    "zh-Hant": {
        "title": "SOMA AI 導覽機台：永不休息的實體 AI 客服員工",
        "desc": "讀過你官網的 AI 接待員，用 iPad＋大電視站在門口，以中英日韓四種語言回答客人，全年無休。適合飯店民宿、百貨商場、觀光景點、體驗場館與門市。",
        "og_locale": "zh_TW",
        "nav_home": "Soma 桌面 AI 夥伴",
        "brand_sub": "AI 導覽機台",
        "hero_h1": "一位<em>永不休息</em>的<br>實體 AI 客服員工",
        "hero_lead": "她讀過你官網上的每一頁：課程、價格、營業時間、交通方式。從開門到打烊，她站在門口，用中英日韓四種語言回答每一位客人。不排班、不請假，也不會累。",
        "facts": ["<b>全年</b>無休", "<b>4</b>種語言：中英日韓", "<b>8</b>位角色可選", "<b>10</b>個工作天上線"],
        "hero_alt": "SOMA 導覽畫面：大電視上的 3D 角色與回答，旁邊是訪客操作的畫面",
        "hero_cap": "實際介面：訪客在操作畫面提問，大電視同步顯示角色與回答",
        "emp_eyebrow": "一位永不休息的員工",
        "emp_h2": "櫃台最常被問的那 20 題，交給她",
        "emp_left": "只有真人櫃台",
        "emp_right": "加上 SOMA AI 員工",
        "emp_rows": [
            ("要排班、輪休，假日尖峰人手永遠不夠", "開門到打烊都在，全年無休"),
            ("同樣的問題一天回答幾十次，耐心會被磨掉", "第 1,000 次回答，一樣清楚、一樣親切"),
            ("外國旅客來了，要看當班的人會不會說", "中英日韓，點一下就換成客人的語言"),
            ("新人要花時間教，離職就把經驗帶走", "後台改一次就學會，知識永遠留在店裡"),
            ("路過的人很難停下腳步", "大電視上會說話、會動的角色，本身就是招牌"),
        ],
        "emp_note": "她不是來取代你的員工，而是接手重複的問答，讓員工把時間留給收款、服務，和真正需要人的時刻。",
        "feat_eyebrow": "特色",
        "feat_h2": "不是網頁上的聊天框，是站在現場的接待員",
        "features": [
            ("只用你的資料回答", "知識庫由你的官網內容建立，價格、時間、地址都照原文回答；遇到答不出來的問題，會請客人洽詢工作人員，不會自己亂編。"),
            ("中英日韓四種語言", "外國旅客點一下語言鈕，她就用對方的語言回答，並以自然的聲音唸出來。"),
            ("會說話、會動的 3D 角色", "說話時嘴型同步，表情跟著對話變化，還會揮手、鞠躬。8 位角色可選，也能依品牌形象打造專屬角色。"),
            ("iPad＋大電視雙畫面", "客人在 iPad 上開口或打字，大電視同步播出角色與回答，排隊和路過的人也看得到。"),
            ("後台自己就能改", "價格或活動異動，在後台改一下，下一位客人問到的就是新答案。每月附上數據報表與「答不出來的問題」清單。"),
            ("硬體可租可買，壞了我們換", "使用一般的 iPad 與電視，不必添購昂貴的專用機櫃；選擇租賃，自然故障由我們負責更換。"),
        ],
        "fit_eyebrow": "誰適合",
        "fit_h2": "有人潮、常被問同樣問題的地方，都用得上",
        "fit_lead": "符合其中兩項，就很適合：每天被問同樣的問題、常有外國客人、門口有路過的人潮、假日或尖峰人手不足。",
        "biz_h3": "適合的商家",
        "biz": [
            ("體驗活動與運動場館", "水上活動、攀岩、健身房、才藝與運動教室"),
            ("飯店、民宿、溫泉會館", "大廳接待、設施說明、周邊景點推薦"),
            ("百貨、商場、購物中心", "樓層導覽、品牌推薦、檔期活動"),
            ("觀光景點、遊樂園、博物館、展覽", "園區導覽、展品介紹、動線指引"),
            ("門市與連鎖店", "商品介紹、優惠說明、會員活動"),
            ("診所、補習班與各式服務櫃台", "報名、預約流程與常見問題"),
            ("遊客中心、車站與公共服務據點", "交通、路線與辦理流程"),
        ],
        "info_h3": "她能回答的資訊",
        "info": ["營業時間、公休日與預約方式", "價格、方案與優惠活動", "樓層、位置、動線與設施", "交通、停車與周邊景點", "課程、商品與服務內容", "活動檔期與最新消息", "報名、集合時間與注意事項", "退改規則與常見問題", "品牌故事與特色介紹", "需要真人時，引導到櫃台或 LINE"],
        "fit_note": "只要寫得下來的資訊，都能成為她的回答。我們會從官網自動整理，再幫你補齊官網上沒寫的部分。",
        "scene_eyebrow": "應用場景",
        "scene_h2": "放在人潮經過的地方，讓客人自己開口問",
        "scenes": [
            ("飯店、民宿大廳", "設施介紹、周邊景點、多語言接待", "民宿大廳的 iPad 操作台與直立式電視，旅客一家人在詢問"),
            ("樂園、景點", "設施介紹、活動推薦、多語言導覽", "樂園入口的 AI 導覽機台，遊客在觸控螢幕上詢問"),
            ("百貨、商場", "樓層導覽、品牌推薦、活動資訊", "百貨公司中庭的直立式 AI 導覽螢幕"),
        ],
        "scene_note": "情境示意圖。實際設備、角色與畫面依方案與場館設定而定；圖中的手機掃碼導覽、排隊資訊與實體公仔屬於延伸構想，不含在標準方案內。",
        "flow_eyebrow": "導入流程",
        "flow_h2": "簽約後 10 個工作天，就能開始接待客人",
        "steps": [
            ("第 1–4 個工作天", "建立知識庫", "從你的官網整理出 50–100 條問答，再補上櫃台最常被問的問題。"),
            ("第 2–5 個工作天", "角色與畫面", "挑選角色，換上你的品牌色與背景，設定四種語言的聲音。"),
            ("第 5–8 個工作天", "內部試用", "由你的員工試問 50 題，我們修正到常見問題的正確率達 90% 以上。"),
            ("第 8–10 個工作天", "安裝上線", "到場安裝、接上電視，進行 30 分鐘教育訓練，驗收後正式上線。"),
        ],
        "plan_eyebrow": "方案",
        "plan_h2": "硬體看擺放位置，軟體看客人多寡",
        "plan_lead": "兩者分開選，依你的場地與人流自由搭配；同一個場館的多台機台，共用一個軟體方案。",
        "hw_h3": "硬體：四種規格，可租可買",
        "hw": [("iPad 單機", "櫃台、小店面"), ("iPad＋43 吋電視", "櫃台旁、小型場館"), ("iPad＋55 吋電視", "場館大廳、主要出入口"), ("iPad＋65 吋電視", "百貨中庭、景點、展場")],
        "sw_h3": "軟體：依每月互動次數，五種方案",
        "sw": [("輕量、入門", "每天幾十位客人詢問"), ("標準", "每天一百多位"), ("進階、旗艦", "每天數百位，或多台機台共用"), ("", "先從低一級開始，上線後看實際數據再調整")],
        "plan_note": "依你的場地、人流與台數提供專屬報價；展覽、快閃活動另有短期租用方案。",
        "prep_eyebrow": "你只需要準備",
        "prep_h2": "四樣東西，不需要 IT 人員",
        "prep": ["官網網址，以及櫃台最常被問的問題", "最新的價目表與活動資訊", "Logo、品牌色，和一張場館照片", "擺放位置、一個插座與 Wi-Fi"],
        "contact_h3": "用你自己的官網，現場展示給你看",
        "contact_p": "我們會先讀過你的官網，帶著 iPad 到現場，讓她直接回答你的客人最常問的問題，並依你的場地提供報價。展示免費，約 15 分鐘。",
        "book": "來信預約展示",
        "mail_note": "請附上店名、官網網址與方便的時段",
        "mail_subject": "預約 SOMA AI 導覽機台展示",
        "legal": "法律資訊",
        "widget": "線上客服",
        # 首頁入口
        "entry_nav": "導覽機台",
        "entry_h2": "把 Soma 放進你的店裡：<br>永不休息的實體 AI 客服員工",
        "entry_p": "SOMA AI 導覽機台讀過你的官網，用 iPad＋大電視站在門口，以中英日韓四種語言回答每一位客人。適合飯店民宿、百貨商場、觀光景點、體驗場館與門市。",
        "entry_btn": "看導覽機台方案 →",
        "entry_alt": "SOMA 導覽機台：大電視上的 3D 角色與回答",
    },
    # ───────────────────────── 简体中文 ─────────────────────────
    "zh-Hans": {
        "title": "SOMA AI 导览机台：永不休息的实体 AI 客服员工",
        "desc": "读过你官网的 AI 接待员，用 iPad＋大屏幕站在门口，以中英日韩四种语言回答客人，全年无休。适合酒店民宿、商场百货、旅游景点、体验场馆与门店。",
        "og_locale": "zh_CN",
        "nav_home": "Soma 桌面 AI 伙伴",
        "brand_sub": "AI 导览机台",
        "hero_h1": "一位<em>永不休息</em>的<br>实体 AI 客服员工",
        "hero_lead": "她读过你官网上的每一页：课程、价格、营业时间、交通方式。从开门到打烊，她站在门口，用中英日韩四种语言回答每一位客人。不排班、不请假，也不会累。",
        "facts": ["<b>全年</b>无休", "<b>4</b>种语言：中英日韩", "<b>8</b>位角色可选", "<b>10</b>个工作日上线"],
        "hero_alt": "SOMA 导览画面：大屏幕上的 3D 角色与回答，旁边是访客操作的画面",
        "hero_cap": "实际界面：访客在操作画面提问，大屏幕同步显示角色与回答",
        "emp_eyebrow": "一位永不休息的员工",
        "emp_h2": "前台最常被问的那 20 个问题，交给她",
        "emp_left": "只有真人前台",
        "emp_right": "加上 SOMA AI 员工",
        "emp_rows": [
            ("要排班、轮休，节假日高峰永远缺人手", "开门到打烊都在，全年无休"),
            ("同样的问题一天回答几十次，耐心会被磨光", "第 1,000 次回答，一样清楚、一样亲切"),
            ("外国游客来了，要看当班的人会不会说", "中英日韩，点一下就换成客人的语言"),
            ("新人要花时间培训，离职就把经验带走", "后台改一次就学会，知识永远留在店里"),
            ("路过的人很难停下脚步", "大屏幕上会说话、会动的角色，本身就是招牌"),
        ],
        "emp_note": "她不是来取代你的员工，而是接手重复的问答，让员工把时间留给收款、服务，和真正需要人的时刻。",
        "feat_eyebrow": "特色",
        "feat_h2": "不是网页上的聊天框，是站在现场的接待员",
        "features": [
            ("只用你的资料回答", "知识库由你的官网内容建立，价格、时间、地址都照原文回答；遇到答不上来的问题，会请客人咨询工作人员，不会自己乱编。"),
            ("中英日韩四种语言", "外国游客点一下语言按钮，她就用对方的语言回答，并以自然的声音读出来。"),
            ("会说话、会动的 3D 角色", "说话时口型同步，表情随对话变化，还会挥手、鞠躬。8 位角色可选，也能按品牌形象打造专属角色。"),
            ("iPad＋大屏幕双画面", "客人在 iPad 上开口或打字，大屏幕同步播出角色与回答，排队和路过的人也看得到。"),
            ("后台自己就能改", "价格或活动有变，在后台改一下，下一位客人问到的就是新答案。每月附上数据报表与“答不上来的问题”清单。"),
            ("硬件可租可买，坏了我们换", "使用普通的 iPad 与电视，不必添购昂贵的专用机柜；选择租赁，自然故障由我们负责更换。"),
        ],
        "fit_eyebrow": "谁适合",
        "fit_h2": "有人流、常被问同样问题的地方，都用得上",
        "fit_lead": "符合其中两项，就很适合：每天被问同样的问题、常有外国客人、门口有路过的人流、节假日或高峰缺人手。",
        "biz_h3": "适合的商家",
        "biz": [
            ("体验活动与运动场馆", "水上活动、攀岩、健身房、兴趣与运动教室"),
            ("酒店、民宿、温泉会馆", "大堂接待、设施说明、周边景点推荐"),
            ("百货、商场、购物中心", "楼层导览、品牌推荐、档期活动"),
            ("旅游景点、游乐园、博物馆、展览", "园区导览、展品介绍、动线指引"),
            ("门店与连锁店", "商品介绍、优惠说明、会员活动"),
            ("诊所、培训机构与各类服务前台", "报名、预约流程与常见问题"),
            ("游客中心、车站与公共服务网点", "交通、路线与办理流程"),
        ],
        "info_h3": "她能回答的信息",
        "info": ["营业时间、休息日与预约方式", "价格、套餐与优惠活动", "楼层、位置、动线与设施", "交通、停车与周边景点", "课程、商品与服务内容", "活动档期与最新消息", "报名、集合时间与注意事项", "退改规则与常见问题", "品牌故事与特色介绍", "需要真人时，引导到前台或客服"],
        "fit_note": "只要写得下来的信息，都能成为她的回答。我们会从官网自动整理，再帮你补齐官网上没写的部分。",
        "scene_eyebrow": "应用场景",
        "scene_h2": "放在人流经过的地方，让客人自己开口问",
        "scenes": [
            ("酒店、民宿大堂", "设施介绍、周边景点、多语言接待", "民宿大堂的 iPad 操作台与立式屏幕，一家游客在咨询"),
            ("乐园、景点", "设施介绍、活动推荐、多语言导览", "乐园入口的 AI 导览机台，游客在触摸屏上咨询"),
            ("百货、商场", "楼层导览、品牌推荐、活动信息", "商场中庭的立式 AI 导览屏幕"),
        ],
        "scene_note": "场景示意图。实际设备、角色与画面依方案与场馆设置而定；图中的手机扫码导览、排队信息与实体手办属于延伸构想，不含在标准方案内。",
        "flow_eyebrow": "导入流程",
        "flow_h2": "签约后 10 个工作日，就能开始接待客人",
        "steps": [
            ("第 1–4 个工作日", "建立知识库", "从你的官网整理出 50–100 条问答，再补上前台最常被问的问题。"),
            ("第 2–5 个工作日", "角色与画面", "挑选角色，换上你的品牌色与背景，设置四种语言的声音。"),
            ("第 5–8 个工作日", "内部试用", "由你的员工试问 50 个问题，我们修正到常见问题的正确率达 90% 以上。"),
            ("第 8–10 个工作日", "安装上线", "到场安装、接上屏幕，进行 30 分钟培训，验收后正式上线。"),
        ],
        "plan_eyebrow": "方案",
        "plan_h2": "硬件看摆放位置，软件看客人多少",
        "plan_lead": "两者分开选，按你的场地与人流自由搭配；同一个场馆的多台机台，共用一个软件方案。",
        "hw_h3": "硬件：四种规格，可租可买",
        "hw": [("iPad 单机", "前台、小店面"), ("iPad＋43 英寸屏幕", "前台旁、小型场馆"), ("iPad＋55 英寸屏幕", "场馆大堂、主要出入口"), ("iPad＋65 英寸屏幕", "商场中庭、景点、展场")],
        "sw_h3": "软件：按每月互动次数，五种方案",
        "sw": [("轻量、入门", "每天几十位客人咨询"), ("标准", "每天一百多位"), ("进阶、旗舰", "每天数百位，或多台机台共用"), ("", "先从低一级开始，上线后看实际数据再调整")],
        "plan_note": "根据你的场地、人流与台数提供专属报价；展会、快闪活动另有短期租用方案。",
        "prep_eyebrow": "你只需要准备",
        "prep_h2": "四样东西，不需要 IT 人员",
        "prep": ["官网网址，以及前台最常被问的问题", "最新的价目表与活动信息", "Logo、品牌色，和一张场馆照片", "摆放位置、一个插座与 Wi-Fi"],
        "contact_h3": "用你自己的官网，现场演示给你看",
        "contact_p": "我们会先读过你的官网，带着 iPad 到现场，让她直接回答你的客人最常问的问题，并根据你的场地提供报价。演示免费，约 15 分钟。",
        "book": "来信预约演示",
        "mail_note": "请附上店名、官网网址与方便的时段",
        "mail_subject": "预约 SOMA AI 导览机台演示",
        "legal": "法律信息",
        "widget": "在线客服",
        "entry_nav": "导览机台",
        "entry_h2": "把 Soma 放进你的店里：<br>永不休息的实体 AI 客服员工",
        "entry_p": "SOMA AI 导览机台读过你的官网，用 iPad＋大屏幕站在门口，以中英日韩四种语言回答每一位客人。适合酒店民宿、商场百货、旅游景点、体验场馆与门店。",
        "entry_btn": "查看导览机台方案 →",
        "entry_alt": "SOMA 导览机台：大屏幕上的 3D 角色与回答",
    },
    # ───────────────────────── English ─────────────────────────
    "en": {
        "title": "SOMA AI Guide Kiosk: a customer-service employee who never takes a break",
        "desc": "An AI concierge that has read your website, standing at your entrance on an iPad and a large screen, answering guests in Chinese, English, Japanese and Korean, every day of the year. Built for hotels, malls, attractions, activity venues and retail stores.",
        "og_locale": "en_US",
        "nav_home": "Soma desktop AI companion",
        "brand_sub": "AI GUIDE KIOSK",
        "hero_h1": "An in-person AI host<br>who <em>never takes a break</em>",
        "hero_lead": "She has read every page of your website: classes, prices, opening hours, directions. From opening to closing she stands at your entrance and answers every guest in Chinese, English, Japanese or Korean. No shifts, no sick days, no fatigue.",
        "facts": ["<b>365</b>days a year", "<b>4</b>languages", "<b>8</b>characters to choose from", "Live in <b>10</b>business days"],
        "hero_alt": "SOMA guide screens: a 3D character and her answer on a large screen, next to the screen guests use",
        "hero_cap": "Actual interface: guests ask on the touch screen; the large screen shows the character and her answer",
        "emp_eyebrow": "An employee who never rests",
        "emp_h2": "Hand her the 20 questions your front desk hears every day",
        "emp_left": "Front desk staff only",
        "emp_right": "With a SOMA AI employee",
        "emp_rows": [
            ("Shifts and days off — never enough hands at weekend peaks", "There from opening to closing, every day of the year"),
            ("The same question dozens of times a day wears anyone down", "The 1,000th answer is as clear and friendly as the first"),
            ("Foreign visitors depend on who happens to be on shift", "Chinese, English, Japanese, Korean — one tap switches"),
            ("New hires take time to train, and leave with what they learned", "Update the back office once; the knowledge stays with you"),
            ("Passers-by rarely stop", "A talking, moving character on a big screen is a sign in itself"),
        ],
        "emp_note": "She isn't here to replace your staff. She takes over the repetitive questions so your team can focus on payments, service, and the moments that need a person.",
        "feat_eyebrow": "Features",
        "feat_h2": "Not a chat box on a website — a host standing in your venue",
        "features": [
            ("Answers only from your information", "Her knowledge base is built from your website, and prices, times and addresses are quoted as written. When she doesn't know, she asks guests to check with staff instead of making something up."),
            ("Four languages", "Foreign visitors tap a language button and she answers in their language, read aloud in a natural voice."),
            ("A 3D character that talks and moves", "Lip-synced speech, expressions that follow the conversation, waves and bows. Choose from 8 characters, or have one designed for your brand."),
            ("iPad plus a large screen", "Guests speak or type on the iPad; the large screen shows the character and her answer, so the queue and passers-by can see too."),
            ("Update it yourself", "Change a price or an event in the back office and the next guest hears the new answer. Every month you get a usage report and a list of questions she couldn't answer."),
            ("Rent or buy — we replace faulty units", "It runs on a regular iPad and TV, no costly custom cabinet. On a rental plan we replace any unit that fails."),
        ],
        "fit_eyebrow": "Who it's for",
        "fit_h2": "Anywhere with foot traffic and the same questions over and over",
        "fit_lead": "A good fit if two of these apply: you get the same questions every day, you see foreign visitors, people walk past your entrance, or you're short-handed at peak times.",
        "biz_h3": "Businesses",
        "biz": [
            ("Activity and sports venues", "Water sports, climbing gyms, fitness studios, classes"),
            ("Hotels, guesthouses, hot-spring resorts", "Lobby welcome, facilities, nearby attractions"),
            ("Department stores, malls, shopping centers", "Floor guides, brand picks, seasonal events"),
            ("Attractions, theme parks, museums, exhibitions", "Park guides, exhibit introductions, wayfinding"),
            ("Retail stores and chains", "Products, promotions, membership"),
            ("Clinics, schools and service counters", "Sign-ups, booking steps, common questions"),
            ("Visitor centers, stations, public service points", "Transport, routes, procedures"),
        ],
        "info_h3": "What she can answer",
        "info": ["Opening hours, closures, bookings", "Prices, plans, promotions", "Floors, locations, routes, facilities", "Transport, parking, nearby spots", "Classes, products, services", "Events and latest news", "Sign-up, meeting times, what to bring", "Cancellation rules and FAQs", "Your brand story", "Handing off to a person at the desk or on LINE"],
        "fit_note": "If it can be written down, it can become her answer. We compile it from your website automatically, then fill in what the website leaves out.",
        "scene_eyebrow": "Where it works",
        "scene_h2": "Place her where people pass, and let guests ask",
        "scenes": [
            ("Hotel and guesthouse lobbies", "Facilities, nearby attractions, multilingual welcome", "An iPad stand and a portrait screen in a guesthouse lobby, with a family asking questions"),
            ("Theme parks and attractions", "Rides, event picks, multilingual guidance", "An AI guide kiosk at a theme-park entrance, with a visitor using the touch screen"),
            ("Department stores and malls", "Floor guides, brand picks, event info", "A portrait AI guide screen in a mall atrium"),
        ],
        "scene_note": "Illustrative scenes. Actual hardware, characters and screens depend on the plan and venue setup; the phone QR guide, queue information and figurine shown are future ideas, not part of the standard plan.",
        "flow_eyebrow": "Getting started",
        "flow_h2": "Welcoming guests 10 business days after signing",
        "steps": [
            ("Business days 1–4", "Knowledge base", "We turn your website into 50–100 Q&As, then add the questions your front desk hears most."),
            ("Business days 2–5", "Character and look", "Pick a character, apply your brand colors and background, set the voice for each language."),
            ("Business days 5–8", "Internal trial", "Your staff ask 50 questions; we tune until common questions are answered correctly at least 90% of the time."),
            ("Business days 8–10", "Installation", "On-site setup, screen connection, 30 minutes of training, sign-off, and you're live."),
        ],
        "plan_eyebrow": "Plans",
        "plan_h2": "Hardware depends on the spot; software depends on the crowd",
        "plan_lead": "Choose them separately to fit your space and foot traffic. Several kiosks in one venue share a single software plan.",
        "hw_h3": "Hardware: four setups, rent or buy",
        "hw": [("iPad only", "Counters, small shops"), ("iPad + 43\" screen", "Beside the counter, small venues"), ("iPad + 55\" screen", "Lobbies, main entrances"), ("iPad + 65\" screen", "Mall atriums, attractions, exhibitions")],
        "sw_h3": "Software: five plans by monthly interactions",
        "sw": [("Lite, Starter", "A few dozen questions a day"), ("Standard", "A hundred or more a day"), ("Advanced, Flagship", "Hundreds a day, or several kiosks sharing"), ("", "Start one level lower and adjust with real data after launch")],
        "plan_note": "We quote for your space, traffic and number of kiosks. Short-term rental is available for exhibitions and pop-ups.",
        "prep_eyebrow": "What you'll need",
        "prep_h2": "Four things, no IT staff required",
        "prep": ["Your website, plus the questions your front desk hears most", "Current price list and events", "Logo, brand colors and one photo of the venue", "A spot, a power outlet and Wi-Fi"],
        "contact_h3": "See it answer from your own website",
        "contact_p": "We'll read your website first, bring an iPad to your venue, and let her answer the questions your guests ask most — then quote for your space. The demo is free and takes about 15 minutes.",
        "book": "Book a demo by email",
        "mail_note": "Please include your venue name, website and a convenient time",
        "mail_subject": "SOMA AI Guide Kiosk demo request",
        "legal": "Legal",
        "widget": "Chat with us",
        "entry_nav": "Guide Kiosk",
        "entry_h2": "Bring Soma to your venue:<br>an AI host who never takes a break",
        "entry_p": "The SOMA AI Guide Kiosk reads your website and stands at your entrance on an iPad and a large screen, answering every guest in Chinese, English, Japanese or Korean. Built for hotels, malls, attractions, activity venues and retail.",
        "entry_btn": "See the Guide Kiosk →",
        "entry_alt": "SOMA Guide Kiosk: a 3D character and her answer on a large screen",
    },
    # ───────────────────────── 日本語 ─────────────────────────
    "ja": {
        "title": "SOMA AI ガイド端末：休まない、店頭の AI 接客スタッフ",
        "desc": "あなたのウェブサイトを読み込んだ AI 接客スタッフが、iPad と大型ディスプレイで入口に立ち、中国語・英語・日本語・韓国語で年中無休でお客様に対応します。ホテル、商業施設、観光地、体験施設、店舗向け。",
        "og_locale": "ja_JP",
        "nav_home": "Soma デスクトップ AI パートナー",
        "brand_sub": "AI ガイド端末",
        "hero_h1": "<em>休むことのない</em><br>店頭の AI 接客スタッフ",
        "hero_lead": "コース、料金、営業時間、アクセス。彼女はあなたのウェブサイトを隅々まで読み込んでいます。開店から閉店まで入口に立ち、中国語・英語・日本語・韓国語でお客様一人ひとりに答えます。シフトも休暇もなく、疲れることもありません。",
        "facts": ["<b>年中</b>無休", "<b>4</b>言語対応", "<b>8</b>種類のキャラクター", "<b>10</b>営業日で導入"],
        "hero_alt": "SOMA ガイド画面：大型ディスプレイの 3D キャラクターと回答、隣にお客様が操作する画面",
        "hero_cap": "実際の画面：お客様が操作画面で質問し、大型ディスプレイにキャラクターと回答が同時に表示されます",
        "emp_eyebrow": "休まないスタッフ",
        "emp_h2": "受付で毎日聞かれる 20 の質問は、彼女に任せる",
        "emp_left": "人の受付だけ",
        "emp_right": "SOMA AI スタッフが加わると",
        "emp_rows": [
            ("シフトと休みの調整が必要で、休日のピークは常に人手不足", "開店から閉店まで、年中無休で対応"),
            ("同じ質問に一日何十回も答えると、余裕がなくなる", "1,000 回目の回答も、変わらず丁寧でわかりやすい"),
            ("外国人のお客様への対応は、その日のスタッフ次第", "中英日韓、ワンタップでお客様の言語に切り替え"),
            ("新人教育に時間がかかり、辞めるとノウハウも去る", "管理画面で一度直せば覚え、知識はお店に残る"),
            ("通りがかりの人はなかなか足を止めない", "大画面で話して動くキャラクターが、そのまま看板になる"),
        ],
        "emp_note": "彼女はスタッフの代わりではありません。繰り返しの質問を引き受け、スタッフがお会計や接客、人にしかできない場面に集中できるようにします。",
        "feat_eyebrow": "特長",
        "feat_h2": "ウェブのチャット欄ではなく、現場に立つ接客スタッフ",
        "features": [
            ("あなたの情報だけで回答", "ナレッジベースはウェブサイトの内容から作成し、料金・時間・住所は原文どおりに答えます。答えられない質問はスタッフへの確認をご案内し、勝手に作り話をしません。"),
            ("4 言語に対応", "外国人のお客様が言語ボタンを押すと、その言語で回答し、自然な音声で読み上げます。"),
            ("話して動く 3D キャラクター", "口の動きが音声に合い、会話に合わせて表情が変わり、手を振ったりお辞儀をしたりします。8 種類から選べるほか、ブランドに合わせた専用キャラクターも制作できます。"),
            ("iPad と大型ディスプレイの 2 画面", "お客様は iPad に話しかけるか入力するだけ。大型ディスプレイにキャラクターと回答が表示され、並んでいる人や通りがかりの人にも見えます。"),
            ("管理画面で自分で更新", "料金やイベントが変わったら管理画面で直すだけで、次のお客様から新しい回答になります。毎月、利用レポートと「答えられなかった質問」リストをお届けします。"),
            ("レンタルも購入も可能、故障時は交換", "一般的な iPad とテレビを使うため、高価な専用筐体は不要です。レンタルなら、自然故障の際は当社が交換します。"),
        ],
        "fit_eyebrow": "導入に向いているお店",
        "fit_h2": "人通りがあり、同じ質問が多い場所ならどこでも",
        "fit_lead": "次のうち 2 つ当てはまれば最適です：毎日同じ質問をされる、外国人のお客様が多い、入口前に人通りがある、休日やピーク時に人手が足りない。",
        "biz_h3": "向いている業種",
        "biz": [
            ("体験アクティビティ・スポーツ施設", "マリンアクティビティ、クライミング、ジム、各種教室"),
            ("ホテル・民宿・温泉旅館", "ロビーでのご案内、館内設備、周辺観光のおすすめ"),
            ("百貨店・商業施設・ショッピングモール", "フロア案内、ブランド紹介、催事情報"),
            ("観光地・テーマパーク・博物館・展示会", "園内案内、展示紹介、動線案内"),
            ("店舗・チェーン店", "商品紹介、キャンペーン、会員サービス"),
            ("クリニック・学習塾・各種受付", "申込・予約の流れとよくある質問"),
            ("観光案内所・駅・公共サービス窓口", "交通、ルート、手続き案内"),
        ],
        "info_h3": "彼女が答えられること",
        "info": ["営業時間・定休日・予約方法", "料金・プラン・キャンペーン", "フロア・場所・動線・設備", "アクセス・駐車場・周辺スポット", "コース・商品・サービス内容", "イベント日程と最新情報", "申込・集合時間・注意事項", "キャンセル規定とよくある質問", "ブランドストーリーと特長", "人が必要なときは受付や LINE へご案内"],
        "fit_note": "文章にできる情報なら、すべて彼女の回答になります。ウェブサイトから自動で整理し、サイトに載っていない情報も補います。",
        "scene_eyebrow": "活用シーン",
        "scene_h2": "人が行き交う場所に置いて、お客様に話しかけてもらう",
        "scenes": [
            ("ホテル・民宿のロビー", "館内設備、周辺観光、多言語での接客", "民宿のロビーにある iPad スタンドと縦型ディスプレイ、質問する家族連れ"),
            ("テーマパーク・観光地", "施設案内、イベント紹介、多言語ガイド", "テーマパーク入口の AI ガイド端末、タッチ画面で質問する来場者"),
            ("百貨店・商業施設", "フロア案内、ブランド紹介、イベント情報", "商業施設の吹き抜けに置かれた縦型 AI ガイド画面"),
        ],
        "scene_note": "イメージ図です。実際の機器・キャラクター・画面はプランと施設の設定によります。図中のスマートフォンでの QR ガイド、待ち時間情報、フィギュアは今後の構想であり、標準プランには含まれません。",
        "flow_eyebrow": "導入の流れ",
        "flow_h2": "ご契約から 10 営業日で、お客様をお迎えできます",
        "steps": [
            ("1〜4 営業日目", "ナレッジベース作成", "ウェブサイトから 50〜100 件の Q&A を作成し、受付でよく聞かれる質問を追加します。"),
            ("2〜5 営業日目", "キャラクターと画面", "キャラクターを選び、ブランドカラーと背景を設定し、4 言語の音声を調整します。"),
            ("5〜8 営業日目", "社内テスト", "スタッフの方に 50 問質問していただき、よくある質問の正答率が 90% 以上になるまで調整します。"),
            ("8〜10 営業日目", "設置・稼働", "現地で設置してディスプレイを接続し、30 分の操作説明を行い、検収後に稼働開始です。"),
        ],
        "plan_eyebrow": "プラン",
        "plan_h2": "ハードは置き場所で、ソフトは来客数で選ぶ",
        "plan_lead": "両者を別々に選び、場所と人の流れに合わせて組み合わせます。同じ施設の複数台は、ひとつのソフトウェアプランを共有します。",
        "hw_h3": "ハードウェア：4 つの構成、レンタルも購入も可",
        "hw": [("iPad のみ", "受付、小さな店舗"), ("iPad＋43 インチ画面", "受付横、小規模施設"), ("iPad＋55 インチ画面", "ロビー、メインエントランス"), ("iPad＋65 インチ画面", "商業施設の吹き抜け、観光地、展示会")],
        "sw_h3": "ソフトウェア：月間の対話回数で選べる 5 プラン",
        "sw": [("ライト・スターター", "1 日数十件の質問"), ("スタンダード", "1 日 100 件以上"), ("アドバンス・フラッグシップ", "1 日数百件、または複数台で共有"), ("", "まずは 1 段階下から始め、稼働後の実績を見て調整")],
        "plan_note": "場所・人の流れ・台数に合わせてお見積りします。展示会やポップアップ向けの短期レンタルもございます。",
        "prep_eyebrow": "ご用意いただくもの",
        "prep_h2": "4 つだけ、IT 担当者は不要です",
        "prep": ["ウェブサイトの URL と、受付でよく聞かれる質問", "最新の料金表とイベント情報", "ロゴ、ブランドカラー、施設の写真 1 枚", "設置場所、コンセント 1 口と Wi-Fi"],
        "contact_h3": "あなたのウェブサイトで、実際にお見せします",
        "contact_p": "事前にウェブサイトを読み込み、iPad を持って伺います。お客様からよく聞かれる質問に彼女がその場で答え、施設に合わせたお見積りもお出しします。デモは無料、約 15 分です。",
        "book": "メールでデモを予約",
        "mail_note": "店名、ウェブサイトの URL、ご都合のよい日時をお書き添えください",
        "mail_subject": "SOMA AI ガイド端末 デモのご予約",
        "legal": "法的情報",
        "widget": "チャットで相談",
        "entry_nav": "ガイド端末",
        "entry_h2": "Soma をあなたのお店に：<br>休まない店頭の AI 接客スタッフ",
        "entry_p": "SOMA AI ガイド端末はウェブサイトを読み込み、iPad と大型ディスプレイで入口に立ち、中国語・英語・日本語・韓国語でお客様一人ひとりに答えます。ホテル、商業施設、観光地、体験施設、店舗向け。",
        "entry_btn": "ガイド端末を見る →",
        "entry_alt": "SOMA ガイド端末：大型ディスプレイの 3D キャラクターと回答",
    },
    # ───────────────────────── 한국어 ─────────────────────────
    "ko": {
        "title": "SOMA AI 안내 키오스크: 쉬지 않는 오프라인 AI 고객응대 직원",
        "desc": "홈페이지를 읽은 AI 안내 직원이 iPad와 대형 화면으로 입구에 서서 중국어·영어·일본어·한국어로 연중무휴 손님을 응대합니다. 호텔, 백화점·쇼핑몰, 관광지, 체험 시설, 매장에 적합합니다.",
        "og_locale": "ko_KR",
        "nav_home": "Soma 데스크톱 AI 파트너",
        "brand_sub": "AI 안내 키오스크",
        "hero_h1": "<em>쉬지 않는</em><br>오프라인 AI 고객응대 직원",
        "hero_lead": "강좌, 가격, 영업시간, 오시는 길까지. 그녀는 홈페이지의 모든 페이지를 읽었습니다. 문을 여는 순간부터 닫을 때까지 입구에 서서 중국어·영어·일본어·한국어로 모든 손님에게 답합니다. 교대도, 휴가도, 지치는 일도 없습니다.",
        "facts": ["<b>연중</b>무휴", "<b>4</b>개 언어", "캐릭터 <b>8</b>종", "영업일 <b>10</b>일 내 도입"],
        "hero_alt": "SOMA 안내 화면: 대형 화면의 3D 캐릭터와 답변, 옆에는 손님이 조작하는 화면",
        "hero_cap": "실제 화면: 손님이 조작 화면에서 질문하면 대형 화면에 캐릭터와 답변이 함께 표시됩니다",
        "emp_eyebrow": "쉬지 않는 직원",
        "emp_h2": "안내 데스크가 매일 듣는 질문 20개, 그녀에게 맡기세요",
        "emp_left": "사람 직원만 있을 때",
        "emp_right": "SOMA AI 직원이 함께할 때",
        "emp_rows": [
            ("교대와 휴무를 짜야 하고, 주말 피크 때는 늘 일손이 부족", "오픈부터 마감까지, 연중무휴"),
            ("같은 질문에 하루 수십 번 답하면 지치기 마련", "1,000번째 답변도 한결같이 명확하고 친절하게"),
            ("외국인 손님 응대는 그날 근무자에게 달려 있음", "중·영·일·한, 한 번 누르면 손님의 언어로"),
            ("신입 교육에 시간이 들고, 퇴사하면 노하우도 사라짐", "관리 화면에서 한 번 고치면 바로 반영, 지식은 매장에 남음"),
            ("지나가는 사람의 발길을 붙잡기 어려움", "대형 화면에서 말하고 움직이는 캐릭터가 곧 간판"),
        ],
        "emp_note": "그녀는 직원을 대신하려는 것이 아닙니다. 반복되는 질문을 맡아, 직원이 결제와 서비스, 그리고 사람이 꼭 필요한 순간에 집중할 수 있게 합니다.",
        "feat_eyebrow": "특징",
        "feat_h2": "웹사이트 속 채팅창이 아닌, 현장에 서 있는 안내 직원",
        "features": [
            ("오직 우리 매장 정보로 답변", "지식 베이스는 홈페이지 내용으로 만들고, 가격·시간·주소는 원문 그대로 안내합니다. 모르는 질문은 직원에게 문의하도록 안내하며 지어내지 않습니다."),
            ("4개 언어 지원", "외국인 손님이 언어 버튼을 누르면 그 언어로 답하고, 자연스러운 음성으로 읽어 줍니다."),
            ("말하고 움직이는 3D 캐릭터", "말할 때 입 모양이 맞춰지고, 대화에 따라 표정이 바뀌며, 손을 흔들거나 인사도 합니다. 8종 중에서 고를 수 있고 브랜드 전용 캐릭터도 제작할 수 있습니다."),
            ("iPad와 대형 화면의 듀얼 스크린", "손님은 iPad에 말하거나 입력하기만 하면 됩니다. 대형 화면에 캐릭터와 답변이 함께 나와 줄 선 사람과 지나가는 사람도 볼 수 있습니다."),
            ("관리 화면에서 직접 수정", "가격이나 이벤트가 바뀌면 관리 화면에서 고치기만 하면, 다음 손님부터 새 답변이 나갑니다. 매월 이용 리포트와 '답하지 못한 질문' 목록을 드립니다."),
            ("렌탈·구매 모두 가능, 고장 시 교체", "일반 iPad와 TV를 사용해 비싼 전용 기기가 필요 없습니다. 렌탈을 선택하면 자연 고장 시 저희가 교체해 드립니다."),
        ],
        "fit_eyebrow": "이런 곳에 적합합니다",
        "fit_h2": "사람이 오가고, 같은 질문을 자주 받는 곳이라면 어디든",
        "fit_lead": "다음 중 두 가지에 해당하면 잘 맞습니다: 매일 같은 질문을 받는다, 외국인 손님이 자주 온다, 입구 앞 유동 인구가 있다, 주말이나 피크 때 일손이 부족하다.",
        "biz_h3": "적합한 업종",
        "biz": [
            ("체험 활동·스포츠 시설", "수상 레저, 클라이밍, 헬스장, 각종 교실"),
            ("호텔·민박·온천 리조트", "로비 안내, 시설 설명, 주변 관광지 추천"),
            ("백화점·쇼핑몰·쇼핑센터", "층별 안내, 브랜드 추천, 행사 정보"),
            ("관광지·테마파크·박물관·전시회", "단지 안내, 전시 소개, 동선 안내"),
            ("매장·프랜차이즈", "상품 소개, 할인 안내, 멤버십"),
            ("병원·학원·각종 서비스 창구", "신청·예약 절차와 자주 묻는 질문"),
            ("관광안내소·역·공공서비스 창구", "교통, 경로, 절차 안내"),
        ],
        "info_h3": "그녀가 답할 수 있는 정보",
        "info": ["영업시간, 휴무일, 예약 방법", "가격, 요금제, 할인 행사", "층·위치·동선·시설", "교통, 주차, 주변 명소", "강좌·상품·서비스 내용", "행사 일정과 최신 소식", "신청, 집합 시간, 유의사항", "취소·변경 규정과 FAQ", "브랜드 스토리와 특징", "사람이 필요할 때 데스크나 LINE으로 연결"],
        "fit_note": "글로 적을 수 있는 정보라면 모두 그녀의 답변이 됩니다. 홈페이지에서 자동으로 정리하고, 홈페이지에 없는 내용도 채워 드립니다.",
        "scene_eyebrow": "활용 사례",
        "scene_h2": "사람이 지나는 곳에 두고, 손님이 먼저 묻게 하세요",
        "scenes": [
            ("호텔·민박 로비", "시설 안내, 주변 관광지, 다국어 응대", "민박 로비의 iPad 스탠드와 세로형 화면, 질문하는 가족 여행객"),
            ("테마파크·관광지", "시설 안내, 행사 추천, 다국어 가이드", "테마파크 입구의 AI 안내 키오스크, 터치 화면으로 질문하는 방문객"),
            ("백화점·쇼핑몰", "층별 안내, 브랜드 추천, 행사 정보", "쇼핑몰 아트리움의 세로형 AI 안내 화면"),
        ],
        "scene_note": "연출 이미지입니다. 실제 기기·캐릭터·화면은 요금제와 시설 설정에 따라 다릅니다. 이미지 속 휴대폰 QR 안내, 대기 정보, 피규어는 향후 구상이며 기본 요금제에 포함되지 않습니다.",
        "flow_eyebrow": "도입 절차",
        "flow_h2": "계약 후 영업일 10일이면 손님을 맞을 수 있습니다",
        "steps": [
            ("영업일 1–4일차", "지식 베이스 구축", "홈페이지 내용으로 Q&A 50–100개를 만들고, 데스크에서 자주 받는 질문을 더합니다."),
            ("영업일 2–5일차", "캐릭터와 화면", "캐릭터를 고르고 브랜드 색상과 배경을 적용하며, 4개 언어의 음성을 설정합니다."),
            ("영업일 5–8일차", "내부 테스트", "직원분들이 50개 질문을 해 보고, 자주 묻는 질문의 정답률이 90% 이상이 될 때까지 조정합니다."),
            ("영업일 8–10일차", "설치 및 운영 시작", "현장 설치와 화면 연결, 30분 사용 교육 후 검수를 마치면 운영을 시작합니다."),
        ],
        "plan_eyebrow": "요금제",
        "plan_h2": "하드웨어는 설치 위치로, 소프트웨어는 손님 수로",
        "plan_lead": "두 가지를 따로 골라 공간과 유동 인구에 맞게 조합합니다. 한 시설의 여러 대는 하나의 소프트웨어 요금제를 함께 씁니다.",
        "hw_h3": "하드웨어: 4가지 구성, 렌탈·구매 가능",
        "hw": [("iPad 단독", "카운터, 소형 매장"), ("iPad + 43인치 화면", "카운터 옆, 소규모 시설"), ("iPad + 55인치 화면", "로비, 주 출입구"), ("iPad + 65인치 화면", "쇼핑몰 아트리움, 관광지, 전시회")],
        "sw_h3": "소프트웨어: 월 대화 수에 따른 5가지 요금제",
        "sw": [("라이트, 스타터", "하루 수십 건의 질문"), ("스탠다드", "하루 100건 이상"), ("어드밴스드, 플래그십", "하루 수백 건, 또는 여러 대가 공유"), ("", "한 단계 낮게 시작해 운영 후 실제 데이터를 보고 조정")],
        "plan_note": "공간, 유동 인구, 대수에 맞춰 견적을 드립니다. 전시회·팝업을 위한 단기 렌탈도 있습니다.",
        "prep_eyebrow": "준비하실 것",
        "prep_h2": "네 가지면 충분합니다. IT 담당자는 필요 없습니다",
        "prep": ["홈페이지 주소와 데스크에서 자주 받는 질문", "최신 가격표와 행사 정보", "로고, 브랜드 색상, 시설 사진 한 장", "설치 위치, 콘센트 하나와 Wi-Fi"],
        "contact_h3": "우리 홈페이지로 현장에서 직접 보여 드립니다",
        "contact_p": "미리 홈페이지를 읽고 iPad를 들고 방문해, 손님들이 가장 자주 묻는 질문에 그녀가 바로 답하는 모습을 보여 드리고 시설에 맞는 견적도 드립니다. 시연은 무료이며 약 15분 걸립니다.",
        "book": "이메일로 시연 예약",
        "mail_note": "매장명, 홈페이지 주소, 편하신 시간을 함께 적어 주세요",
        "mail_subject": "SOMA AI 안내 키오스크 시연 예약",
        "legal": "법적 고지",
        "widget": "채팅 상담",
        "entry_nav": "안내 키오스크",
        "entry_h2": "Soma를 매장으로:<br>쉬지 않는 오프라인 AI 고객응대 직원",
        "entry_p": "SOMA AI 안내 키오스크는 홈페이지를 읽고 iPad와 대형 화면으로 입구에 서서 중국어·영어·일본어·한국어로 모든 손님에게 답합니다. 호텔, 쇼핑몰, 관광지, 체험 시설, 매장에 적합합니다.",
        "entry_btn": "안내 키오스크 보기 →",
        "entry_alt": "SOMA 안내 키오스크: 대형 화면의 3D 캐릭터와 답변",
    },
}


def url_for(d: str, page: str = "kiosk") -> str:
    return f"{SITE}/{d + '/' if d else ''}{page}"


def e(s: str) -> str:
    """屬性值跳脫（文案裡刻意寫的 HTML 標籤只出現在內文，不經過這裡）。"""
    return html.escape(s, quote=True)


def page(code: str, d: str) -> str:
    t = T[code]
    font_q, font_stack = FONTS[code]
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="{url_for(dd)}">' for c, dd, _ in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{url_for("en")}">'
    langs = "".join(
        f'<a href="/{dd + "/" if dd else ""}kiosk" lang="{c}"'
        + (' aria-current="page"' if c == code else "")
        + f">{label}</a>"
        for c, dd, label in LANGS
    )
    home = f"/{d + '/' if d else ''}"
    mailto = f"mailto:{EMAIL}?subject={urllib.parse.quote(t['mail_subject'])}"

    facts = "".join(f"<span>{f}</span>" for f in t["facts"])
    rows = "".join(f"<div>{a}</div><div class=\"after\">{b}</div>" for a, b in t["emp_rows"])
    feats = "".join(
        f'<div class="feature"><h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[i]}</svg>{name}</h3><p>{text}</p></div>'
        for i, (name, text) in enumerate(t["features"])
    )
    biz = "".join(f"<li><b>{n}</b>{dsc}</li>" for n, dsc in t["biz"])
    info = "".join(f"<li>{x}</li>" for x in t["info"])
    imgs = [("scene-hotel", 1024, 765), ("scene-park", 1600, 1067), ("scene-mall", 1600, 1067)]
    scenes = "".join(
        f'<figure><img src="/assets/kiosk/{f}.jpg" width="{w}" height="{h}" loading="lazy" alt="{e(alt)}">'
        f"<figcaption><b>{n}</b>{dsc}</figcaption></figure>"
        for (f, w, h), (n, dsc, alt) in zip(imgs, t["scenes"])
    )
    steps = "".join(
        f'<div class="step"><div class="day">{day}</div><h3>{ti}</h3><p>{tx}</p></div>' for day, ti, tx in t["steps"]
    )
    hw = "".join(f"<li><b>{n}</b>　{w}</li>" for n, w in t["hw"])
    sw = "".join(f"<li><b>{n}</b>　{w}</li>" if n else f"<li>{w}</li>" for n, w in t["sw"])
    prep = "".join(f"<li>{x}</li>" for x in t["prep"])

    return f"""<!DOCTYPE html>
<!-- 由 scripts/build-kiosk.py 產生，請改產生器，不要直接編這個檔案 -->
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<meta name="theme-color" content="#F2F4F7">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="{url_for(d)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url_for(d)}">
<meta property="og:image" content="{SITE}/assets/kiosk/hero-ui.jpg">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1067">
<meta property="og:site_name" content="Soma Agent">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/kiosk/hero-ui.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family={font_q}:wght@400;500;700;900&family=Orbitron:wght@800&display=swap">
<style>
{CSS}  :root {{ --font: {font_stack}; }}
</style>
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','2231262713555584');fbq('init','1068005176190695');fbq('track','PageView');
// 按下「來信預約展示」＝機台頁的轉換訊號
document.addEventListener('click',function(e){{
  var a=e.target.closest&&e.target.closest('a[href^="mailto:"]');
  if(a) fbq('track','Contact',{{content_name:'kiosk_demo'}});
}},true);
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=2231262713555584&ev=PageView&noscript=1"/></noscript>
</head>
<body>
<header class="site">
  <nav>
    <a class="logo" href="{home}">SOMA<i>_</i></a>
    <div class="right">
      <span class="langs">{langs}</span>
      <a class="navlink" href="{home}">{t['nav_home']}</a>
    </div>
  </nav>
</header>
<main class="sheet">
  <section class="hero">
    <div>
      <div class="brand"><b>SOMA</b><i></i><span>{t['brand_sub']}</span></div>
      <h1>{t['hero_h1']}</h1>
      <p class="lead">{t['hero_lead']}</p>
      <div class="facts">{facts}</div>
    </div>
    <figure class="hero-shot">
      <img src="/assets/kiosk/hero-ui.jpg" width="1600" height="1067" alt="{e(t['hero_alt'])}">
      <figcaption>{t['hero_cap']}</figcaption>
    </figure>
  </section>

  <section>
    <p class="eyebrow">{t['emp_eyebrow']}</p>
    <h2>{t['emp_h2']}</h2>
    <div class="pairs">
      <div class="head">{t['emp_left']}</div><div class="head after">{t['emp_right']}</div>
      {rows}
    </div>
    <p class="note">{t['emp_note']}</p>
  </section>

  <section>
    <p class="eyebrow">{t['feat_eyebrow']}</p>
    <h2>{t['feat_h2']}</h2>
    <div class="features">{feats}</div>
  </section>

  <section>
    <p class="eyebrow">{t['fit_eyebrow']}</p>
    <h2>{t['fit_h2']}</h2>
    <p class="lead" style="margin-bottom:24px">{t['fit_lead']}</p>
    <div class="fit">
      <div><h3>{t['biz_h3']}</h3><ul class="biz">{biz}</ul></div>
      <div><h3>{t['info_h3']}</h3><ul class="info">{info}</ul><p class="note">{t['fit_note']}</p></div>
    </div>
  </section>

  <section>
    <p class="eyebrow">{t['scene_eyebrow']}</p>
    <h2>{t['scene_h2']}</h2>
    <div class="scenes">{scenes}</div>
    <p class="note">{t['scene_note']}</p>
  </section>

  <section>
    <p class="eyebrow">{t['flow_eyebrow']}</p>
    <h2>{t['flow_h2']}</h2>
    <div class="steps">{steps}</div>
  </section>

  <section>
    <p class="eyebrow">{t['plan_eyebrow']}</p>
    <h2>{t['plan_h2']}</h2>
    <p class="lead" style="margin-bottom:24px">{t['plan_lead']}</p>
    <div class="plan-grid">
      <div class="plan-col"><h3>{t['hw_h3']}</h3><ul class="tick">{hw}</ul></div>
      <div class="plan-col"><h3>{t['sw_h3']}</h3><ul class="tick">{sw}</ul></div>
    </div>
    <p class="note">{t['plan_note']}</p>
  </section>

  <section class="two">
    <div>
      <p class="eyebrow">{t['prep_eyebrow']}</p>
      <h2>{t['prep_h2']}</h2>
      <ul class="tick">{prep}</ul>
    </div>
    <div class="contact">
      <h3>{t['contact_h3']}</h3>
      <p>{t['contact_p']}</p>
      <a class="book" href="{e(mailto)}">{t['book']}</a>
      <p class="mail">{EMAIL}｜{t['mail_note']}</p>
    </div>
  </section>
</main>
<footer class="site">
  <span>© 2026 Soma Agent</span>
  <span><a href="/legal.html">{t['legal']}</a> ・ <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</footer>
<!-- AICMS AI 客服（embed_key 是公開識別碼，護城河是後端的 domain allowlist） -->
<script src="https://waterman-sports.cc/widget.js" data-key="wk_bc9f4842e30745e48191174d59780958" data-label="{e(t['widget'])}" data-color="#0091AD" data-position="right" defer></script>
<script src="/assets/track.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for code, d, _ in LANGS:
        out = ROOT / (f"{d}/kiosk.html" if d else "kiosk.html")
        out.write_text(page(code, d))
        print(f"{out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
