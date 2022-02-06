import ctypes as ct
import ctypes.util as util
from numba import njit, types
import numpy as np
import os
import platform

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
ida_wrapper.argtypes = [ct.c_void_p, ct.c_int, ct.c_void_p, ct.c_void_p,
                        ct.c_void_p, ct.c_void_p, ct.c_int, ct.c_int,
                        ct.c_void_p, ct.c_void_p, ct.c_double, ct.c_void_p,
                        ct.c_void_p]

# Status returned via success parameter
ida_wrapper.restype = None


@njit
def ida(funcptr, u0, du0, res, t_eval, data=np.array([0.0], np.float64),
        rtol=1.0e-3, atol=1e-03):

    avtol = np.full(len(res), atol)

    neq = len(u0)
    print("neq is ", neq)
    print(u0)
    nt = len(t_eval)
    usol = np.full((nt, neq), np.nan, dtype=np.float64)
    success = np.array((2,), np.int32)

    ida_wrapper(funcptr, neq, u0.ctypes.data, du0.ctypes.data, res.ctypes.data,
                data.ctypes.data, len(data), nt, t_eval.ctypes.data,
                usol.ctypes.data, rtol, avtol.ctypes.data, success.ctypes.data)

    bool_success = (success[0] == 0)
    print("retval was:", success[0])
    return usol, bool_success
