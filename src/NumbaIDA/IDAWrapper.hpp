#ifndef IDAWRAPPER_HPP
#define IDAWRAPPER_HPP

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ida/ida.h>
#include <sundials/sundials_types.h>
#include <nvector/nvector_serial.h>

extern "C"{
  void ida_wrapper(void (*F_func)(double, double*, double*, double*, double*),
                   void (*jac_func)(double, double, double*, double*, double*, double*),
                   int neq, double* u0, const double* du0, double* res, double* data,
                   int data_size, int nt, const double* teval, double* usol, double rtol,
                   double* avtol, int* success, int maxsteps);
}
#endif
