import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
current_time = time.time()
command = "0"

WIDTH = int(config.get("frame", "WIDTH"))
HEIGHT = int(config.get("frame", "HEIGHT"))

CTR_PORT = int(config.get("network", "CTR_PORT"))
FRAME_PORT = int(config.get("network", "FRAME_PORT"))
CLIENT_PORT = int(config.get("network", "CLIENT_PORT"))



