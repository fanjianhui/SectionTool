col=3

row=4

class abkt:
    def __init__(self, n):
        self.n = n
    def pt(self):
        print self.n

myList = [abkt(i) for i in range(5)]
myList.insert(3,abkt(10))
for o in myList:
    o.pt()



