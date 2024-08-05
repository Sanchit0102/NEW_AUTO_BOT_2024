if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Sanchit0102/NEW_AUTO_BOT_2024.git /NEW_AUTO_BOT_2024
else
  echo "Cloning Custom Repo from" "$UPSTREAM_REPO"
  git clone "$UPSTREAM_REPO" /NEW_AUTO_BOT_2024
fi
cd /NEW_AUTO_BOT_2024
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py

