import sys
from cx_Freeze import setup, Executable

buildExeOptions = {"packages": ["os"], "includes": ["tkinter", "datetime", "psycopg2"], "include_files": ["crud.py"]}
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "gestão de estoque",
    version = "0.0.1b",
    description = "Versão beta da gestão de estoque da Frumar",
    options = {"build_exe": buildExeOptions},
    executables = [Executable(script="main.py", base=base)]
)