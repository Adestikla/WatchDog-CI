from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# ==========================================
# ⚙️ 终极配置区：你的“项目登记册”
# ==========================================
PROJECTS_CONFIG = {
    # 服务器的项目
    "tg-bot": {  # 注意：这里的名字最好跟 GitHub 上的仓库名保持一致
        "path": "/user/XXXX",  # 你的绝对路径
        "script": "deploy.sh",  # 部署脚本名称
        "branch": "refs/heads/main"  # 监听的分支
    }
    # 以后有新项目，直接在这里往下加就行！
}


# ==========================================

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json

    # 获取 GitHub 传过来的仓库名和分支名
    repo_name = data.get("repository", {}).get("name")
    pushed_branch = data.get("ref")

    print(f"📡 收到来自仓库 [{repo_name}] 的推送信号...")

    # 检查项目是否在我们的配置名单里
    if repo_name in PROJECTS_CONFIG:
        config = PROJECTS_CONFIG[repo_name]

        # 检查分支是否匹配
        if pushed_branch == config["branch"]:
            print(f"🚀 分支匹配 ({pushed_branch})，准备部署 [{repo_name}]...")

            try:
                script_path = os.path.join(config["path"], config["script"])
                # 核心执行语句
                subprocess.run(["sh", script_path], check=True, cwd=config["path"])

                print(f"✅ [{repo_name}] 部署成功！")
                return jsonify({"status": "success", "message": f"{repo_name} deployed!"}), 200

            except Exception as e:
                print(f"❌ [{repo_name}] 部署失败: {str(e)}")
                return jsonify({"status": "error", "message": str(e)}), 500
        else:
            print(f"⚠️ 分支不匹配，忽略。")
            return jsonify({"status": "ignored", "message": "Branch not targeted"}), 200
    else:
        print(f"🛑 仓库 [{repo_name}] 不在配置列表中，忽略。")
        return jsonify({"status": "ignored", "message": "Repository not configured"}), 200


if __name__ == '__main__':
    # 启动监听服务
    app.run(host='0.0.0.0', port=5050)