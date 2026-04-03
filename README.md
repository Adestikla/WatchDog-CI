# WatchDog-CI (极简 Webhook 部署器) 🚀

这是一个专为个人开发者和小型云服务器设计的极轻量级 CI/CD 自动化部署插件。
基于 Python + Flask 构建，资源占用极低（仅需几十MB内存），完美拯救小霸王服务器！

## ✨ 核心特性
- **极低开销**：告别 Jenkins/GitLab Runner 的臃肿，完美适配 1核1G 服务器。
- **配置即代码**：支持多项目集中管理，部署脚本 (`deploy.sh`) 留在各项目本地，灵活解耦。
- **开箱即用**：无需复杂配置，只需配置 GitHub Webhook 即可实现“Push 即上线”。

## 🛠️ 快速开始

### 1. 安装依赖
请确保你的服务器已安装 Python 3，然后执行：
```bash
pip install -r requirements.txt
```

2. 配置项目
打开 main.py，在 PROJECTS_CONFIG 字典中配置你的项目信息：
```
Python
PROJECTS_CONFIG = {
    "你的 GitHub 仓库名": {
        "path": "/服务器上/你的/项目绝对路径",
        "script": "deploy.sh",       # 确保项目目录下有此脚本
        "branch": "refs/heads/main"  # 监听的分支
    }
}
```
3. 在你的网站/机器人项目中准备脚本
在你实际要部署的项目根目录下，创建一个 deploy.sh。例如：

```Bash
#!/bin/bash
set -e
echo "1. 拉取最新代码..."
git pull origin main
echo "2. 重启服务..."
# 此处填写你的重启命令，如 pm2 restart 或 systemctl restart
echo "🎉 部署完成！"
```
注意：在 Linux 上记得给该脚本执行权限：chmod +x deploy.sh

4. 运行监听服务
```Bash
python main.py
```
(推荐使用 nohup python main.py & 或 systemd 让其在后台常驻运行)

5. 配置 GitHub

进入你的 GitHub 仓库 -> Settings -> Webhooks -> Add webhook
```
Payload URL: http://你的服务器IP:5000/webhook
Content type: application/json
Events: 选 Just the push event.
```