@echo off
echo Installing Pip's updates!
python -m pip install -U pip setuptools
echo Installing Discord.Py
python -m pip install -U https://github.com/Rapptz/discord.py/archive/master.zip#egg=discord.py[voice]
echo starting bot, from now on use start.bat!
python bot.py
pause
