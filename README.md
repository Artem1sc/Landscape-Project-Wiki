# LANDSCAPE WIKI

**Global Landscape Architecture Atlas｜全球景觀設計案例研究與知識整合**

以全球景觀設計案例為研究基礎，透過 AI 輔助資料蒐集、繁體中文整理、空間策略分析與人工雙階段審核，建立可持續新增與交叉比較的案例 Wiki。

網站採用國際景觀競圖的極簡編輯式版型：圖紙白、植被灰綠、植栽淡粉、水文灰藍、細線及留白。目前四案封面改為**真實案例攝影**，採 Wikimedia Commons 提供的 Public Domain、CC0 或 Creative Commons 授權照片，逐張標明作者、授權與來源。Enghaveparken 採 2005 年改造前歷史照片，並附改造後官方專案連結。

## 目前成果

- 4 個已經使用者雙階段審核的景觀案例：Benthemplein Water Square、Enghaveparken、Bishan–Ang Mo Kio Park、Qunli Stormwater Park。
- 6 個設計策略頁面；13 筆原始來源紀錄。
- 首頁、案例詳頁、策略知識頁。
- 搜尋與交叉篩選（類型、設計策略、空間尺度、實際面積），支援電腦與手機版。
- 面積來源衝突不猜測：Benthemplein／Bishan／Qunli 結構化欄位仍為 `null`。

## 不懂程式的人，先從哪裡開始？

**直接在電腦上開啟 `docs/index.html`**，就可以瀏覽目前網站。此版本不依賴外部網路程式庫，也不需要自己架設伺服器。按下案例卡片可以看完整研究；使用上方篩選選單可以查找不同空間尺度、類型和策略。

## 主要檔案分工

| 位置 | 作用 | 是否通常要自行編輯 |
|---|---|---|
| `AGENTS.md` | AI 工作手冊，規定研究、審核、引用、設計、更新流程 | 規則變動才編輯 |
| `wiki/cases/*.md` | 每個景觀案例的正式研究內容（Markdown + YAML） | 新增案例時需要 |
| `wiki/strategies/*.md` | 跨案例策略知識 | 新研究核准後可更新 |
| `raw/sources/**` | 來源資訊及證據紀錄 | 新增來源時需要 |
| `wiki/index.md` | 所有案例與策略的內容索引 | 正式收錄時更新 |
| `wiki/log.md` | 每次收錄、審核與更新的歷史 | 每次知識更新追加 |
| `scripts/build_site.py` | 從 Wiki 內容產生瀏覽器使用的資料檔 | 通常不用改 |
| `docs/assets/data.js` | **自動產生**的網站資料 | **不要手動修改** |
| `docs/index.html` | 首頁與案例篩選 | 需要改首頁才改 |
| `docs/case.html` | 所有案例共用的研究內頁 | 修改案例版型才改 |
| `docs/strategy.html` | 策略頁共用版型 | 修改策略版型才改 |
| `docs/assets/style.css` | 全站視覺設計 | 修改風格才改 |
| `docs/assets/app.js` | 讀取資料、互動與頁面導覽 | 修改功能才改 |
| `wiki/cases/*.md` 的 `hero_image` | 真實照片網址、出處、作者與授權資訊 | 更換主圖時需檢查授權；重新 build 後更新網站 |

## 新增一個案例，為什麼不用重做網頁？

1. 你告訴 AI 一個研究主題；它先看 `AGENTS.md` 和 `wiki/index.md`，再搜尋並提出候選案例。
2. **第一次審核**：你選擇要研究的案例，AI 才建立 `raw/sources/` 來源紀錄及 `wiki/cases/` Markdown 草稿。
3. AI 根據統一的六章節模板整理繁體中文研究，記錄引用，建立分類與關聯。
4. **第二次審核**：你批准後，它將 `status` 設為 `published`，更新策略、索引與日誌。
5. 執行 `python3 scripts/build_site.py` 重新產生 `docs/assets/data.js`，首頁就會顯示新案例；點入時自動套用既有六章節內頁版型。

這就是這次 `AGENTS.md` 作業要驗證的「同一套規則可以重複使用」。網頁本身是**靜態展示介面**；真正的 AI 網路搜尋需在具備網路及檔案存取能力的 Agent 工具執行，網站本身不會自動搜尋網路。

## 有程式工具時：重新產生網站資料

```bash
python3 -m pip install -r requirements.txt
python3 scripts/build_site.py
```

`docs/` 已包含目前生成成果，**第一次瀏覽或上傳 GitHub 不需要先執行這些指令**。

## 透過 GitHub Pages 公開

1. 在 GitHub 建立 Public Repository，例如 `landscape-wiki`。
2. 將本資料夾**裡面的全部檔案與子目錄**上傳到 Repository 根目錄。確保 `AGENTS.md` 在根目錄，而不是被多包一層資料夾。
3. 到 Repository → **Settings → Pages**，在 `Build and deployment` 選擇 `Deploy from a branch`。
4. 設定 Branch=`main`、Folder=`/docs` 並儲存。
5. 公開網址通常為 `https://<github-user>.github.io/landscape-wiki/`；實際以 GitHub Pages 提供的網址為準。
6. `AGENTS.md` 的瀏覽網址通常為 `https://github.com/<github-user>/landscape-wiki/blob/main/AGENTS.md`。

**本資料夾目前尚未自行上傳 GitHub，也沒有公開網址。** 請由使用者確認帳號與發布動作。

## 研究限制與圖片版權

- 案例引用的來源及網址見 `raw/sources/`；設計方宣稱的效果不等同外部獨立驗證。
- 完工年份、容量、面積等若有來源差異，保留原始數值及不確定性。
- 封面已改為真實專案照片（非設計配置圖），圖片與來源頁資訊見各案例 `hero_image`。
- Enghaveparken 封面為 2005 年**改造前**照片，不代表 2019 年後的防洪設計；提供設計事務所現況連結。
- 使用 Wikimedia Commons 開放授權的遠端圖片網址；**開啟網站時需連網**，圖片伺服器若無法連線可能無法顯示。
- 未取得合法轉載權的其他官方照片不重新保存或上架；公開頁面保留圖片作者、授權與來源連結。
