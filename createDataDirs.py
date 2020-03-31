'''
Creates the rootDataDirs and moves there the files depending on the source (the type of registration) and th
number of interceptions
'''
from os import listdir, mkdir
from os.path import isdir, join, isfile, exists
from shutil import copyfile, move
from PIL import Image, ImageOps

def createDir(path):
    if not exists(path):
        mkdir(path)

def flipImage(initialPath):
  im = Image.open(initialPath)
  return ImageOps.flip(im)

def createDirs(rootRowDataPath, rootDataPath, dirs, lasers):
    rootDataDirs = ["train", "test", "trainFilled", "testFilled"]
    imgType = "rowCropSquared"
    imgTypeFilled = "squared"
    createDir(rootDataPath)
    for rootDataDir in rootDataDirs:
        createDir(join(rootDataPath, rootDataDir))
    for d in dirs: # eg: ['DowglasForward', 'oneDouglasForward', 'oneDouglasNormal', 'twoDouglasOpposite', 'twoDouglasWalking']
        for l in lasers:
            for shapesN in range(4): # I checked that we have max 4 shapes in png files
                myFiles = [f for f in listdir(join(rootRowDataPath, d)) if isfile(join(rootRowDataPath, d, f)) and f.rfind(l+imgType+str(shapesN+1)) > 0]
                myFilesFilled = [f for f in listdir(join(rootRowDataPath, d)) if isfile(join(rootRowDataPath, d, f)) and f.rfind(l+imgTypeFilled+str(shapesN+1)) > 0]
                print("Found " + str(len(myFiles)) + " for "+ l + str(shapesN+1) + " in " + join(rootRowDataPath, d))
                if len(myFiles):
                    for rootDataDir in rootDataDirs:
                        newDataPath = join(rootDataPath, rootDataDir, d+l+str(shapesN+1))
                        createDir(newDataPath)
                        # oneDouglasForwardT1
                        if (rootDataDir == rootDataDirs[0]): # Copy files with just lines in train dir
                            for i in range(len(myFiles)):
                                if (len(myFiles) == 1 or i % 10 != 0):
                                    copyfile(join(rootRowDataPath, d, myFiles[i]), join(newDataPath, myFiles[i]))
                                    flipImage(join(newDataPath, myFiles[i])).save(join(newDataPath, "Flipped" + myFiles[i]))
                        if (rootDataDir == rootDataDirs[1]): # Move the 10% of the files to create the validation set
                            for i in range(len(myFiles)):
                                if (i % 10 == 0):
                                    copyfile(join(rootRowDataPath, d, myFiles[i]), join(newDataPath, myFiles[i]))
                                    flipImage(join(newDataPath, myFiles[i])).save(join(newDataPath, "Flipped" + myFiles[i]))
                        if (rootDataDir == rootDataDirs[2]): # Copy the files with just filled shapes in trainFilled dir
                            for i in range(len(myFilesFilled)):
                                if (len(myFilesFilled) == 1 or i % 10 != 0):
                                    copyfile(join(rootRowDataPath, d, myFilesFilled[i]), join(newDataPath, myFilesFilled[i]))
                                    flipImage(join(newDataPath, myFilesFilled[i])).save(join(newDataPath, "Flipped" + myFilesFilled[i]))
                        if (rootDataDir == rootDataDirs[3]): #  Move the 10% of the files to create the validation set
                            for i in range(len(myFilesFilled)):
                                if (i % 10 == 0):
                                    copyfile(join(rootRowDataPath, d, myFilesFilled[i]), join(newDataPath, myFilesFilled[i]))
                                    flipImage(join(newDataPath, myFilesFilled[i])).save(join(newDataPath, "Flipped" + myFilesFilled[i]))

    # createDir(validDir)
    # createDir(trainDir)

    