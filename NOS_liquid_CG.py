from constants import TankDimensionsMetres
from NOS_mass_and_volume import NOSMassAndVolume
from math import pi



class NOSLiquidCG:
    '''
    A class for holding all the data arrays for NOS liquid CG calculations.

    It self-calculates all remaining fields during initialization.
    '''
    def calculate_cases(self):
        for curr_vol in self.NOS_mass_and_volume_data.liquid_volume_m3:
            if curr_vol <= TankDimensionsMetres.volume[1]:
                self.case.append(0)
            elif curr_vol > TankDimensionsMetres.volume[1] and curr_vol <= sum(TankDimensionsMetres.volume[1:3]):
                self.case.append(1)
            elif curr_vol > sum(TankDimensionsMetres.volume[1:3]) and curr_vol <= sum(TankDimensionsMetres.volume[1:4]):
                self.case.append(2)
            elif curr_vol > sum(TankDimensionsMetres.volume[1:4]) and curr_vol <= sum(TankDimensionsMetres.volume[1:5]):
                self.case.append(3)
            elif curr_vol > sum(TankDimensionsMetres.volume[1:5]) and curr_vol <= sum(TankDimensionsMetres.volume[1:6]):
                self.case.append(4)

    def calculate_liquid_heights(self):
        for vol,case in zip(self.NOS_mass_and_volume_data.liquid_volume_m3,self.case):
            curr_liq_height = 0

            if case == 0:
                curr_liq_height = vol / (pi*TankDimensionsMetres.radius[1]**2)
            elif case == 1:
                curr_liq_height = TankDimensionsMetres.length[1] + (vol - TankDimensionsMetres.volume[1]) / (pi*TankDimensionsMetres.radius[2]**2)
            elif case == 2:
                curr_liq_height = sum(TankDimensionsMetres.length[1:2]) + (vol - sum(TankDimensionsMetres.volume[1:2])) / (pi*TankDimensionsMetres.radius[3]**2)
            elif case == 3:
                curr_liq_height = sum(TankDimensionsMetres.length[1:3]) + (vol - sum(TankDimensionsMetres.volume[1:3])) / (pi*TankDimensionsMetres.radius[4]**2)
            elif case == 4:
                curr_liq_height = sum(TankDimensionsMetres.length[1:4]) + (vol - sum(TankDimensionsMetres.volume[1:4])) / (pi*TankDimensionsMetres.radius[5]**2)

            self.liquid_height_m.append(curr_liq_height)

    def __init__(self, i_NOS_mass_and_volume):
        self.NOS_mass_and_volume_data = i_NOS_mass_and_volume

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = []
        self.calculate_cases()

        self.liquid_height_m = []
        self.calculate_liquid_heights()

        self.liquid_CG_m= None
        self.liquid_mass_lb = None
        self.liquid_CG_in = None
  
if __name__ == "__main__":
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('test_csv.csv')
    
    test_data = NOSLiquidCG(NOSMassAndVolume(raw_dat))
    test_file = open('NOS_liquid_CG_test.csv','w')

    i = 0
    while i < len(test_data.case):
        test_file.write(f'{raw_dat.time_s[i]},{test_data.NOS_mass_and_volume_data.liquid_volume_m3[i]},{test_data.case[i]}'\
            +f',{test_data.liquid_height_m[i]}\n')
        i += 1

    test_file.close()