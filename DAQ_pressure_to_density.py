#!/usr/bin/env/python

from vapour_pressure_calculations import VapourPressureCalculations
from DAQ_raw import DAQRaw
from constants import NitrousOxideProperties
from constants import EquationConstants

class DAQPressureToDensity:
    '''
    Use oxidizer tank pressure data to determine liquid and vapour NOS densities.
    '''

    def find_closest_match(value, matching_array):
        '''
        Finds and returns closest match (less than or equal to) to value in matching_array.
        Uses the fact that the values in matching_array are monotonically increasing

        Parameters
        ----------
        value: float
            Value to be compared against matching_array; seek to find closest equivalent in matching_array.
        matching_array: list of floats
            List of floats in increasing order where the closest match will occur.
        '''
        return_index = 0 #index of closest match
        curr_value = matching_array[return_index] #curr_value in matching_array being visited

        #Find closest value by checking until either end of list reached or curr_value >= value
        while return_index < len(matching_array) and value <= curr_value:
            return_index += 1
            curr_value = matching_array[return_index]
        
        #Subtract by one to accout for overshoot
        return return_index - 1

    def calculate_reduced_temp(self):
        '''
        Uses linear interpolation to calculates reduced temperature for each tank pressure.
        Stores results in self.t_reduced
        '''
       
        i = 0 #Current index being visited

        #Iterate through every tank pressure (all columns are same length so doesnt matter which length is checked here)
        while i < len(self.closest_p):
            frac = (DAQ_data.tank_pressure_psia[i] - self.closest_p[i]) / (self.next_p[i] - self.closest_p[i])
            result = frac + self.vapour_pressure_data.t_kelvin[self.index_with_closest_p[i]] / NitrousOxideProperties.critical_temp
            self.t_reduced.append(result)

    def eqn4_2(curr_one_minus_t_reduced):
        '''
        Implementation of Equation 4.2 to solve liquid NOS density in kg / m^3

        Parameters
        ----------
        curr_one_minus_t_reduced: float
            Equal to one minus the reduced temperature
        '''
        result = NitrousOxideProperties.critical_density * exp(EquationConstants.eqn4_2[1] * curr_one_minus_t_reduced**(1/3) +\
            EquationConstants.eqn4_2[2] * curr_one_minus_t_reduced**(2/3) + EquationConstants.eqn4_2[3] * curr_one_minus_t_reduced +\
            EquationConstants.eqn4_2[4] * curr_one_minues_t_reduced**(4/3))
        return result

    def eqn4_3(curr_recip_t_reduced_minus_one):
        '''
        Implementation of Equation 4.3 to solve for vapour NOS density in kg / m^3

        Parameters
        ----------
        curr_recip_t_reduced_minus_one: float
            Equal to the reciprocal of reduced temperature minus one
        '''
        result = NitrousOxideProperties.critical_density * exp(EquationConstants.eqn4_3[1] * curr_recip_t_reduced_minus_one**(1/3) +\
            EquationConstants.eqn4_3[2] * curr_recip_t_reduced_minus_one**(2/3) + EquationConstants.eqn4_3[3] * curr_recip_t_reduced_minus_one +\
            EquationConstants.eqn4_3[4] * curr_recip_t_reduced_minus_one**(4/3) + EquationConstants.eqn4_3[4] * curr_recip_t_reduced_minus_one**(5/3))

        return result

    def __init__(self, DAQ_data):
        '''
        Initialize all base values

        Parameters
        ----------
        DAQ_data: DAQRaw Object
            Object containing all input data (input oxidizer tank pressure)
        '''
        self.vapour_pressure_data = VapourPressureCalculations()
        self.index_with_closest_p = [find_closest_match(x, vapour_pressure_data.pressure_psi) for x in DAQ_data.tank_pressure_psia]
        self.closest_p = [vapour_pressure_data.pressure_psi[x] for x in self.index_with_closest_p]
        self.next_p = [vapour_pressure_data.pressure_psi[x + 1] for x in self.index_with_closest_p]
        
        self.t_reduced = []
        calculate_reduced_temp()

        self.one_minus_t_reduced = [1 - x for x in self.t_reduced]
        self.reciprocal_t_reduced_minus_one = [(1 / x) - 1 for x in self.t_reduced]
        
        self.density_liquid = [eqn4_2(x) for x in self.one_minus_t_reduced]
        self.density_gas = [eqn4_3(x) for x in self.reciprocal_t_reduced_minus_one]
        