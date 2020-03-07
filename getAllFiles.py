#!/c/Python27/python.exe
from os import listdir
from os.path import isdir, join, isfile
from createAndCleanShapes import draw_line
mypath = "C:/Users/e7470/rowData/"
rootDirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

print(rootDirs)
for myDir in rootDirs:
    tempPath = mypath + myDir
    myFiles = [f for f in listdir(tempPath) if isfile(join(tempPath, f)) and f.rfind('Left') > 0]
    for myFile in myFiles:
        prefix = myFile[0:myFile.rfind('Left')]
        draw_line(tempPath + '/', prefix)
