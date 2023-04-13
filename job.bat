@echo off
del models.txt
cd src\Process-Data\
dir
python setup.py

cd ..\..
cd src\Train-Models\
dir
python setup.py

cd ..\..
python main.py -A -odds=fanduel > output.txt
