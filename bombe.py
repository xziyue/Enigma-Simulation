import numpy as np

class Menu:
    adjancency = None

    def __init__(self):
        self.adjancency = np.zeros((26, 26), np.bool)

