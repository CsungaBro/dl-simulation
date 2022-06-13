cd "D:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-DYNA"
Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH
cd "C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization"
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_106_50x50x17.5_R6.5\sim_106_50x50x17.5_R6.5.k -submit -cleanjobs
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_107_50x50x23.75_R6.5\sim_107_50x50x23.75_R6.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_108_50x50x23.75_R11.0\sim_108_50x50x23.75_R11.0.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_109_50x50x23.75_R15.5\sim_109_50x50x23.75_R15.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_110_50x50x30.0_R6.5\sim_110_50x50x30.0_R6.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_111_50x50x30.0_R11.0\sim_111_50x50x30.0_R11.0.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_112_50x50x30.0_R15.5\sim_112_50x50x30.0_R15.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_113_50x50x30.0_R20.0\sim_113_50x50x30.0_R20.0.k -submit -wait -1
Start-Sleep 1