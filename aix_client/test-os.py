#!/usr/bin/python





from asyncio import subprocess


AIXVersion =  subprocess.Popen("oslevel -s", shell=True, stdout=subprocess.PIPE).stdout
print (AIXVersion)
AIXVersion =  AIXVersion.read().decode().replace("\n","")

print(AIXVersion)