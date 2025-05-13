import os
from pathlib import Path

# ... existing code ...

# 媒體文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 允許的圖片類型
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

# 最大圖片大小（5MB）
MAX_IMAGE_SIZE = 5 * 1024 * 1024 