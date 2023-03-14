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
                         # time
                         types.double,
                         # cj: inverse of the timestep - subtract from diagonal(!)
                         types.CPointer(types.double),
                         # y: state vector
                         types.CPointer(types.double),
                         # yp: derivative vector
                         types.CPointer(types.double),
                         # JJ: storage for Jacobian
                         types.CPointer(types.double),
                         # user_data: user data (parameters)
                         )

# Load NumbaIDA library
rootdir = os.path.dirname(os.path.realpath(__file__))+'/'

# Get wrapper library
lib_name = "libNumbaIDA"
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
    # func_ptr
    ct.c_void_p,
    # jac_ptr
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
    # t_eval
    ct.c_void_p,
    # usol
    ct.c_void_p,
    # rtol
    ct.c_double,
    # avtol
    ct.c_void_p,
    # success
    ct.c_void_p,
    # nmaxsteps
    ct.c_int]

# Status returned via success parameter
ida_wrapper.restype = None


@njit
def ida(func_ptr, u0, du0, nres, t_eval, data=np.array([0.0], np.float64),
        rtol=1.0e-3, atol=1e-03, jac_ptr=0, nmaxsteps=-1):

    neq = len(u0)
    assert(len(u0) == len(du0))

    # Setup vector or absolute tolerances (one per residual)
    avtol = np.full(neq, atol)

    nt = len(t_eval)
    usol = np.full((nt, neq), np.nan, dtype=np.float64)
    success = np.array((1,), np.int32)

    ida_wrapper(func_ptr, jac_ptr, neq, u0.ctypes.data, du0.ctypes.data,
                data.ctypes.data, nt,
                t_eval.ctypes.data, usol.ctypes.data, rtol, avtol.ctypes.data,
                success.ctypes.data, nmaxsteps)

    bool_success = (success[0] == 0)
    return usol, bool_success
