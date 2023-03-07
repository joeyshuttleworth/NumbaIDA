#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <mutex>

#include <cmath>

#include <ida/ida.h>
#include <nvector/nvector_serial.h>
#include <sundials/sundials_types.h>
#include <sunlinsol/sunlinsol_dense.h>        /* access to dense SUNLinearSolver      */

#include "IDAWrapper.hpp"

/* Used to store the users function.

   We're using the primitives instead of Sundials' types because the
   function is generated by Numba.
 */
void (*tmp_func)(double, double*, double*, double*, double*);

void (*tmp_jac)(double, double, double*, double*, double*, double*);

/* Mutex to protect tmp_func and tmp_jac from being modified during ida_wrapper call*/
std::mutex ida_wrapper_mutex;

/* Evaluate the users function (if it has been defined) */
static int translated_func(realtype t, N_Vector u, N_Vector du, N_Vector resval,
                       void *data)
{
  if(tmp_func == nullptr) {
    return -1;
  }      {tmp_func(static_cast<double>(t), static_cast<double*>NV_DATA_S(u), static_cast<double*>NV_DATA_S(du),
             static_cast<double*>NV_DATA_S(resval), static_cast<double*>(data));
}
  return 0;
}

static int translated_jacobian_func(realtype  tt,  realtype  cj,
                                    N_Vector yy, N_Vector    yp, N_Vector  /*resvec*/,
                                    SUNMatrix  JJ, void * user_data,
                                    N_Vector  /*tempv1*/, N_Vector  /*tempv2*/, N_Vector  /*tempv3*/){
  if(tmp_jac == nullptr) {
    return -1;
}

  tmp_jac(double(tt), double(cj), static_cast<double*>NV_DATA_S(yy), static_cast<double*>NV_DATA_S(yp),
           static_cast<double*>NV_DATA_S(JJ), static_cast<double*>(user_data));
  return 0;
}


static int check_retval(void *returnvalue, const char *funcname, int opt)
{
  int *retval = nullptr;
  /* Check if SUNDIALS function returned NULL pointer - no memory allocated */
  if (opt == 0 && returnvalue == nullptr) {
    fprintf(stderr,
            "\nSUNDIALS_ERROR: %s() failed - returned NULL pointer\n\n",
            funcname);
    return(1);
  } if (opt == 1) {
    /* Check if retval < 0 */
    retval = static_cast<int *>(returnvalue);
    if (*retval < 0) {
      fprintf(stderr,
              "\nSUNDIALS_ERROR: %s() failed with retval = %d\n\n",
              funcname, *retval);
      return(1);
    }
  } else if (opt == 2 && returnvalue == nullptr) {
    /* Check if function returned NULL pointer - no memory allocated */
    fprintf(stderr,
            "\nMEMORY_ERROR: %s() failed - returned NULL pointer\n\n",
            funcname);
    return(1);
  }

  return(0);
}


extern "C"{
#include <unistd.h>

  void ida_wrapper(void (*F_func)(double, double*, double*, double*, double*),
                   void (*jac_func)(double, double, double*, double*, double*, double*),
                   int neq, double* u0, const double* du0, double*  /*res*/,
                   double* data, int  /*data_size*/, int nt, const double* teval,
                   double* usol, double rtol,
                   double* avtol, int* success){


    int retval = 0;
    SUNContext ctx = nullptr;

    retval = SUNContext_Create(nullptr, &ctx);
    void* ida_mem = IDACreate(ctx);

    if(check_retval(ida_mem, "IDACreate", 0) != 0){
      *success = -1;
      printf("Failed to create IDA solver\n");
      return;
    }

    N_Vector y = N_VNew_Serial(neq, ctx);
    N_Vector dydt = N_VNew_Serial(neq, ctx);

    /* Set user config data */
    retval = IDASetUserData(ida_mem, &data);
    // printf("Set user data \n");

    *success = 1;

    for(int i = 0; i < neq; i++){
      NV_Ith_S(y, i) = u0[i];
      NV_Ith_S(dydt, i) = du0[i];
      usol[i] = u0[i];
      // printf("%f ", u0[i]);
    }

    double t = teval[0];
    double tout = NAN;

    /* Lock the mutex to protect the global function pointers */
    std::lock_guard<std::mutex> guard(ida_wrapper_mutex);

    /* Set global function pointers for 'translated functions' */
    tmp_func = F_func;
    tmp_jac  = jac_func;

    retval = IDAInit(ida_mem, &translated_func, teval[0], y, dydt);

    N_Vector nvec_avtol = N_VNew_Serial(neq, ctx);
    NV_DATA_S(nvec_avtol) = avtol;

    retval = IDASVtolerances(ida_mem, rtol, nvec_avtol);
    if(check_retval(&retval, "IDASVtolerances", 1) != 0){
      *success = -1;
      return;
    }

    /* Create dense SUNMatrix for use in linear solves */
    SUNMatrix A = SUNDenseMatrix(neq, neq, ctx);
    SUNLinearSolver LS = SUNLinSol_Dense(y, A, ctx);
    if(check_retval((void *)A, "SUNDenseMatrix", 0) != 0){*success = -1; goto cleanup;}

    /* Create dense SUNLinearSolver object */
    if(check_retval((void *)LS, "SUNLinSol_Dense", 0) != 0){*success = -1; goto cleanup;}

    /* Attach the matrix and linear solver */
    retval = IDASetLinearSolver(ida_mem, LS, A);
    if(check_retval(&retval, "IDASetLinearSolver", 1) != 0){*success = -1; goto cleanup;}

    /* Set the user-supplied Jacobian routine */
    if(jac_func != nullptr)
      {
        retval = IDASetJacFn(ida_mem, translated_jacobian_func);
        if(check_retval(&retval, "IDASetJacFn", 1) != 0){*success=-1; return;}
      }

    /* Set max steps */
    retval = IDASetMaxNumSteps(ida_mem, maxsteps);
    if(check_retval(&retval, "IDASetMaxNumStep", 1) != 0){*success=-1; goto cleanup;}

    for (int i = 1; i < nt; i++){
      // printf("Doing integration step %i\n", i);
      if (teval[i] < teval[i-1]){
        *success = 0;
        return;
      }

      tout = teval[i];

      retval = IDASolve(ida_mem, tout, &t, y, dydt, IDA_NORMAL);

      if (retval != 0){
        // there is a problem!
        *success = retval;
        return;
      }
      // save solution
      for (int j = 0; j < neq; j++){
        usol[j + neq*i] = NV_Ith_S(y, j);
      }
    }
    /* Ran successfully */
    *success = 0;

  cleanup:
    IDAFree(&ida_mem);

    /* Free vectors */
    N_VDestroy(y);
    N_VDestroy(dydt);
}
}
