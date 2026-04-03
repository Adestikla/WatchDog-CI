# Simple Webhook Deployer
一个轻量级的基于 Python + Flask 的自动部署小插件。用来监听 GitHub Push 事件，并自动在服务器拉取最新代码并重启服务。

## 如何使用
1. 修改 `main.py` 中的 `TARGET_PROJECT_PATH` 为你的项目路径。
2. 确保你的项目根目录下有一个 `deploy.sh` 文件。
3. 运行 `python main.py`。