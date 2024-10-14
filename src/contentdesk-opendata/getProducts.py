from akeneo.akeneo import Akeneo

class ContentdeskOpenData:
    def __init__(self, host, clientid, secret, user, passwd):
        self.host = host
        self.clientid = clientid
        self.secret = secret
        self.user = user
        self.passwd = passwd
        self.produccts = self.getProducts(self)
        
    def getProducts(self):
        target = Akeneo(self.host, self.clientid, self.secret, self.user, self.passwd)
        search = '{"completeness":[{"operator":"=","value":100,"scope":"ecommerce"}],"enabled":[{"operator":"=","value":true}],"license":[{"operator":"IN","value":["cc0","ccby","ccbync","ccbynd","ccbysa","ccbyncnd","ccbyncsa"]}]}'
        products = target.getProducts(search)
        return products
    
    def createMd(self):
        pass