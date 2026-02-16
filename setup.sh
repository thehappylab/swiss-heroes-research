git config --global --add safe.directory /data/openclaw-data
gh auth setup-git
git pull
openclaw gateway restart