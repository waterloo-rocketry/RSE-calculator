#!/usr/bin/env/python

from constants import NitrousOxideProperties
from constants import EquationConstants
from constants import pascals_to_psi
from math import exp

class VapourPressureCalculations:
    '''
    Establish the vapour pressure of NOS between -90 and 36 degrees Celsius
    '''
    def eqn4_1(self, curr_t_reduced, curr_one_minus_t_reduced):
        '''
        Implementation of Equation 4.1 to solve for pressure in kPa

        Parameters
        ----------
        curr_t_reduced: float
            Reduced temperature; defined as: Temp / CriticalTemp.

        curr_one_minus_t_reduced: float
            Equal to one minus the reduced temperature.
        '''
        #Using Equation 4.1 to solve for pressure
        result = NitrousOxideProperties.critical_pressure * exp((1/curr_t_reduced)*\
                 (EquationConstants.eqn4_1[1]*curr_one_minus_t_reduced +\
                 EquationConstants.eqn4_1[2]*curr_one_minus_t_reduced**(1.5) +\
                 EquationConstants.eqn4_1[3]*curr_one_minus_t_reduced**(2.5) +\
                 EquationConstants.eqn4_1[4]*curr_one_minus_t_reduced**5))
        return result #Return pressure

    def __init__(self):
        #Temperature values ranging from -90 to 36 degrees celsius
        self.t_deg_c = range(-90,37)
        #Converting t_deg_c into Kelvin
        self.t_kelvin = [x + 273.15 for x in self.t_deg_c]
        #Reduced temperature for each temperature step
        self.t_reduced = [x / NitrousOxideProperties.critical_temp for x in self.t_kelvin]
        #One minus the reduced temperature for each temperature step
        self.one_minus_t_reduced = [1 - x for x in self.t_reduced]
        #Pressure at each temperature step found using Equation 4.1
        self.pressure_kpa = [self.eqn4_1(x,y) for x,y in zip(self.t_reduced,self.one_minus_t_reduced)]
        #Pressure at each temperature step converted to psi
        self.pressure_psi = [pascals_to_psi(x * 1000) for x in self.pressure_kpa]

if __name__ == '__main__':
    test_data = VapourPressureCalculations()
    test_file = open('vapour_pressure_test.csv','w')

    i = 0
    while i < len(test_data.t_deg_c):
        test_file.write(f'{test_data.t_deg_c[i]},{test_data.t_kelvin[i]},{test_data.t_reduced[i]}'\
            +f',{test_data.one_minus_t_reduced[i]},{test_data.pressure_kpa[i]},'+\
            f'{test_data.pressure_psi[i]}\n')
        i += 1

    test_file.close()