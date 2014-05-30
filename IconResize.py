from Tkinter import *
import tkFileDialog
import os
from PIL import Image

class Application(Frame):
        
    def Execute(self):
        dirList = ['drawable-xxhdpi','drawable-xhdpi','drawable-hdpi','drawable-mdpi', 'drawable-ldpi']
        dimList = [144,96,72,48, 36]
        imgSrc = Image.open(self.PathInVar.get());
        tmpTokens = str(self.PathInVar.get()).split('/')
        imgName = tmpTokens[len(tmpTokens)-1]
        
        imgFilter = Image.ANTIALIAS;
        if self.strOpType.get()=="ANTIALIAS":
            imgFilter = Image.ANTIALIAS;
        if self.strOpType.get()=="NEAREST":
            imgFilter = Image.NEAREST;
        if self.strOpType.get()=="BILINEAR":
            imgFilter = Image.BILINEAR;
        if self.strOpType.get()=="BICUBIC":
            imgFilter = Image.BICUBIC;
        it = 0
        for strDir in dirList:
            if not os.path.exists("./"+strDir):
                os.makedirs("./"+strDir)
            dim = dimList[it]
            imgOut = imgSrc.resize((dim,dim),imgFilter)
            imgOut.save("./"+strDir+"/"+imgName)
            it = it + 1

    # end combination operations            
    def SelectInputFolder(self):
        strPath = tkFileDialog.askopenfilename(parent=root,initialdir="./",title='Please select a directory')
        self.PathInVar.set(strPath)
        
    def CreateWidgets(self):
        self.LabelFile = Label(self, text="File").grid(row=0, columnspan=2)
        self.PathInVar = StringVar()
        self.PathInVar.set("")
        self.PathIn = Entry(self, textvariable=self.PathInVar).grid(row=0,column=2)
        self.SelectPathIn =  Button(self, text="...", command=self.SelectInputFolder).grid(row=0,column=3)

        self.strOpType = StringVar()
        self.strOpType.set("ANTIALIAS")
        self.OpType = OptionMenu(self, self.strOpType,"ANTIALIAS", "NEAREST", "BILINEAR", "BICUBIC").grid(row=0,column=4,columnspan=1)
        self.Execute = Button(self,text="Execute", command=self.Execute).grid(row=3, column=1)
        self.Exit = Button(self, text="quit",fg="red", command=self.quit).grid(row=3,column=4)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.CreateWidgets()
        
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
