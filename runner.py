from time import sleep
import psutil
import os


def isRAMSafe():
    RAM = psutil.virtual_memory().percent
    print("RAM now is: ", RAM)
    return RAM < 65


def isStopped():
    status = False
    with open('status.txt') as f:
        status = f.read().strip() == 'stop'
    print("status: ", status)
    return status


def runMain():
    setStatusRun()
    command = 'python3 main.py; python3 stop.py;'
    os.system(command)

def runStop():
    command = 'python3 stop.py;'
    os.system(command)
    sleep(2)


def setStatusRun():
    with open('status.txt', 'w') as f:
        f.write('run')


runStop()
while True:
    if isStopped() and isRAMSafe():
        runMain()

    else:
        sleep(60*3)
