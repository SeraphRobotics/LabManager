from distutils.core import setup  
import py2exe  
  
setup(windows=[{
        "script":'mainwindow.py',
        "icon_resources":[(1,"small.ico"),(2,"Main.ico")]
        }],
      data_files = [
            ('imageformats', [
              r'C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll'
              ])],
      zipfile = None,
      options={"py2exe": {
                        "includes": ["sip", "PyQt4.QtGui"],
                        "bundle_files":1,
                        "dll_excludes":["QtCore4.dll","QtGui4.dll"]
                        }
              }
     ) 
	 
	 
'''
FROM :http://www.py2exe.org/index.cgi/Py2exeAndPyQt 
PyQt4 and image loading (JPG, GIF, etc)

PyQt4 uses plugins to read those image formats, so you'll need to copy the folder PyQt4\plugins\imageformats to <appdir>\imageformats. Like in the above cases, you can use data_files for this. This won't work with bundle_files on.

If the plugins are not reachable, then QPixmap.load/loadFromData will return False when loading an image in those formats.

This will work with bundle_files as well, but you need to exclude the Qt DLLs from bundle (using the dll_excludes option) and add them to the directory with the executable through some other mechanism (such as data_files).

Make sure to copy the QtCore files from the PyQt direcrtory and not from the Qt directory.

Failing to do so will cause compiling errors


'''