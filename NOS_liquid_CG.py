from constants import TankDimensionsMetres
from constants import kg_to_pounds
from constants import metres_to_inches
from NOS_mass_and_volume import NOSMassAndVolume
from math import pi

class NOSLiquidCG:
    '''
    A class for holding all the data arrays for NOS liquid CG calculations.

    It self-calculates all remaining fields during initialization.
    '''
    def calculate_cases(self):
        '''
        Calculates case values based on what volume of the tank is filled

        Case 1: volume less than v1
        Case 2: volume less than v2
        Case 3: volume less than v3
        Case 4: volume less than v4
        '''
        for curr_vol in self.NOS_mass_and_volume_data.liquid_volume_m3:
            if curr_vol <= TankDimensionsMetres.volume[1]:
                self.case.append(0)
            elif curr_vol > TankDimensionsMetres.volume[1] and\
               curr_vol <= sum(TankDimensionsMetres.volume[1:3]):
                self.case.append(1)
            elif curr_vol > sum(TankDimensionsMetres.volume[1:3]) and\
               curr_vol <= sum(TankDimensionsMetres.volume[1:4]):
                self.case.append(2)
            elif curr_vol > sum(TankDimensionsMetres.volume[1:4]) and\
               curr_vol <= sum(TankDimensionsMetres.volume[1:5]):
                self.case.append(3)
            elif curr_vol > sum(TankDimensionsMetres.volume[1:5]) and\
               curr_vol <= sum(TankDimensionsMetres.volume[1:6]):
                self.case.append(3)
            else:
                self.case.append(4)

    def calculate_liquid_heights(self):
        '''
        Calculates liquid heights using case to determine which cylinders in tank have liquid

        Uses volume equations to calculate height
        '''
        #Iterate through every time step
        for vol,case in zip(self.NOS_mass_and_volume_data.liquid_volume_m3,self.case):
            curr_liq_height = 0

            curr_liq_height = sum(TankDimensionsMetres.length[1:case + 1]) +\
               (vol - sum(TankDimensionsMetres.volume[1:case + 1])) / \
               (pi*TankDimensionsMetres.radius[case + 1]**2)

            self.liquid_height_m.append(curr_liq_height)

    def calculate_liquid_cg(self):
        '''
        Calculates liquid centre of gravity as average of all CG multiplied by their masses
        '''
        for vol,case,liq_height,density in zip(self.NOS_mass_and_volume_data.liquid_volume_m3,\
            self.case,self.liquid_height_m,\
            self.NOS_mass_and_volume_data.DAQ_pressure_to_density_data.density_liquid_kg_m3):
            
            numerator = 0

            #Case 0 is special (no filled cylinders)
            if case == 0:
                numerator = TankDimensionsMetres.volume[1] * density * liq_height / 2 *\
                   vol * density
            
            #General case
            else:
                i = 0
                #Adding filled cylinders
                for i in range(case):
                    numerator += TankDimensionsMetres.volume[i + 1] * density *\
                       TankDimensionsMetres.length[i + 1]/2

                #Accounting for partially filled cylinder
                numerator += (liq_height + sum(TankDimensionsMetres.length[1:case + 1]))/2*\
                    (vol-sum(TankDimensionsMetres.volume[1:case + 1]))*density
          
            self.liquid_CG_m.append(numerator/(vol*density))

    def __init__(self, i_NOS_mass_and_volume):
        '''
        Initialize all base values in class

        Parameters
        ----------
        i_NOS_mass_and_volume: NOSMassAndVolume object
            Contains data pertaining to NOS mass,volume and density
        '''
        self.NOS_mass_and_volume_data = i_NOS_mass_and_volume

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = []
        self.calculate_cases()

        self.liquid_height_m = []
        self.calculate_liquid_heights()

        self.liquid_CG_m = []
        self.calculate_liquid_cg()

        self.liquid_mass_lb = [kg_to_pounds(x) for x in \
            self.NOS_mass_and_volume_data.liquid_mass_kg]
        self.liquid_CG_in = [metres_to_inches(x) for x in self.liquid_CG_m]
  
if __name__ == "__main__":
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('test_csv.csv')
    
    test_data = NOSLiquidCG(NOSMassAndVolume(raw_dat))
    test_file = open('NOS_liquid_CG_test.csv','w')

    i = 0
    while i < len(raw_dat.time_s):
        test_file.write(f'{raw_dat.time_s[i]},'+\
            f'{test_data.NOS_mass_and_volume_data.liquid_volume_m3[i]},{test_data.case[i]}'+\
            f',{test_data.liquid_height_m[i]},'+\
            str(test_data.NOS_mass_and_volume_data.DAQ_pressure_to_density_data.\
            density_liquid_kg_m3[i])+f',{test_data.NOS_mass_and_volume_data.liquid_mass_kg[i]}'+\
            f',{test_data.liquid_CG_m[i]},{test_data.liquid_mass_lb[i]},'+\
            f'{test_data.liquid_CG_in[i]}\n')
        i += 1

    test_file.close()