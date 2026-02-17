git config --global --add safe.directory /data/openclaw-data
git config --global user.email "hello@thehappylab.com"
git config --global user.name "The Happy Lab"
git config --global pull.rebase true

gh auth setup-git

if [[ "$1" == "--update" ]]; then
  git pull
  rm /data/.openclaw/openclaw.json
  openclaw gateway restart
elif [[ "$1" == "--push" ]]; then
  git add.
  git commit -a -m"Update" 
  git push
fi