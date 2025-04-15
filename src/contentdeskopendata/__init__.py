from src.contentdeskopendata.extract.extract import Extraction
from src.contentdeskopendata.transform.transform import Transform
from src.contentdeskopendata.load.load import Load

class ContentdeskOpenData:
    """
    ContentdeskOpenData class to extract data from a given target and generate a markdown file.
    """
    def __init__(self, target, config):
        print("INIT - ContentdeskOpenData")
        self.target = target
        self.config = config
        self.extractProducts = Extraction(self.target['host'], self.target['clientid'], self.target['secret'], self.target['user'], self.target['passwd'])
        self.debugExtractProducts()
        self.transformProducts = Transform(self.extractProducts.getProducts(), self.config)
        self.debugTransformProducts()
        self.loadProducts = Load(self.transformProducts.getTransformProducts())
        self.debugLoadProducts()
    
    def getExtractProducts(self):
        """
        Returns the extracted products.
        """
        return self.extractProducts
    
    def getTransformProducts(self):
        return self.transformProducts
    
    def getLoadProducts(self):
        return self.loadProducts
    
    def getConfig(self):
        print("ContentdeskOpenData Config")
        print(self.config)
        return self.config
    
    def debugExtractProducts(self):
        Load.debugToFile(self.extractProducts.getProducts(), "extractProducts")
        print("Debug file extractProducts created")
    
    def debugTransformProducts(self):
        Load.debugToFile(self.transformProducts.getTransformProducts(), "transformProducts")
        print("Debug file transformProducts created")
        
    def debugLoadProducts(self):
        Load.debugToFile(self.loadProducts.getLoadProducts(), "loadProducts")
        print("Debug file loadProducts created")