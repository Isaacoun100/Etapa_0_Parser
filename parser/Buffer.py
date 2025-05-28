class Buffer:
    def __init__(self):
        self.max_size = 8
        self.buffer = []
        self.index = 0
        self.currentLoad = 0
        self.bufferLoads = 0
        self.lastLoad = 0
        
    def calcBufferLoads(self, userInput):
        usersInputLen = len(userInput)
        
        if usersInputLen % 8 == 0:
            self.bufferLoads = (usersInputLen // 8)-1  # A unit is substracted because the loadCounter will star in zero
        else:
            self.bufferLoads = usersInputLen // 8
            self.lastLoad = usersInputLen % 8

    def load(self, string_list):
        self.buffer = string_list[:self.max_size]
        self.index = 0

    def next(self):
        if self.index < len(self.buffer) - 1:
            self.index += 1
            return self.buffer[self.index]
        else:
            return None

    def length(self):
        return len(self.buffer)

    def current(self):
        if self.buffer:
            return self.buffer[self.index]
        return None
    

    def flush(self):
        self.buffer = []
        self.index = 0

    def getIndex(self):
        return self.index
    
    def getBufferLoads(self):
        return self.bufferLoads
    
    def getLastLoad(self):
        return self.lastLoad
    
    def getCurrentLoad(self):
        return self.currentLoad
    
    def incCurrentLoad(self):
        self.currentLoad += 1 
    
    def __str__(self):
        display = [f"[{val}]" if i == self.index else val for i, val in enumerate(self.buffer)]
        return "Buffer: " + " | ".join(display)