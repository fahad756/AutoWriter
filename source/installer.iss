; AutoWriter — Inno Setup Script
; Compiled by build_installer.bat

#define MyAppName      "AutoWriter"
#define MyAppVersion   "2.0"
#define MyAppPublisher "AutoWriter"
#define MyAppExeName   "AutoWriter.exe"
#define MyAppDesc      "Human-like typing automation"

[Setup]
AppId={{8F3A1C2D-4B5E-4F6A-9C7D-E8F1234567AB}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppComments={#MyAppDesc}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=AutoWriter_Setup_v2.0
SetupIconFile=autowriter.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Version metadata embedded in the Setup exe
VersionInfoVersion=2.0.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Setup
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCopyright=Copyright 2024 {#MyAppPublisher}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";  Description: "{cm:CreateDesktopIcon}";           GroupDescription: "{cm:AdditionalIcons}"
Name: "startupentry"; Description: "Launch AutoWriter when Windows starts"; GroupDescription: "Startup:"; Flags: unchecked

[Files]
; Main executable (built by PyInstaller)
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}";                     Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}";           Filename: "{uninstallexe}"
; Desktop (optional task)
Name: "{commondesktop}\{#MyAppName}";             Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Optional: run at startup
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
  ValueType: string; ValueName: "{#MyAppName}"; \
  ValueData: """{app}\{#MyAppExeName}"""; \
  Flags: uninsdeletevalue; Tasks: startupentry

[Run]
; Offer to launch after install
Filename: "{app}\{#MyAppExeName}"; \
  Description: "{cm:LaunchProgram,{#MyAppName}}"; \
  Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any generated files in the install dir
Type: files; Name: "{app}\*"
Type: dirifempty; Name: "{app}"
