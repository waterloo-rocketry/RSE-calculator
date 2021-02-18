import numpy as np

from NOS_mass_and_volume import NOSMassAndVolume
from NOS_liquid_CG import NOSLiquidCG
from constants import kg_to_pounds
from constants import metres_to_inches
from constants import ConstantsManager as ConstsM


class NOSVapourCG:
    '''
    A class for holding all the data arrays for NOS vapour CG calculations.

    It self-calculates all remaining fields during initialization.
    '''

    @staticmethod
    def calculate_cases(nos_vapour_volumes, tank_volumes):
        '''
        Calculate case values based on what volume of the tank is filled.

        Case 1: volume less than v1
        Case 2: volume less than v2
        Case 3: volume less than v3
        Case 4: volume less than v4

        Parameters
        ----------
        nos_vapour_volumes: list of float
            The vapour volume of the NOS for each moment in time, in m3.
        tank_volumes: list of float
            The volumes of the tank sections - constants.

        Returns
        -------
        list of int:
            The case for each moment in time.
        '''
        cases = []

        for curr_vol in nos_vapour_volumes:
            if curr_vol <= tank_volumes[4]:
                cases.append(0)
            elif tank_volumes[4] < curr_vol <= sum(tank_volumes[3:]):
                cases.append(1)
            elif sum(tank_volumes[3:]) < curr_vol <= sum(tank_volumes[2:]):
                cases.append(2)
            elif sum(tank_volumes[2:]) < curr_vol <= sum(tank_volumes[1:]):
                cases.append(3)
            elif sum(tank_volumes[1:]) < curr_vol <= sum(tank_volumes):
                cases.append(3)
            else:
                cases.append(4)

        return cases

    @staticmethod
    def calculate_vapour_cg(vapour_volume_m3, gas_density_kg_m3, cases, vapour_height,
                            tank_dimensions_m, NOS_data_full=None):
        '''
        Calculate vapour centre of gravity as average of all CG multiplied by their masses.

        Parameters
        ----------
        vapour_volume_m3: list of float
            The liquid volumes for each data points, in m^3.
        gas_density_kg_m3: list of float
            The calculated density of the liquid for each data point, in kg per m^3.
        cases: list of int
            The case classification for each data point.
        vapour_height: list of float
            The height of the vapour at each data point.
        tank_dimensions_m: dict
            The dimensions of the tank in meters - a dict of constants.
        NOS_data: NOS_mass_and_volume.NOSMassAndVolume
            The data object containing full NOS properties for input flexibility. Default is None,
            in which case the individual variables will be used.

        Returns
        -------
        list of float:
            The vapour centre of gravity for each moment in time.

        '''
        if NOS_data_full is not None:
            vapour_volume_m3 = NOS_data_full.vapour_volume_m3
            gas_density_kg_m3 = NOS_data_full.DAQ_pressure_to_density_data.gas_density_kg_m3

        vapour_cg_m = np.array([])

        # TODO: Optimize cases here
        for vol, case, height, density in zip(vapour_volume_m3,
                                              cases, vapour_height,
                                              gas_density_kg_m3):

            numerator = 0

            # Case 0 is special (no filled cylinders)
            if case == 0:
                numerator = tank_dimensions_m['volume'][4] * density * height / 2 *\
                    vol

            # General case
            else:
                # Adding filled cylinders
                for idx in range(case):
                    numerator += (tank_dimensions_m['volume'][4 - idx] *
                                  tank_dimensions_m['length'][4 - idx]/2)

                # Accounting for partially filled cylinder
                numerator += (height + sum(tank_dimensions_m['length'][-case:]))/2 *\
                    (vol-sum(tank_dimensions_m['volume'][-case:]))

            vapour_cg_m = np.append(vapour_cg_m,
                                    tank_dimensions_m['total_length'] - numerator/(vol))

        return vapour_cg_m

    def __init__(self, i_NOS_mass_and_volume, i_NOS_liquid_CG, i_constants=None):
        '''
        Initialize all base values in class.

        Parameters
        ----------
        i_NOS_mass_and_volume: NOSMassAndVolume object
            Contains data pertaining to NOS mass,volume and density
        i_NOS_liquid_CG: NOSLiquidCG object 
            The details about the NOS centre of gravity
        i_constants: constants.ConstantsManager
            Object containing all the constants for the program. Default is None, in which case
            a default object will be imported and created.
        '''
        self.consts_m = None
        if i_constants is None:
            self.consts_m = ConstsM()
        else:
            self.consts_m = i_constants

        self.NOS_mass_and_volume_data = i_NOS_mass_and_volume
        self.NOS_liquid_CG_data = i_NOS_liquid_CG

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = self.calculate_cases(self.NOS_mass_and_volume_data.vapour_volume_m3,
                                         self.consts_m.tank_dimensions_meters['volume'])

        self.vapour_height_m = (self.consts_m.tank_dimensions_meters['total_length']
                                - self.NOS_liquid_CG_data.liquid_height_m)

        self.vapour_cg_m = self.calculate_vapour_cg(
            self.NOS_mass_and_volume_data.vapour_volume_m3,
            self.NOS_mass_and_volume_data.DAQ_pressure_to_density_data.gas_density_kg_m3,
            self.case, self.vapour_height_m, self.consts_m.tank_dimensions_meters)

        self.vapour_mass_lb = kg_to_pounds(
            self.NOS_mass_and_volume_data.vapour_mass_kg)
        self.vapour_cg_in = metres_to_inches(self.vapour_cg_m)


def create_output_file(target_path='NOS_vapour_CG_test.csv',
                       daq_source_path='test_csv.csv', downsample=1):
    '''
    Utility function for creating an ouput file of the class contents.

    Parameters
    ----------
    target_path: str
        the name of the ouput file.
    daq_source_path: str
        the path of the the daq file to be used for generating the file.
    downsample: int
        how much the output needs to be downsampled by. Default value is 1 (no downsampling).
    '''
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(daq_source_path)
    test_nmv = NOSMassAndVolume(raw_dat)
    test_nlc = NOSLiquidCG(test_nmv)
    test_data = NOSVapourCG(test_nmv, test_nlc)

    with open(target_path, 'w') as test_file:
        i = 0
        while i < len(test_nmv.NOS_mass_kg):
            if i % downsample == 0:
                test_file.write(f'{raw_dat.time_s[i]},' +
                                f'{test_data.NOS_mass_and_volume_data.vapour_volume_m3[i]},' +
                                f'{test_data.case[i]}' +
                                f',{test_data.vapour_height_m[i]},' +
                                (str(test_data.NOS_mass_and_volume_data.
                                     DAQ_pressure_to_density_data.gas_density_kg_m3[i])) +
                                f',{test_data.NOS_mass_and_volume_data.vapour_mass_kg[i]}' +
                                f',{test_data.vapour_cg_m[i]},{test_data.vapour_mass_lb[i]},' +
                                f'{test_data.vapour_cg_in[i]}\n')
            i += 1
