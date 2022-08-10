import os
from ctypes import *

self_path = os.path.abspath(__file__)
working_dir = os.path.dirname(self_path)
os.chdir(working_dir)

#x86_64-w64-mingw32-gcc-win32 -fPIC -shared -o functions.so functions.c
function = CDLL(os.path.join(working_dir, "c_files/functions.so"))
function.hello.argtypes = [c_int]