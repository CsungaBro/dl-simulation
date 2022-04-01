cd "D:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-DYNA"
Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH
cd "C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization"
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_0_120x120x27.5_R6.5\sim_0_120x120x27.5_R6.5.k -submit -cleanjobs
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_1_120x120x33.75_R6.5\sim_1_120x120x33.75_R6.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_2_120x120x33.75_R11.0\sim_2_120x120x33.75_R11.0.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_3_120x120x33.75_R15.5\sim_3_120x120x33.75_R15.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_4_120x120x40.0_R6.5\sim_4_120x120x40.0_R6.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_5_120x120x40.0_R11.0\sim_5_120x120x40.0_R11.0.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_6_120x120x40.0_R15.5\sim_6_120x120x40.0_R15.5.k -submit -wait -1
Start-Sleep 1
lsrun C:\Users\CsungaBro\Documents\code\dl-simulation\ls-dyna-automatization\output\k_files\sim_7_120x120x40.0_R20.0\sim_7_120x120x40.0_R20.0.k -submit -wait -1
Start-Sleep 1