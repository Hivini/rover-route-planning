import pickle
import numpy as np
from skimage.feature.texture import greycomatrix, greycoprops
from scipy.stats import kurtosis

nav_data = np.load(f'processed_nav_data.npy')
nav_labels = np.load(f'nav_data_labels.npy')

file = open('nav_knn.pkl', 'rb')
model = pickle.load(file)

inputFile = open('./maps/variado2.obj', 'rb')
data = pickle.load(inputFile)
n_img = len(data)

for i in range(n_img):

    # Append the class of the image.
    if (data[i][0] == 0):
        continue

    # Data
    surface = (data[i][2]-data[i][2].min()).astype(int)
    glcm = greycomatrix(surface, distances=[5], angles=[0], levels=1024,
                        symmetric=True, normed=True)

    # Slope
    slope = data[i][3]

    # Depression
    depression = data[i][4]

    # Rise
    rise = data[i][5]

    glmc_disimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
    slope_max = slope.max()
    slope_mean = slope.mean()
    slope_variance = slope.var()
    depression_max = depression.max()
    depression_mean = depression.mean()
    depression_variance = depression.var()
    rise_max = rise.max()
    rise_mean = rise.mean()
    rise_variance = rise.var()

    image_data = [
        glmc_disimilarity,
        slope_max,
        slope_mean,
        slope_variance,
        depression_max,
        depression_mean,
        depression_variance,
        rise_max,
        rise_mean,
        rise_variance]
    prediction = model.predict([image_data])
    if(prediction[0] == 0):
        print('navegable') 
    elif(prediction[0] == 1):
        print('no navegable') 
