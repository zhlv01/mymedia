#!/bin/bash

# MediaVault 启动脚本

echo "=================================="
echo "  MediaVault - 个人媒体收藏平台"
echo "=================================="
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cp .env.example .env
    echo "请编辑 .env 文件配置数据库信息"
    exit 1
fi

# 执行数据库迁移
echo "执行数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
echo ""
read -p "是否创建超级用户？(y/n): " createsuperuser
if [ "$createsuperuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo "=================================="
echo "  启动开发服务器..."
echo "  访问地址: http://127.0.0.1:8000"
echo "  管理后台: http://127.0.0.1:8000/admin"
echo "=================================="

python manage.py runserver
