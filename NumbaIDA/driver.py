import ctypes as ct
import ctypes.util as util
import os
import platform

import numpy as np
from numba import njit, types

ida_sig = types.void(types.double,
                     types.CPointer(types.double),
                     types.CPointer(types.double),
                     types.CPointer(types.double),
                     types.CPointer(types.double))

ida_jac_sig = types.void(types.double,
                         types.CPointer(types.double))


# # Find and load ida
# libida_path = util.find_library("sundials_ida")
# print(f"found ida at {libida_path}")
# ct.cdll.LoadLibrary(libida_path)

rootdir = os.path.dirname(os.path.realpath(__file__))+'/'
lib_name = "libNumbaIDA"
# Get wrapper library
if platform.uname()[0] == "Windows":
    ext = ".dll"
elif platform.uname()[0] == "Linux":
    ext = ".so"
else:
    ext = ".dylib"

name = lib_name + ext
libida = ct.cdll.LoadLibrary(rootdir+name)

# Setup ida_wrapper function from IDAWrapper.cpp
ida_wrapper = libida.ida_wrapper
ida_wrapper.argtypes = [
    # F_func
    ct.c_void_p,
    # neq
    ct.c_int,
    # u0
    ct.c_void_p,
    # du0
    ct.c_void_p,
    # data
    ct.c_void_p,
    # nt
    ct.c_int,
    # teval
    ct.c_int,
    # usol
    ct.c_void_p,
    # rtol
    ct.c_double,
    # avtol
    ct.c_void_p,
    # success
    ct.c_void_p,
    # maxsteps
    ct.c_int
]

# Status returned via success parameter
ida_wrapper.restype = None


@njit
def ida(funcptr, u0, du0, res, t_eval, data=np.array([0.0], np.float64),
        rtol=1.0e-3, atol=1e-03, maxsteps=10000):

    ida_success = np.array((2,), np.int32)

    avtol = np.full(len(res), atol)

    neq = len(u0)
    nt = len(t_eval)
    usol = np.full((nt, neq), np.nan, dtype=np.float64)

    ida_wrapper(funcptr, neq, u0.ctypes.data, du0.ctypes.data,
                data.ctypes.data, nt, t_eval.ctypes.data, usol.ctypes.data,
                rtol, avtol.ctypes.data, ida_success.ctypes.data, maxsteps)

    return usol, ida_success
