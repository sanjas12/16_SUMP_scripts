#0.0.1.0
import sys
# import os
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "path": sys.path + ["src"],  # Добавляем путь к 'src'
    "excludes": ["tkinter", "unittest", "http",
                "pydoc_data", "email",
                "concurent", 
                # "xml",
                # "asyncio", "curses", "distutils", "html", "multiprocessing",
                "sqlite3", "test", "urlib"],
    "optimize": 0,      # c 2 exe не запускается
}

# base="Win32GUI" should be used only for Windows GUI app. If comment this line, will appear console
# base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Auto_back_up",
    #version=version.strip('#'),
    description="My Auto_back_up",
    options={"build_exe": build_exe_options},
    executables=[Executable("auto_back_up.py", target_name="Auto_back_up")],
)
