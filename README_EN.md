# WatchDog-CI 🚀 (Minimalist Webhook Automated Deployment Manager)

Welcome to this tool!
This is an **ultra-lightweight CI/CD automated deployment plugin** designed specifically for solo developers and small cloud servers.
Built with Python + Flask, it has an extremely low resource footprint (requires only a few dozen megabytes of RAM), perfectly saving those tiny 1-core 1GB servers!

Say goodbye to the bloat and complex configurations of Jenkins or GitLab Runner. With this, all you need to do is a local `git push`. WatchDog-CI will automatically handle the dirty work of pulling code and restarting services beautifully in the background!

---

## ✨ Core Features

* **Extremely Low Overhead**: Doesn't eat up RAM or hog the CPU; it just quietly does its job perfectly in the background.
* **Configuration as Code**: Supports centralized management of multiple projects. The deployment script (`deploy.sh`) stays locally in each project for flexible decoupling.
* **Seamless Updates**: Farewell to tedious SSH logins and manual command typing. Enjoy the modern "Push to Deploy" development workflow.
* **Minimalist Troubleshooting**: Comes with detailed runtime logs, making it clear at a glance what it has been doing.

---

## 🛠️ Deployment Guide (Step-by-Step Tutorial)

To ensure the system runs perfectly, we need to maintain good directory hygiene on the server. **Highly Recommended: Keep the WatchDog-CI plugin itself and the business project you want to deploy in separate folders.**

### 1. Download and Install the Plugin

Execute the following commands in your server's home directory (e.g., `/home/ubuntu`):

```bash
# 1. Clone this repository to your server
git clone https://github.com/YourUsername/WatchDog-CI.git

# 2. Enter the folder and install dependencies
cd WatchDog-CI
pip3 install -r requirements.txt

```

### 2. Configure the Server Manager (main.py)

Open `main.py`, locate the `PROJECTS_CONFIG` dictionary, and register the business projects you want to deploy here:

```python
PROJECTS_CONFIG = {
    "Your-GitHub-Repo-Name": {       # ⚠️ CRITICALLY IMPORTANT: This name must exactly match your GitHub repository name!
        "path": "/home/ubuntu/your-project-folder",  # The absolute path to your business project
        "script": "deploy.sh",       # The name of the deployment script inside your business project
        "branch": "refs/heads/master" # The branch to monitor (newer GitHub repos usually use refs/heads/main)
    }
    # Add more projects below using the same structure as needed...
}

```

### 3. Configure Your Business Project (Crucial)

Inside the folder of the business project you are deploying, you need to do two things:

**First: Create an extremely robust `deploy.sh**`
It is strongly recommended to use absolute paths and a forced synchronization mechanism to prevent Git from getting stuck. Here is a recommended template:

```bash
#!/bin/bash
echo "🚀 Starting the automated deployment script..."

# 1. CRUCIAL: Forcibly enter your website's folder! (Prevents path confusion that scatters files everywhere)
cd /home/ubuntu/your-project-folder || exit
echo "📍 Current directory: $(pwd)"

# 2. Force pull code (discard all local modifications on the server, 100% sync with GitHub)
git fetch --all
git reset --hard origin/master
git pull origin master
echo "✅ Code sync complete!"

# 3. Kill the old process (modify according to your actual running program)
sudo pkill -f app.py
echo "💀 Old process cleaned up!"

# 4. Restart the new service
nohup python3 app.py > website.log 2>&1 &
echo "🎉 New version started successfully!"

```

**Second: Grant execution permissions to the script (A common pitfall for beginners!)**
In the business project directory, you must grant permissions to the script, otherwise the manager cannot execute it:

```bash
chmod +x deploy.sh

```

### 4. Start the WatchDog-CI Listening Service

Return to the WatchDog-CI directory and let the manager run persistently in the background (occupies port 5050 by default):

```bash
cd ~/WatchDog-CI
nohup python3 main.py > watchdog.log 2>&1 &

```

*Tip: You can use `tail -f watchdog.log` at any time to view the manager's real-time work diary.*

### 5. Configure GitHub Webhook

Go to the GitHub repository page you want to auto-deploy -> **Settings** -> **Webhooks** -> **Add webhook**

* **Payload URL:** `http://Your-Server-Public-IP:5050/webhook` *(Note: Your server's firewall must allow traffic on port 5050)*
* **Content type:** `application/json`
* **Events:** Select `Just the push event.`

Click **Add webhook** to save. As long as you see a green checkmark ✅ appear next to it, it means the communication is successfully connected!

---

## 🚑 Common Errors & Ultimate Troubleshooting Guide

Automated deployment seems magical, but it's very easy to fall into traps during the configuration phase. If you encounter problems, please match your "symptoms" against the list below:

❌ **Symptom 1: GitHub reports a timeout error, or the server receives no request**

* **Diagnostic concept:** Network is unreachable.
* **Solution:** Go to your cloud provider's console (e.g., Alibaba Cloud, Google Cloud), check the security group/firewall rules, and ensure that TCP traffic on port 5050 is allowed in the inbound rules.

❌ **Symptom 2: Server reports "Address already in use" when starting main.py**

* **Diagnostic concept:** A "phantom process" is occupying port 5050. It's likely that a previously started manager wasn't shut down cleanly.
* **Solution:** Brute-force kill the program occupying the port:

```bash
sudo fuser -k 5050/tcp
# Or use: sudo pkill -f "python3 main.py"

```

Then restart `main.py`.

❌ **Symptom 3: Logs show "Already up to date", but the website code hasn't changed**

* **Diagnostic concept 1:** Your local IDE only Committed but didn't Push. There is simply no new code on GitHub.
* **Diagnostic concept 2:** The business folder on the server is lost and connected to the wrong remote repository.
* **Solution:** Execute `git remote -v` in the business directory to check if the URL is correct. If not, reset it:

```bash
git remote set-url origin https://github.com/Your-Real-Repo-URL.git

```

❌ **Symptom 4: After executing the script, code is pulled to the server's root directory (files scattered everywhere)**

* **Diagnostic concept:** You accidentally ran `git init` in the server's home directory (`~`), or you didn't write an absolute `cd` path in `deploy.sh`.
* **Solution:** 1. Delete the fake Git memory in the root directory: `cd ~ && rm -rf .git`
2. Make sure to add an explicit `cd /your/business/absolute/path` to the very first line of your `deploy.sh`.

❌ **Symptom 5: Log indicates pull failed, reporting "fatal: not a git repository"**

* **Diagnostic concept:** The business folder you want to deploy is not a Git repository at all, so the manager doesn't know how to pull the code.
* **Solution:** Give the folder a Git identity and bind it to GitHub:

```bash
cd /your/business/directory
git init
git branch -M master
git remote add origin https://github.com/Your-Repo-URL.git
git fetch --all && git reset --hard origin/master

```