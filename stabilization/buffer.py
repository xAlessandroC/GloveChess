import numpy as np

class Buffer:
    size = 0
    buffer = []

    def __init__(self, N):
        self.size = N
        self.buffer = []

    def push(self, el):
        if len(self.buffer) >= self.size:
            self.pop()
        self.buffer.append(el)

    def pop(self):
        res = self.buffer[0]
        self.buffer.pop(0)
        return res

    def getAll(self):
        return self.buffer

    def getMaxSize(self):
        return self.size
