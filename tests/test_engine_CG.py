from NOS_mass_and_volume import NOSMassAndVolume as NMV
from NOS_vapour_CG import NOSVapourCG as NVC
from NOS_liquid_CG import NOSLiquidCG as NLC
from engine_CG import EngineCG as ECG
from constants import ConstantsManager as CM

ERROR_TOLERANCE = 0.001
EXAMPLE_COEFFCIENT = 1.01
SAMPLE_FILE_PATH = 'data/Engine_CG_sample_output.csv'


def test_calculate_NOS_CG_values():

    # Basic functionality
    assert ECG.calculate_NOS_CG_values(1, 0, 1, 0)[0] == 1
    assert ECG.calculate_NOS_CG_values(1, 1, 0, 0)[0] == 0
    assert ECG.calculate_NOS_CG_values(1, 1, 1, 1)[0] == 1

    # Picked data cases
    assert abs(ECG.calculate_NOS_CG_values(11.6145, 0.0105137, 18.5946, 39.997)[0]
               - 18.61340) <= 18.61340*ERROR_TOLERANCE

    assert abs(ECG.calculate_NOS_CG_values(11.0916, 0.110046, 18.8509, 38.604)[0]
               - 19.04496) <= 19.04496*ERROR_TOLERANCE

    assert abs(ECG.calculate_NOS_CG_values(3.8884, 1.00752, 6.4026, 25.866)[0]
               - 10.40793) <= 10.40793*ERROR_TOLERANCE

    assert abs(ECG.calculate_NOS_CG_values(1.9883, 0.77356, 3.2159, 22.762)[0]
               - 8.690501) <= 8.690501*ERROR_TOLERANCE


def test_calculate_fuel_mass_values():
    cm = CM('data\\test_constants.yaml')

    test_set1 = ECG.calculate_fuel_mass_values(
        range(5), cm.engine_info, end_of_burn=4)
    correct_set1 = [6.929129, 5.86934675, 4.8095645, 3.74978225, 2.69000]

    test_set2 = ECG.calculate_fuel_mass_values(
        range(5), cm.engine_info, end_of_burn=3)
    correct_set2 = [6.929129, 5.516086, 4.103043, 2.69000, 1.276957]

    for c, t in zip(correct_set1, test_set1):
        assert abs(t - c) < c*ERROR_TOLERANCE

    for c2, t2 in zip(correct_set2, test_set2):
        assert abs(t2 - c2) < c2*ERROR_TOLERANCE


def test_with_sample_file():
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('data\\test_csv.csv')

    consts = CM('data\\test_constants.yaml')
    nmv = NMV(raw_dat, i_constants=consts)
    nlc = NLC(nmv)
    nvc = NVC(nmv, nlc)
    ecg = ECG(raw_dat, nvc, nlc)

    sample_file = open(SAMPLE_FILE_PATH, 'r')

    for idx in range(len(raw_dat.time_s)):  # all lists the same length
        current_line_split = sample_file.readline().split(',')
        assert abs(raw_dat.time_s[idx] -
                   float(current_line_split[0])) < ERROR_TOLERANCE
        assert abs(nlc.liquid_mass_lb[idx] -
                   float(current_line_split[1])) < ERROR_TOLERANCE
        assert abs(nlc.liquid_cg_in[idx] -
                   float(current_line_split[2])) < ERROR_TOLERANCE
        assert abs(nvc.vapour_mass_lb[idx] -
                   float(current_line_split[3])) < ERROR_TOLERANCE
        assert abs(nvc.vapour_cg_in[idx] -
                   float(current_line_split[4])) < ERROR_TOLERANCE
        assert abs(
            raw_dat.adjusted_mass_lb[idx] - float(current_line_split[5])) < ERROR_TOLERANCE
        assert abs(ecg.NOS_CG_in[idx] -
                   float(current_line_split[6])) < ERROR_TOLERANCE
        assert abs(ecg.fuel_mass_lb[idx] -
                   float(current_line_split[7])) < ERROR_TOLERANCE
        assert ecg.fuel_CG_in == float(current_line_split[8])
        assert abs(
            ecg.propellant_mass_lb[idx] - float(current_line_split[9])) < ERROR_TOLERANCE
        assert abs(
            ecg.propellant_CG_in[idx] - float(current_line_split[10])) < ERROR_TOLERANCE
