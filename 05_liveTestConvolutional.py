#!/home/pi/venv3/bin/python3.5
import pathlib
from os.path import join
from livePredictionUtils import getImageToPredictForConvolutional, getProbabilityModel, loadClassesNames, getImageToPlot, getPredictions, plotImgAndPrediction
import platform
import platform
from os import listdir
from os.path import join, isfile

if platform.system() == "Windows":
    models_dir = pathlib.Path("C:/Users/e7470/models")
    testDir = "C:/Users/e7470/rowData/testDouglas"
else:
    models_dir = pathlib.Path("/home/pi/Models")
    testDir = "..."

try:
    modelName
except NameError:
    modelName = "20200503115629OneNormLatConv56_50" # Type here the testName of the model you want to load
    size = 56

try:
    probability_model    
except NameError:
    model_file = join(str(models_dir), 'model'+modelName+'.json')
    weights_file = join(str(models_dir), 'weights'+modelName+'.h5')
    probability_model = getProbabilityModel(model_file, weights_file, True)
    CLASS_NAMES = loadClassesNames(join(str(models_dir), 'classes'+modelName+'.json'))# np.array(['oneNormB1', 'oneNormB2', 'oneNormBackB1', 'oneNormBackB2', 'oneNormBackM1', 'oneNormBackM2', 'oneNormBackT1', 'oneNormM1', 'oneNormM2', 'oneNormT1'])

def predict(imgDir, imgName):
    img2plot = getImageToPlot(join(str(imgDir), imgName))
    img = getImageToPredictForConvolutional(join(str(imgDir), imgName), size)
    predictions = getPredictions(probability_model, img, True)
    plotImgAndPrediction(img2plot, predictions[0], CLASS_NAMES)

if __name__ == '__main__':
    if platform.system() == "Windows":
        imagesToEvaluate = [f for f in listdir(testDir) if isfile(join(testDir, f)) and f.rfind('FilledSquared') >= 0]
        for f in imagesToEvaluate:
            print("Image: " + f)
            predict(testDir, f)
        # predict("C:/Users/e7470/rowData/testDouglas", "202005031437265633TFilledSquared1.png")
    else:
        predict("/home/pi/Scripts", "fooFilledSquared.png")
