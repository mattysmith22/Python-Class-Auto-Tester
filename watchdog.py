import configparser
import os
import re
import subprocess
from time import sleep

config = "conf.ini"
handinpath = " "
storepath = " "
testerpath = " "
timeout = 1

def readConfig(path):
    global handinpath, storepath, testerpath
    print("Getting config...")
    configin = configparser.ConfigParser()
    configin.read(path)
    handinpath = configin.get("Paths", "handinpath")
    storepath = configin.get("Paths", "storepath")
    testerpath = configin.get("Paths", "testerpath")
    print("handinpath: {}".format(handinpath))
    print("storepath: {}".format(storepath))
    print("testerpath: {}".format(testerpath))


def runTest(path):
    print("Pathin {}".format(path), end=' ')
    try:
        result = subprocess.run(["python3", testerpath, os.path.join(handinpath,path)], stdout=subprocess.PIPE, timeout=timeout)
        output = result.stdout.decode('utf-8')
    except subprocess.TimeoutExpired:
        print("Error, timeout expired")
        output = "ERROR: Your program could not run in the {} second allotment, please check your code for infinite loops".format(timeout)

    outputfilepath = os.path.splitext(os.path.basename(path))[0]
    print(outputfilepath)
    fd = open(os.path.join(handinpath, outputfilepath + ".html"), "w")
    fd.write(output)
    fd.close()

    m = re.search(r'''Score:\s+\d+\/+\d+\s+-+\s+(\d*.+\d)\%''', output)
    if not m is None:
        print("Got score of {}%".format(m.group(1)))
    else:
        print("Error: score of 0%")

    os.rename(os.path.join(handinpath, path), os.path.join(storepath, os.path.basename(path)))

def checkFolder():
    directory = os.listdir(handinpath)
    os.listdir(handinpath)
    for possibleFile in directory:
        m = re.search(r'''(\w+[.]+py)''', possibleFile)
        if not m is None:
            print("Testing {}".format(possibleFile))
            runTest(os.path.abspath(os.path.join(handinpath,m.group(1))))

def main():
    try:
        readConfig(config)
        while True:
            checkFolder()
            sleep(1)
    except KeyboardInterrupt:
        print("Bye!")

if __name__ == "__main__":
    main()