#!/usr/bin/env python3

import os

import matplotlib.pyplot as plt
import numba
import numpy as np
from numba import cfunc, njit

import NumbaIDA

p = np.array((2.26E-4, 6.99E-2, 3.44E-5, 5.460E-2, 0.0873,
              8.91E-3, 5.15E-3, 0.003158))


@njit
def get_rates(p, V):
    rates = np.empty((4,))

    for i in range(len(rates)):
        rates[i] = p[2*i] * np.exp(p[2*i + 1] * V * (-1)**(i))

    return rates


@njit
def voltage_func(t):
    if t < 100:
        return -80
    elif t < 500:
        return 0
    elif t < 1000:
        return 40
    elif t < 1500:
        return -40
    else:
        return -80


@njit
def f_deriv(t, u, p):
    V = voltage_func(t)
    k1, k2, k3, k4 = get_rates(p, V)

    O = u[0]
    I = u[1]
    IC = u[2]
    C = u[3]

    du = np.empty((4,))

    du[0] = -O * (k2 + k3) + k4 * I + k1 * C
    du[1] = -I * (k2 + k4) + k1 * IC + k3 * O
    du[2] = -IC * (k4 + k1) + k2 * I + k3 * C
    du[3] = -C * (k3 + k1) + k4 * IC + k2 * O

    return du


# Use X = (O I IC C)^T
# Define residual function
@cfunc(NumbaIDA.ida_sig)
def res_func(t: np.float64, u: np.array, du: np.array, res: np.array,
             p: np.array):

    u_vec = numba.carray(u, 4)
    p_vec = numba.carray(p, 4)
    derivs = f_deriv(t, u_vec, p_vec)

    # Set residuals
    for i in range(4):
        res[i] = derivs[i] - du[i]

    res[4] = u[0] + u[1] + u[2] + u[3] - 1


def main():
    output_dir = "example_output"
    func_ptr = res_func.address
    u0 = np.array([0, 0, 0, 1], dtype=np.float64)
    du0 = f_deriv(0, u0, p).astype(np.float64)
    print(f"du0 = {du0}")
    print(f"u0 = {u0}")
    res = np.empty((5,), dtype=np.float64)
    t_eval = np.linspace(0, 2000, 20000)

    sol, success = NumbaIDA.ida(func_ptr, u0, du0, res, t_eval, p)

    print(f"Successful: {success}")
    print(sol)
    plt.plot(t_eval, sol)
    plt.legend(("O", "I", "IC", "C"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.savefig(os.path.join(output_dir, "herg_channel_example_plot.png"))


if __name__ == "__main__":
    main()
