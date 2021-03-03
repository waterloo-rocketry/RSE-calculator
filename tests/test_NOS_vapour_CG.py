import numpy as np

from NOS_mass_and_volume import NOSMassAndVolume as NMV
from NOS_liquid_CG import NOSLiquidCG as NLC
from constants import ConstantsManager as CM
from csv_extractor import CSVExtractor
from NOS_vapour_CG import NOSVapourCG as NVC

ERROR_TOLERANCE = 0.001
EXAMPLE_COEFFCIENT = 1.01
SAMPLE_FILE_PATH = 'tests/sample_files/downsampled_NOS_vapour_CG_sample_output.csv'


def test_calculate_cases():

    consts = CM('tests/test_constants.yaml')
    tank_volumes = consts.tank_dimensions_meters['volume']

    # Arbitrary values

    nos_volumes_test = np.array([0, 0.0001, 0.0002, 0.00645, 0.01])
    correct_results = np.array([0, 1, 2, 3, 4])

    results = NVC.calculate_cases(nos_volumes_test, tank_volumes)

    assert np.array_equal(results, correct_results)

    # Exact values (by definition)

    nos_volumes_test2 = np.array([tank_volumes[4], sum(tank_volumes[3:]),
                                  sum(tank_volumes[2:]), sum(
                                      tank_volumes[1:]),
                                  sum(tank_volumes[:]),
                                  sum(tank_volumes[:])*EXAMPLE_COEFFCIENT])

    correct_results2 = np.array([0, 1, 2, 3, 3, 4])

    results2 = NVC.calculate_cases(nos_volumes_test2, tank_volumes)

    assert np.array_equal(results2, correct_results2)


def test_calculate_vapour_cg():

    tank_dims_m = CM('tests/test_constants.yaml').tank_dimensions_meters

    assert np.allclose(NVC.calculate_vapour_cg([3.3099*10**(-5)], [144.082],
                                               [0], [0.01405], tank_dims_m)[0],
                       1.015929, rtol=ERROR_TOLERANCE)

    assert np.allclose(NVC.calculate_vapour_cg([8.5757*10**(-5)], [143.911],
                                               [1], [0.02559], tank_dims_m)[0],
                       1.002594, rtol=ERROR_TOLERANCE)

    assert np.allclose(NVC.calculate_vapour_cg([0.0059583], [22.2713],
                                               [2], [0.91250], tank_dims_m)[0],
                       0.551429, rtol=ERROR_TOLERANCE)

    assert np.allclose(NVC.calculate_vapour_cg([0.0064893], [22.2711],
                                               [3], [0.99594], tank_dims_m)[0],
                       0.551432, rtol=ERROR_TOLERANCE)

    assert np.allclose(NVC.calculate_vapour_cg([0.006902], [22.2144],
                                               [4], [1.1016], tank_dims_m)[0],
                       0.528926, rtol=ERROR_TOLERANCE)


def test_with_sample_file():
    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(
        'tests/sample_files/downsampled_sample_DAQ_file.csv')

    consts = CM('tests/test_constants.yaml')
    nmv = NMV(raw_dat, i_constants=consts)
    nlc = NLC(nmv)
    nvc = NVC(nmv, nlc)

    sample_file = open(SAMPLE_FILE_PATH, 'r')

    for idx in range(len(raw_dat.time_s)):  # all lists the same length
        current_line_split = sample_file.readline().split(',')

        assert np.allclose(raw_dat.time_s[idx],
                           float(current_line_split[0]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nmv.vapour_volume_m3[idx], float(current_line_split[1]),
                           rtol=ERROR_TOLERANCE)

        assert nvc.case[idx] == float(current_line_split[2])

        assert np.allclose(nvc.vapour_height_m[idx], float(current_line_split[3]),
                           rtol=ERROR_TOLERANCE)
        assert np.allclose(nmv.DAQ_pressure_to_density_data.gas_density_kg_m3[idx],
                           float(current_line_split[4]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nmv.vapour_mass_kg[idx],
                           float(current_line_split[5]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nvc.vapour_cg_m[idx],
                           float(current_line_split[6]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nvc.vapour_mass_lb[idx],
                           float(current_line_split[7]), rtol=ERROR_TOLERANCE)
        assert np.allclose(nvc.vapour_cg_in[idx],
                           float(current_line_split[8]), rtol=ERROR_TOLERANCE)
