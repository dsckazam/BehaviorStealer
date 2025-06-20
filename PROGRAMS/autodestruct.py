import os

filepath = os.path.abspath(__file__)

try:
    os.remove(filepath)
except:
    pass