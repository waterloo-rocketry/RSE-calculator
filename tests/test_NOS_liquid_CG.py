from NOS_mass_and_volume import NOSMassAndVolume as NMV
from NOS_liquid_CG import NOSLiquidCG as NLC
from constants import ConstantsManager as CM
from csv_extractor import CSVExtractor

ERROR_TOLERANCE = 0.001
EXAMPLE_COEFFCIENT = 1.01
SAMPLE_FILE_PATH = 'data/downsampled_NOS_liquid_CG_sample_output.csv'


def test_calculate_cases():

    consts = CM('data\\test_constants.yaml')
    tank_volumes = consts.tank_dimensions_meters['volume']

    # Arbitrary values

    assert NLC.calculate_cases([0], tank_volumes) == [0]

    assert NLC.calculate_cases([0.0001], tank_volumes) == [1]

    assert NLC.calculate_cases([0.0002], tank_volumes) == [2]

    assert NLC.calculate_cases([0.00645], tank_volumes) == [3]

    assert NLC.calculate_cases([0.01], tank_volumes) == [4]

    # Exact values

    assert NLC.calculate_cases([tank_volumes[1]], tank_volumes) == [0]

    assert NLC.calculate_cases([sum(tank_volumes[1:3])], tank_volumes) == [1]

    assert NLC.calculate_cases([sum(tank_volumes[1:4])], tank_volumes) == [2]

    assert NLC.calculate_cases([sum(tank_volumes[1:5])], tank_volumes) == [3]

    assert NLC.calculate_cases([sum(tank_volumes[1:6])], tank_volumes) == [3]

    assert NLC.calculate_cases([sum(tank_volumes[1:6])*EXAMPLE_COEFFCIENT],
                               tank_volumes) == [4]


def test_calculate_liquid_heights():

    consts = CM('data\\test_constants.yaml')
    tank_volumes = consts.tank_dimensions_meters['volume']

    assert abs(NLC.calculate_liquid_heights([0.0001], [1], consts.tank_dimensions_meters)[0]
               - 0.025808) < 0.025808*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([0.0002], [2], consts.tank_dimensions_meters)[0]
               - 0.042699) < 0.042699*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([0.00645], [3], consts.tank_dimensions_meters)[0]
               - 0.984114) < 0.984114*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([0.01], [4], consts.tank_dimensions_meters)[0]
               - 2.100546) < 2.100546*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([sum(tank_volumes[1:2])], [0],
                                            consts.tank_dimensions_meters)[0]
               - 0.0127) < 0.0127*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([sum(tank_volumes[1:3])], [1],
                                            consts.tank_dimensions_meters)[0]
               - 0.03175) < 0.03175*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([sum(tank_volumes[1:4])], [2],
                                            consts.tank_dimensions_meters)[0]
               - 0.97536) < 0.97536*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([sum(tank_volumes[1:5])], [3],
                                            consts.tank_dimensions_meters)[0]
               - 0.99441) < 0.99441*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([sum(tank_volumes[1:6])], [3],
                                            consts.tank_dimensions_meters)[0]
               - 1.0098) < 1.0098*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_heights([sum(tank_volumes[1:6])*EXAMPLE_COEFFCIENT], [4],
                                            consts.tank_dimensions_meters)[0]
               - 1.0374) < 1.0374*ERROR_TOLERANCE


def test_calculate_liquid_cg():

    consts = CM('data\\test_constants.yaml')
    tank_dims_m = consts.tank_dimensions_meters

    # Test for each case

    assert abs(NLC.calculate_liquid_cg([4], [1.264], tank_dims_m, [0.007349], [794.31])[0]
               - 0.53455 < 0.53455*ERROR_TOLERANCE)

    assert abs(NLC.calculate_liquid_cg([3], [1.0002], tank_dims_m, [0.006530], [806.77])[0]
               - 0.47226 < 0.47226*ERROR_TOLERANCE)

    assert abs(NLC.calculate_liquid_cg([2], [0.9676], tank_dims_m, [0.006358], [808.16])[0]
               - 0.48986 < 0.48986*ERROR_TOLERANCE)

    assert abs(NLC.calculate_liquid_cg([1], [0.0241], tank_dims_m, [9.221*10**(-5)], [1085.32])[0] -
               0.013144) < 0.013144*ERROR_TOLERANCE

    assert abs(NLC.calculate_liquid_cg([0], [0.0001657], tank_dims_m, [5.249*10**(-7)],
                                       [1085.32])[0] - 3.6165*10**(-6)) < 3.6165*10**(-6)*ERROR_TOLERANCE


def test_with_sample_file():
    ext = CSVExtractor()
    raw_dat = ext.extract_data_to_raw_DAQ('data\\downsampled_test_csv.csv')

    consts = CM('data\\test_constants.yaml')
    nmv = NMV(raw_dat, i_constants=consts)
    nlc = NLC(nmv)

    sample_file = open(SAMPLE_FILE_PATH, 'r')

    for idx in range(len(raw_dat.time_s)):  # all lists the same length
        current_line_split = sample_file.readline().split(',')
        assert abs(raw_dat.time_s[idx] -
                   float(current_line_split[0])) < ERROR_TOLERANCE
        assert abs(
            nmv.liquid_volume_m3[idx] - float(current_line_split[1])) < ERROR_TOLERANCE
        assert nlc.case[idx] == float(current_line_split[2])
        assert abs(
            nlc.liquid_height_m[idx] - float(current_line_split[3])) < ERROR_TOLERANCE
        assert abs(nmv.DAQ_pressure_to_density_data.density_liquid_kg_m3[idx] -
                   float(current_line_split[4])) < ERROR_TOLERANCE
        assert abs(nmv.liquid_mass_kg[idx] -
                   float(current_line_split[5])) < ERROR_TOLERANCE
        assert abs(nlc.liquid_cg_m[idx] -
                   float(current_line_split[6])) < ERROR_TOLERANCE
        assert abs(nlc.liquid_mass_lb[idx] -
                   float(current_line_split[7])) < ERROR_TOLERANCE
        assert abs(nlc.liquid_cg_in[idx] -
                   float(current_line_split[8])) < ERROR_TOLERANCE
