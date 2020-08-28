import constants as consts
from NOS_mass_and_volume import NOSMassAndVolume



class NOSVapourCG:
    '''
    A class for holding all the data arrays for NOS liquid CG calculations.

    It self-calculates all remaining fields during initialization.
    '''

    def __init__(self, i_NOS_mass_and_volume):
        self.NOS_mass_and_volume = i_NOS_mass_and_volume

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = None
        self.liquid_height_m = None
        self.liquid_CG_m= None
        self.liquid_mass_lb = None
        self.liquid_CG_in = None


        self.self_calculate_remaining_values()


    # TODO: Finish along with supporting functions
    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        pass