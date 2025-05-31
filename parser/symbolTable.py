class SymbolTable:
    def __init__(self):
        self._table = {}

    def contains(self, key):
        return key in self._table

    def getData(self, key):
        return self._table.get(key, None)

    def modify(self, key, value):
        self._table[key] = value

    def destroyTb(self):
        self._table.clear()
        del self._table
        
    def display(self):
        if not hasattr(self, '_table'):
            print("Symbol table has been destroyed.")
            return
        if not self._table:
            print("Symbol table is empty.")
            return
        print("Symbol Table Contents:")
        for key, value in self._table.items():
            print(f"{key}: {value}")