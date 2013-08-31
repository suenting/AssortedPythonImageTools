from Tkinter import *
import tkFileDialog
import tkColorChooser
import os
from PIL import Image

class Application(Frame):

    def SelectInputFolder(self):
        strPath = tkFileDialog.askdirectory(parent=root,initialdir="./",title='Please select a directory')
        self.PathInVar.set(strPath)
        
    def SelectOutputFolder(self):
        strPath = tkFileDialog.askdirectory(parent=root,initialdir="./",title='Please select a directory')
        self.PathOutVar.set(strPath)

    def ConvertToHexColor(self,rgb):
        hexcolor = '#%02x%02x%02x' % rgb
        return hexcolor
    
    def LoadKey(self):
        strPath = tkFileDialog.askopenfilename(parent=root,initialdir="./",title='Please select a color key', filetypes=[ ("PNG","*.png") ])
        im = Image.open(strPath)
        pixColorKey = im.load()
        maxIter = im.size[0]
        self.iter = maxIter
        self.color_original=[]
        self.color_swap=[]
        
        for label in self.color_original_label:
            label.grid_forget()

        for label in self.color_swap_label:
            label.grid_forget()

        self.color_original_label=[]
        self.color_swap_label=[]
        #self.color_original
        for i in range(0,maxIter):
            color1 = pixColorKey[i,0]
            colorLabel1 = self.ConvertToHexColor( (color1[0],color1[1],color1[2]) )
            color2 = pixColorKey[i,1]
            colorLabel2 = self.ConvertToHexColor( (color2[0],color2[1],color2[2]) )

            oLabel = Label(self, background=colorLabel1)
            oLabel.grid(row=2,column=(4+i))
            self.color_original_label.append(oLabel)
            sLabel = Label(self, background=colorLabel2)
            sLabel.grid(row=3,column=(4+i))
            self.color_swap_label.append(sLabel)
            self.color_original.append(color1)
            self.color_swap.append(color2)

    def Execute(self):
        listing = os.listdir(self.PathInVar.get())
        for infile in listing:
            suffix = infile[-3:]
            if( (suffix =="png") or (suffix=="jpg")):
                im = Image.open(self.PathInVar.get()+infile)
                width = im.size[0]
                height = im.size[1]
                newImage = Image.new(im.mode, im.size, "black")
                newImage.paste(im)
                opix = im.load()
                pix = newImage.load()
                for y in range(0,height):
                    for x in range(0,width):
                        for it in range(0,self.iter):
                            if opix[x,y] == self.color_original[it]:
                                pix[x,y] = self.color_swap[it]
                newImage.save(self.PathOutVar.get()+"\\"+infile)
        
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

        self.LoadKey =  Button(self, text="LoadKey", command=self.LoadKey).grid(row=2,column=0)

        self.Execute = Button(self,text="Execute", command=self.Execute).grid(row=2, column=1, columnspan=2)
        
        self.Exit = Button(self, text="quit",fg="red", command=self.quit).grid(row=2,column=3)


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
