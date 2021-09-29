# main.py
import logging
import routes.routing_planner as rp
import time
from routes.utils import SearchAlgorithm
from matplotlib import pyplot as plt

START_X = 1
START_Y = 2
END_X = 3
END_Y = 4

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
manager = rp.RoverManager()
manager.map_image.showImagePoints(
    'Rouver Points', 'Mars Map Overview', (START_X, START_Y), (END_X, END_Y))
start = time.time()
path = manager.findRoute(START_X, START_Y, END_X,
                         END_Y, SearchAlgorithm.ASTAR)
end = time.time()
logging.info(f"Time elapsed: %.4fs.", end - start)
if path:
    manager.map_image.showImageWithPath(
        'Rover Route Planning', 'Mars Map Overview', path, rp.MAP_SCALE)
else:
    logging.info(f"No solution was found for x: %d y: %d to x: %d y: %d",
                 START_X, START_Y, END_X, END_Y)
plt.show()
