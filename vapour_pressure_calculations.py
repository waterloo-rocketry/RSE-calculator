import numpy as np

from constants import pascals_to_psi

class VapourPressureCalculations:
    '''
    Establish the vapour pressure of NOS between -90 and 36 degrees Celsius.
    '''

    @staticmethod
    def eqn4_1(curr_t_reduced, curr_one_minus_t_reduced, consts_m):
        '''
        Implement Equation 4.1 to solve for pressure in kPa.

        Parameters
        ----------
        curr_t_reduced: float
            Reduced temperature; defined as: Temp / CriticalTemp.

        curr_one_minus_t_reduced: float
            Equal to one minus the reduced temperature.

        consts_m: constants.ConstantsManager
            The constants manager that contains all of the constants loaded from file.
        '''
        # Using Equation 4.1 to solve for pressure
        result = consts_m.nitrous_oxide_properties['critical_pressure'] * \
            np.exp((1/curr_t_reduced) *
                   (consts_m.equation_constants['eqn4_1'][0]*curr_one_minus_t_reduced +
                    consts_m.equation_constants['eqn4_1'][1]*curr_one_minus_t_reduced**(1.5) +
                    consts_m.equation_constants['eqn4_1'][2]*curr_one_minus_t_reduced**(2.5) +
                    consts_m.equation_constants['eqn4_1'][3]*curr_one_minus_t_reduced**5))

        return result  # Return pressure

    def __init__(self, i_constants=None):
        '''
        Initialize all base values.

        Parameters
        ----------
        i_constants: constants.ConstantsManager
            Object containing all the constants for the program. Default is None, in which case
            a default object will be imported and created.
        '''

        if i_constants is None:
            from constants import ConstantsManager as ConstsM
            self.consts_m = ConstsM()
        else:
            self.consts_m = i_constants

        self.t_deg_c = np.arange(-90, 36, 0.1)
        # Converting t_deg_c into Kelvin
        self.t_kelvin = self.t_deg_c + 273.15
        # Reduced temperature for each temperature step
        self.t_reduced = self.t_kelvin / \
            self.consts_m.nitrous_oxide_properties['critical_temp']
        # One minus the reduced temperature for each temperature step
        self.one_minus_t_reduced = 1 - self.t_reduced
        # Pressure at each temperature step found using Equation 4.1
        self.pressure_kpa = self.eqn4_1(
            self.t_reduced, self.one_minus_t_reduced, self.consts_m)
        # Pressure at each temperature step converted to psi
        self.pressure_psi = pascals_to_psi(self.pressure_kpa * 1000)


def create_output_file(path='vapour_pressure_test.csv', downsample=1):
    '''
    Create an ouput file containing the class contents.

    Parameters
    ----------
    path: str
        The name of the ouput file.
    downsample: int
        How much the output needs to be downsampled by. Default value is 1 (no downsampling).
    '''
    test_data = VapourPressureCalculations()

    # Note: new field output lines should be added at the end of the write to ensure compliance
    # with existing test cases (`test_with_sample_file()` in test_vapour_pressure_calculations.py)
    with open(path, 'w') as test_file:
        i = 0
        while i < len(test_data.t_deg_c):
            if i % downsample == 0:
                test_file.write(f'{test_data.t_deg_c[i]},{test_data.t_kelvin[i]},' +
                                f'{test_data.t_reduced[i]}' +
                                f',{test_data.one_minus_t_reduced[i]},' +
                                f'{test_data.pressure_kpa[i]},' +
                                f'{test_data.pressure_psi[i]}\n')
            i += 1
