import constants as consts
from DAQ_raw import DAQRaw
from engine_CG import EngineCG



class EngineXML:
    '''
    A class for holding all the data arrays for Engine XML calculations.

    It self-calculates all remaining fields during initialization.
    '''

    def __init__(self, i_DAQ_data, i_engine_CG):
        '''
        Initializes all base values.

        Parameters
        ----------

        i_DAQ_data: DAQRaw
            The timestamps for the test data.
            
        i_engine_CG: EngineCG
            The tank pressure at each timestamp.
        '''

        self.DAQ_data = i_DAQ_data
        self.engine_CG = i_engine_CG

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.zeroed_time = None
        self.thust_N = None
        self.engine_mass_g = None
        self.propellant_CG_mm = None

        self.XML_tags = None

        self.self_calculate_remaining_values()


    # TODO: Finish along with supporting functions
    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        pass

