
class DAQRaw():
    '''
    A class for holding all the data arrays for the raw DAQ data.

    It self-calculates all remaining fields during initialization.
    '''

    def __init__(self, i_time_s, i_tank_pressure_psig, \
                 i_recorded_mass_lb, i_thrust_lb, i_test_cond = None):
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

        i_test_cond: dict of float
            Information about the test conditions. Default to None, in which case a
            default constants.ConstantsManager will be imported and created, and the
            values taken from there.
        '''

        if i_test_cond is None:
            from constants import ConstantsManager as CM
            self.test_cond = CM().test_conditions
        else:
            self.test_cond = i_test_cond

        self.data_size = len(i_time_s)

        self.time_s = [float(time) for time in i_time_s]
        self.tank_pressure_psig = [float(val) for val in i_tank_pressure_psig]
        self.tank_pressure_psia = None
        self.recorded_mass_lb = [float(val) for val in i_recorded_mass_lb]
        self.adjusted_mass_lb = None
        self.thrust_lb = [float(val) for val in i_thrust_lb]

        self.self_calculate_remaining_values()

    @classmethod
    def sample_instance(cls, data_length):
        '''
        Provides a primitive instance of the class based on the fixed given data length

        Parameters
        ----------

        data_length: int
            How many data points the instance should possess.

        Returns
        -------

        `DAQRaw`:
            The sample class
        '''
        return cls(\
            list(range(data_length)), [100 - 10*x for x in range(data_length)],\
            [1000 - 100*x for x in range(data_length)], [1.0 - 0.1*x for x in range(data_length)])

    @classmethod
    def sample_instance_linear(cls, data_length):
        '''
        Provides a primitive instance of the class based on the fixed given data length,
        with data decaying linearly.

        Parameters
        ----------

        data_length: int
            How many data points the instance should possess.

        Returns
        -------

        `DAQRaw`:
            The sample class
        '''
        return cls(\
            list(range(data_length)), [100*(1 - x/data_length) for x in range(data_length)],\
            [1000*(1 - x/data_length) for x in range(data_length)],\
            [1.0*(1 - x/data_length) for x in range(data_length)])

    @classmethod
    def sample_instance_exp(cls, data_length, exp_factor = 2.71):
        '''
        Provides a primitive instance of the class based on the fixed given data length,
        with data decaying exponentially

        Parameters
        ----------

        data_length: int
            How many data points the instance should possess.
        exp_factor: float
            How fast the data needs to decay. Default is 2.71.

        Returns
        -------

        `DAQRaw`:
            The sample class
        '''
        return cls(\
            list(range(data_length)), [100*(exp_factor**(-x)) for x in range(data_length)],\
            [1000*(exp_factor**(-x)) for x in range(data_length)], [1.0*(exp_factor**(-x)) for x \
            in range(data_length)])


    def self_calculate_remaining_values(self):
        '''
        Calculates the remaining values that were not given during initialization.
        '''
        self.tank_pressure_psia = [tp_psig_val + self.test_cond['local_atmos_pressure'] \
                for tp_psig_val in self.tank_pressure_psig]

        self.adjusted_mass_lb = [rec_mass_lb_val - self.test_cond['water_used_for_heating'] \
                for rec_mass_lb_val in self.recorded_mass_lb]
