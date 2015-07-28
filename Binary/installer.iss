 [Setup]
AppName=Seraph Lab Manager
AppVersion=1.0
DefaultDirName={pf}\Seraph Robotics
DefaultGroupName = Seraph Lab Manager
LicenseFile=license.txt

[Dirs]
Name: "{app}\calibrator"
Name: "{app}\documents"
Name: "{app}\files"
Name: "{app}\manipulator"
Name: "{app}\SeraphPrint"
Name: "{app}\SeraphStudio"
Name: "{app}\tcl"
Name: "{app}\viewer"

[Files]
Source: "calibrator\*"; DestDir:"{app}\calibrator"; Flags: recursesubdirs
Source: "documents\*"; DestDir:"{app}\documents"; Flags: recursesubdirs
Source: "files\*"; DestDir:"{app}\files"; Flags: recursesubdirs
Source: "manipulator\*"; DestDir:"{app}\manipulator"; Flags: recursesubdirs
Source: "SeraphPrint\*"; DestDir:"{app}\SeraphPrint"; Flags: recursesubdirs
Source: "SeraphStudio\*"; DestDir:"{app}\SeraphStudio"; Flags: recursesubdirs
Source: "tcl\*"; DestDir:"{app}\tcl"; Flags: recursesubdirs
Source: "viewer\*"; DestDir:"{app}\viewer"; Flags: recursesubdirs
Source: "Seraph Lab Manager.exe"; DestDir:"{app}";
Source: "tcl85.dll"; DestDir:"{app}";
Source: "tk85.dll"; DestDir:"{app}";

[Icons]
Name: "{commondesktop}\Seraph Lab Manager"; Filename: "{app}\Seraph Lab Manager.exe"; WorkingDir: "{app}" ; IconFilename: "{app}\files\Main.ico"
Name: "{commonprograms}\Seraph Lab Manager"; Filename: "{app}\Seraph Lab Manager.exe"; WorkingDir: "{app}"; IconFilename: "{app}\files\Main.ico"