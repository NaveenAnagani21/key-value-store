class kvstore:
    def __init__(self):
        self.data={}
    def set(self,key,value):
        self.data[key]=value
    def get(self,key):
        return self.data[key]
    def isin(self,key):
        return key in self.data
    def remove(self,key):
        del self.data[key]

