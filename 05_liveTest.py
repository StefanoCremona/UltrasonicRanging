#!/home/pi/venv3/bin/python3.5
"""
Spyder Editor

This is a temporary script file.

"""
# from saveImage import draw_line
from livePrediction import predict
import platform
from os import listdir
from os.path import join, isfile

testDir = "C:/Users/e7470/rowData/testDowglas"
modelName = "20200402150758OneNormLatSeq100"

imagesToEvaluate = [f for f in listdir(testDir) if isfile(join(testDir, f)) and f.rfind('FilledSquared') >= 0] # DowglasForward is a test Dir
# print(imagesToEvaluate)
# draw_line("/home/pi/Scripts" + "/", "", "")
if platform.system() == "Windows":
    for f in imagesToEvaluate:
        print("Image: " + f)
        predict(testDir, f)
else:
    predict("/home/pi/Scripts", "FilledCropSquared.png")