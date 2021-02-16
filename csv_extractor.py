import csv
import os
from DAQ_raw import DAQRaw


class CSVExtractor:
    '''
    Extract relevant data from a .csv file.
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

    def extract_data_to_raw_DAQ(self, file_path, downsample=1):
        '''
        Create a DAQRaw object from the contents of the provided csv file.

        Parameters
        ----------

        file_path: str
            The location of the .csv file.
        downsample: int
            how much the output needs to be downsampled by. Default value is 1 (no downsampling).
        '''
        csvfile = open(file_path, newline='')
        reader = list(csv.reader(csvfile))

        label_table = reader[0]
        if self.debug_mode:
            print(label_table)

        time_col_idx = -1
        tank_pressure_col_idx = -1
        recorded_mass_col_idx = -1
        thrust_col_idx = -1

        for idx, itm in enumerate(label_table):
            p_itm = itm.strip().upper()
            if p_itm == 'TIME (S)':
                time_col_idx = idx
            if p_itm == 'TANK PRESSURE (PSIG)':
                tank_pressure_col_idx = idx
            if p_itm == 'RECORDED MASS (LB)':
                recorded_mass_col_idx = idx
            if p_itm == 'THRUST (LB)':
                thrust_col_idx = idx

        if (time_col_idx == -1 or tank_pressure_col_idx == -1
                or recorded_mass_col_idx == -1 or thrust_col_idx == -1):
            time_col_idx = 0
            tank_pressure_col_idx = 1
            recorded_mass_col_idx = 2
            thrust_col_idx = 3

        DAQ_times = []
        DAQ_tank_pressures = []
        DAQ_recorded_masses = []
        DAQ_thrust_values = []

        for row_idx in range(1, len(reader)):
            if row_idx % downsample == 0:
                DAQ_times.append(reader[row_idx][time_col_idx])
                DAQ_tank_pressures.append(
                    reader[row_idx][tank_pressure_col_idx])
                DAQ_recorded_masses.append(
                    reader[row_idx][recorded_mass_col_idx])
                DAQ_thrust_values.append(reader[row_idx][thrust_col_idx])

        csvfile.close()

        return DAQRaw(DAQ_times, DAQ_tank_pressures, DAQ_recorded_masses, DAQ_thrust_values)

    @staticmethod
    def downsample_file(target_file_path, new_file_path=None, downsample=10,
                        downsample_offset=0, data_possesses_header=False):
        '''
        Downsample a given csv file into another file.

        This is mostly intended for one-time command line use. Note that for subdirectories
        double backslashes should be used.

        Parameters
        ----------

        target_file_path: str
            The location of the .csv file to be downsampled.
        new_file_path: str
            The location of the output file where the downsampled data should go. Default
            value is None, which gets equivocated to target path with a 'downsampled_' tag
            attached in front.
        downsample: int
            How much the output needs to be downsampled by. Default value is 10.
        downsample_offset: int
            How much the downsampling needs to be shifted forward.
        data_possesses_header: bool
            If the data possessess a header that needs to be preserved across downsampling.
        '''
        if new_file_path is None:
            split_path = list(os.path.split(target_file_path))
            split_path[1] = 'downsampled_' + split_path[1]
            new_file_path = os.path.join(split_path[0], split_path[1])
            print('new file path: ' + new_file_path)

        reader = open(target_file_path, 'r')
        d_writer = open(new_file_path, 'w')

        header_flag = False
        if data_possesses_header:
            header_flag = True

        read_idx = 0
        for line in reader:
            if header_flag:
                d_writer.write(line)
                header_flag = False
                continue

            if (read_idx - downsample_offset) % downsample == 0:
                d_writer.write(line)
            read_idx += 1

        reader.close()
        d_writer.close()
        print('downsampling complete!')
