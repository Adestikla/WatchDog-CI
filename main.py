from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

# ==========================================
# ⚙️ 插件配置区 (使用者需要修改这里)
# ==========================================
# 你的网站/项目代码在服务器上的绝对路径 (例如：/home/user/my-website)
TARGET_PROJECT_PATH = "/path/to/your/website"
# 要执行的部署脚本的名字
DEPLOY_SCRIPT_NAME = "deploy.sh"
# 监听的分支
TARGET_BRANCH = "refs/heads/main"


# ==========================================

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json

    # 检查是否是目标分支的推送
    if data and data.get("ref") == TARGET_BRANCH:
        print("🚀 收到 GitHub 更新信号，开始自动部署...")

        try:
            # 组合出脚本的完整路径
            script_path = os.path.join(TARGET_PROJECT_PATH, DEPLOY_SCRIPT_NAME)

            # 执行脚本！cwd 参数非常关键，它会让命令在你网站的目录下运行，而不是插件目录下
            subprocess.run(["sh", script_path], check=True, cwd=TARGET_PROJECT_PATH)

            print("✅ 部署成功！")
            return "部署成功", 200
        except Exception as e:
            print(f"❌ 部署失败: {str(e)}")
            return f"部署失败: {str(e)}", 500

    return "非目标分支，忽略", 200


if __name__ == '__main__':
    # 启动监听服务
    app.run(host='0.0.0.0', port=5000)