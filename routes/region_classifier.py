import os
import numpy as np
import richdem as rd
import pickle

from typing import Tuple, List
from dataclasses import dataclass
from skimage.transform import downscale_local_mean
from skimage.feature.texture import greycomatrix, greycoprops
from scipy.stats import kurtosis, skew
from sklearn import preprocessing


MAP_IMG = 'data/map.IMG'
SUBIMAGE_SIZE = 20


@dataclass(init=False)
class BoundingRectangle:
    """Defines a bounding rectangle"""
    topLeft: Tuple[int, int]
    topRight: Tuple[int, int]
    bottomLeft: Tuple[int, int]
    bottomRight: Tuple[int, int]
    isNav: bool


class RegionClassifier:

    def __init__(self, rows: int, columns: int) -> None:
        self._createMapSurfaces()
        if not os.path.isfile('regions.pkl') or not os.path.isfile('navMatrix.pkl'):
            self._createRegions(rows, columns)
        else:
            self.regions = pickle.load(open('regions.pkl', 'rb'))
            self.navMatrix = pickle.load(open('navMatrix.pkl', 'rb'))

    def _createRegions(self, rows: int, columns: int):
        loaded_model = pickle.load(
            open('routes/model/nav_decision_tree.pkl', 'rb'))
        regions: List[BoundingRectangle] = []
        navMatrix = []
        for i in range(0, rows - rows % SUBIMAGE_SIZE, SUBIMAGE_SIZE):
            currentMatrix = []
            for y in range(0, columns - columns % 20, SUBIMAGE_SIZE):
                rect = BoundingRectangle()
                rect.topLeft = (y, i)
                rect.topRight = (y + 20, i)
                rect.bottomLeft = (y, i + 20)
                rect.bottomRight = (y + 20, i + 20)
                # Remove loaded model
                data = self._getRegionData(rect.topLeft[1], rect.topLeft[0])
                if data == None:
                    rect.isNav = False
                else:
                    prediction = self._determineNavegability(
                        data, loaded_model)
                    if prediction == 1:
                        rect.isNav = True
                    else:
                        rect.isNav = False
                regions.append(rect)
                # Add to matrix
                currentMatrix.append(rect.isNav)
            navMatrix.append(currentMatrix)
        self.regions = regions
        self.navMatrix = navMatrix
        pickle.dump(self.regions, open('regions.pkl', 'wb'))
        pickle.dump(self.navMatrix,  open('navMatrix.pkl', 'wb'))

    def _determineNavegability(self, data, model):
        # Data
        surface = (data[1]-data[1].min()).astype(int)
        glcm = greycomatrix(surface, distances=[5], angles=[0], levels=1024,
                            symmetric=True, normed=True)
        # Slope
        slope = data[2]
        # Depression
        depression = data[3]
        # Rise
        rise = data[4]

        glmc_disimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
        slope_max = slope.max()
        slope_mean = slope.mean()
        slope_variance = slope.var()
        depression_max = depression.max()
        depression_mean = depression.mean()
        depression_variance = depression.var()
        depression_skewness = skew(depression.flatten())
        depression_kurtosis = kurtosis(depression.flatten())
        rise_max = rise.max()
        rise_mean = rise.mean()
        rise_variance = rise.var()
        rise_skewness = skew(rise.flatten())
        rise_kurtosis = kurtosis(rise.flatten())

        image_data = [
            glmc_disimilarity,
            slope_max,
            slope_mean,
            slope_variance,
            depression_max,
            depression_mean,
            depression_variance,
            depression_skewness,
            depression_kurtosis,
            rise_max,
            rise_mean,
            rise_variance,
            rise_skewness,
            rise_kurtosis]

        norm = preprocessing.normalize([image_data], axis=1)
        return model.predict(norm)

    def _getRegionData(self, row, col):
        valid_image = False
        subimg_row = row
        subimg_column = col
        if (subimg_row + SUBIMAGE_SIZE) < self.new_n_rows and \
                (subimg_column + SUBIMAGE_SIZE) < self.new_n_columns:
            surface_section = self.surface[subimg_row:(
                subimg_row+SUBIMAGE_SIZE), subimg_column:(subimg_column+SUBIMAGE_SIZE)]
            if surface_section.min() > 0:
                slope_section = self.slope[subimg_row:(
                    subimg_row+SUBIMAGE_SIZE), subimg_column:(subimg_column+SUBIMAGE_SIZE)]
                depression_section = self.depression[subimg_row:(
                    subimg_row+SUBIMAGE_SIZE), subimg_column:(subimg_column+SUBIMAGE_SIZE)]
                rise_section = self.rise[subimg_row:(
                    subimg_row+SUBIMAGE_SIZE), subimg_column:(subimg_column+SUBIMAGE_SIZE)]
                valid_image = True
        if not valid_image:
            return None
        return [self.maxZ, surface_section, slope_section, depression_section, rise_section]

    def _createMapSurfaces(self):
        data_file = open(MAP_IMG, "rb")
        endHeader = False
        while not endHeader:
            line = data_file.readline().rstrip().lower()

            sep_line = line.split(b'=')

            if len(sep_line) == 2:
                itemName = sep_line[0].rstrip().lstrip()
                itemValue = sep_line[1].rstrip().lstrip()

                if itemName == b'valid_maximum':
                    maxV = float(itemValue)
                elif itemName == b'valid_minimum':
                    minV = float(itemValue)
                elif itemName == b'lines':
                    n_rows = int(itemValue)
                elif itemName == b'line_samples':
                    n_columns = int(itemValue)
                elif itemName == b'map_scale':
                    scale_str = itemValue.split()
                    if len(scale_str) > 1:
                        scale = float(scale_str[0])

            elif line == b'end':
                endHeader = True
                char = 0
                while char == 0 or char == 32:
                    char = data_file.read(1)[0]
                pos = data_file.seek(-1, 1)

        image_size = n_rows*n_columns
        data = data_file.read(4*image_size)

        surface = np.frombuffer(data, dtype=np.dtype('f'))
        surface = surface.reshape((n_rows, n_columns))
        surface = np.array(surface)
        surface = surface.astype('float64')

        surface = surface - minV
        surface[surface < -10000] = -1

        sub_rate = round(10/scale)
        surface = downscale_local_mean(surface, (sub_rate, sub_rate))
        surface[surface < 0] = -1

        new_scale = scale*sub_rate
        new_n_rows = surface.shape[0]
        new_n_columns = surface.shape[1]

        inverted_surface = surface * (-1.0) + surface.max()
        inverted_surface[surface < 0] = -1

        rda1 = rd.rdarray(surface, no_data=-1)
        rda2 = rd.rdarray(inverted_surface, no_data=-1)

        slope = rd.TerrainAttribute(rda1, attrib='slope_riserun')
        slope[surface < 0] = -1

        depression = rd.FillDepressions(
            rda1, epsilon=True, in_place=False) - rda1
        depression[surface < 0] = -1

        rise = rd.FillDepressions(rda2, epsilon=True, in_place=False) - rda2
        rise[surface < 0] = -1

        x = new_scale*np.arange(surface.shape[1])
        y = new_scale*np.arange(surface.shape[0])
        # X, Y = np.meshgrid(x, y)
        maxZ = maxV - minV

        self.surface = surface
        self.new_n_rows = new_n_rows
        self.new_n_columns = new_n_columns
        self.slope = slope
        self.depression = depression
        self.rise = rise
        self.maxZ = maxZ
        self.scale = scale
        self.n_columns = n_columns
        self.n_rows = n_rows
