cd "D:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-DYNA"
Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH
cd "C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization"
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\test2\test2.k -submit -wait -1