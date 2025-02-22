from imutils import paths
import os

class Uname():
    
    dir = []
    name = []
    labelnum = 0
    i = 0 
    def fetch(self):
        for imagePath in paths.list_images('dataBase'):
            if self.i==0:
                self.dir.append(imagePath.split(os.path.sep)[-2])
                self.name.append(imagePath.split(os.path.sep)[-2]+" id:"+str(self.labelnum))
            else:
                if self.dir[self.i]!=imagePath.split(os.path.sep)[-2]:
                  self.labelnum+=1
                  self.name.append(imagePath.split(os.path.sep)[-2]+" id:"+str(self.labelnum))
            self.dir.append(imagePath.split(os.path.sep)[-2])
            self.i+=1
           
        return self.name
x = Uname()
print(x.fetch())
