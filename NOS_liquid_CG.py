from math import pi

from constants import kg_to_pounds
from constants import metres_to_inches
from NOS_mass_and_volume import NOSMassAndVolume


class NOSLiquidCG:
    '''
    A class for holding all the data arrays for NOS liquid CG calculations.

    It self-calculates all remaining fields during initialization.
    '''

    @staticmethod
    def calculate_cases(nos_volumes, tank_volumes):
        '''
        Calculates case values based on what volume of the tank is filled.

        Case 1: volume less than v1
        Case 2: volume less than v2
        Case 3: volume less than v3
        Case 4: volume less than v4

        Parameters
        ----------
        nos_volumes: list of float
            The liquid volume of the NOS for each moment in time, in m3.
        tank_volumes: list of float
            The volumes of the tank sections - constants.

        Returns
        -------
        list of int:[]
            The case for each moment in time.
        '''
        cases = []

        for curr_vol in nos_volumes:
            if curr_vol <= tank_volumes[1]:
                cases.append(0)
            elif tank_volumes[1] < curr_vol <= sum(tank_volumes[1:3]):
                cases.append(1)
            elif sum(tank_volumes[1:3]) < curr_vol <= sum(tank_volumes[1:4]):
                cases.append(2)
            elif sum(tank_volumes[1:4]) < curr_vol <= sum(tank_volumes[1:5]):
                cases.append(3)
            elif sum(tank_volumes[1:5]) < curr_vol <= sum(tank_volumes[1:6]):
                cases.append(3)
            else:
                cases.append(4)

        return cases

    @staticmethod
    def calculate_liquid_heights(liquid_volume_m3, cases, tank_dimensions_m):
        '''
        Calculates liquid heights using case to determine which cylinders in the tank have liquid

        Parameters
        ----------
        nos_volume_m3: list of float
            The liquid volume of the NOS for each moment in time, in m3.
        cases: list of int
            The case classification for each data point
        tank_dimensions_m: dict
            The dimensions of the tank in meters - a dict of constants.

        Returns
        -------
        list of float:
            The liquid height for each moment in time.
        '''
        liquid_heights_m = []
        # Iterate through every time step
        for vol, case in zip(liquid_volume_m3, cases):
            curr_liq_height = 0

            curr_liq_height = sum(tank_dimensions_m['length'][1:case + 1]) +\
                (vol - sum(tank_dimensions_m['volume'][1:case + 1])) / \
                (pi*tank_dimensions_m['radius'][case + 1]**2)

            liquid_heights_m.append(curr_liq_height)

        return liquid_heights_m

    @staticmethod
    def calculate_liquid_cg(cases, liquid_height, tank_dimensions_m,
                            liquid_volume_m3, liquid_density_kg_m3, NOS_data_full=None):
        '''
        Calculates liquid centre of gravity as average of all CG multiplied by their masses

        Parameters
        ----------
        cases: list of int
            The case classification for each data point.
        liquid_height: list of float
            The height of the liquid at each data point.
        tank_dimensions_m: dict
            The dimensions of the tank in meters - a dict of constants.
        liquid_volume_m3: list of float
            The liquid volumes for each data points, in m^3.
        liquid_density_kg_m3: list of float
            The calculated density of the liquid for each data point, in kg per m^3.
        NOS_data_full: NOS_mass_and_volume.NOSMassAndVolume
            The NOS mass and volume data still packaged in an object. Default is None,
            in which case the individual variables will be used.

        Returns
        -------
        list of float:
            The liquid height for each moment in time.

        '''

        if NOS_data_full is not None:
            liquid_volume_m3 = NOS_data_full.liquid_volume_m3
            liquid_density_kg_m3 = NOS_data_full.DAQ_pressure_to_density_data.density_liquid_kg_m3

        liquid_cg_m = []
        for vol, case, liq_height, density in zip(liquid_volume_m3,
                                                  cases, liquid_height, liquid_density_kg_m3):

            numerator = 0

            # Case 0 is special (no filled cylinders)
            if case == 0:
                numerator = tank_dimensions_m['volume'][1] * density * liq_height / 2 *\
                    vol * density

            # General case
            else:
                # Adding filled cylinders
                for idx in range(case):
                    numerator += tank_dimensions_m['volume'][idx + 1] * density *\
                        tank_dimensions_m['length'][idx + 1]/2

                # Accounting for partially filled cylinder
                numerator += (liq_height + sum(tank_dimensions_m['length'][1:case + 1]))/2 *\
                    (vol-sum(tank_dimensions_m['volume'][1:case + 1]))*density

            liquid_cg_m.append(numerator/(vol*density))

        return liquid_cg_m

    def __init__(self, i_NOS_mass_and_volume, i_constants=None):
        '''
        Initialize all base values in class

        Parameters
        ----------
        i_NOS_mass_and_volume: NOSMassAndVolume object
            Contains data pertaining to NOS mass,volume and density
        i_constants: constants.ConstantsManager
            Object containing all the constants for the program. Default is None, in which case
            a default object will be imported and created.
        '''
        self.consts_m = None
        if i_constants is None:
            from constants import ConstantsManager as CM
            self.consts_m = CM()
        else:
            self.consts_m = i_constants

        self.NOS_mass_and_volume_data = i_NOS_mass_and_volume

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = []
        self.case = self.calculate_cases(self.NOS_mass_and_volume_data.liquid_volume_m3,
                                         self.consts_m.tank_dimensions_meters['volume'])

        self.liquid_height_m = \
            self.calculate_liquid_heights(self.NOS_mass_and_volume_data.liquid_volume_m3,
                                          self.case, self.consts_m.tank_dimensions_meters)

        self.liquid_cg_m = \
            self.calculate_liquid_cg(self.case, self.liquid_height_m,
                                     self.consts_m.tank_dimensions_meters,
                                     self.NOS_mass_and_volume_data.liquid_volume_m3,
                                     self.NOS_mass_and_volume_data.
                                     DAQ_pressure_to_density_data.density_liquid_kg_m3)

        self.liquid_mass_lb = [kg_to_pounds(x) for x in
                               self.NOS_mass_and_volume_data.liquid_mass_kg]
        self.liquid_cg_in = [metres_to_inches(x) for x in self.liquid_cg_m]


def create_output_file(target_path='NOS_liquid_CG_test.csv',
                       daq_source_path='test_csv.csv', downsample=1):
    '''
    Utility function for creating an ouput file of the class contents

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
    extracted_mv = NOSMassAndVolume(raw_dat)
    test_data = NOSLiquidCG(extracted_mv)

    with open(target_path, 'w') as test_file:
        i = 0
        while i < len(test_data.NOS_mass_and_volume_data.NOS_mass_kg):
            if i % downsample == 0:
                test_file.write(f'{raw_dat.time_s[i]},' +
                                f'{test_data.NOS_mass_and_volume_data.liquid_volume_m3[i]},' +
                                f'{test_data.case[i]}' +
                                f',{test_data.liquid_height_m[i]},' +
                                (str(test_data.NOS_mass_and_volume_data.
                                     DAQ_pressure_to_density_data.density_liquid_kg_m3[i])) +
                                f',{test_data.NOS_mass_and_volume_data.liquid_mass_kg[i]}' +
                                f',{test_data.liquid_cg_m[i]},{test_data.liquid_mass_lb[i]},' +
                                f'{test_data.liquid_cg_in[i]}\n')
            i += 1
