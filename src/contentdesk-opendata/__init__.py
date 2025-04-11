import extract
import transform
import load

class ContentdeskOpenData:
    """
    ContentdeskOpenData class to extract data from a given target and generate a markdown file.
    """

    def __init__(self, target):
        self.target = target
        self.extractProducts = extract.Extraction(self.target)
        self.transformProducts = transform.Transform(self.extractProducts)
    
    
    def getExtractProducts(self):
        return self.extractProducts
        