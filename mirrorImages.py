#!/c/Python27/python.exe
'''
Mirror all the images contained in RowData dir
'''

from os import listdir
from os.path import isdir, join, isfile
from createAndCleanShapes import draw_line
import sys
from createDataDirs import createDirs
from PIL import Image, ImageOps
from os import listdir, mkdir
from os.path import isdir, join, isfile, exists
from shutil import copyfile, move

def createDir(path):
    if not exists(path):
        mkdir(path)
        print("Created " + path)

def mirrorImage(initialPath):
    im = Image.open(initialPath)
    return ImageOps.mirror(im)

def doMirror(rootDirs):
    homeDir = "C:/Users/e7470" 
    rootRowDataPath = homeDir+"/rowData/"
    # rootDirs = [f for f in listdir(rootRowDataPath) if isdir(join(rootRowDataPath, f)) and f.rfind('DowglasForward') < 0] # DowglasForward is a test Dir

    print("Mirroring: " + str(rootDirs))

    for rootDataDir in rootDirs:
        backDir = join(rootRowDataPath, rootDataDir + "Back")
        createDir(backDir)
        mySquaredFiles = [f for f in listdir(join(rootRowDataPath, rootDataDir)) if isfile(join(rootRowDataPath, rootDataDir, f)) and f.upper().rfind("SQUARED") > 0]
        for mySquaredFile in mySquaredFiles:
            mirrored = mirrorImage(join(rootRowDataPath, rootDataDir, mySquaredFile))
            mirrored.save(join(backDir, mySquaredFile))
        print("Mirrored: " + str(len(mySquaredFiles)) + " files")

if __name__ == '__main__':
    rootDirs = []
    if (len(sys.argv) > 1):
        rootDirs = [sys.argv[1]]
    doMirror(rootDirs)