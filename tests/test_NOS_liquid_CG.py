import numpy as np

from NOS_mass_and_volume import NOSMassAndVolume as NMV
from NOS_liquid_CG import NOSLiquidCG as NLC
from constants import ConstantsManager as CM
from csv_extractor import CSVExtractor

ERROR_TOLERANCE = 0.001
EXAMPLE_COEFFCIENT = 1.01
SAMPLE_FILE_PATH = 'tests/sample_files/downsampled_NOS_liquid_CG_sample_output.csv'


def test_calculate_cases():

    consts = CM('tests/test_constants.yaml')
    tank_volumes = consts.tank_dimensions_meters['volume']

    # Arbitrary values

    nos_volumes_test = np.array([0, 0.0001, 0.0002, 0.00645, 0.01])
    correct_results = np.array([0, 1, 2, 3, 4])

    results = NLC.calculate_cases(nos_volumes_test, tank_volumes)

    assert np.array_equal(results, correct_results)

    # Exact values
    nos_volumes_test2 = np.array([tank_volumes[0], sum(tank_volumes[:2]),
                                  sum(tank_volumes[:3]),
                                  sum(tank_volumes[:4]),
                                  sum(tank_volumes[:]),
                                  sum(tank_volumes[:])*EXAMPLE_COEFFCIENT])

    correct_results2 = np.array([0, 1, 2, 3, 3, 4])

    results2 = NLC.calculate_cases(nos_volumes_test2, tank_volumes)

    assert np.array_equal(results2, correct_results2)


def test_calculate_liquid_heights():

    consts = CM('tests/test_constants.yaml')
    tank_volumes = consts.tank_dimensions_meters['volume']

    assert np.allclose(NLC.calculate_liquid_heights([0.0001], [1],
                                                    consts.tank_dimensions_meters)[0],
                       0.025808, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([0.0002], [2],
                                                    consts.tank_dimensions_meters)[0],
                       0.042699, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([0.00645], [3],
                                                    consts.tank_dimensions_meters)[0],
                       0.984114, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([0.01], [4],
                                                    consts.tank_dimensions_meters)[0],
                       2.100546, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([tank_volumes[0]], [0],
                                                    consts.tank_dimensions_meters)[0],
                       0.0127, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([sum(tank_volumes[:2])], [1],
                                                    consts.tank_dimensions_meters)[0],
                       0.03175, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([sum(tank_volumes[:3])], [2],
                                                    consts.tank_dimensions_meters)[0],
                       0.97536, rtol=0.97536*ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([sum(tank_volumes[:4])], [3],
                                                    consts.tank_dimensions_meters)[0],
                       0.99441, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([sum(tank_volumes[:])], [3],
                                                    consts.tank_dimensions_meters)[0],
                       1.0098, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_heights([sum(tank_volumes[:])*EXAMPLE_COEFFCIENT],
                                                    [4], consts.tank_dimensions_meters)[0],
                       1.0374, rtol=ERROR_TOLERANCE)


def test_calculate_liquid_cg():

    consts = CM('tests/test_constants.yaml')
    tank_dims_m = consts.tank_dimensions_meters

    # Test for each case

    assert np.allclose(NLC.calculate_liquid_cg([4], [1.264], tank_dims_m,
                                               [0.007349], [794.31])[0],
                       0.53455, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_cg([3], [1.0002], tank_dims_m,
                                               [0.006530], [806.77])[0],
                       0.47226, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_cg([2], [0.9676], tank_dims_m,
                                               [0.006358], [808.16])[0],
                       0.48986, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_cg([1], [0.0241], tank_dims_m,
                                               [9.221*10**(-5)], [1085.32])[0],
                       0.013144, rtol=ERROR_TOLERANCE)

    assert np.allclose(NLC.calculate_liquid_cg([0], [0.0001657], tank_dims_m,
                                               [5.249*10**(-7)],
                                               [1085.32])[0], 3.6165*10**(-6),
                       rtol=ERROR_TOLERANCE)


def test_with_sample_file():
    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ(
        'tests/sample_files/downsampled_sample_DAQ_file.csv')

    consts = CM('tests/test_constants.yaml')
    nmv = NMV(raw_dat, i_constants=consts)
    nlc = NLC(nmv)

    with open(SAMPLE_FILE_PATH, 'r') as sample_file:
        for idx in range(len(raw_dat.time_s)):  # all lists the same length
            current_line_split = sample_file.readline().split(',')
            assert np.allclose(raw_dat.time_s[idx],
                               float(current_line_split[0]), rtol=ERROR_TOLERANCE)
            assert np.allclose(
                nmv.liquid_volume_m3[idx], float(current_line_split[1]), rtol=ERROR_TOLERANCE)
            assert nlc.case[idx] == float(current_line_split[2])
            assert np.allclose(nlc.liquid_height_m[idx],
                               float(current_line_split[3]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.DAQ_pressure_to_density_data.density_liquid_kg_m3[idx],
                               float(current_line_split[4]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nmv.liquid_mass_kg[idx],
                               float(current_line_split[5]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nlc.liquid_cg_m[idx],
                               float(current_line_split[6]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nlc.liquid_mass_lb[idx],
                               float(current_line_split[7]), rtol=ERROR_TOLERANCE)
            assert np.allclose(nlc.liquid_cg_in[idx],
                               float(current_line_split[8]), rtol=ERROR_TOLERANCE)
