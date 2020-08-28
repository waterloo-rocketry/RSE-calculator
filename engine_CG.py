from DAQ_raw import DAQRaw
import constants as consts


#from NOS_vapor_CG import NOSVapourCG # Does not exist yet
#from NOS_liquid_CG import NOSLiquidCG # Does not exist yet
class EngineCG():
    '''
    A class for holding all the data arrays for Engine CG.

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

        self.DAQ_data = i_DAQ_data
        self.NOS_vap_CG = i_NOS_vap_CG
        self.NOS_liq_CG = i_NOS_liq_CG

        self.NOS_CG = None
        self.fuel_mass = None
        self.fuel_CG = consts.EngineInfo.fuel_grain_length / 2
        self.propellant_mass = None
        self.propellant_CG = None

        self.self_calculate_remaining_values()

    # TODO: Finish along with supporting functions
    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''

        self.NOS_CG = []

        self.fuel_mass = [self.calculate_fuel_mass_value(time_stamp) for \
                time_stamp in self.DAQ_data.time_s]


        pass

    def calculate_NOS_CG_value(self, val_idx):
        '''
        Calculates and returns the correct NOS_CG value for a single data point.

        Parameters
        ----------

        val_idx: int
            The location of the data point in the arrays

        Returns
        -------

        float:
            The NOS CG value for the data point.
        '''
        pass

    def calculate_fuel_mass_value(self, time_stamp):
        '''
        Calculates and returns the correct fuel mass value for a single data point.

        Parameters
        ----------

        time_stamp: float
            The time at which the fuel mass needs to be calculated

        Returns
        -------

        float:
            The fuel mass value for the given time stamp.
        '''
        with consts.EngineInfo.fuel_grain_intial_mass as m_FI, \
                consts.EngineInfo.fuel_grain_final_mass as m_FF, \
                self.DAQ_data.time_s as time:

            result = float(m_FI - ((m_FI-m_FF)/(time[-1] - time[0]))*(time_stamp - time[0]))

        return result