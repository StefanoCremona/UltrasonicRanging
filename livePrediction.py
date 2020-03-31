#!/home/pi/venv3/bin/python3.5
import pathlib
from os.path import join
from livePredictionUtils import getProbabilityModel, loadClassesNames, getImageToPlot, getPredictions, plotImgAndPrediction

models_dir = pathlib.Path("/home/pi/Models")
modelName = "Seq20200324222341AllFilled" # Type here the testName of the model you want to load
# imgDir = pathlib.Path("/home/pi/Images/oneNormT1")
# imgName = 'Flipped202003101656127128Tsquared1.png'

try:
    probability_model    
except NameError:
    model_file = join(str(models_dir), 'model'+modelName+'.json')
    weights_file = join(str(models_dir), 'weights'+modelName+'.h5')
    probability_model = getProbabilityModel(model_file, weights_file)
    CLASS_NAMES = loadClassesNames(join(str(models_dir), 'classesNames'+modelName+'.json'))# np.array(['oneNormB1', 'oneNormB2', 'oneNormBackB1', 'oneNormBackB2', 'oneNormBackM1', 'oneNormBackM2', 'oneNormBackT1', 'oneNormM1', 'oneNormM2', 'oneNormT1'])

def predict(imgDir, imgName):
    img = getImageToPlot(join(str(imgDir), imgName))
    predictions = getPredictions(probability_model, img)
    plotImgAndPrediction(img, predictions[0], CLASS_NAMES)

if __name__ == '__main__':
    # (path, timeRecording, laserHeight)
    predict("/home/pi/Scripts", "fooFilledSquared.png")
