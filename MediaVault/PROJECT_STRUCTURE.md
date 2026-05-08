# MediaVault 项目结构

```
MediaVault/
├── manage.py                 # Django 管理入口脚本
├── requirements.txt          # Python 依赖包列表
├── .env.example             # 环境变量示例
├── .gitignore               # Git 忽略文件配置
├── README.md                # 项目说明文档
├── start.sh                 # 快速启动脚本（Linux/Mac）
├── PROJECT_STRUCTURE.md     # 项目结构说明
│
├── mediavault/              # 项目主配置目录
│   ├── __init__.py
│   ├── settings.py          # Django 配置文件
│   ├── urls.py              # 项目路由配置
│   └── wsgi.py              # WSGI 配置
│
├── core/                    # 核心功能模块
│   ├── __init__.py
│   ├── apps.py              # 应用配置
│   ├── models.py            # 数据模型 (MediaItem, Category)
│   ├── views.py             # 视图函数
│   ├── urls.py              # 路由配置
│   ├── forms.py             # 表单类
│   └── admin.py             # 管理后台配置
│
├── users/                   # 用户管理模块
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py            # 用户扩展模型 (Profile)
│   ├── views.py             # 注册、登录、个人资料
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── music/                   # 音乐模块
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py            # 音乐模型
│   ├── views.py             # 音乐 CRUD
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── video/                   # 视频模块
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py            # 视频模型
│   ├── views.py             # 视频 CRUD
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── notes/                   # 笔记模块
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py            # 笔记模型
│   ├── views.py             # 笔记 CRUD
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── share/                   # 分享模块
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py            # 分享链接模型
│   ├── views.py             # 分享功能
│   ├── urls.py
│   └── admin.py
│
├── templates/               # 模板文件目录
│   ├── base.html            # 基础模板
│   ├── core/                # 核心模块模板
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── search.html
│   │   ├── category_list.html
│   │   ├── category_form.html
│   │   └── category_confirm_delete.html
│   ├── users/               # 用户模块模板
│   │   ├── login.html
│   │   ├── logout.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── music/               # 音乐模块模板
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── video/               # 视频模块模板
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── notes/               # 笔记模块模板
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   └── share/               # 分享模块模板
│       ├── list.html
│       ├── create.html
│       ├── password.html
│       ├── view.html
│       ├── music_view.html
│       ├── video_view.html
│       ├── note_view.html
│       └── confirm_delete.html
│
├── static/                  # 静态文件目录
│   └── css/
│       └── custom.css       # 自定义样式
│
├── media/                   # 用户上传文件目录（运行时创建）
│   ├── music/               # 音乐文件
│   ├── video/               # 视频文件
│   ├── covers/              # 封面图片
│   └── avatars/             # 用户头像
│
└── staticfiles/             # 收集的静态文件（生产环境）
```

## 模块说明

### Core（核心模块）
- 提供基础数据模型：MediaItem（媒体项目）、Category（分类）
- 仪表盘功能
- 搜索功能
- 分类管理

### Users（用户模块）
- 用户注册、登录、登出
- 个人资料管理
- 头像上传

### Music（音乐模块）
- 音乐文件上传
- 外部音乐链接添加
- 音乐播放
- 标签管理

### Video（视频模块）
- 视频文件上传
- 外部视频链接添加
- 视频播放
- 标签管理

### Notes（笔记模块）
- Markdown 编辑器
- 笔记渲染
- 标签管理

### Share（分享模块）
- 生成分享链接
- 密码保护
- 有效期设置
- 访问统计

## 技术栈

- **后端**: Django 4.2
- **数据库**: MySQL 8.0+
- **前端**: Bootstrap 5 + Vanilla JS
- **Markdown**: Python-Markdown
- **标签**: Django-Taggit
- **表单**: Django-Crispy-Forms + Bootstrap5

## 数据库关系

```
User (1) ──< (N) MediaItem
                 │
                 ├── Music (1:1)
                 ├── Video (1:1)
                 └── Note  (1:1)
                 │
                 ├── Category (M:1)
                 └── Tags (M:N)
                     
MediaItem (1) ──< (N) Share
```

## 快速开始

1. 复制 `.env.example` 为 `.env` 并配置数据库
2. 运行 `pip install -r requirements.txt` 安装依赖
3. 运行 `python manage.py makemigrations` 创建迁移
4. 运行 `python manage.py migrate` 执行迁移
5. 运行 `python manage.py createsuperuser` 创建管理员
6. 运行 `python manage.py runserver` 启动服务器
7. 访问 http://127.0.0.1:8000
