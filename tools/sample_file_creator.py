import sys
import os


def create_sample_files():
    '''
    Create sample files using the current implmentation of RSE calculator, in such format that
    they can be used by the test suite.

    NOTE: Created files will be placed in the 'tools/creator_output/' directory so 
    that nothing gets overwritten.
    '''
    sys.path.insert(1, os.path.join(sys.path[0], '..'))

    from vapour_pressure_calculations import create_output_file as create_vpc_file
    from DAQ_pressure_to_density import create_output_file as create_dpd_file
    from NOS_mass_and_volume import create_output_file as create_nmv_file
    from NOS_liquid_CG import create_output_file as create_nlc_file
    from NOS_vapour_CG import create_output_file as create_nvc_file
    from engine_CG import create_output_file as create_ecg_file
    from calculator_main import execute_calculation

    create_vpc_file(path='tools/creator_output/downsampled_vapour_pressure_sample_output.csv',
                    downsample=10)
    create_dpd_file(
        path='tools/creator_output/downsampled_DAQ_pressure_to_density_sample_output.csv',
        daq_source_path='data/downsampled_test_csv.csv')
    create_nmv_file(
        target_path='tools/creator_output/downsampled_NOS_mass_and_volume_sample_output.csv',
                    daq_source_path='data/downsampled_test_csv.csv')
    create_nlc_file(target_path='tools/creator_output/downsampled_NOS_liquid_CG_sample_output.csv',
                    daq_source_path='data/downsampled_test_csv.csv')
    create_nvc_file(target_path='tools/creator_output/downsampled_NOS_vapour_CG_sample_output.csv',
                    daq_source_path='data/downsampled_test_csv.csv')

    # Engine CG file should not be downsampled
    create_ecg_file(target_path='tools/creator_output/Engine_CG_sample_output.csv',
                    daq_source_path='data/test_csv.csv')

    execute_calculation('data/test_csv.csv', 'tools/creator_output/created_correct_xml.txt',
                        suppress_printout=True)
    print('File creation successful!')


if __name__ == "__main__":
    # Note: for proper usage *please* run this from command line in the root directory
    # so that it can access files correctly.
    # This will dump files into the 'creator_output' directory so that people do not accidentally
    # overwrite all of the test suite sample files.
    create_sample_files()
