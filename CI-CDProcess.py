import subprocess
import sys

# Stop the bot if running
try:
    subprocess.run(["pkill", "-f", "BeastBotInitiator.py"], check=True)
except subprocess.CalledProcessError as e:
    if e.returncode == 1:
        print("No running bot process found")
    else:
        print(f"Error while attempting to stop the bot: {e}")
        sys.exit(1)


# Pull the latest code from remote
subprocess.run(["git", "pull", "origin", "main"])

# Restart BeastBot
subprocess.run(["python", "BeastBotInitiator.py"])
