import constants as consts
from constants import ConstantsManager as ConstsM


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

        self.consts_m = ConstsM()

        self.DAQ_data = i_DAQ_data
        self.engine_CG = i_engine_CG

        # Remaining spreadsheet values are direct copies of columns from other sheets
        self.zeroed_time = None
        self.thrust_N = None
        self.engine_mass_g = None
        self.propellant_CG_mm = None

        self.XML_tags = None

        self.self_calculate_remaining_values()

    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        time = self.DAQ_data.time_s
        self.zeroed_time = [time[idx] - time[0] for idx in range(len(time))]

        self.thrust_N = [consts.pounds_to_N(thrust) for thrust in self.DAQ_data.thrust_lb]

        self.engine_mass_g = [consts.pounds_to_kg(mass)*1000 for \
                mass in self.engine_CG.propellant_mass_lb]

        self.propellant_CG_mm = [self.recalculate_propellant_CG_mm(\
                prop_CG_in_val, self.consts_m) for \
                prop_CG_in_val in self.engine_CG.propellant_CG_in]

#         self.XML_tags = [self.prepare_XML_tag_for_data_point(idx) for \
#                 idx in range(len(self.DAQ_data.time_s))]
        self.XML_tags = [self.prepare_XML_tag_for_data_point(z_t, t_N, eng_m, prop_CG) \
                for z_t, t_N, eng_m, prop_CG in zip(self.zeroed_time, self.thrust_N, \
                self.engine_mass_g, self.propellant_CG_mm)]


    @staticmethod
    def recalculate_propellant_CG_mm(prop_CG_in_val, consts_m):
        '''
        Calculates the final centre of gravity considering the oxidizer tank location

        Parameters
        ----------

        prop_CG_in_val: float
            The time stamp, zeroed considering the start of the burn
        consts_m: constants.ConstantsManager
            The constants manager containing the engine geometry data

        Returns
        -------

        float:
            The final propellant CG in mm.
        '''
        result = consts_m.tank_dimensions_meters['total_length']*1000
        result += consts.inches_to_metres(consts_m.engine_info['dist_to_tank_start'])*1000
        result -= consts.inches_to_metres(prop_CG_in_val)*1000
        return result

    @staticmethod
    def prepare_XML_tag_for_data_point(zeroed_time, thrust_N, engine_mass_g, propellant_CG_mm):
        '''
        Calculates and returns the correct fuel mass values for a all data points.

        Parameters
        ----------

        zeroed_time: float
            The time stamp, zeroed considering the start of the burn
        thurst_N: float
            The amount of force, in newtons, at this data point
        engine_mass_g: float
            The mass of the engine at the data point, in grams
        propellant_CG_mm: float
            The centre of gravity for the engine at the data point, in mm from the bottom

        Returns
        -------

        str:
            The finsihed xml tag for a specific data point.
        '''

        xml_tag = ''
        xml_tag += '<eng-data t=\"'
        xml_tag += "{:.2f}".format(round(zeroed_time,2)) + '\" '
        xml_tag += 'f=\"' + "{:.2f}".format(round(thrust_N, 2)) + '\" '
        xml_tag += 'm=\"' + "{:.3f}".format(round(engine_mass_g, 3)) + '\" '
        xml_tag += \
            'cg=\"' + "{:.3f}".format(round(propellant_CG_mm, 3)) + '\"/>'
        return xml_tag

