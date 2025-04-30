# 求職網站

這是一個使用 Vue 3 和 Django 構建的求職網站專案。

## 專案結構

```
.
├── frontend/          # Vue 3 前端專案
└── backend/          # Django 後端專案
```

## 技術棧

- 前端：Vue 3 + JavaScript + Pinia + Vue Router
- 後端：Django + Django REST framework
- 資料庫：SQLite（開發環境）

## 開發環境設置

### 前端設置

1. 進入前端目錄：
```bash
cd frontend
```

2. 安裝依賴：
```bash
npm install
```

3. 啟動開發伺服器：
```bash
npm run dev
```

4. 在瀏覽器中開啟：http://localhost:5173

### 後端設置

1. 確保你在專案根目錄下，然後創建並激活虛擬環境：
```bash
# 創建虛擬環境
python -m venv venv

# 激活虛擬環境
# Mac/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```

2. 安裝所有必要的依賴：
```bash
pip install -r requirements.txt
```

3. 運行資料庫遷移：
```bash
python manage.py migrate
```

4. 啟動Django開發伺服器：
```bash
先回到整個資料夾的路徑
cd..
python manage.py runserver
```
#日後開啟專案
1.在Vscode中開啟終端機
```bash
Crtl + j 
```
2.進入frontend資料夾
```bash
cd frontend
```
3.運行前端項目
```bash
npm run dev
```

4.新增終端機（在原終端機視窗右上角的加號）

5.執行後端
```bash
python manage.py runserver
```

注意事項：
- 確保你的Python版本是3.8或更高版本
- 如果遇到端口被佔用的問題，可以使用 `python manage.py runserver 8001` 來指定不同的端口
- 要停止伺服器，按 Ctrl+C

## 功能特性

- 用戶認證系統
- 職位搜尋和篩選
- 履歷上傳和管理
- 職位申請追蹤
- 公司資訊展示

## 貢獻指南

1. Fork 專案
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request
