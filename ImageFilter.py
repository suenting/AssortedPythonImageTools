from Tkinter import *
import tkFileDialog
import tkColorChooser
import os
from PIL import Image
from math import *
from BoxFilters import *

# Gaussian Matrix variables
rad = 2
sig = rad/2.0

# contrast
contrast = 128

# brighten
bright = 1.5

class Application(Frame):
    #box filters
    def ExecuteEdgeDetect(self):
        boxFilter = EdgeDetectMatrix.calculate()
        self.ExecuteBoxfilter(boxFilter)
        
    def ExecuteGaussian(self,rad,sig):
        boxFilter = GaussianMatrix.calculate(rad,sig)
        self.ExecuteBoxfilter(boxFilter)
        
    def ExecuteRaise(self):
        boxFilter = RaiseMatrix.calculate()
        self.ExecuteBoxfilter(boxFilter)
        
    def ExecuteSharpen(self):
        boxFilter = SharpenMatrix.calculate()
        self.ExecuteBoxfilter(boxFilter)
        
    def ExecuteMotionBlur(self):
        boxFilter = MotionBlurMatrix.calculate()
        self.ExecuteBoxfilter(boxFilter)
        
    def ExecuteBoxfilter(self,boxFilter):
        listing = os.listdir(self.PathInVar.get())
        for infile in listing:
            suffix = infile[-3:]
            if( (suffix =="png") or (suffix=="jpg")):
                im = Image.open(self.PathInVar.get()+infile)
                width = im.size[0]
                height = im.size[1]
                newImage = Image.new(im.mode, im.size, "black")
                newImage.paste(im)
                opix = im.convert('RGB')
                pix = newImage.load()
                for y in range(0,height):
                    for x in range(0,width):
                        r = 0
                        g = 0
                        b = 0
                        missflag = 0
                        for ny in range(0,len(boxFilter)):
                            for nx in range(0,len(boxFilter)):
                                my = y+(ny-(1+len(boxFilter)/2))
                                mx = x+(nx-(1+len(boxFilter)/2))
                                if((mx>=0)and(my>=0)):
                                    weight = boxFilter[ny][nx]
                                    nr,ng,nb = opix.getpixel((mx,my))
                                    r = r+(nr*weight)
                                    g = g+(ng*weight)
                                    b = b+(nb*weight)
                                else:
                                    missflag = 1
                        pix[x,y] = (int(r),int(g),int(b))
                        if(1==missflag):
                            nr,ng,nb = opix.getpixel((mx,my))
                            pix[x,y] = (int(nr),int(ng),int(nb))
                outfile = self.PathOutVar.get()+"\\"+infile
                newImage.save(outfile)
    # end box filters

    # pixel operations
    def ExecutePixelOp(self, fn):
        listing = os.listdir(self.PathInVar.get())
        for infile in listing:
            suffix = infile[-3:]
            if( (suffix =="png") or (suffix=="jpg")):
                im = Image.open(self.PathInVar.get()+infile)
                width = im.size[0]
                height = im.size[1]
                newImage = Image.new(im.mode, im.size, "black")
                newImage.paste(im)
                opix = im.convert('RGB')
                pix = newImage.load()
                for y in range(0,height):
                    for x in range(0,width):
                        fn(opix,pix,x,y)
                outfile = self.PathOutVar.get()+"\\"+infile
                newImage.save(outfile)
                
    def GreyScale(self, opix,pix,x,y):
        nr,ng,nb = opix.getpixel((x,y))
        color = (nr+ng+nb)/3
        pix[x,y] = (int(color),int(color),int(color))
    def BlackToWhite(self, opix,pix,x,y):
        nr,ng,nb = opix.getpixel((x,y))
        color = (nr+ng+nb)
        if(color < 70):
            pix[x,y] = (int(255),int(255),int(255))
    def Invert(self, opix, pix, x,y):
        nr,ng,nb = opix.getpixel((x,y))
        pix[x,y] = (int(255-nr),int(255-ng),int(255-nb))
    def Contrast(self, opix,pix,x,y):
        nr,ng,nb = opix.getpixel((x,y))
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        nr = factor*(nr-128)+128
        ng = factor*(ng-128)+128
        nb = factor*(nb-128)+128
        pix[x,y] = (int(nr),int(ng),int(nb))
    def Brighten(self, opix,pix,x,y):
        nr,ng,nb = opix.getpixel((x,y))
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        nr = nr*bright
        ng = ng*bright
        nb = nb*bright
        pix[x,y] = (int(nr),int(ng),int(nb))
    # end pixel operations
        
    # def combination operations
    def PencilOperations(self):
        self.ExecuteEdgeDetect()
        inPath = self.PathInVar.get()
        outPath = self.PathOutVar.get()
        self.PathInVar.set(outPath)
        # convert black to white
        self.ExecutePixelOp(self.GreyScale)
        self.ExecuteGaussian(rad,sig)
        self.ExecutePixelOp(self.Invert)
        self.PathInVar.set(inPath)
        
    def BloomOperation(self):
        self.ExecutePixelOp(self.Contrast)
        inPath = self.PathInVar.get()
        outPath = self.PathOutVar.get()
        self.PathInVar.set(outPath)
        self.ExecuteGaussian(rad,sig);
        self.ExecutePixelOp(self.Brighten)
        self.ExecuteSharpen()
        self.PathInVar.set(outPath)
        
    # end combination operations            
    def SelectInputFolder(self):
        strPath = tkFileDialog.askdirectory(parent=root,initialdir="./",title='Please select a directory')
        self.PathInVar.set(strPath)
        
    def SelectOutputFolder(self):
        strPath = tkFileDialog.askdirectory(parent=root,initialdir="./",title='Please select a directory')
        self.PathOutVar.set(strPath)

    def ConvertToHexColor(self,rgb):
        hexcolor = '#%02x%02x%02x' % rgb
        return hexcolor

    def Execute(self):
        if(self.strOpType.get()=="Gaussian Blur"):
            self.ExecuteGaussian(rad,sig)
        if(self.strOpType.get()=="Sharpen"):
            self.ExecuteSharpen()
        if(self.strOpType.get()=="Motion Blur"):
            self.ExecuteMotionBlur()
        if(self.strOpType.get()=="Raise"):
            self.ExecuteRaise()
        if(self.strOpType.get()=="Edge Detect"):
            self.ExecuteEdgeDetect()
        if(self.strOpType.get()=="Grey Scale"):
            self.ExecutePixelOp(self.GreyScale)
        if(self.strOpType.get()=="Pencil"):
            self.PencilOperations()
        if(self.strOpType.get()=="Bloom"):
            self.BloomOperation()
            
    def CreateWidgets(self):
        self.LabelPathIn = Label(self, text="input folder").grid(row=0, columnspan=2)
        self.PathInVar = StringVar()
        self.PathInVar.set(".\\in\\")
        self.PathIn = Entry(self, textvariable=self.PathInVar).grid(row=0,column=2)
        self.SelectPathIn =  Button(self, text="...", command=self.SelectInputFolder).grid(row=0,column=3)
        self.LablePathOut = Label(self, text="output folder").grid(row=1, columnspan=2)
        self.PathOutVar = StringVar()
        self.PathOutVar.set(".\\out\\")
        self.PathOut = Entry(self, textvariable=self.PathOutVar).grid(row=1,column=2)
        self.SelectPathOut =  Button(self, text="...", command=self.SelectOutputFolder).grid(row=1,column=3)
        self.strOpType = StringVar()
        self.strOpType.set("Gaussian Blur")
        self.OpType = OptionMenu(self, self.strOpType,"Gaussian Blur", "Sharpen", "Motion Blur", "Raise","Edge Detect", "Bloom", "Grey Scale", "Pencil").grid(row=2,column=1,columnspan=2)
        self.Execute = Button(self,text="Execute", command=self.Execute).grid(row=3, column=1, columnspan=2)
        self.Exit = Button(self, text="quit",fg="red", command=self.quit).grid(row=3,column=3)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.color_original_label = []
        self.color_swap_label = []
        self.color_original = []
        self.color_swap = []
        self.colors = 0
        self.iter=0
        self.pack()
        self.CreateWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
