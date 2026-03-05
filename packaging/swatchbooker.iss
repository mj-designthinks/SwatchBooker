; swatchbooker.iss - Inno Setup script for SwatchBooker Windows installer
;
; Build with:
;   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" packaging\swatchbooker.iss
; (or let build-windows.bat call it automatically)

#define AppName      "SwatchBooker"
#define AppVersion   "0.8"
#define AppPublisher "Olivier Berten"
#define AppURL       "https://github.com/olivierberten/SwatchBooker"
#define AppExeName   "SwatchBooker.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=..\src\COPYING
OutputDir=..\dist
OutputBaseFilename=SwatchBooker-Setup
SetupIconFile=..\data\swatchbooker.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Require Windows 10 or later
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; SwatchBooker editor (PyInstaller --onedir output)
Source: "..\dist\SwatchBooker\*"; DestDir: "{app}\SwatchBooker"; Flags: ignoreversion recursesubdirs createallsubdirs
; SBConvertor batch converter (PyInstaller --onedir output)
Source: "..\dist\SBConvertor\*";  DestDir: "{app}\SBConvertor";  Flags: ignoreversion recursesubdirs createallsubdirs
; liblcms2.dll — copy into both app directories (must be in repo root before building)
Source: "..\liblcms2.dll"; DestDir: "{app}\SwatchBooker"; Flags: ignoreversion; Check: FileExists('..\liblcms2.dll')
Source: "..\liblcms2.dll"; DestDir: "{app}\SBConvertor";  Flags: ignoreversion; Check: FileExists('..\liblcms2.dll')

[Icons]
Name: "{group}\{#AppName}";                        Filename: "{app}\SwatchBooker\{#AppExeName}"
Name: "{group}\SB Convertor";                      Filename: "{app}\SBConvertor\SBConvertor.exe"
Name: "{group}\{cm:UninstallProgram,{#AppName}}";  Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}";                  Filename: "{app}\SwatchBooker\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\SwatchBooker\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
