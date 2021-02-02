#!/usr/bin/env/python

from math import e
from vapour_pressure_calculations import VapourPressureCalculations

class DAQPressureToDensity:
    '''
    Use oxidizer tank pressure data to determine liquid and vapour NOS densities.
    '''

    def find_closest_match_idx(self, value, matching_array):
        '''
        Finds and returns the index of closest match (less than or equal to) to value in
        matching_array. Uses the fact that the values in matching_array are monotonically
        increasing.

        Parameters
        ----------
        value: float
            Value to be compared against matching_array.
        matching_array: list of floats
            List of floats in increasing order where the match is to be searched for.

        Returns
        -------
        int:
            The index of the closest match
        '''
        return_index = 0 #insdex of closest match
        curr_value = matching_array[return_index] #curr_value in matching_array being visited

        if self.debug and False:
            print(str(value) + ',' + str(curr_value) + '\n')

        #Find closest value by checking until either end of list reached or curr_value >= value
        while return_index < len(matching_array) and value >= curr_value:
            return_index += 1
            if return_index < len(matching_array): # re-check to account for last index
                curr_value = matching_array[return_index]

        #Subtract by one to account for overshoot
        return return_index - 1


    @staticmethod
    def calculate_reduced_temp(DAQ_data, closest_p, next_p, temp_at_closest_p, critical_temp):
        '''
        Uses linear interpolation to calculates reduced temperature for each tank pressure.

        Stores results in self.t_reduced.

        Parameters
        ----------
        DAQ_data: `DAQRaw`
            The local daq data
        closest_p: python list of float
            The list containing the closest pressures for each data point
        next_p: python list of float
            The list containing the next closest pressures for each data point
        closest_p: python list of float
            The list containing the associated temperatures at each closest pressure
        critical_temp: float
            The value of the critical temperature for nitrous oxide, a constant

        Returns
        -------
        python list of float:
            The result of the calculation - reduced temperatures for each data point
        '''

        t_reduced = []
        #Iterate through every tank pressure
        #All columns are same length so doesnt matter which length is checked here
        for i in range(len(closest_p)):
#             print(DAQ_data.tank_pressure_psia[i])
#             print(closest_p[i])
#             print(next_p[i])
#             print(temp_at_closest_p[i])
#             print('next')
            try:
                frac = (DAQ_data.tank_pressure_psia[i] - closest_p[i])/(next_p[i] - closest_p[i])
                result = (frac + temp_at_closest_p[i])/critical_temp
            except ZeroDivisionError:
                #seems to be the maximum value for this variable
                result = 1
                print('ZeroDivisionError caught in DAQ_pressure_to_density, function ' +\
                      'calculate_reduced_temp. Either NitrousOxideProperties.critical_temp '+\
                      'has been set to 0, or the previous and next temperatures at a reading ' +\
                      'are identical. A default value of 1 was returned for that data value.')
            except IndexError:
                print('IndexError caught in DAQ_pressure_to_density, function ' +\
                      'calculate_reduced_temp. List size mismatch detected, ' +\
                      'results truncated to shortest length array was returned.')
                return t_reduced

            t_reduced.append(result)

        return t_reduced

    @staticmethod
    def eqn4_2(curr_one_minus_t_reduced, eqn4_2_constants, critical_density):
        '''
        Implementation of Equation 4.2 to solve liquid NOS density in kg / m^3

        Parameters
        ----------
        curr_one_minus_t_reduced: float
            Equal to one minus the reduced temperature
        eqn4_2_constants: list of float
            The constants related to this equation
        critical_density: float
            The value of the critical density for nitrous oxide, a constant

        Returns
        -------
        float:
            The result of the calculation.
        '''
        result = critical_density*e**(eqn4_2_constants[1]*\
            curr_one_minus_t_reduced**(1/3) + eqn4_2_constants[2]*\
            curr_one_minus_t_reduced**(2/3) + eqn4_2_constants[3]*\
            curr_one_minus_t_reduced + eqn4_2_constants[4]*curr_one_minus_t_reduced**(4/3))
        return result

    @staticmethod
    def eqn4_3(curr_recip_t_reduced_minus_one, eqn4_3_constants, critical_density):
        '''
        Implementation of Equation 4.3 to solve for vapour NOS density in kg / m^3

        Parameters
        ----------
        curr_recip_t_reduced_minus_one: float
            Equal to the reciprocal of reduced temperature minus one.
        eqn4_3_constants: list of float
            The constants related to this equation.
        critical_density: float
            The value of the critical density for nitrous oxide, a constant.

        Returns
        -------
        float:
            The result of the calculation.
        '''
        result = critical_density*e**(eqn4_3_constants[1]*\
            curr_recip_t_reduced_minus_one**(1/3) + eqn4_3_constants[2]*\
            curr_recip_t_reduced_minus_one**(2/3) + eqn4_3_constants[3]*\
            curr_recip_t_reduced_minus_one + eqn4_3_constants[4]*\
            curr_recip_t_reduced_minus_one**(4/3) + eqn4_3_constants[5]*\
            curr_recip_t_reduced_minus_one**(5/3))

        return result

    def __init__(self, DAQ_data, i_constants = None):
        '''
        Initialize all base values

        Parameters
        ----------
        DAQ_data: DAQRaw Object
            Object containing all input data (input oxidizer tank pressure).
        i_constants: constants.ConstantsManager
            Object containing all the constants for the program. Default is None, in which case
            a default object will be imported and created.
        '''
        if i_constants is None:
            from constants import ConstantsManager as CM
            self.consts_m = CM()
        else:
            self.consts_m = i_constants

        self.debug = True
        #Data from VapourPressureCalculations
        self.vapour_pressure_data = VapourPressureCalculations()
        #Index of vapour pressure value closest to DAQ pressure
        self.index_with_closest_p = \
            [self.find_closest_match_idx(x, self.vapour_pressure_data.pressure_psi) \
            for x in DAQ_data.tank_pressure_psia]
        #Closest vapour pressure value (<=) to DAQ pressure
        self.closest_p = \
            [self.vapour_pressure_data.pressure_psi[x] for x in self.index_with_closest_p]
        #Value right after closest vapour pressure value
        self.next_p = \
            [self.vapour_pressure_data.pressure_psi[x + 1] for x in self.index_with_closest_p]

        #Define the temperature values at each of the closest pressures
        temps_of_closest_p = [self.vapour_pressure_data.t_kelvin[self.index_with_closest_p[i]] \
            for i in range(len(self.index_with_closest_p))]

        #Define and calculate reduced temperatures
        self.t_reduced = self.calculate_reduced_temp(\
            DAQ_data, self.closest_p, self.next_p,\
             temps_of_closest_p, self.consts_m.nitrous_oxide_properties['critical_temp'])
        #self.calculate_reduced_temp(DAQ_data)

        #Intermediate math
        self.one_minus_t_reduced = [1 - x for x in self.t_reduced]
        self.reciprocal_t_reduced_minus_one = [(1 / x) - 1 for x in self.t_reduced]

        #Lists of liquid and gasseous densities
        self.density_liquid_kg_m3 = [self.eqn4_2(x, self.consts_m.equation_constants['eqn4_2'], \
            self.consts_m.nitrous_oxide_properties['critical_density'])\
             for x in self.one_minus_t_reduced]
        self.gas_density_kg_m3 = [self.eqn4_3(x, self.consts_m.equation_constants['eqn4_3'], \
            self.consts_m.nitrous_oxide_properties['critical_density'])\
            for x in self.reciprocal_t_reduced_minus_one]

def create_ouput_file(path = 'DAQ_pressure_to_density_test', downsample = 1):
    '''
    Utility function for creating an ouput file of the class contents

    Parameters
    ----------
    path: str
        the name of the ouput file.
    downsample: int
        how much the output needs to be downsampled by. Default value is 1 (no downsampling).

    Returns
    -------
    str:
        The path at which the file was saved.
    '''
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('data\\test_csv.csv')

    test_data = DAQPressureToDensity(raw_dat)
    test_file = open(path + '.csv','w')

    i = 0
    while i < len(test_data.next_p):
        if i % downsample == 0:
            test_file.write(f'{raw_dat.time_s[i]},{raw_dat.tank_pressure_psia[i]},'+\
                f'{test_data.index_with_closest_p[i]},{test_data.closest_p[i]},'+\
                f'{test_data.next_p[i]},{test_data.t_reduced[i]},'+\
                f'{test_data.one_minus_t_reduced[i]},'+\
                f'{test_data.reciprocal_t_reduced_minus_one[i]},' +\
                f'{test_data.density_liquid_kg_m3[i]},'+\
                f'{test_data.gas_density_kg_m3[i]}\n')
        i += 1

    test_file.close()
