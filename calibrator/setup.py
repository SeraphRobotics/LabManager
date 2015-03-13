from distutils.core import setup  
import py2exe  
  
setup(windows=[{
        "script":'toolscriptGUI.py',
        "icon_resources":[(1,"files/small.ico"),(2,"files/Main.ico")]
        }],
      zipfile = None,
      options={"py2exe": {   
                        'includes': ['Tkinter'],
                        "bundle_files":1,
                        "dll_excludes":["tk85.dll","tcl85.dll"]
                        }
              }
     ) 
