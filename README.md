# 工作搜尋網站

這是一個使用 Django REST Framework 構建的工作搜尋網站後端 API。

## 技術棧

- Python
- Django
- Django REST Framework
- JWT 認證
- SQLite 數據庫
- drf-spectacular (API 文檔)

## 功能特點

- 公司信息管理
- 職位發布和搜索
- 用戶認證和授權
- API 文檔自動生成

## API 文檔

本項目提供了三種方式查看 API 文檔：

1. **Swagger UI** (推薦)
   - 訪問地址：`http://127.0.0.1:8000/api/docs/`
   - 提供互動式界面，可直接在頁面上測試 API

2. **ReDoc**
   - 訪問地址：`http://127.0.0.1:8000/api/redoc/`
   - 提供更清晰的文檔閱讀體驗

3. **OpenAPI Schema**
   - 訪問地址：`http://127.0.0.1:8000/api/schema/`
   - 原始的 OpenAPI schema 格式

## API 端點

### 公司相關 (Companies)

- `GET /api/companies/` - 獲取所有公司列表
- `GET /api/companies/{id}/` - 獲取特定公司詳情

### 職位相關 (Jobs)

- `GET /api/jobs/` - 獲取所有職位列表
- `GET /api/jobs/{id}/` - 獲取特定職位詳情
- `POST /api/jobs/` - 創建新職位（需要認證）
- `PUT /api/jobs/{id}/` - 更新職位信息（需要認證）
- `DELETE /api/jobs/{id}/` - 刪除職位（需要認證）

### 用戶認證 (Users)

- `POST /api/users/register/` - 用戶註冊
- `POST /api/users/login/` - 用戶登入（獲取 JWT token）
- `POST /api/users/logout/` - 用戶登出（廢止 token）

## 數據模型

### 公司（Company）

- 基本信息：名稱、行業、簡介等
- 福利信息：法定福利、其他福利
- 聯繫方式：電話、郵箱、傳真等
- 媒體資源：公司 Logo、照片等

### 職位（Job）

- 職位名稱
- 職位描述
- 薪資範圍
- 工作地點
- 所需技能
- 職位類型（全職/兼職）

### 用戶（User）

- 基本信息：用戶名、電子郵件
- 認證信息：密碼（加密存儲）
- JWT Token 認證

## 開發環境設置

1. 克隆項目：
```bash
git clone [項目地址]
cd job-search-website
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行數據庫遷移：
```bash
cd backend
python manage.py migrate
```

4. 啟動開發服務器：
```bash
python manage.py runserver
```

## 項目結構

```
backend/
├── apps/
│   ├── companies/    # 公司相關功能
│   ├── jobs/         # 職位相關功能
│   └── users/        # 用戶相關功能
├── config/           # 項目配置
└── manage.py
```

## 注意事項

- 開發環境下請確保 DEBUG=True
- API 文檔需要服務器運行才能訪問
- 所有 API 返回格式均為 JSON
- 部分 API 端點需要 JWT 認證才能訪問
- Token 格式：`Bearer <your_token>`

## 待實現功能

- [ ] 職位搜索和篩選功能
- [ ] 用戶個人資料管理
- [ ] 簡歷上傳和管理
- [ ] 職位申請流程
- [ ] 公司評價系統
