import numpy as np

from NOS_mass_and_volume import NOSMassAndVolume as NMV
from NOS_vapour_CG import NOSVapourCG as NVC
from NOS_liquid_CG import NOSLiquidCG as NLC
from engine_CG import EngineCG as ECG
from constants import ConstantsManager as CM

ERROR_TOLERANCE = 0.001
SAMPLE_FILE_PATH = 'tests/sample_files/Engine_CG_sample_output.csv'


def test_calculate_NOS_CG_values():

    # Basic functionality
    assert ECG.calculate_NOS_CG_values(1, 0, 1, 0) == 1
    assert ECG.calculate_NOS_CG_values(1, 1, 0, 0) == 0
    assert ECG.calculate_NOS_CG_values(1, 1, 1, 1) == 1

    # Additional functionality
    assert ECG.calculate_NOS_CG_values(5, 5, 1, 1) == 1
    assert ECG.calculate_NOS_CG_values(10, 1, 1, 1) == 1
    assert ECG.calculate_NOS_CG_values(5, 5, 2, 2) == 2
    assert ECG.calculate_NOS_CG_values(2, 6, 4, 4) == 4
    assert ECG.calculate_NOS_CG_values(2, 3, 10, 20) == 16

    # Picked data cases
    assert np.allclose(ECG.calculate_NOS_CG_values(11.6145, 0.0105137, 18.5946, 39.997),
                       18.61340, rtol=ERROR_TOLERANCE)

    assert np.allclose(ECG.calculate_NOS_CG_values(11.0916, 0.110046, 18.8509, 38.604),
                       19.04496, rtol=ERROR_TOLERANCE)

    assert np.allclose(ECG.calculate_NOS_CG_values(3.8884, 1.00752, 6.4026, 25.866),
                       10.40793, rtol=ERROR_TOLERANCE)

    assert np.allclose(ECG.calculate_NOS_CG_values(1.9883, 0.77356, 3.2159, 22.762),
                       8.690501, rtol=8.690501*ERROR_TOLERANCE)


def test_calculate_fuel_mass_values():
    cm = CM('tests/test_constants.yaml')

    test_set1 = ECG.calculate_fuel_mass_values(
        np.arange(5), cm.engine_info, end_of_burn=4)
    correct_set1 = [6.929129, 5.86934675, 4.8095645, 3.74978225, 2.69000]

    test_set2 = ECG.calculate_fuel_mass_values(
        np.arange(5), cm.engine_info, end_of_burn=3)
    correct_set2 = [6.929129, 5.516086, 4.103043, 2.69000, 1.276957]

    assert np.allclose(correct_set1, test_set1, rtol=ERROR_TOLERANCE)
    assert np.allclose(correct_set2, test_set2, rtol=ERROR_TOLERANCE)


def test_with_sample_file():
    from csv_extractor import CSVExtractor

    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(
        'tests/sample_files/sample_DAQ_file.csv')

    consts = CM('tests/test_constants.yaml')
    nmv = NMV(raw_dat, i_constants=consts)
    nlc = NLC(nmv)
    nvc = NVC(nmv, nlc)
    ecg = ECG(raw_dat, nvc, nlc)

    sample_file = open(SAMPLE_FILE_PATH, 'r')

    for idx in range(len(raw_dat.time_s)):  # all lists the same length
        current_line_split = sample_file.readline().split(',')
        assert np.allclose(raw_dat.time_s[idx],
                           float(current_line_split[0]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nlc.liquid_mass_lb[idx],
                           float(current_line_split[1]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nlc.liquid_cg_in[idx],
                           float(current_line_split[2]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nvc.vapour_mass_lb[idx],
                           float(current_line_split[3]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nvc.vapour_cg_in[idx],
                           float(current_line_split[4]), rtol=ERROR_TOLERANCE)
        assert np.allclose(
            raw_dat.adjusted_mass_lb[idx], float(current_line_split[5]), rtol=ERROR_TOLERANCE)
        assert np.allclose(ecg.NOS_CG_in[idx],
                           float(current_line_split[6]), rtol=ERROR_TOLERANCE)
        assert np.allclose(ecg.fuel_mass_lb[idx],
                           float(current_line_split[7]), rtol=ERROR_TOLERANCE)

        assert ecg.fuel_CG_in == float(current_line_split[8])

        assert np.allclose(
            ecg.propellant_mass_lb[idx], float(current_line_split[9]), rtol=ERROR_TOLERANCE)
        assert np.allclose(
            ecg.propellant_CG_in[idx], float(current_line_split[10]), rtol=ERROR_TOLERANCE)
