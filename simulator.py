import seaborn as sns
import matplotlib.pyplot as plt
from collections import deque
import random
import numpy as np

# This clas generates neuron objects which are embedded in the brain matrix
class Neurons:
    def __init__(self, row, column):
        self.id =f"Neuron-{row}-{column}"
        self.threshold = random.randint(1,10)
        self.fired = False
        self.last_update_time = 0
        self.last_signal_id = 0
