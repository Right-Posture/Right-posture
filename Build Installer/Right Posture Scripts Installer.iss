; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Right Posture"
#define MyAppVersion "1.1.8.5"
#define MyAppPublisher "Right Posture TEAM"
#define MyAppURL "https://github.com/astrrr/Right-posture"
#define MyAppExeName "main.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

#define AppId "{3D7B9F82-D821-46F3-B4E0-CB6EA4F093C3}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{3D7B9F82-D821-46F3-B4E0-CB6EA4F093C3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Build Installer\Info.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=admin
OutputDir=C:\Users\Mero Asebi\Downloads
OutputBaseFilename=Right Posture
SetupIconFile=C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[CustomMessages]
english.NewerVersionExists=A newer version of {#MyAppName} is already installed.%nDo you want to uninstall it?%n%nInstaller version: {#MyAppVersion}%nCurrent version: 
english.OlderVersionExists=An old version of {#MyAppName} was detected.%nDo you want to uninstall it?

[Code]
function GetUninstallString: string;
var
  sUnInstPath: string;
  sUnInstallString: String;
begin
  Result := '';
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{{#AppId}_is1'); { Your App GUID/ID }
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade: Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function InitializeSetup: Boolean;
var
  V: Integer;
  iResultCode: Integer;
  sUnInstallString: string;
  Version: String;
  Text: String;
begin
  Result := True; { in case when no previous version is found }
  if RegValueExists(HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#AppId}_is1', 'UninstallString') then  { Your App GUID/ID }
  begin
    RegQueryStringValue(HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#AppId}_is1', 'DisplayVersion', Version);
    if Version > '{#MyAppVersion}' then
      begin
        Text := ('{cm:NewerVersionExists} '+Version);
        Result := False;
      end
    else
      begin
        Text := ('{cm:OlderVersionExists} ');
        Result := True;
      end;
    V := MsgBox(ExpandConstant(Text), mbInformation, MB_YESNO); { Custom Message if App installed }
    if V = IDYES then
    begin
      sUnInstallString := GetUninstallString();
      sUnInstallString :=  RemoveQuotes(sUnInstallString);
      Exec(ExpandConstant(sUnInstallString), '', '', SW_SHOW, ewWaitUntilTerminated, iResultCode);
      Result := True; { if you want to proceed after uninstall }
      { Exit; //if you want to quit after uninstall }
    end
    else
      Result := False; { when older version present and not uninstalled }
  end;
end;

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: "{app}"; Permissions: everyone-full

[Files]
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\python3.dll"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\python39.dll"; DestDir: "{app}"; Flags: ignoreversion; Permissions: everyone-full
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\themes\*"; DestDir: "{app}\themes"; Flags: ignoreversion recursesubdirs; Permissions: everyone-full
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs; Permissions: everyone-full
Source: "C:\Users\Mero Asebi\Documents\GitHub\Right-posture\Right Posture\build\exe.win-amd64-3.9\bin\*"; DestDir: "{app}\bin"; Flags: ignoreversion recursesubdirs; Permissions: everyone-full
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: runascurrentuser nowait postinstall skipifsilent;

