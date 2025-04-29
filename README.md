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

### 後端設置

1. 創建並激活虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行資料庫遷移：
```bash
python manage.py migrate
```

4. 啟動開發伺服器：
```bash
python manage.py runserver
```

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
