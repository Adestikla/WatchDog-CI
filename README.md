[English](./README_EN.md) | [简体中文](./README.md)
# WatchDog-CI 🚀 (极简 Webhook 自动化部署管家)
欢迎大家使用此工具
这是一个专为个人开发者和小型云服务器设计的**极轻量级 CI/CD 自动化部署插件**。
基于 Python + Flask 构建，资源占用极低（仅需几十MB内存），完美拯救 1核1G 的小霸王服务器！

告别 Jenkins / GitLab Runner 的臃肿与复杂配置。有了它，你只需在本地 `git push`，剩下的拉取、重启服务等脏活累活，WatchDog-CI 都会在后台全自动帮你干得漂漂亮亮！

---

## ✨ 核心特性

- **极低开销**：不吃内存，不占 CPU，安静地在后台做个美男子。
- **配置即代码**：支持多项目集中管理，部署脚本 (`deploy.sh`) 留在各项目本地，灵活解耦。
- **无感更新**：告别繁琐的 SSH 登录和手动敲命令，享受“Push 即上线”的现代开发流。
- **极简排错**：自带详细运行日志，干了什么一目了然。

---

## 🛠️ 部署指南 (保姆级教程)

为了让系统完美运行，我们需要在服务器上保持良好的目录卫生。**强烈建议：WatchDog-CI 插件本身和你要部署的业务项目，分别放在不同的文件夹中。**

### 1. 下载与安装插件
在你的服务器主目录（如 `/home/ubuntu`）下执行以下命令：

```bash
# 1. 克隆本仓库到服务器
git clone [https://github.com/你的用户名/WatchDog-CI.git](https://github.com/你的用户名/WatchDog-CI.git)

# 2. 进入文件夹并安装依赖
cd WatchDog-CI
pip3 install -r requirements.txt
```

2. 配置服务器大管家 (main.py)
打开 main.py，找到 PROJECTS_CONFIG 字典，在这里登记你要部署的业务项目：

```PROJECTS_CONFIG = {
    "Your-GitHub-Repo-Name": {       # ⚠️ 极其重要：这里的名字必须和 GitHub 上的仓库名完全一致！
        "path": "/home/ubuntu/your-project-folder",  # 你业务项目的绝对路径
        "script": "deploy.sh",       # 业务项目里的部署脚本名称
        "branch": "refs/heads/master" # 监听的分支 (新版 GitHub 通常是 refs/heads/main)
    }
    # 如有多项目集中管理需求，依此格式向下追加即可...
}
```
3. 配置你的业务项目 (极其关键)
在你要部署的业务项目文件夹里，你需要做两件事：

第一件事：创建一个极其健壮的 deploy.sh
强烈建议使用绝对路径和强制同步机制，避免 Git 卡死。以下是推荐模板：

```Bash
#!/bin/bash
echo "🚀 开始执行自动化部署脚本..."

# 1. 极其关键：强制进入你网站的文件夹！（防止路径错乱导致天女散花）
cd /home/ubuntu/your-project-folder || exit
echo "📍 当前所在目录: $(pwd)"

# 2. 强制拉取代码（放弃服务器上的所有本地修改，100% 同步 GitHub）
git fetch --all
git reset --hard origin/master
git pull origin master
echo "✅ 代码同步完成！"

# 3. 杀掉旧进程 (根据你的实际运行程序修改)
sudo pkill -f app.py
echo "💀 旧进程清理完毕！"

# 4. 重启新服务
nohup python3 app.py > website.log 2>&1 &
echo "🎉 新版本启动成功！"
```
第二件事：赋予脚本执行权限 (新手必踩坑！)
在业务项目目录下，必须给脚本赋予权限，否则管家无法执行它：

```Bash
chmod +x deploy.sh
```
4. 启动 WatchDog-CI 监听服务
回到 WatchDog-CI 目录，让大管家在后台持久运行（默认占用 5050 端口）：

```Bash
cd ~/WatchDog-CI
nohup python3 main.py > watchdog.log 2>&1 &
```
提示：你可以随时用 tail -f watchdog.log 来查看大管家的实时工作日记。

5. 配置 GitHub Webhook
进入你要自动部署的 GitHub 仓库页面 -> Settings -> Webhooks -> Add webhook

Payload URL: http://你的服务器公网IP:5050/webhook (注意服务器防火墙需放行 5050 端口)

Content type: application/json

Events: 选择 Just the push event.

点击 Add webhook 保存。只要看到前面出现绿色勾勾 ✅，就说明通讯打通了！

🚑 常见报错与终极排坑指南
自动化部署看似神奇，但在配置阶段极容易踩坑。如果你遇到了问题，请对照以下“症状”对号入座：

❌ 症状一：GitHub 报错超时，或者服务器没收到请求
排查思路：网络不通。

解决办法：去云服务商（如阿里云、Google Cloud）的控制台，检查安全组/防火墙规则，确保入站规则中放行了 5050 端口的 TCP 流量。

❌ 症状二：服务器启动 main.py 报错 Address already in use
排查思路：有“幽灵进程”霸占了 5050 端口。可能是你之前启动的管家没关干净。

解决办法：直接暴力击杀霸占端口的程序：

```Bash
sudo fuser -k 5050/tcp
# 或者 sudo pkill -f "python3 main.py"
```
然后再重新启动 main.py。

❌ 症状三：日志显示 Already up to date，但网站代码没变
排查思路 1：你本地 IDE 只是 Commit 了，并没有点击 Push，GitHub 上压根没新代码。

排查思路 2：服务器的业务文件夹跑错了片场，连接到了错误的远程仓库。

解决办法：在业务目录下执行 git remote -v 检查网址对不对。如果不对，重新设置：

```Bash
git remote set-url origin [https://github.com/你的真实仓库地址.git](https://github.com/你的真实仓库地址.git)
```

❌ 症状四：执行脚本后，代码被拉取到了服务器根目录（天女散花）
排查思路：你在服务器的主目录（~）不小心执行过 git init，或者 deploy.sh 里没有写 cd 绝对路径。

解决办法：

删掉根目录的假 Git 记忆：cd ~ && rm -rf .git

务必在 deploy.sh 的第一行加上明确的 cd /你的/业务/绝对路径。

❌ 症状五：日志提示拉取失败，报错 fatal: not a git repository
排查思路：你要部署的业务文件夹根本不是一个 Git 仓库，大管家不知道怎么去拉代码。

解决办法：赋予该文件夹 Git 身份并绑定 GitHub：

```Bash
cd /你的业务目录
git init
git branch -M master
git remote add origin [https://github.com/你的仓库地址.git](https://github.com/你的仓库地址.git)
git fetch --all && git reset --hard origin/master
```
