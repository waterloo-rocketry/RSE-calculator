from constants import TestConditions as test_cond

class DAQRaw():
    '''
    A class for holding all the data arrays for the raw DAQ data.

    It self-calculates all remaining fields during initialization. 
    '''

    def __init__(self, i_time_s, i_tank_pressure_psig, i_recorded_mass_lb, i_thrust_lb):
        '''
        Initializes all base values.

        Parameters
        ----------

        i_time: python list of float
            The timestamps for the test data.

        i_tank_pressure_psig: python list of float
            The tank pressure at each timestamp.

        i_recorded_mass: python list of float
            The recorded mass at each timestamp

        i_thrust: python list of float
            The recorded thrust at each timestamp
        '''

        self.time_s = [float(time) for time in i_time_s]
        self.tank_pressure_psig = [float(val) for val in i_tank_pressure_psig]
        self.tank_pressure_psia = None
        self.recorded_mass_lb = [float(val) for val in i_recorded_mass_lb]
        self.adjusted_mass_lb = None
        self.thrust_lb = [float(val) for val in i_thrust_lb]

        self.self_calculate_remaining_values()



    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        self.tank_pressure_psia = [tp_psig_val + test_cond.local_atmos_pressure \
                for tp_psig_val in self.tank_pressure_psig]

        self.adjusted_mass_lb = [rec_mass_lb_val - test_cond.water_used_for_heating \
                for rec_mass_lb_val in self.recorded_mass_lb]