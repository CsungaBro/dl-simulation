from post_proc import post_proc_curv_gen as ppcg

folder_path = 'output\k_files\sim_0_120x120x27.5_R6.5'
PVCG = ppcg.PyVistaCurvatureGenerator()
PVCG.main(folder_path)