# TagSpace2Billfish
import tags from TagSpace into Billfish  
從 TagSpace 匯入 Tag 到 Billfish

## 工作原理
- 掃描目標路徑下所有 .ts 資料
- 匯入 TagSpace 的 tag-library 到 Billfish資料庫
- 從檔名進行配對並匯入Billfish資料庫

## 限制
- 重名 tag 可能導致映射錯誤
- 檔案不區分資料夾進行配對，重名檔案可能會產生問題

## 使用說明
1. 直接將 TagSpace資源庫資料夾創建為 Billfish 資源庫
2. 備份 billfish.db
3. 設置 main.py 參數
    - TARGETFOLDER_PATH 為目標 TagSpace 資源庫目錄
    - DATABASE_PATH 為目標 Billfish 資源庫的 billfish.db
    - TAG_FILE_PATH 為 TagSpace 匯出的tag庫 json檔案
4. 運行腳本 python main.py

## 致謝
- 感謝 [Pixiv2Billfish](https://github.com/Ai-desu-2333/Pixiv2Billfish) 提供的 Billfish 資料庫操作基礎參考