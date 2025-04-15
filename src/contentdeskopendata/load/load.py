import json
import os

class Load:
    
    def __init__(self, transformProducts):
        self.transformProducts = transformProducts
        self.loadProducts = self.setLoadProducts()
        
    def getLoadProducts(self):
        return self.loadProducts
    
    def setLoadProducts(self):
        return self.transformProducts