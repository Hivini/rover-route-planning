# ------------------------------------------------------------------------------------------------------------------
#   Surface data processing
# ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------
#   Imports
# ------------------------------------------------------------------------------------------------------------------

import pickle
import copy
import numpy as np
from scipy.stats import kurtosis, skew
from skimage.feature.texture import greycomatrix, greycoprops
from os import listdir
from os.path import isfile, join

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LightSource

# ------------------------------------------------------------------------------------------------------------------
#   Show images
# ------------------------------------------------------------------------------------------------------------------

# n_plots = int(n_img/10) + int((n_img % 10) != 0)

# ls = LightSource(315, 45)
# cmap = copy.copy(plt.cm.get_cmap('hot'))
# cmap.set_under(color='white')

# cmap2 = copy.copy(plt.cm.get_cmap('jet'))
# cmap2.set_under(color='white')

# img_index = 0

# for i in range(n_plots):
#     fig, ax = plt.subplots(4, 10, figsize=(20, 10))

#     for j in range(10):
#         if img_index < n_img:
#             rgb = ls.shade(data[img_index][2], cmap=cmap, vmin = 0, vmax = data[img_index][1], vert_exag=2, blend_mode='hsv')
#             im = ax[0, j].imshow(rgb, cmap=cmap, vmin = 0, vmax = data[img_index][1], interpolation ='nearest', origin ='upper')
#             ax[0, j].set_title('Clase: ' + str(data[img_index][0]))

#             im = ax[1, j].imshow(data[img_index][3], cmap=cmap2, vmin = 0, vmax = 5, interpolation ='nearest', origin ='upper')
#             im = ax[2, j].imshow(data[img_index][4], cmap=cmap2, vmin = 0, vmax = 20, interpolation ='nearest', origin ='upper')
#             im = ax[3, j].imshow(data[img_index][5], cmap=cmap2, vmin = 0, vmax = 20, interpolation ='nearest', origin ='upper')

#         ax[0, j].axis('off')
#         ax[1, j].axis('off')
#         ax[2, j].axis('off')
#         ax[3, j].axis('off')
#         img_index+=1

#     plt.show()

# ------------------------------------------------------------------------------------------------------------------
#   Process features of each image
# ------------------------------------------------------------------------------------------------------------------

DATA_PATH = 'surface_data'
all_files = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f))]
labels = np.array([
    'glmc_disimilarity',
    'glmc_correlation',
    'slope_max',
    'slope_min',
    'slope_variance',
    'slope_skewness',
    'slope_kurtosis',
    'depression_max',
    'depression_min',
    'depression_variance',
    'depression_skewness',
    'depression_kurtosis',
    'rise_max',
    'rise_min',
    'rise_variance',
    'rise_skewness',
    'rise_kurtosis'])

all_data = []

for file_name in all_files:
    inputFile = open(DATA_PATH + '/' + file_name, 'rb')
    data = pickle.load(inputFile)
    n_img = len(data)

    for i in range(n_img):
        # print("**********")
        # print("Image", i+1)

        # Data
        surface = (data[i][2]-data[i][2].min()).astype(int)
        glcm = greycomatrix(surface, distances=[5], angles=[0], levels=512,
                            symmetric=True, normed=True)
        # print("GLCM - Disimilaridad: ", greycoprops(glcm, 'dissimilarity')[0, 0])
        # print("GLCM - Correlación: ", greycoprops(glcm, 'correlation')[0, 0])

        # Slope
        slope = data[i][3]
        # print("Max slope: ", slope.max())
        # print("Min slope: ", slope.min())
        # print("Slope variance: ", slope.var())
        # print("Slope skewness: ", skew(slope.flatten()))
        # print("Slope kurtosis: ", kurtosis(slope.flatten()))

        # Depression
        depression = data[i][4]
        # print("Max depression: ", depression.max())
        # print("Min depression: ", depression.min())
        # print("Depression variance: ", depression.var())
        # print("Depression skewness: ", skew(depression.flatten()))
        # print("Depression kurtosis: ", kurtosis(depression.flatten()))

        # Rise
        rise = data[i][5]
        # print("Max rise: ", rise.max())
        # print("Min rise: ", rise.min())
        # print("Rise variance: ", rise.var())
        # print("Rise skewness: ", skew(rise.flatten()))
        # print("Rise kurtosis: ", kurtosis(rise.flatten()))

        glmc_disimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
        glmc_correlation = greycoprops(glcm, 'correlation')[0, 0]
        slope_max = slope.max()
        slope_min = slope.min()
        slope_variance = slope.var()
        slope_skewness = skew(slope.flatten())
        slope_kurtosis = kurtosis(slope.flatten())
        depression_max = depression.max()
        depression_min = depression.min()
        depression_variance = depression.var()
        depression_skewness = skew(depression.flatten())
        depression_kurtosis = kurtosis(depression.flatten())
        rise_max = rise.max()
        rise_min = rise.min()
        rise_variance = rise.var()
        rise_skewness = skew(rise.flatten())
        rise_kurtosis = kurtosis(rise.flatten())

        image_data = [
            glmc_disimilarity,
            glmc_correlation,
            slope_max,
            slope_min,
            slope_variance,
            slope_skewness,
            slope_kurtosis,
            depression_max,
            depression_min,
            depression_variance,
            depression_skewness,
            depression_kurtosis,
            rise_max,
            rise_min,
            rise_variance,
            rise_skewness,
            rise_kurtosis]

        all_data.append(image_data)

all_data = np.array(all_data)
labels = np.array(labels)
np.save('surface_data', all_data)
np.save('surface_labels', labels)


# ------------------------------------------------------------------------------------------------------------------
#   End of file
# ------------------------------------------------------------------------------------------------------------------
