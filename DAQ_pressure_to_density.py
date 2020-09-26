#!/usr/bin/env/python

from math import e

from vapour_pressure_calculations import VapourPressureCalculations

from constants import NitrousOxideProperties
from constants import EquationConstants


class DAQPressureToDensity:
    '''
    Use oxidizer tank pressure data to determine liquid and vapour NOS densities.
    '''

    def find_closest_match(self, value, matching_array):
        '''
        Finds and returns closest match (less than or equal to) to value in matching_array.
        Uses the fact that the values in matching_array are monotonically increasing

        Parameters
        ----------
        value: float
            Value to be compared against matching_array.
        matching_array: list of floats
            List of floats in increasing order where the closest match will occur.
        '''
        return_index = 0 #insdex of closest match
        curr_value = matching_array[return_index] #curr_value in matching_array being visited

        if self.debug:
            print(str(value) + ',' + str(curr_value) + '\n')

        #Find closest value by checking until either end of list reached or curr_value >= value
        while return_index < len(matching_array) and value >= curr_value:
            return_index += 1
            curr_value = matching_array[return_index]

        #Subtract by one to account for overshoot
        return return_index - 1

    def calculate_reduced_temp(self, DAQ_data):
        '''
        Uses linear interpolation to calculates reduced temperature for each tank pressure.
        Stores results in self.t_reduced
        '''

        i = 0 #Current index being visited

        #Iterate through every tank pressure
        #All columns are same length so doesnt matter which length is checked here
        while i < len(self.closest_p):
            frac = (DAQ_data.tank_pressure_psia[i] - self.closest_p[i])/\
                (self.next_p[i] - self.closest_p[i])
            result = (frac + self.vapour_pressure_data.t_kelvin[self.index_with_closest_p[i]])/\
                NitrousOxideProperties.critical_temp
            self.t_reduced.append(result)
            i += 1

    def eqn4_2(self, curr_one_minus_t_reduced):
        '''
        Implementation of Equation 4.2 to solve liquid NOS density in kg / m^3

        Parameters
        ----------
        curr_one_minus_t_reduced: float
            Equal to one minus the reduced temperature
        '''
        result = NitrousOxideProperties.critical_density*e**(EquationConstants.eqn4_2[1]*\
            curr_one_minus_t_reduced**(1/3)+EquationConstants.eqn4_2[2]*\
            curr_one_minus_t_reduced**(2/3)+EquationConstants.eqn4_2[3]*\
            curr_one_minus_t_reduced+EquationConstants.eqn4_2[4]*curr_one_minus_t_reduced**(4/3))
        return result

    def eqn4_3(self, curr_recip_t_reduced_minus_one):
        '''
        Implementation of Equation 4.3 to solve for vapour NOS density in kg / m^3

        Parameters
        ----------
        curr_recip_t_reduced_minus_one: float
            Equal to the reciprocal of reduced temperature minus one
        '''
        result = NitrousOxideProperties.critical_density*e**(EquationConstants.eqn4_3[1]*\
            curr_recip_t_reduced_minus_one**(1/3)+EquationConstants.eqn4_3[2]*\
            curr_recip_t_reduced_minus_one**(2/3)+EquationConstants.eqn4_3[3]*\
            curr_recip_t_reduced_minus_one+EquationConstants.eqn4_3[4]*\
            curr_recip_t_reduced_minus_one**(4/3)+EquationConstants.eqn4_3[5]*\
            curr_recip_t_reduced_minus_one**(5/3))
        return result

    def __init__(self, DAQ_data):
        '''
        Initialize all base values

        Parameters
        ----------
        DAQ_data: DAQRaw Object
            Object containing all input data (input oxidizer tank pressure)
        '''
        self.debug = False
        #Data from VapourPressureCalculations
        self.vapour_pressure_data = VapourPressureCalculations()
        #Index of vapour pressure value closest to DAQ pressure
        self.index_with_closest_p = [self.find_closest_match(x, self.vapour_pressure_data.pressure_psi)\
           for x in DAQ_data.tank_pressure_psia]
        #Closest vapour pressure value (<=) to DAQ pressure
        self.closest_p = [self.vapour_pressure_data.pressure_psi[x] for x in self.index_with_closest_p]
        #Value right after closest vapour pressure value
        self.next_p = [self.vapour_pressure_data.pressure_psi[x + 1] for x in self.index_with_closest_p]

        #Define and calculate reduced temperatures
        self.t_reduced = []
        self.calculate_reduced_temp(DAQ_data)

        #Intermediate math
        self.one_minus_t_reduced = [1 - x for x in self.t_reduced]
        self.reciprocal_t_reduced_minus_one = [(1 / x) - 1 for x in self.t_reduced]

        #Lists of liquid and gasseous densities
        self.density_liquid_kg_m3 = [self.eqn4_2(x) for x in self.one_minus_t_reduced]
        self.density_gas_kg_m3 = [self.eqn4_3(x) for x in self.reciprocal_t_reduced_minus_one]

if __name__ == '__main__':
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('test_csv.csv')
    test_data = DAQPressureToDensity(raw_dat)
    test_file = open('DAQ_pressure_to_density_test.csv','w')

    i = 0
    while i < len(test_data.next_p):
        test_file.write(f'{raw_dat.time_s[i]},{raw_dat.tank_pressure_psia[i]},'+\
            f'{test_data.index_with_closest_p[i]},{test_data.closest_p[i]},'+\
            f'{test_data.next_p[i]},{test_data.t_reduced[i]},{test_data.one_minus_t_reduced[i]},'+\
            f'{test_data.reciprocal_t_reduced_minus_one[i]},{test_data.density_liquid_kg_m3[i]},'+\
            f'{test_data.density_gas_kg_m3[i]}\n')
        i += 1

    test_file.close()
