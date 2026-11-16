# 網站原始設計與輸出

這是一個無前端框架、無後端、無 API 金鑰的 GitHub Pages 靜態網站。

- 網站入口：`docs/index.html`
- 案例內頁：`docs/case.html?id=<slug>`
- 策略內頁：`docs/strategy.html?id=<slug>`
- 版面樣式：`docs/assets/style.css`
- 互動與篩選：`docs/assets/app.js`
- 由 Wiki 自動產出的資料：`docs/assets/data.js`
- 原創概念圖：`docs/assets/<slug>.svg`

`wiki/` 中的 Markdown 是內容的唯一真實來源。修改研究後，執行 `python3 scripts/build_site.py`，會重新產生 `data.js`，**不要直接修改 `data.js`**。

這個 `site/` 資料夾暫放維護說明；公開檔案輸出到 `docs/` 是為了讓 GitHub Pages 可以從 main 分支的 `/docs` 目錄部署。網站無需 JS 套件伺服器，直接用瀏覽器開啟 `docs/index.html` 即可。
