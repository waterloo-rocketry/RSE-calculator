from constants import pounds_to_kg
from constants import ConstantsManager as ConstsM

from DAQ_pressure_to_density import DAQPressureToDensity


class NOSMassAndVolume:
    '''
    Use oxidizer tank mass data along with density data to calculate
    liquid and vapour NOS volumes and masses.
    '''

    @staticmethod
    def calculate_liquid_volume(nos_mass_kg, gas_density_kg_m3, liquid_density_kg_m3, total_v_m3):
        '''
        Calculate the volume of the liquid

        Parameters
        ----------
        nos_mass_kg: float
            The weight of the NOS as a moment in time, in kg.
        gas_density_kg_m3: float
            The density of the gaseous NOS as a moment in time, in kg/m3.
        liquid_density_kg_m3: float
            The density of the liquid NOS as a moment in time, in kg/m3.
        total_v_m3: float
            The value of the total volume, in m3.

        Returns
        -------
        float:
            The result of the calculation.
        '''
        try:
            result = (nos_mass_kg - (gas_density_kg_m3*total_v_m3)) /\
                (liquid_density_kg_m3 - gas_density_kg_m3)
        except ZeroDivisionError:
            print('ZeroDivisionError caught in NOS_mass_and_volume, function ' +
                  'calculate_liquid_volume. The gas and liquid densities as  ' +
                  'provided to the method were equal. The total volume was returned')
            result = total_v_m3
        return result

    def __init__(self, DAQ_data, i_constants=None):
        '''
        Initialize all base values.

        Parameters
        ----------
        DAQ_data: DAQRaw Object
            Object containing all input data (input oxidizer tank pressure)
        i_constants: constants.ConstantsManager
            Object containing all the constants for the program. Default is None, in which case
            a default object will be imported and created.
        '''
        self.consts_m = None
        if i_constants is None:
            self.consts_m = ConstsM()
        else:
            self.consts_m = i_constants

        # Data from pressure_to_density calculations
        self.DAQ_pressure_to_density_data = \
            DAQPressureToDensity(DAQ_data, i_constants=self.consts_m)
        # Mass of NOS converted to kg
        self.NOS_mass_kg = pounds_to_kg(DAQ_data.adjusted_mass_lb)

        # Define and calculate volume of liquid in m^3
        self.liquid_volume_m3 = []

        total_volume = self.consts_m.tank_dimensions_meters['total_volume']
        self.liquid_volume_m3 = \
            self.calculate_liquid_volume(self.NOS_mass_kg,
                                         self.DAQ_pressure_to_density_data.gas_density_kg_m3,
                                         self.DAQ_pressure_to_density_data.density_liquid_kg_m3,
                                         total_volume)

        # Calculate volume of vapour in m^3
        self.vapour_volume_m3 =\
            self.consts_m.tank_dimensions_meters['total_volume'] - \
            self.liquid_volume_m3

        # Calculating mass of liquid and vapour at each time step in kg/m^3
        self.liquid_mass_kg = \
            self.DAQ_pressure_to_density_data.density_liquid_kg_m3 * self.liquid_volume_m3
        self.vapour_mass_kg = \
            self.DAQ_pressure_to_density_data.gas_density_kg_m3 * self.vapour_volume_m3


def create_output_file(target_path='NOS_mass_and_volume_test.csv',
                       daq_source_path='test_csv.csv', downsample=1):
    '''
    Utility function for creating an ouput file of the class contents.

    Parameters
    ----------
    target_path: str
        The name of the ouput file.
    daq_source_path: str
        The path of the the daq file to be used for generating the file.
    downsample: int
        How much the output needs to be downsampled by. Default value is 1 (no downsampling).
    '''

    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(daq_source_path)
    test_data = NOSMassAndVolume(raw_dat)
    pressure_to_density = test_data.DAQ_pressure_to_density_data

    with open(target_path, 'w') as test_file:
        i = 0
        while i < len(test_data.NOS_mass_kg):
            if i % downsample == 0:
                test_file.write(f'{raw_dat.time_s[i]},{raw_dat.adjusted_mass_lb[i]},' +
                                f'{test_data.NOS_mass_kg[i]},' +
                                f'{pressure_to_density.density_liquid_kg_m3[i]},' +
                                f'{pressure_to_density.gas_density_kg_m3[i]},' +
                                f'{test_data.liquid_volume_m3[i]},' +
                                f'{test_data.vapour_volume_m3[i]},' +
                                f'{test_data.liquid_mass_kg[i]},{test_data.vapour_mass_kg[i]},\n')
            i += 1
