# main.py
import logging
from routes.router_cache import RouteCache
import routes.routing_planner as rp
import time
from matplotlib import pyplot as plt

# START_X = 2485
# START_Y = 8039
# END_X = 2200
# END_Y = 8210

# START_X = 4508
# START_Y = 4479
# END_X = 2606
# END_Y = 8004

# POINT THAT CANNOT FIND ROUTE WITH ONLY NAVS
# START_X = 2485
# START_Y = 8039
# END_X = 3721
# END_Y = 10726

# POINT THAT AVOIDS NAVS
# START_X = 2485
# START_Y = 8039
# END_X = 3484
# END_Y = 5298

# # Point 1
# START_X = 4508
# START_Y = 4479
# END_X = 3721
# END_Y = 10726

# # Point 2
# START_X = 4724
# START_Y = 3496
# END_X = 2606
# END_Y = 8004

# # Point 3
# START_X = 3701
# START_Y = 8860
# END_X = 4910
# END_Y = 14230

# Point 4
START_X = 3900
START_Y = 17327
END_X = 4505
END_Y = 12047

# # POINT 5
# START_X = 1435
# START_Y = 13000
# END_X = 4600
# END_Y = 3000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
manager = rp.RoverManager()
start = time.time()
onlyNavs = True
path = manager.findRoute(START_X, START_Y, END_X, END_Y, useNavMatrix=True)
end = time.time()
if not path:
    logging.info('Time elapsed: %.4fs', (end - start))
    logging.info(
        'Path not found using only navigable regions, now using all...')
    start = time.time()
    path = manager.findRoute(START_X, START_Y, END_X, END_Y)
    end = time.time()
    onlyNavs = False
    if path:
        logging.info('\033[91mRuta Contiene zonas no navegables!\033[0m')

if path:
    logging.info('Time elapsed: %.4fs', (end - start))
    manager.map_image.showImageWithPathSimple(
        'Rover Route Planning', 'Mars Map Overview', path, (START_X, START_Y), (END_X, END_Y))
    manager.map_image.showImageWithPathSimpleWithRegions(
        'Rover Route Planning', 'Path Overview with Regions', path, (START_X, START_Y), (END_X, END_Y))
    manager.map_image.showImageRegions('Nav Map', 'Navegability Map')
    plt.show()
else:
    logging.info('Time elapsed: %.4fs', (end - start))
    logging.info('No path found :(')
    manager.map_image.showImageRegions('Nav Map', 'Navegability Map')
    manager.map_image.showImagePoints(
        'Rover Route Planning', 'Mars Map Overview', (START_X, START_Y), (END_X, END_Y))
    plt.show()
