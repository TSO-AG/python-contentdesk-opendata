import extract
import transform
import load

class ContentdeskOpenData:
    """
    ContentdeskOpenData class to extract data from a given target and generate a markdown file.
    """

    def __init__(self, target):
        self.target = target
        self.extractProducts = extract.Extraction(self.target['host'], self.target['clientid'], self.target['secret'], self.target['user'], self.target['passwd'])
        self.debugExtractProducts()
        self.transformProducts = transform.Transform(self.extractProducts)
        self.debugTransformProducts()
        self.loadProducts = load.Load(self.transformProducts)
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
    
    def debugExtractProducts(self):
        extract.Extraction.loadToDebug(self.extractProducts, "extractProducts")
        print("Debug file extractProducts created")
    
    def debugTransformProducts(self):
        transform.Transform.loadToDebug(self.transformProducts, "transformProducts")
        print("Debug file transformProducts created")
        
    def debugLoadProducts(self):
        load.Load.loadToDebug(self.loadProducts, "loadProducts")
        print("Debug file loadProducts created")