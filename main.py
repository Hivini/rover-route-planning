# main.py
import images.npy_image as npy_i

MAP_FILE = 'data/map.npy'
MAP_SCALE = 10.0174

map = npy_i.NpyImage(MAP_FILE, MAP_SCALE)
map.showImage('Rover Route Planning', 'Mars Map Overview')