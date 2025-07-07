@echo off
color 1F

echo 'Installing Required Python Modules'

pip install requests pwinput flask datetime

echo 'Finished Installing python Modules, Running Setup Script'

py setup.py

cls

echo 'Finished Setup Flow! | Please Run startup.bat'

pause