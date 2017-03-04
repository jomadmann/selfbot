#!/bin/sh
echo Installing Pips updates!
python -m pip install -U pip setuptools
echo Installing Discord.Py
python -m pip install -U https://github.com/Rapptz/discord.py/archive/master.zip#egg=discord.py[voice]
echo starting bot, from now on use start.bat!
echo If this is your first time, you might need to verify your IP through your email!
python bot.py
pause
