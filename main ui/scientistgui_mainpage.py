from Tkinter import *
import tkMessageBox
import subprocess
import webbrowser
import os


tk = Tk()
canvas = Canvas(tk, width=1000, height=450)
canvas.pack()
myimage = PhotoImage(file=r"files\mainpage.gif")
tk.wm_iconbitmap(bitmap = r"files\main.ico")
canvas.create_image(0, 0, anchor=NW, image=myimage)
tk.title("Seraph Scientist LabManager(TM) v1.0")
tk.resizable(0, 0)


## Launch external EXE files 

def runcmd(dir,cmd):
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #si.wShowWindow = subprocess.SW_HIDE # default
        subprocess.Popen(dir+"\\"+cmd,cwd=dir) #, startupinfo=si
    except:
        tkMessageBox.showinfo("Error", "could not find "+cmd +" in sub folder "+dir)
    
def openfile(file):
    os.startfile(file)

def launchseraphstudio():
    runcmd(r"SeraphStudio","SeraphStudio.exe")

def launchseraphprint():
    runcmd(r"SeraphPrint","SeraphPrint.exe")

def launchmanipulator():
    runcmd(r"manipulator","manipulator.exe")

def launchviewer():
    runcmd(r"viewer","viewer.exe")

def launchcalibrator():
    runcmd(r"calibrator","calibrator.exe")

## Launch external URLs
def launchwebsite():
    webbrowser.open('http://www.seraphrobotics.com')

## Launch external PDF files
def heatedtray():
    openfile(r"Documents\Heated Build Tray.pdf")

def tempctrl():
    openfile(r"Documents\Temperature controller.pdf")
    
def usbmcr():
    openfile(r"Documents\USB Microscope Tool.pdf")
def uvspcs():
    openfile(r"Documents\UV tool.pdf")
'''
helpmenu.add_command(label="View Software Guide", command=launchwebsite)
helpmenu.add_command(label="View XDFL & Calibration Guide", command=launchwebsite)
helpmenu.add_command(label="View Assembly Instructions", command=launchwebsite)
'''    
def swguide():
    openfile(r"Documents\SeraphSW guide.pdf")
    
def xdfl():
    openfile(r"Documents\XDFL User Guide.pdf")


def quit():         #exits tk window, program still running
    tk.destroy()


## Buttons on GUI


spacerframe1 = Frame(tk, bg = "white", width = 1000, height = 10)
spacerframe1.pack(fill=X)

f = Frame(tk, bg = "white", width = 1000, height = 150)
f.pack(fill=X)

btn = Button(f, text="Click to launch SeraphStudio", command=launchseraphstudio, height=3, width=60, fg="white", bg="#1F4E79")
btn.grid(row=1, column=1)

#btn = Button(f, text="Click to launch Material Calibrator", command=launchseraphprint, height=3, width=60, fg="white", bg="#1F4E79")   ## uncomment and delete spacer frames to remove spaces
#btn.grid(row=2, column=1)

btn = Button(f, text="Launch Manipulator", command=launchmanipulator, height=3, width=28, fg="white", bg="#2C74B4")
btn.grid(row=1, column=2)

#btn = Button(f, text="Launch XDFL Viewer", command=launchseraphprint, height=3, width=28, fg="white", bg="#2C74B4")    ## uncomment and delete spacer frames to remove spaces
#btn.grid(row=2, column=2)

btn = Button(f, text="Click to launch SeraphPrint", command=launchseraphprint, height=3, width=45, fg="white", bg="#9DC3E6")
btn.grid(row=1, column=3)


spacerframe2 = Frame(tk, bg = "white", width = 1000, height = 10)
spacerframe2.pack(fill=X)

f = Frame(tk, bg = "white", width = 1000, height = 150)
f.pack(fill=X)

btn = Button(f, text="Click to launch Material Calibrator", command=launchcalibrator, height=3, width=60, fg="white", bg="#1F4E79")
btn.grid(row=2, column=1)

btn = Button(f, text="Launch XDFL Viewer", command=launchviewer, height=3, width=28, fg="white", bg="#2C74B4")
btn.grid(row=2, column=2)

btn = Button(f, text="Quit LabManager", command=quit, height=3, width=45, fg="white", bg="#9DC3E6")
btn.grid(row=2, column=3)


## File Menu

menubar = Menu(tk)  

def hello():            #test function; delete at end of dev
    print ("hello!")

    
## create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

# Essential Tools Menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Launch Seraph Studio", command=launchseraphstudio)
editmenu.add_command(label="Launch Seraph Print", command=launchseraphprint)
menubar.add_cascade(label="Essential Tools", menu=editmenu)

# Optional & Advanced Tools menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Calibrate New Material", command=launchcalibrator)
editmenu.add_separator()
editmenu.add_command(label="Manipulate and Merge XDFL Files", command=launchmanipulator)
editmenu.add_command(label="Visualize XDFL Layers", command=launchviewer)
menubar.add_cascade(label="Optional & Advanced Tools", menu=editmenu)


# Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Launch Seraph Robotics Website", command=launchwebsite)
helpmenu.add_separator()
## need to add functions for this
helpmenu.add_command(label="View Software Guide", command=swguide)
helpmenu.add_command(label="View XDFL & Calibration Guide", command=xdfl)
#helpmenu.add_command(label="View Assembly Instructions", command=launchwebsite)
helpmenu.add_separator()
helpmenu.add_command(label="Heated Tray Specs", command=heatedtray)
helpmenu.add_command(label="Temperature controller Specs", command=tempctrl)
helpmenu.add_command(label="USB Microscope Tool Specs", command=usbmcr)
helpmenu.add_command(label="UV Tool Specs", command=uvspcs)
menubar.add_cascade(label="Help Manuals & Specs", menu=helpmenu)

# display the menu
tk.config(menu=menubar)

mainloop()
