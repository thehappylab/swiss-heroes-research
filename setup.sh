git config --global --add safe.directory /data/openclaw-data
git config --global user.email "hello@thehappylab.com"
git config --global user.name "The Happy Lab"
git config --global pull.rebase true

gh auth setup-git

if [[ "$1" == "--update-restart" ]]; then
  git pull
  openclaw gateway restart
else
  echo "No restart flag provided"
fi