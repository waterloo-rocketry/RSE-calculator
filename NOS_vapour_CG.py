import constants as consts
from NOS_mass_and_volume import NOSMassAndVolume



class NOSVapourCG:
    '''
    A class for holding all the data arrays for NOS vapour CG calculations.

    It self-calculates all remaining fields during initialization.
    '''

    def __init__(self, i_NOS_mass_and_volume):
        self.NOS_mass_and_volume = i_NOS_mass_and_volume

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = None
        self.vapour_height_m = None
        self.vapour_CG_m= None
        self.vapour_mass_lb = None
        self.vapour_CG_in = None


        self.self_calculate_remaining_values()


    # TODO: Finish along with supporting functions
    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        pass