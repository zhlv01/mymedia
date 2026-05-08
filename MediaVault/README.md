# MediaVault - 个人媒体收藏平台

一个基于 Django 的个人媒体收藏和分享平台，支持收藏音乐、视频、笔记，并可生成分享链接分享给他人。

## 功能特性

### 核心功能
- 🎵 **音乐收藏** - 支持本地上传和外部链接（网易云、QQ音乐等）
- 🎬 **视频收藏** - 支持本地上传和外部链接（YouTube、B站等）
- 📝 **笔记记录** - 支持 Markdown 语法的笔记功能
- 🔗 **分享功能** - 生成公开分享链接，支持密码保护和有效期设置
- 🏷️ **标签系统** - 灵活的标签分类管理
- 📂 **分类管理** - 自定义分类文件夹
- 🔍 **全文搜索** - 搜索标题、描述、标签

### 用户系统
- 👤 用户注册/登录
- 🖼️ 个人资料和头像设置
- 🔐 密码重置

## 技术栈

- **后端框架**: Django 4.2
- **数据库**: MySQL 8.0+
- **前端框架**: Bootstrap 5
- **表单处理**: Django Crispy Forms
- **标签系统**: Django Taggit
- **Markdown 渲染**: Python-Markdown

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- pip

### 安装步骤

1. **克隆项目**
```bash
cd MediaVault
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**

复制 `.env.example` 为 `.env` 并修改配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=mediavault
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

5. **创建数据库**
```sql
CREATE DATABASE mediavault CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. **执行数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **创建超级用户**
```bash
python manage.py createsuperuser
```

8. **启动开发服务器**
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 即可使用。

## 项目结构

```
MediaVault/
├── manage.py                 # Django 管理脚本
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量示例
├── mediavault/              # 项目配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # 核心模块
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── users/                   # 用户模块
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── music/                   # 音乐模块
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── video/                   # 视频模块
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── notes/                   # 笔记模块
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── share/                   # 分享模块
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/               # 模板文件
│   ├── base.html
│   ├── core/
│   ├── users/
│   ├── music/
│   ├── video/
│   ├── notes/
│   └── share/
├── media/                   # 用户上传文件
└── static/                  # 静态文件
```

## 使用说明

### 基础使用

1. **注册账号** - 访问 /users/register/ 注册一个新账号
2. **登录** - 使用注册的账号登录
3. **添加内容** - 在导航菜单中选择添加音乐、视频或笔记
4. **管理分类** - 创建分类来组织你的内容
5. **添加标签** - 给你的内容添加标签便于搜索
6. **分享** - 生成分享链接分享给朋友

### 媒体上传建议

- **音乐**: 建议 MP3 格式，单文件不超过 50MB
- **视频**: 建议 MP4 格式，单文件不超过 500MB
- **封面图**: 建议正方形，大小不超过 2MB

## 部署建议

### 生产环境配置

1. **设置 DEBUG=False**
2. **使用强 SECRET_KEY**
3. **配置 ALLOWED_HOSTS**
4. **配置静态文件服务（Nginx）**
5. **配置媒体文件服务**
6. **配置 HTTPS**

### 使用 Gunicorn

```bash
gunicorn mediavault.wsgi:application --bind 0.0.0.0:8000
```

### 使用 Nginx 反向代理

参考配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /path/to/MediaVault/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/MediaVault/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 开发计划

- [ ] 视频在线转码
- [ ] 批量上传功能
- [ ] 评论系统
- [ ] 收藏夹功能
- [ ] 社交账号登录
- [ ] 移动端 APP
- [ ] API 接口

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请提交 Issue。
