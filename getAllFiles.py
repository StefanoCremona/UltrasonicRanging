#!/c/Python27/python.exe
# Gets all the files from a root directory and passes them to the routine 
# for generating the 28*28 images

from os import listdir
from os.path import isdir, join, isfile
from createAndCleanShapes import draw_line
mypath = "C:/Users/e7470/rowData/"
rootDirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]
lasers = ["B", "M", "T"]

print("Directories found: ")
print(rootDirs)
for myDir in rootDirs:
    tempPath = mypath + myDir
    for myLaser in lasers:
        myFiles = [f for f in listdir(tempPath) if isfile(join(tempPath, f)) and f.rfind('Left'+myLaser) > 0]
        for myFile in myFiles:
            timeRecording = myFile[0:myFile.rfind('Left'+myLaser)]
            draw_line(tempPath + '/', timeRecording, myLaser)
        print("File converted for " + myDir + ": " + str(len(myFiles)) + " laserH: " + myLaser)
