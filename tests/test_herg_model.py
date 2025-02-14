import logging
import os
import unittest

import matplotlib.pyplot as plt
import numba
import numpy as np
from numba import cfunc, njit

import numbaida

# Parameters / user_data
p = np.array((2.26E-4, 6.99E-2, 3.44E-5, 5.460E-2, 0.0873,
              8.91E-3, 5.15E-3, 0.003158))


@njit
def get_rates(p, V):
    rates = np.empty((4,))
    rates[:] = 1e-5, 1e-5, 1e-5, 1e-5
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

    state_O = u[0]
    state_I = u[1]
    state_IC = u[2]
    state_C = u[3]

    du = np.empty((4,))

    du[0] = -state_O * (k2 + k3) + k4 * state_I + k1 * state_C
    du[1] = -state_I * (k2 + k4) + k1 * state_IC + k3 * state_O
    du[2] = -state_IC * (k4 + k1) + k2 * state_I + k3 * state_C
    du[3] = -state_C * (k3 + k1) + k4 * state_IC + k2 * state_O

    return du


# Use X = (O I IC C)^T
# Define residual function
@cfunc(numbaida.ida_sig)
def res_func(t: np.float64, u: np.array, du: np.array, res: np.array,
             p: np.array):

    u_vec = numba.carray(u, 4)
    du = numba.carray(du, 4)
    p_vec = numba.carray(p, 8).copy()
    derivs = f_deriv(t, u_vec, p_vec).flatten()

    # Set residuals
    res = numba.carray(res, 5)
    res[:derivs.shape[0]] = derivs - du[:derivs.shape[0]]
    res[-1] = u_vec.sum() - 1

    return None


@njit
def _jac_func(p, V):
    rates = get_rates(p, V)
    k1, k2, k3, k4 = rates

    jacobian = np.full((5, 5), 0.0)
    # Diagonals first
    jacobian[0, 0] = -k2 - k3
    jacobian[1, 1] = -k2 - k4
    jacobian[2, 2] = -k4 - k1
    jacobian[3, 3] = -k1 - k3

    # Open state
    jacobian[0, 1] = k4
    jacobian[0, 2] = 0
    jacobian[0, 3] = k1

    # Inactive state
    jacobian[1, 0] = k3
    jacobian[1, 2] = k1
    jacobian[1, 3] = 0

    # Inactive-Closed state
    jacobian[2, 0] = 0
    jacobian[2, 1] = k2
    jacobian[2, 3] = k3

    # Closed state
    jacobian[3, 0] = k2
    jacobian[3, 1] = 0
    jacobian[3, 0] = k4

    jacobian[4, :] = 0.0
    jacobian[:, 4] = 0.0

    return jacobian


@cfunc(numbaida.ida_jac_sig)
def jac_func(t, cj, y, yp, JJ, p):
    jacobian = numba.carray(JJ, (5, 5))
    p = numba.carray(p, 8).copy()

    V = voltage_func(t)
    jacobian[:, :] = _jac_func(p, V)[:, :]

    # Subtract cj
    jacobian -= np.eye(5)*cj

    return None


class TestHergModel(unittest.TestCase):
    def setUp(self):
        self.output_dir = os.path.join("test_output",
                                       f"{type(self).__name__}")

        # Get function pointers
        self.func_ptr = res_func.address
        self.jac_ptr = jac_func.address

        # Setup initial conditions
        self.u0 = np.array([0, 0, 0, 1, 0], dtype=np.float64)
        self.du0 = np.append(f_deriv(0, self.u0, p).astype(np.float64),
                             0.0)

    def test_solve(self):
        t_eval = np.linspace(0, 2000, 20000)

        sol, succ = numbaida.ida(
            self.func_ptr, self.u0, self.du0, t_eval, data=p.copy(),
            jac_ptr=self.jac_ptr
        )

        self.assertTrue(succ)
        self.assertTrue(np.all(np.isfinite(sol)))

        plt.plot(t_eval, sol)
        plt.legend(["O", "I", "IC", "C"])

        sol, succ = numbaida.ida(
            self.func_ptr, self.u0, self.du0, t_eval, data=p.copy(),
            jac_ptr=self.jac_ptr
        )

        self.assertTrue(succ)
        self.assertTrue(np.all(np.isfinite(sol)))

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        plt.savefig(os.path.join(self.output_dir,
                    "herg_channel_example_plot.png"))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()
