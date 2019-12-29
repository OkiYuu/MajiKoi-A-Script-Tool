Usage: Use MajiKoi A Script Tool.bat and options will be on-screen

This .bat files uses python to filter out content of .bin files for Majikoi A

Put all .bin files in .\IN\ for mass unpacking
Otherwise, you can use MajiKoi A Script Tool.bat to select a specific .bin
The file will output a subdirectory in .\EDIT\ for translation
Once finished, packing files will automatically detect if new lines for neXAs need to
be inserted.

Debug testing: Install barebones portable python to .\source\pp27\ so python.exe is in
that folder. The python source code was written for python 2.7
Portable Python Source: https://portablepython.com/wiki/Download/
Alternatively use Python 2.7 by yourself by editing the batch file

DEFAULT FOLDER STRUCTURE:
ROOT
>EDIT
>>SUBDIRECTORIES FOR TRANSLATION
>IN
>>RAW .bin FILES
>OUT
>>RAW EDITED .bin FILES
>source
>>pp27 (put portable python here for easy debugging)
>>main.py (python source code for program)
>>main.exe (compiled code for universal access)
>>script_ex.txt (example block for translation .txt output)
>MajiKoi A Script Tool.bat
>README.txt (this)