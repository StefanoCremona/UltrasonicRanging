import pathlib
from os.path import join
from livePredictionUtils import getProbabilityModel, loadClassesNames, getImageToPlot, getPredictions, plotImgAndPrediction

models_dir = pathlib.Path("/home/pi/Models")
testName = "Seq20200324222341AllFilled"
imgDir = pathlib.Path("/home/pi/Images/oneNormT1")
imgName = 'Flipped202003101656127128Tsquared1.png'

try:
    probability_model    
except NameError:
    # Type here the testName of the model you want to load
    model_file = join(str(models_dir), 'model'+testName+'.json')
    weights_file = join(str(models_dir), 'weights'+testName+'.h5')
    probability_model = getProbabilityModel(model_file, weights_file)
    CLASS_NAMES = loadClassesNames(join(str(models_dir), 'classesNames'+testName+'.json'))# np.array(['oneNormB1', 'oneNormB2', 'oneNormBackB1', 'oneNormBackB2', 'oneNormBackM1', 'oneNormBackM2', 'oneNormBackT1', 'oneNormM1', 'oneNormM2', 'oneNormT1'])

img = getImageToPlot(join(str(imgDir), imgName))

predictions = getPredictions(probability_model, img)

plotImgAndPrediction(img, predictions[0], CLASS_NAMES)
