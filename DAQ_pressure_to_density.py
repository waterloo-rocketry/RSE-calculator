from math import e
from vapour_pressure_calculations import VapourPressureCalculations
import numpy as np


class DAQPressureToDensity:
    '''
    Use oxidizer tank pressure data to determine liquid and vapour NOS densities.
    '''

    def set_debug_mode(self, mode):
        '''
        Set the local debug mode.

        Parameters
        ----------

        mode: bool
            The desired state of the debug mode for the class.
        '''

        self.debug = mode

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
        result = (critical_density *
                  e**(eqn4_2_constants[1] *
                      curr_one_minus_t_reduced**(1/3) + eqn4_2_constants[2] *
                      curr_one_minus_t_reduced**(2/3) + eqn4_2_constants[3] *
                      curr_one_minus_t_reduced + eqn4_2_constants[4] *
                      curr_one_minus_t_reduced**(4/3)))
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
        result = (critical_density *
                  e**(eqn4_3_constants[1] *
                      curr_recip_t_reduced_minus_one**(1/3) + eqn4_3_constants[2] *
                      curr_recip_t_reduced_minus_one**(2/3) + eqn4_3_constants[3] *
                      curr_recip_t_reduced_minus_one + eqn4_3_constants[4] *
                      curr_recip_t_reduced_minus_one**(4/3) + eqn4_3_constants[5] *
                      curr_recip_t_reduced_minus_one**(5/3)))

        return result

    def __init__(self, DAQ_data, i_constants=None):
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

        self.debug = False
        self.vapour_pressure_data = VapourPressureCalculations()

        # Define and calculate reduced temperatures using numpy interpolate
        self.t_reduced = (np.array(np.interp(DAQ_data.tank_pressure_psia,
                                             self.vapour_pressure_data.pressure_psi,
                                             self.vapour_pressure_data.t_kelvin)) /
                          self.consts_m.nitrous_oxide_properties['critical_temp'])

        # Intermediate math
        self.one_minus_t_reduced = 1 - self.t_reduced
        self.reciprocal_t_reduced_minus_one = (1 / self.t_reduced) - 1

        # Lists of liquid and gaseous densities
        self.density_liquid_kg_m3 = self.eqn4_2(self.one_minus_t_reduced,
                                                self.consts_m.equation_constants['eqn4_2'],
                                                self.consts_m.nitrous_oxide_properties['critical_density'])

        self.gas_density_kg_m3 = \
            self.eqn4_3(self.reciprocal_t_reduced_minus_one,
                        self.consts_m.equation_constants['eqn4_3'],
                        self.consts_m.nitrous_oxide_properties['critical_density'])


def create_ouput_file(path='DAQ_pressure_to_density_test', downsample=1):
    '''
    Utility function for creating an ouput file of the class contents

    Parameters
    ----------
    path: str
        the name of the ouput file.
    downsample: int
        how much the output needs to be downsampled by. Default value is 1 (no downsampling).
    '''
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('data\\test_csv.csv')

    test_data = DAQPressureToDensity(raw_dat)

    with open(path + '.csv', 'w') as test_file:
        i = 0
        while i < len(test_data.t_reduced):
            if i % downsample == 0:
                test_file.write(f'{raw_dat.time_s[i]},{raw_dat.tank_pressure_psia[i]},' +
                                f'{test_data.t_reduced[i]},' +
                                f'{test_data.one_minus_t_reduced[i]},' +
                                f'{test_data.reciprocal_t_reduced_minus_one[i]},' +
                                f'{test_data.density_liquid_kg_m3[i]},' +
                                f'{test_data.gas_density_kg_m3[i]}\n')
            i += 1
