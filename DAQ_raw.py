import numpy as np


class DAQRaw:
    '''
    Hold and populate all the data arrays for the raw DAQ data.
    '''

    def __init__(self, i_time_s, i_tank_pressure_psig,
                 i_recorded_mass_lb, i_thrust_lb, i_test_cond=None):
        '''
        Initialize all base values.

        Parameters
        ----------

        i_time: python list of float
            The timestamps for the test data.

        i_tank_pressure_psig: python list of float
            The tank pressure at each timestamp.

        i_recorded_mass: python list of float
            The recorded mass at each timestamp.

        i_thrust: python list of float
            The recorded thrust at each timestamp.

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

        self.time_s = np.array(i_time_s).astype(float)
        self.tank_pressure_psig = np.array(i_tank_pressure_psig).astype(float)
        self.tank_pressure_psia = None
        self.recorded_mass_lb = np.array(i_recorded_mass_lb).astype(float)
        self.adjusted_mass_lb = None
        self.thrust_lb = np.array(i_thrust_lb).astype(float)

        self.calculate_derived_fields()

    def calculate_derived_fields(self):
        '''
        Calculate fields that are not given directy through DAQ data.
        '''


        if not self.test_cond["end_idx"]:
            self.end_of_burn_idx = self.find_idx_of_nearest(list(self.time_s),
                                                self.test_cond['end_of_burn'])
        else:
            self.end_of_burn_idx = self.test_cond["end_idx"]

        # If the start time (or index) is nonzero, 
        # the dataset mut be trimmed since the calculator was not initally written to support such functionality
        if self.test_cond["start_idx"]:  
            self.start_idx = self.test_cond["start_idx"]
            self.time_s = self.time_s[self.start_idx:]
            self.tank_pressure_psig = np.array(self.tank_pressure_psig[self.start_idx:])
            self.recorded_mass_lb = self.recorded_mass_lb[self.start_idx:]
            self.thrust_lb = self.thrust_lb[self.start_idx:]
            self.end_of_burn_idx -= self.start_idx
        else:
            self.start_idx = "NOT-SPECIFIED"

        self.tank_pressure_psia = self.tank_pressure_psig + \
            self.test_cond['local_atmos_pressure']
        self.adjusted_mass_lb = self.recorded_mass_lb - \
            self.test_cond['water_used_for_heating']

    @staticmethod
    def find_idx_of_nearest(array, value):
        '''
        Find the nearest value in the given array
         
        Credit: 
        https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        '''
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    @classmethod
    def sample_instance(cls, data_length):
        '''
        Provide a primitive instance of the class based on the fixed given data length.

        Parameters
        ----------

        data_length: int
            How many data points the instance should possess.

        Returns
        -------

        `DAQRaw`:
            The sample class.
        '''
        time_s = np.arange(data_length)
        return cls(time_s, 100 - 10*time_s, 1000 - 100*time_s, 1.0 - 0.1*time_s)

    @classmethod
    def sample_instance_linear(cls, data_length):
        '''
        Provide a primitive instance of the class based on the fixed given data length,
        with data decaying linearly.

        Parameters
        ----------

        data_length: int
            How many data points the instance should possess.

        Returns
        -------

        `DAQRaw`:
            The sample class.
        '''

        time_s = np.arange(data_length)
        return cls(time_s, 100*(1 - time_s/data_length),
                   1000*(1 - time_s/data_length), 1.0*(1 - time_s/data_length))
