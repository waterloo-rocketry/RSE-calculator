import constants as consts
from constants import ConstantsManager as ConstsM
from NOS_mass_and_volume import NOSMassAndVolume
from NOS_liquid_CG import NOSLiquidCG
from NOS_vapour_CG import NOSVapourCG

class EngineCG():
    '''
    A class for holding all the data arrays for Engine CG calculations.

    It self-calculates all remaining fields during initialization.
    '''

    def __init__(self, i_DAQ_data, i_NOS_vap_CG, i_NOS_liq_CG):
        '''
        Initializes all base values.

        Parameters
        ----------

        i_DAQ_data: DAQRaw
            The timestamps for the test data.

        i_NOS_vap_CG: NOSVapourCG
            The tank pressure at each timestamp.

        i_NOS_liq_CG: NOSLiquidCG
            The recorded mass at each timestamp
        '''
        self.consts_m = ConstsM()
        self.debug_mode = False # needs to be set manually for debugging purposes

        self.end_of_burn = 201

        self.DAQ_data = i_DAQ_data
        self.NOS_vap_CG = i_NOS_vap_CG
        self.NOS_liq_CG = i_NOS_liq_CG

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.NOS_CG_in = None
        self.fuel_mass_lb = None
        self.fuel_CG_in = self.consts_m.engine_info['fuel_grain_length'] / 2
        self.propellant_mass_lb = None
        self.propellant_CG_in = None

        self.self_calculate_remaining_values()

    def set_end_of_burn(self, end_idx):
        '''
        Setter for the end_of_burn field

        Parameters
        ----------

        end_idx: int
            The end index of the burn values within the DAQ data table
        '''

        self.end_of_burn = end_idx

    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''

        self.NOS_CG_in = self.calculate_NOS_CG_values(0,0,0,0,
                self.NOS_liq_CG, self.NOS_vap_CG)
        self.fuel_mass_lb = self.calculate_fuel_mass_values(self.DAQ_data.time_s,\
            self.consts_m.engine_info, self.end_of_burn)
#         self.fuel_mass_lb = [self.calculate_fuel_mass_value(time_stamp) for \
#                 time_stamp in self.DAQ_data.time_s]

        self.propellant_mass_lb = [self.fuel_mass_lb[idx] + self.DAQ_data.adjusted_mass_lb[idx] \
                for idx in range(len(self.DAQ_data.time_s))]

        y_OS = consts.EngineInfo.dist_to_tank_start
        fuel_CG = self.fuel_CG_in

        self.propellant_CG_in = [(self.DAQ_data.adjusted_mass_lb[idx]*(self.NOS_CG_in[idx] + y_OS)\
                 + self.fuel_mass_lb[idx]*fuel_CG)/self.propellant_mass_lb[idx] \
                 for idx in range(len(self.DAQ_data.time_s))]

        if self.debug_mode:
            for val in self.propellant_CG_in:
                print(val)

    @staticmethod
    def calculate_NOS_CG_values(liquid_mass, vapour_mass, liquid_cg_in, vapour_cg_in
            , NOS_liq_CG_fulldata = None, NOS_vap_CG_fulldata = None):
        '''
        Calculates and returns the correct NOS_CG_in value for all data points.

        Parameters
        ----------
        liquid_mass: float or list of float
            The mass of the liquid NOS.
        vapour_mass: float or list of float
            The mass of vapour NOS
        liquid_cg_in: float or list of float
            The centre of gravity for the liquid NOS
        vapour_cg_in: float ro list of float
            The cnetre of gravity for the vapour NOS
        NOS_liq_CG_fulldata: NOS_liquid_CG.NOSLiquidCG
            The data object containing info regarding the liquid NOS center of gravity. Default to
            None for input flexibility
        NOS_vap_CG_fulldata: NOS_vapour_CG.NOSVapourCG
            The data object containing infro regarding the vapour NOS center of gravity. Default to
            None for input flexibility

        Returns
        -------

        list of float:
            The NOS CG values for all data points.
        '''


        values = []
        if NOS_liq_CG_fulldata is not None:
            liquid_mass = NOS_liq_CG_fulldata.liquid_mass_lb
            vapour_mass = NOS_vap_CG_fulldata.vapour_mass_lb
        if NOS_vap_CG_fulldata is not None:
            liquid_cg_in = NOS_liq_CG_fulldata.liquid_cg_in
            vapour_cg_in = NOS_vap_CG_fulldata.vapour_cg_in

        # packages into itereables if single floats are passed in
        if not hasattr(liquid_mass, '__iter__'):
            liquid_mass = [liquid_mass]
        if not hasattr(vapour_mass, '__iter__'):
            vapour_mass = [vapour_mass]
        if not hasattr(liquid_cg_in, '__iter__'):
            liquid_cg_in = [liquid_cg_in]
        if not hasattr(vapour_cg_in, '__iter__'):
            vapour_cg_in = [vapour_cg_in]

        for val_idx in range(len(liquid_mass)):
            result = (liquid_mass[val_idx]*liquid_cg_in[val_idx] +\
                    vapour_mass[val_idx]*vapour_cg_in[val_idx])
            result /= (liquid_mass[val_idx] + vapour_mass[val_idx])
            values.append(result)

        return values

    @staticmethod
    def calculate_fuel_mass_values(time, engine_info, end_of_burn):
        '''
        Calculates and returns the correct fuel mass values for a all data points.

        Parameters
        ----------

        time: list of float
            The times stamps of the data points
        engine_info: dict of float
            Data regarding the engine - constants.
        end_of_burn: float
            The time at which the burn is manually determined to be over

        Returns
        -------

        float:
            The fuel mass value for all time stamps.
        '''
        values = []
        m_FI = engine_info['fuel_grain_init_mass']
        m_FF = engine_info['fuel_grain_final_mass']

        for time_stamp in time:
            result = float(m_FI - ((m_FI-m_FF)/(time[end_of_burn] - time[0]))*\
                           (time_stamp - time[0]))
            values.append(result)

        return values

def create_output_file(target_path = 'Engine_CG_test.csv', daq_source_path =\
         'test_csv.csv', downsample = 1):
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(daq_source_path)
    test_nmv = NOSMassAndVolume(raw_dat)
    test_nlc = NOSLiquidCG(test_nmv)
    test_nvc = NOSVapourCG(test_nmv, test_nlc)
    test_data = EngineCG(raw_dat, test_nvc, test_nlc)
    test_file = open(target_path,'w')

    i = 0
    while i < len(test_nmv.NOS_mass_kg):
        if i % downsample == 0:
            test_file.write(f'{raw_dat.time_s[i]},'+\
                f'{test_nlc.liquid_mass_lb[i]},' +\
                f'{test_nlc.liquid_cg_in[i]},'+\
                f'{test_nvc.vapour_mass_lb[i]},' +\
                f'{test_nvc.vapour_cg_in[i]},' +\
                f'{raw_dat.adjusted_mass_lb[i]},' +\
                f'{test_data.NOS_CG_in[i]},' +\
                f'{test_data.fuel_mass_lb[i]},' +\
                f'{test_data.fuel_CG_in},' +\
                f'{test_data.propellant_mass_lb[i]},' +\
                f'{test_data.propellant_CG_in[i]},' + '\n')

        i += 1

    test_file.close()


