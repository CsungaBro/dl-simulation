cd "D:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-DYNA"
Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH
cd "C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization"
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\50x50x20.0_R15.0\50x50x20.0_R15.0.k -submit -cleanjobs
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\50x50x6.0_R2.0\50x50x6.0_R2.0.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\50x50x7.27273_R2.0\50x50x7.27273_R2.0.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\50x50x7.27273_R3.18182\50x50x7.27273_R3.18182.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\50x50x8.54545_R2.0\50x50x8.54545_R2.0.k -submit -wait -1
Start-Sleep 1