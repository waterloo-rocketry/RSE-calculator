
from DAQ_pressure_to_density import DAQPressureToDensity as dpd
from DAQ_raw import DAQRaw

from constants import ConstantsManager as ConstsM

SAMPLE_FILE_PATH = 'data/downsampled_DAQ_pressure_to_density_sample_output.csv'

def test_find_closest_match():
    empty_instance = dpd(DAQRaw([],[],[],[]))
    sample_array = [3,3,4,5,5,6,7,8,100]
    assert empty_instance.find_closest_match_idx(1, sample_array) == -1
    assert empty_instance.find_closest_match_idx(11, sample_array) == 7
    assert empty_instance.find_closest_match_idx(99, sample_array) == 7
    assert empty_instance.find_closest_match_idx(100, sample_array) == 8
    assert empty_instance.find_closest_match_idx(999, sample_array) == 8
    assert empty_instance.find_closest_match_idx(5, sample_array) == 4
    assert empty_instance.find_closest_match_idx(3, sample_array) == 1

def test_calculate_reduced_temp():

    consts = ConstsM('data\\test_constants.yaml')
    crit_t = consts.nitrous_oxide_properties['critical_temp']

    # Sample calculations
    assert abs(dpd.calculate_reduced_temp(DAQRaw.sample_instance(1),[1],[2],[1], crit_t)[0]\
         - 0.3695) < 0.01
    assert abs(dpd.calculate_reduced_temp(DAQRaw.sample_instance(1),[500],[550],[250], crit_t)[0]\
         - 0.7827) < 0.01

    # Error handling
    assert dpd.calculate_reduced_temp(DAQRaw.sample_instance(1),[1],[1],[1], crit_t)[0]\
         == 1
    assert dpd.calculate_reduced_temp(DAQRaw.sample_instance(1),[100],[100],[-99], crit_t)[0]\
         == 1
    assert len(dpd.calculate_reduced_temp(DAQRaw.sample_instance(1),[1,1],[1],[1], crit_t))\
         == 1
    assert abs(dpd.calculate_reduced_temp(DAQRaw.sample_instance(1),[1,1],[2],[1], crit_t)[0]\
         - 0.3695) < 0.01

    # Multi-value test
    test_closest_p = [700,700,700,600,600]
    test_next_p = [750,750,750,700,700]
    test_temp_at_p = [250,250,250,249,249]

    correct_results_approx = [0.7697, 0.7691, 0.7684, 0.7877, 0.7874]

    test_results = dpd.calculate_reduced_temp(\
        DAQRaw.sample_instance(5), test_closest_p, test_next_p, test_temp_at_p, crit_t)

    for idx in range(len(test_results)):
        assert abs(correct_results_approx[idx] - test_results[idx]) < 0.01

def test_eqn4_2():
    consts = ConstsM('data\\test_constants.yaml')

    assert abs(dpd.eqn4_2(0.05, consts.equation_constants['eqn4_2'], \
        consts.nitrous_oxide_properties['critical_density']) - 779.1615) < 0.001

    assert abs(dpd.eqn4_2(0.00, consts.equation_constants['eqn4_2'], \
        consts.nitrous_oxide_properties['critical_density']) - 452.0000) < 0.001

    assert abs(dpd.eqn4_2(0.25, consts.equation_constants['eqn4_2'], \
        consts.nitrous_oxide_properties['critical_density']) - 1072.1024) < 0.001

    assert abs(dpd.eqn4_2(1.00, consts.equation_constants['eqn4_2'], \
        consts.nitrous_oxide_properties['critical_density']) - 1642.4465) < 0.001

def test_eqn4_3():
    consts = ConstsM('data\\test_constants.yaml')

    assert abs(dpd.eqn4_3(0.05, consts.equation_constants['eqn4_3'], \
        consts.nitrous_oxide_properties['critical_density']) - 167.7364) < 0.001

    assert abs(dpd.eqn4_3(0.00, consts.equation_constants['eqn4_3'], \
        consts.nitrous_oxide_properties['critical_density']) - 452.0000) < 0.001

    assert abs(dpd.eqn4_3(0.25, consts.equation_constants['eqn4_3'], \
        consts.nitrous_oxide_properties['critical_density']) - 39.4907) < 0.001

    assert abs(dpd.eqn4_3(1.00, consts.equation_constants['eqn4_3'], \
        consts.nitrous_oxide_properties['critical_density']) - 0.3847) < 0.001

def test_with_sample_file():
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('data\\downsampled_test_csv.csv')

    sample_file = open(SAMPLE_FILE_PATH, 'r')
    consts = ConstsM('data\\test_constants.yaml')
    dpd_object = dpd(DAQ_data=raw_dat, i_constants = consts)


    for idx in range(len(raw_dat.time_s)): # all lists the same length
        current_line_split = sample_file.readline().split(',')
        assert abs(raw_dat.time_s[idx] - float(current_line_split[0])) < 0.001
        assert abs(raw_dat.tank_pressure_psia[idx] - float(current_line_split[1])) < 0.001
        assert abs(dpd_object.index_with_closest_p[idx] - float(current_line_split[2])) < 0.001
        assert abs(dpd_object.closest_p[idx] - float(current_line_split[3])) < 0.001
        assert abs(dpd_object.next_p[idx] - float(current_line_split[4])) < 0.001
        assert abs(dpd_object.t_reduced[idx] - float(current_line_split[5])) < 0.001
        assert abs(dpd_object.one_minus_t_reduced[idx] - float(current_line_split[6])) < 0.001
        assert abs(dpd_object.reciprocal_t_reduced_minus_one[idx] - \
            float(current_line_split[7])) < 0.001
        assert abs(dpd_object.density_liquid_kg_m3[idx] - float(current_line_split[8])) < 0.001
        assert abs(dpd_object.gas_density_kg_m3[idx] - float(current_line_split[9])) < 0.001
