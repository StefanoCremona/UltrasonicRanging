#!/c/Python27/python.exe
# Gets all the files from a root directory and passes them to the routine 
# for generating the 28*28 images

from os import listdir
from os.path import isdir, join, isfile
from createAndCleanShapes import draw_line
import sys
from createDataDirs import createDirs
from mirrorImages import doMirror

homeDir = "C:/Users/e7470" 
rootRowDataPath = homeDir+"/rowData/"
rootDataPath = homeDir+"/dataTest/"

def mirrorImage(initialPath):
  im = Image.open(initialPath)
  return ImageOps.mirror(im)

rootDirs = [f for f in listdir(rootRowDataPath) if isdir(join(rootRowDataPath, f)) and f.rfind('DowglasForward') < 0] # DowglasForward is a test Dir

# Accept one input as a directory to work with
if (len(sys.argv) > 1):
    rootDirs = [sys.argv[1]]

lasers = ["B", "M", "T"]

# Force here the directory you want to parse
# rootDirs = ["DowglasForward"]

print("Directories found: " + str(rootDirs))

# Convert all the txt files in images
# Comment if you did it already
'''
for myDir in rootDirs:
    tempPath = rootRowDataPath + myDir
    for myLaser in lasers:
        myFiles = [f for f in listdir(tempPath) if isfile(join(tempPath, f)) and f.rfind('Left'+myLaser) > 0]
        # Force here the files you want to parse
        # print(myFiles[0])
        # myFiles = ["202003102249415054LeftB.txt"]
        # myLaser = 'B'
        for myFile in myFiles:
            timeRecording = myFile[0:myFile.rfind('Left'+myLaser)]
            # print('timeRecording: ' + str(timeRecording))
            draw_line(tempPath + '/', timeRecording, myLaser)
        print("File converted for " + myDir + ": " + str(len(myFiles)) + " laserH: " + myLaser)
'''
# doMirror(rootDirs)
# createDirs(rootRowDataPath, rootDataPath, rootDirs, lasers)