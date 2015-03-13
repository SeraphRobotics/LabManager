from Tkinter import *
import tkFileDialog
import tkMessageBox

tk = Tk()
canvas = Canvas(tk, width=275, height=100)
canvas.pack()
myimage = PhotoImage(file=r"files\calibrator.gif")
tk.wm_iconbitmap(bitmap = r"files\main.ico")
canvas.create_image(0, 0, anchor=NW, image=myimage)
tk.title("Seraph Scientist Calibrator(TM) v1.0")
tk.resizable(0, 0)

#Default Value Settings
pwdefault="1.2"
pldefault="1.2"
phdefault="1.2"
psdefault="1.2"
acdefault="1"
namedefault="default_name"
descriptiondefault="default description"
materialdefault="default_material"

#inputs for title

fr = Frame(tk, bg = "white")
fr.pack(fill=X)

name = StringVar()
L1 = Label(fr, text="Name:")
L1.grid(column=1, row=1)
e = Entry(fr, textvariable=name, bd=5, width=25)
e.grid(column=2, row=1)
e.delete(0, END)
e.insert(0, namedefault) #default value

description = StringVar()
L1 = Label(fr, text="Description:")
L1.grid(column=1, row=2)
e = Entry(fr, textvariable=description, bd=5, width=25)
e.grid(column=2, row=2)
e.delete(0, END)
e.insert(0, descriptiondefault) #default value

material = StringVar()
L1 = Label(fr, text="Material:")
L1.grid(column=1, row=3)
e = Entry(fr, textvariable=material, bd=5, width=25)
e.grid(column=2, row=3)
e.delete(0, END)
e.insert(0, materialdefault) #default value



#inputs for settings
f = Frame(tk, bg = "white", width = 1000, height = 15)
f.pack(fill=X)

pw = StringVar()
L1 = Label(f, text="Path Width (mm):")
L1.grid(column=1, row=1)
e = Entry(f, textvariable=pw, bd=5, width=6)
e.grid(column=2, row=1)
e.delete(0, END)
e.insert(0, pwdefault) #default value


pl = StringVar()
L1 = Label(f, text="Path Length(mm):")
L1.grid(column=1, row=2)
e = Entry(f, textvariable=pl, bd=5, width=6)
e.grid(column=2, row=2)
e.delete(0, END)
e.insert(0, pldefault) #default value

ph = StringVar()
L1 = Label(f, text="Path Height(mm):")
L1.grid(column=1, row=3)
e = Entry(f, textvariable=ph, bd=5, width=6)
e.grid(column=2, row=3)
e.delete(0, END)
e.insert(0, phdefault) #default value

ps = StringVar()
L1 = Label(f, text="Path Speed(mm/s):")
L1.grid(column=1, row=4)
e = Entry(f, textvariable=ps, bd=5, width=6)
e.grid(column=2, row=4)
e.delete(0, END)
e.insert(0, psdefault) #default value

ac = StringVar()
L1 = Label(f, text="Area Constant (0.5-->1.5):")
L1.grid(column=1, row=5)
e = Entry(f, textvariable=ac, bd=5, width=6)
e.grid(column=2, row=5)
e.delete(0, END)
e.insert(0, acdefault) #default value

# Calculate Deposition rate from Area Constant, return as string for createscript function to put into xml
def depositionrate(ac): 
    rate =  float(ac.get())/ (3.14159265*64/float(ac.get())/float(ac.get()))
    rate_str = str(rate)
    return rate_str
    
#Control Buttons


#create labels for notes_output
import time 
settings = "Calibration settings file called: " + name.get() + "created at:  " + time.asctime() + " for Material:" + material.get() + "_______" + "path width" + pw.get()+ "path height" + ph.get() + "path speed" + ps.get() + "area constatn" + ac.get()

#output a txt file with settings so dont need to touch xml

def createnotes():  ## an old fxn that saves notes to set folder, notes_saveas replaces this - just here for syntax reference FYI
    notes_output= settings
    filename1="calibration_notes\\"+name.get()+".txt"
    file = open(filename1, "w")
    file.write(notes_output)
    file.close()

def notes_saveas():     #outputs notes to a file you can save as in directory of choice
    notes_output= settings
    filename1=tkFileDialog.asksaveasfilename(initialdir = "C:/",title = "choose your file",filetypes = (("txt files","*.txt"),("all files","*.*")), defaultextension=".txt")
    file = open(filename1, "w")
    file.write(notes_output)
    file.close()

###### create xml tool script #######

def createscript():

    variablename = name.get()+material.get()

    part1='''<toolScript name="'''
    part2='''"
            description="'''
    part3='''"
	    printer="Seraph">

	<settings>
		<printAcceleration text="Print Acceleration" units="mm/s^2">100</printAcceleration>
	</settings>
	<tool name="Blue Taper Silicone" material="'''
    part3b='''" scriptVariable="'''+variablename+'''">
		<settings>
			<sliceHeight text="Slice Height" units="mm">'''
    part4='''</sliceHeight>
			<pathSpeed text="Path Speed" units="mm/s">'''
    part5='''</pathSpeed>
			<pathWidth text="Path Width" units="mm">'''
    part6='''</pathWidth>
			<depositionRate text="DepositionRate" units="mm/mm">'''
    part7='''</depositionRate>
			<pushout text="Pushout" units="seconds">0.2</pushout>
			<suckback text="Suckback" units="seconds">0.2</suckback>
			<suckbackDelay text="Suckback Delay" units="seconds">0</suckbackDelay>
			<clearance text="Clearance" units="mm">4</clearance>
			<pausePaths text="Pause after # Paths" units="# of paths">300</pausePaths>
			<pitch text="Pitch" units="?">0.000397</pitch>
		</settings>
	</tool>
	<printScript>
<![CDATA[
function makeCalib(x){
  x.CompressionVolume = (x.pushout+x.suckback)*.5*5000*x.pitch;
  x.AreaConstant  = x.depositionRate*3.14159265*64/x.sliceHeight/x.pathWidth;

  y={pathSpeed: x.pathSpeed,
	 pathHeight: x.sliceHeight,
	 pathWidth: x.pathWidth,
	 areaConstant: x.AreaConstant,
	 compressionVolume: x.CompressionVolume
	}
  return y;
}

progress.setSteps('''+variablename+'''.meshes.length*2 + 4);

slicer.setSliceHeight('''+variablename+'''.sliceHeight);
pather.set("PathWidth", '''+variablename+'''.pathWidth);
for (var i = 0; i < '''+variablename+'''.meshes.length; ++i) {
  progress.log("Slicing Silicone Mesh");
  slicer.doSlicing('''+variablename+'''.meshes[i]);
  progress.step();
  progress.log("Pathing Silicone Mesh");
  pather.doPathing('''+variablename+'''.meshes[i]);
  progress.step();
}

var blueSiliconeDisplacementMaterialCalibration = makeCalib('''+variablename+''');

var fabWriter = fabFile.fabAtHomeModel2Writer();

fabWriter.addMeshes("'''+variablename+'''", blueSiliconeDisplacementMaterialCalibration, '''+variablename+'''.meshes);
progress.step();

fabWriter.sortBottomUp();
fabWriter.setPrintAcceleration(printAcceleration);

progress.step();
fabWriter.print();

progress.finish();

  ]]>
  </printScript>
</toolScript>'''

    toolscript=part1+name.get()+part2+description.get()+part3+material.get()+part3b+ph.get()+part4+ps.get()+part5+pw.get()+part6+depositionrate(ac)+part7

    ##saves in directory of choice, defaults to xml filetype, even w/o typing .xml extension ##
    filename1=tkFileDialog.asksaveasfilename(initialdir = ".",title = "Save in same folder as SeraphStudio.exe",filetypes = (("XDFL/XML files","*.xml"),("all files","*.*")), defaultextension=".xml")
    if (filename1):
        try:
            file = open(filename1, "w")
            file.write(toolscript)
            file.close()
        except:
            tkMessageBox.showinfo("Error", "could not write to"+filename1)

    
#control buttons using fxn above

frm = Frame(tk, bg = "white", width = 1000, height = 20)
frm.pack(fill=X)

btn = Button(frm, text="Generate ToolScript with Calibration Settings", command=createscript, fg="white", bg="#1F4E79", wraplength=275)
btn.grid(row=1, column=1)

btn = Button(frm, text="Save *txt file with Notes of Calibration Settings", command=notes_saveas, fg="white", bg="#1F4E79", wraplength=275)
btn.grid(row=2, column=1)

## File Menu

menubar = Menu(tk)  

## Launch external URLs for website in help menu
def launchwebsite():
    import webbrowser
    webbrowser.open('http://www.seraphrobotics.com')

    
def hello():            #test function; delete at end of dev
    print ("hello!")

    
## create a pulldown menu, and add it to the menu bar
##filemenu = Menu(menubar, tearoff=0)
##filemenu.add_command(label="Exit", command=quit)
##menubar.add_cascade(label="File", menu=filemenu)

# Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Launch Seraph Robotics Website", command=launchwebsite)
helpmenu.add_separator()
## need to add functions for this
#helpmenu.add_command(label="View Software Guide", command=launchwebsite)
#helpmenu.add_command(label="View XDFL & Calibration Guide", command=launchwebsite)
#helpmenu.add_command(label="View Assembly Instructions", command=launchwebsite)
#menubar.add_cascade(label="Help Manuals", menu=helpmenu)

# display the menu
tk.config(menu=menubar)


mainloop()
