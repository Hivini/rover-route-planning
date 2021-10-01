# main.py
import logging
from routes.router_cache import RouteCache
import routes.routing_planner as rp
import time
from matplotlib import pyplot as plt

START_X = 2485
START_Y = 8039
END_X = 2200
END_Y = 8210

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
manager = rp.RoverManager()
m = RouteCache(manager)
start = time.time()
path = m.findPath(manager, (START_X, START_Y), (END_X, END_Y))
end = time.time()
if path:
    logging.info('Time elapsed: %.4fs', (end - start))
    plt.show()
else:
    logging.info('No path found :(')
