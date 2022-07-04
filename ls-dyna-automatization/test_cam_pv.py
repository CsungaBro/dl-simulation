from post_proc import post_proc_curv_gen as cg


if __name__ == "__main__":
    # t_path = 'output\\k_files\\sim_7546_80.0x80.0x11.73_R7.36'
    t_path = 'output\\k_files\\sim_1087_25.45x63.64x15.27_R8.45'
    curv_generator = cg.PyVistaCurvatureGenerator()
    curv_generator.main(t_path)
    camera_pos = curv_generator.plotter.camera_position
    with open("camera_pos_test.txt", 'x') as fr:
        fr.write(camera_pos)
        print(camera_pos)
