#!C:\python35\python.exe
import subprocess
import time
import os
import urllib.request


with open('Out.txt', "w"):
    pass


def internet_on():
    i = 1
    while True:
        try:
            urllib.request.urlopen('http://www.google.com', timeout=20)
            return True
        except:
            print("Internet not found for last %s minutes" % i)
            i = i + 1
            time.sleep(60)
            if i == 60:
                return False
            pass


for i in range(300):
    if internet_on():
        print("Starting New Session with Number %s" % i)
        print("=============================================================================")
        # print("Internet is present")
        proc = subprocess.Popen('C:\python35\python.exe test.py')
        result = None
        while result is None:
            counter=0
            with open('Out.txt', 'r') as f:
                first = f.read(1)
                if not first:
                    time.sleep(5)
                    counter+=1
                    if counter==360:
                        result='error'
                else:
                    result = "Error"
                    with open('Out.txt', "w"):
                        pass
        proc.terminate()
print("Shutting system down in 20 seconds")
os.system("start end.wav")
time.sleep(120)
os.system('shutdown -s')
