# main.py
from os import sys
import logging
import routes.routing_planner as rp

START_X = 2850
START_Y = 6400
END_X = 3150
END_Y = 6800

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
manager = rp.RoverManager()
path = manager.findRoute(START_X, START_Y, END_X, END_Y)
manager.map_image.showImageWithPath('Rover Route Planning', 'Mars Map Overview', path)