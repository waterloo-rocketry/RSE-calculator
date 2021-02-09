import numpy as np
from DAQ_pressure_to_density import DAQPressureToDensity as dpd
from DAQ_raw import DAQRaw

from constants import ConstantsManager as ConstsM

SAMPLE_FILE_PATH = 'data/downsampled_DAQ_pressure_to_density_sample_output.csv'
ERROR_TOLERANCE = 0.001


def test_eqn4_2():
    consts = ConstsM('data\\test_constants.yaml')

    one_minus_t_reduced_values = np.array([0.05, 0.00, 0.25, 1.00])
    correct_results = np.array([779.1615, 452.0000, 1072.1024, 1642.4465])

    results = dpd.eqn4_2(one_minus_t_reduced_values, consts.equation_constants['eqn4_2'],
                         consts.nitrous_oxide_properties['critical_density'])

    assert np.allclose(results, correct_results, rtol=ERROR_TOLERANCE)


def test_eqn4_3():
    consts = ConstsM('data\\test_constants.yaml')

    one_minus_t_reduced_values = np.array([0.05, 0.00, 0.25, 1.00])
    correct_results = np.array([167.7364, 452.0000, 39.4907, 0.3847])

    results = dpd.eqn4_3(one_minus_t_reduced_values, consts.equation_constants['eqn4_3'],
                         consts.nitrous_oxide_properties['critical_density'])

    assert np.allclose(results, correct_results, rtol=ERROR_TOLERANCE)


def test_with_sample_file():
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('data\\downsampled_test_csv.csv')

    sample_file = open(SAMPLE_FILE_PATH, 'r')
    consts = ConstsM('data\\test_constants.yaml')
    dpd_object = dpd(DAQ_data=raw_dat, i_constants=consts)

    for idx in range(len(raw_dat.time_s)):  # all lists the same length
        current_line_split = sample_file.readline().split(',')
        assert abs(raw_dat.time_s[idx] - float(current_line_split[0])) < 0.001
        assert abs(
            raw_dat.tank_pressure_psia[idx] - float(current_line_split[1])) < 0.001
        assert abs(dpd_object.t_reduced[idx] -
                   float(current_line_split[2])) < 0.001
        assert abs(
            dpd_object.one_minus_t_reduced[idx] - float(current_line_split[3])) < 0.001
        assert abs(dpd_object.reciprocal_t_reduced_minus_one[idx] -
                   float(current_line_split[4])) < 0.001
        assert abs(
            dpd_object.density_liquid_kg_m3[idx] - float(current_line_split[5])) < 0.001
        assert abs(
            dpd_object.gas_density_kg_m3[idx] - float(current_line_split[6])) < 0.001
