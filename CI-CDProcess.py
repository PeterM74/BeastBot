import subprocess

# Stop the bot if running
subprocess.run(["pkill", "-f", "BeastBotInitiator.py"])

# Pull the latest code from remote
subprocess.run(["git", "pull", "origin", "main"])

# Restart BeastBot
subprocess.run(["python", "your_bot_script.py"])
