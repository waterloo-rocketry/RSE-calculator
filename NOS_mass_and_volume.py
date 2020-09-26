from constants import pounds_to_kg
from constants import TankDimensionsMetres
from DAQ_pressure_to_density import DAQPressureToDensity

class NOSMassAndVolume:
    '''
    Use oxidizer tank mass data along with density data to calculate
    liquid and vapour NOS volumes and masses.
    '''
    def calculate_liquid_volume(self):
        '''
        Uses equations for two component mixtures to calculate liquid volume at each timestep
        '''
        i = 0 #current index being visited

        #Iterate through each time step
        #Use values from DAQ_pressure_to_density and DAQRaw
        while i < len(self.NOS_mass_kg):
            result = (self.NOS_mass_kg[i]-(self.DAQ_pressure_to_density_data.density_gas_kg_m3[i]*\
               TankDimensionsMetres.total_volume))/\
               (self.DAQ_pressure_to_density_data.density_liquid_kg_m3[i]-\
               self.DAQ_pressure_to_density_data.density_gas_kg_m3[i]) 

            self.liquid_volume_m3.append(result)
            i += 1

    def __init__(self, DAQ_data):
        '''
        Initialize all base values

        Parameters
        ----------
        DAQ_data: DAQRaw Object
            Object containing all input data (input oxidizer tank pressure)
        '''
        #Data from pressure_to_density calculations
        self.DAQ_pressure_to_density_data = DAQPressureToDensity(DAQ_data)
        #Mass of NOS converted to kg
        self.NOS_mass_kg = [pounds_to_kg(x) for x in DAQ_data.adjusted_mass_lb]

        #Define and calculate volume of liquid in m^3
        self.liquid_volume_m3 = []
        self.calculate_liquid_volume()

        #Calculate volume of vapour in m^3
        self.vapour_volume_m3 = [TankDimensionsMetres.total_volume - x\
            for x in self.liquid_volume_m3]

        #Calculating mass of liquid and vapour at each time step in kg/m^3
        self.liquid_mass_kg = [x*y for x,y in\
            zip(self.DAQ_pressure_to_density_data.density_liquid_kg_m3,self.liquid_volume_m3)]
        self.vapour_mass_kg = [x*y for x,y in\
            zip(self.DAQ_pressure_to_density_data.density_gas_kg_m3, self.vapour_volume_m3)]

if __name__ == '__main__':
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('test_csv.csv')
    test_data = NOSMassAndVolume(raw_dat)
    test_file = open('NOS_mass_and_volume_test.csv','w')

    i = 0
    while i < len(test_data.NOS_mass_kg):
        test_file.write(f'{raw_dat.time_s[i]},{raw_dat.adjusted_mass_lb[i]},'+\
            f'{test_data.NOS_mass_kg[i]},' +\
            f'{test_data.DAQ_pressure_to_density_data.density_liquid_kg_m3[i]},'+\
            f'{test_data.DAQ_pressure_to_density_data.density_gas_kg_m3[i]},' +\
            f'{test_data.liquid_volume_m3[i]},{test_data.vapour_volume_m3[i]},'+\
            f'{test_data.liquid_mass_kg[i]},{test_data.vapour_mass_kg[i]},\n')
        i += 1

    test_file.close()
