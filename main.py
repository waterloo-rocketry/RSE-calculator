from calculator_main import execute_calculation

if __name__ == '__main__':

    HARD_CODED_PATH = None
    HARD_CODED_PATH = 'test_csv.csv'

    if HARD_CODED_PATH is None:
        print('Please enter the filepath of the raw DAQ data to be used')
        file_path = input()
    else:
        file_path = HARD_CODED_PATH

    execute_calculation(file_path, 'outputxml.txt')
