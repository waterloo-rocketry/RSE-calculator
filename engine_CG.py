from DAQ_raw import DAQRaw
import constants as consts
#from NOS_vapor_CG import NOSVaporCG # Does not exist yet
#from NOS_liquid_CG import NOSLiquidCG # Does not exist yet

class EngineCG():
    
    def __init__(self, i_DAQ_data, i_NOS_vap_CG, i_NOS_liq_CG):
        self.DAQ_data = i_DAQ_data
        self.NOS_vap_CG = i_NOS_vap_CG
        self.NOS_liq_CG = i_NOS_liq_CG

        self.NOS_CG = None
        self.fuel_mass = None
        self.fuel_CG = consts


    def self_calculate_remaining_values(self):
        pass