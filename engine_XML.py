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
        self.thrust_N = None
        self.engine_mass_g = None
        self.propellant_CG_mm = None

        self.XML_tags = None

        self.self_calculate_remaining_values()


    # TODO: Finish along with supporting functions
    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        time = self.DAQ_data.time_s
        self.zeroed_time = [time[idx] - time[0] for idx in range(len(time))]

        self.thrust_N = [self.DAQ_data.thrust_lb]

        self.thrust_N = [consts.pounds_to_N(thrust) for thrust in self.DAQ_data.thrust_lb]

        self.engine_mass_g = [consts.pounds_to_kg(mass)*1000 for \
                mass in self.engine_CG.propellant_mass_lb]

        self.propellant_CG_mm = [self.recalculate_propellant_CG_mm(prop_CG_in_val) for \
                prop_CG_in_val in self.engine_CG.propellant_CG_in]

        self.XML_tags = [self.prepare_XML_tag_for_data_point(idx) for \
                idx in range(len(self.DAQ_data.time_s))]
        pass

    def recalculate_propellant_CG_mm(self, prop_CG_in_val):
        result = consts.TankDimensionsMetres.total_length*1000
        result += consts.inches_to_metres(consts.EngineInfo.dist_to_tank_start)*1000
        result -= consts.inches_to_metres(prop_CG_in_val)*1000
        return result

    def prepare_XML_tag_for_data_point(self, data_point_idx):
        XML_tag = ''
        XML_tag += '<eng_data t=\"'
        XML_tag += str(round(self.zeroed_time[data_point_idx], 2)) + '\" '
        XML_tag += 'f=\"' + str(round(self.thrust_N[data_point_idx], 2)) + '\" '
        XML_tag += 'm=\"' + str(round(self.engine_mass_g[data_point_idx], 3)) + '\" '
        XML_tag += 'cg=\"' + str(round(self.propellant_CG_mm[data_point_idx], 3)) + '\"/>'
        return XML_tag
        
