import csv
from DAQ_raw import DAQRaw

TEST = 1

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

        time_col_idx = -1
        tank_pressure_col_idx = -1
        recorded_mass_col_id = -1
        thrust_col_idx = -1

        for idx, itm in enumerate(label_table): 
            if (itm == 'Time (s)'):
                time_col_idx = idx
            if (itm == 'Tank Pressure (psig)'):
                tank_pressure_col_idx = idx
            if (itm == 'Recorded mass (lb)'):
                recorded_mass_col_idx = idx
            if (itm == 'Thrust (lb)'):
                thrust_col_idx = idx

        if (time_col_idx == -1 or tank_pressure_col_idx == -1 \
                or recorded_mass_col_idx == -1 or thrust_col_idx == -1):
            time_col_idx = 0
            tank_pressure_col_idx = 1
            recorded_mass_col_idx = 2
            thrust_col_idx = 3

        DAQ_times = []
        DAQ_tank_pressures = []
        DAQ_recorded_masses = []
        DAQ_thrust_values = []

        for row_idx in range(1,len(reader)):
            DAQ_times.append(reader[row_idx][time_col_idx])
            DAQ_tank_pressures.append(reader[row_idx][tank_pressure_col_idx])
            DAQ_recorded_masses.append(reader[row_idx][recorded_mass_col_idx])
            DAQ_thrust_values.append(reader[row_idx][thrust_col_idx])
            
        return DAQRaw(DAQ_times, DAQ_tank_pressures, DAQ_recorded_masses, DAQ_thrust_values)

# Testing code, to be implemented into a unit test later
if __name__ == "__main__":
    print('Extractor test active!')
    ext = CSVExtractor()
    dat = ext.extract_data_to_raw_DAQ('test_csv.csv')
    
    writer = open('csv_extractor_test.csv','w')

    i = 0
    while i < len(dat.time_s):
        w_string = f'{dat.time_s[i]},{dat.tank_pressure_psig[i]},{dat.tank_pressure_psia[i]},' +\
                f'{dat.recorded_mass_lb[i]},{dat.adjusted_mass_lb[i]},{dat.thrust_lb[i]}\n'
        i+=1
        print(w_string, '')
        writer.write(w_string)

    writer.close()