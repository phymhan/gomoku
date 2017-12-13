import cx_Freeze

executables = [cx_Freeze.Executable("fivechessonline21.py")]

cx_Freeze.setup(
    name = "Five-Chess",
    options = {"build_exe": {"packages": ["pygame"],
                             "include_files": ["./sources/pics/board.png",
                                               "./sources/pics/cp_k_29.png",
                                               "./sources/pics/cp_w_29.png",
                                               "./sources/pics/panel.png",
                                               "./sources/pics/catsmall.png",
                                               "./sources/music/BackgroundMusic.ogg",
                                               "./sources/music/Snd_click.ogg"]}},
    executables = executables
    )
##cx_Freeze.setup(
##    name = "Five-Chess",
##    options = {"build_exe": {"packages": ["pygame"],
##                             "include_files": ["board.png",
##                                               "cp_k_29.png",
##                                               "cp_w_29.png",
##                                               "panel.png",
##                                               "catsmall.png",
##                                               "BackgroundMusic.ogg",
##                                               "Snd_click.ogg"]}},
##    executables = executables
##    )
