class Stack:
    def __init__(self):
        self.items = []
        self.popped = []
        
    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            self.popped.append(self.items[-1]) #Saves the element that will be deleted
            self.items.pop()
            return 
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = []

    # Use  this method to add elemets to the stack in inverted order
    # We need to do this so that the top of the stack is the first element on the list
    def stack_insertion(self, lista):
        for item in reversed(lista):
            self.push(item)

    def peekPopped (self):
        if not self.is_empty():
            return self.popped[-1]
        else:
            return None
    
    def show(self):
        print("Stack (top -> bottom):", self.items[::-1])