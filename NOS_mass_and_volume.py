from constants import pounds_to_kg
from constants import TankDimensionsMetres
from DAQ_pressure_to_density import DAQPressureToDensity
from DAQ_raw import DAQRaw

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
        calculate_liquid_volume()

        #Calculate volume of vapour in m^3
        self.vapour_volume_m3 = [TankDimensionsMetres.total_volume - x\
            for x in self.liquid_volume_m3]

        #Calculating mass of liquid and vapour at each time step in kg/m^3
        self.liquid_mass_kg = [x*y for x,y in\
            zip(self.DAQ_pressure_to_density_data.density_liquid_kg_m3,self.liquid_volume_m3)]
        self.vapour_mass_kg = [x*y for x,y in\
            zip(self.DAQ_pressure_to_density_data.density_gas_kg_m3, self.vapour_volume_m3)]



