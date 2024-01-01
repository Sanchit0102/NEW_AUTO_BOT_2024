if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Abhibotssz/filter.git /Souravmkv/AutoFilerAdv 
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Abhibotssz/filter 
fi
cd /Auto-filter 
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
