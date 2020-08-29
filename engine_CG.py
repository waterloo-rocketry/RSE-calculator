import constants as consts

from DAQ_raw import DAQRaw
from NOS_vapor_CG import NOSVapourCG
from NOS_liquid_CG import NOSLiquidCG


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

        self.DAQ_data = i_DAQ_data
        self.NOS_vap_CG = i_NOS_vap_CG
        self.NOS_liq_CG = i_NOS_liq_CG

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.NOS_CG_in = None
        self.fuel_mass_lb = None
        self.fuel_CG_in = consts.EngineInfo.fuel_grain_length / 2
        self.propellant_mass_lb = None
        self.propellant_CG_in = None

        self.self_calculate_remaining_values()

    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''

        self.NOS_CG_in = [self.calculate_NOS_CG_value(idx) for \
                idx in range(len(self.DAQ_data.time_s))]

        self.fuel_mass_lb = [self.calculate_fuel_mass_value(time_stamp) for \
                time_stamp in self.DAQ_data.time_s]

        self.propellant_mass_lb = [self.fuel_mass_lb[idx] + self.DAQ_data.adjusted_mass_lb[idx] for \
                idx in range(len(self.DAQ_data.time_s))]


    def calculate_NOS_CG_value(self, val_idx):
        '''
        Calculates and returns the correct NOS_CG_in value for a single data point.

        Parameters
        ----------

        val_idx: int
            The location of the data point in the arrays

        Returns
        -------

        float:
            The NOS CG value for the data point.
        '''

        result = (self.NOS_liq_CG.liquid_mass_lb[val_idx]*self.NOS_liq_CG.liquid_CG_in[val_idx] +\
                self.NOS_vap_CG.vapour_mass_lb[val_idx]*self.NOS_liq_CG.vapour_CG_in[val_idx])
        result /= (self.NOS_liq_CG.liquid_mass_lb[val_idx] +\
                self.NOS_vap_CG.vapour_mass_lb[val_idx])
        
        return result

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
    
    def calculate_propellant_CG_value(self, val_idx):
        '''
        Calculates and returns the correct propellant CG value for a single data point.

        Parameters
        ----------

        val_idx: int
            The location of the data point in the arrays

        Returns
        -------

        float:
            The correct propellant CG value for the data point.
        '''
        result = self.DAQ_data.adjusted_mass_lb[val_idx]*(self.NOS_CG_in[val_idx] + \
                 consts.EngineInfo.dist_to_tank_start)
        result += self.fuel_mass_lb[val_idx]*self.fuel_CG_in
        result /= self.propellant_mass_lb[val_idx]
        
        