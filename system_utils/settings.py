from queue import *

# CAMERA PARAMETERS
camera_matrix = []
dist_coefs = []

# COLOR THRESHOLDS
low_th = []
high_th = []

# WINDOW DIMENSIONS
width_CV = 1280
height_CV = 720

width_GL = 900
height_GL = 506
init_width_GL = 370
init_height_GL = 150

# QUEUE
queue_A = Queue()
queue_B = Queue()
queue_img = Queue()

# PLAYERS
human_role = "WHITE"
ia_role = "BLACK"
