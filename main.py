from calculator_main import execute_calculation

if __name__ == '__main__':

    # In case someone wants to hard-code a value into this in the future
    DAQ_PATH = None
    TARGET_PATH = None

    if DAQ_PATH is None:
        print('Please enter the filepath of the raw DAQ data to be used')
        daq_path = input()
    else:
        daq_path = DAQ_PATH

    if TARGET_PATH is None:
        print('Please enter the filepath to which the xml will be saved')
        target_path = input()
        if target_path == '':
            target_path = 'outputxml.txt'
    else:
        target_path = TARGET_PATH

    execute_calculation(daq_path, target_path)
