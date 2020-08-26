#!/usr/bin/env/python

from constants import NitrousOxideProperties
from constants import EquationConstants
from constants import pascals_to_psi
from math import exp

class VapourPressureCalculations:
    def eqn4_1(curr_t_reduced, curr_one_minus_t_reduced):
        result = NitrousOxideProperties.critical_pressure * exp((1/curr_t_reduced)*\
                 (EquationConstants.eqn4_1[1]*curr_one_minus_t_reduced+EquationConstants.eqn4_1[2]*curr_one_minus_t_reduced**(1.5)\
                 +EquationConstants.eqn4_1[3]*curr_one_minus_t_reduced**(2.5)+EquationConstants.eqn4_1[4]*curr_one_minus_t_reduced**5))
        return result

    t_deg_c = range(-90,37)
    t_kelvin = [x + 273.15 for x in tDegC]
    t_reduced = [x / NitrousOxideProperties.critical_temp for x in t_kelvin]
    one_minus_t_reduced = [1 - x for x in t_reduced]
    pressure_kpa = [eqn4_1(x,y) for x,y in zip(t_reduced,one_minus_t_reduced)]
    pressure_psi = [pascals_to_psi(x * 1000) for x in pressure_kpa]