from NOS_mass_and_volume import NOSMassAndVolume
from NOS_liquid_CG import NOSLiquidCG
from constants import TankDimensionsMetres
from constants import kg_to_pounds
from constants import metres_to_inches


class NOSVapourCG:
    '''
    A class for holding all the data arrays for NOS vapour CG calculations.

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
        for vol in self.NOS_mass_and_volume_data.vapour_volume_m3:
            if vol <= TankDimensionsMetres.volume[5]:
                self.case.append(0)
            elif vol > TankDimensionsMetres.volume[5] and vol <= sum(TankDimensionsMetres.volume[4:]):
                self.case.append(1)
            elif vol > sum(TankDimensionsMetres.volume[4:]) and vol <= sum(TankDimensionsMetres.volume[3:]):
                self.case.append(2)
            elif vol > sum(TankDimensionsMetres.volume[3:]) and vol <= sum(TankDimensionsMetres.volume[2:]):
                self.case.append(3)
            elif vol > sum(TankDimensionsMetres.volume[2:]) and vol <= sum(TankDimensionsMetres.volume[1:]):
                self.case.append(4)

    def calculate_vapour_cg(self):
        '''
        Calculates vapour centre of gravity as average of all CG multiplied by their masses
        '''
        for vol,case,height,density in zip(self.NOS_mass_and_volume_data.vapour_volume_m3,\
            self.case,self.vapour_height_m,\
            self.NOS_mass_and_volume_data.DAQ_pressure_to_density_data.density_gas_kg_m3):

            numerator = 0

            #Case 0 is special (no filled cylinders)
            if case == 0:
                numerator = TankDimensionsMetres.volume[5] * density * height / 2 *\
                   vol * density

            #General case
            else:
                i = 0
                #Adding filled cylinders
                for i in range(case):
                    numerator += TankDimensionsMetres.volume[5 - i] * density *\
                       TankDimensionsMetres.length[5 - i]/2

                #Accounting for partially filled cylinder
                numerator += (height + sum(TankDimensionsMetres.length[-case:]))/2*\
                    (vol-sum(TankDimensionsMetres.volume[-case:]))*density

            self.vapour_CG_m.append(TankDimensionsMetres.total_length - numerator/(vol*density))

    def __init__(self, i_NOS_mass_and_volume, i_NOS_liquid_CG):
        self.NOS_mass_and_volume_data = i_NOS_mass_and_volume
        self.NOS_liquid_CG_data = i_NOS_liquid_CG

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.case = []
        self.calculate_cases()

        self.vapour_height_m = [TankDimensionsMetres.total_length - x for x in \
            self.NOS_liquid_CG_data.liquid_height_m]

        self.vapour_CG_m = []
        self.calculate_vapour_cg()

        self.vapour_mass_lb = [kg_to_pounds(x) for x in \
            self.NOS_mass_and_volume_data.vapour_mass_kg]
        self.vapour_CG_in = [metres_to_inches(x) for x in self.vapour_CG_m]


if __name__ == "__main__":
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('test_csv.csv')

    test_data = NOSVapourCG(NOSMassAndVolume(raw_dat),NOSLiquidCG(NOSMassAndVolume(raw_dat)))
    test_file = open('NOS_vapour_CG_test.csv','w')

    i = 0
    while i < len(raw_dat.time_s):
        test_file.write(f'{raw_dat.time_s[i]},'+\
            f'{test_data.NOS_mass_and_volume_data.liquid_volume_m3[i]},'+\
            f'{test_data.case[i]},{test_data.vapour_height_m[i]},'+\
            str(test_data.NOS_mass_and_volume_data.DAQ_pressure_to_density_data.\
            density_gas_kg_m3[i])+f',{test_data.NOS_mass_and_volume_data.vapour_mass_kg[i]},'+\
            f'{test_data.vapour_CG_m[i]},{test_data.vapour_mass_lb[i]},'+\
            f'{test_data.vapour_CG_in[i]}\n')
        i += 1

    test_file.close()
