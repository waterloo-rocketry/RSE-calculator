import csv
from DAQ_raw import DAQRaw


class CSVExtractor():
    '''
    Extracts relevant data from a .csv file
    '''

    def __init__(self):
        self.debug_mode = False

    def set_debug_mode(self, mode):
        '''
        Set the local debug mode.

        Parameters
        ----------

        mode: bool
            The desired state of the debug mode for the extractor.
        '''

        self.debug_mode = mode

    def extract_data_to_raw_DAQ(self, file_path):
        '''
        Creates a DAQRaw object from the contents of the provided csv file.
        
        Parameters
        ----------

        file_path: str
            The location of the .csv file
        '''
        csvfile = open(file_path, newline='')
        reader = list(csv.reader(csvfile))

        output_list = []

        label_table = reader[0]
        print(label_table)

        for idx, itm in enumerate(label_table): 
            if (itm == 'Time (s)'):
                time_col_idx = idx
            if (itm == 'Tank Pressure (psig)'):
                tank_pressure_col_idx = idx
            if (itm == 'Recorded mass (lb)'):
                recorded_mass_col_idx = idx
            if (itm == 'Thurst (lb)'):
                thurst_col_idx = idx

        DAQ_times = []
        DAQ_tank_pressures = []
        DAQ_recorded_masses = []
        DAQ_thurst_values = []

        for row_idx in range(1,len(reader)):
            DAQ_times.append(reader[row_idx][time_col_idx])
            DAQ_tank_pressures.append(reader[row_idx][tank_pressure_col_idx])
            DAQ_recorded_masses.append(reader[row_idx][recorded_mass_col_idx])
            DAQ_thrust_values.append(reader[row_idx][thrust_col_idx])
            
        return DAQRaw(DAQ_times, DAQ_tank_pressures, DAQ_recorded_masses, DAQ_thurst_values)
