cd "D:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-DYNA\env.ps1"
Set-Alias lspp $ENV:ANSYS_STUDENT_LSDYNA_LSPREPOST_PATH
cd "C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization"
lspp c=output\c_files\test2.cfile -nographics