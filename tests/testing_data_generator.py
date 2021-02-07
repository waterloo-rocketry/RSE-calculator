from DAQ_raw import DAQRaw
from math import e


def sigmoid(x, rise_coefficient):
    '''
    Calculates a basic sigmoid function

    Parameters
    ----------

    x: float
        The x value of the sigmoid
    rise_coefficient: float
        The coefficient that dictates the steepness of the sigmoid.

    Returns
    -------

    float:
        The y output of this sigmoid function.
    '''
    k = rise_coefficient
    return 1/(e**(-k*x) + 1)


def sigmoid_advanced(start_x, amplitude, rise_coefficient, cutoff_coefficient, top_half_only):
    '''
    Calculates a sigmoid function with more complex parameters

    Parameters
    ----------

    start_x: float
        The x value of the sigmoid
    rise_coefficient: float
        The coefficient that dictates the steepness of the main sigmoid.
    rise_coefficient: float
        The coefficient that dictates how rapid the onset of growth is.
    top_half_only: bool
        Whether only the top half of the function should be utilized, or the whole function.

    Returns
    -------

    float:
        The y output of this sigmoid function.
    '''
    primary_factor = sigmoid(start_x, rise_coefficient)
    cutoff_factor = sigmoid(start_x, cutoff_coefficient)

    if top_half_only:
        primary_factor = (2*amplitude*primary_factor - amplitude)
    else:
        primary_factor *= amplitude

    return primary_factor*cutoff_factor


def thrust_function_model(x):
    '''
    Based on some very rough approximation, a thrust function that can be used for
    generating DAQ data.

    Parameters
    ----------

    x: float
        The x value for which thrust is desired for.

    Returns
    -------

    float:
        the simulated thrust at this instant
    '''

    y_result = 0
    y_result += sigmoid_advanced(x, 150, (1/3), 1, top_half_only=True)
    y_result += sigmoid_advanced(x - 25, 350, (1/5),
                                 (1/2), top_half_only=False)
    y_result -= sigmoid_advanced(x - 50, 230, (1/50), 1,  top_half_only=True)
    y_result -= sigmoid_advanced(x - 200, 270, (1/30), 1,  top_half_only=True)

    return y_result


def generate_thrust_curve():
    '''
    Based on some very rough approximation, a function to generate a thrust curve.

    Returns
    -------
    list of float:
        a simaulated thrust curve.
    '''
    return [thrust_function_model(x) for x in range(400)]


def generate_pressure_curve():
    '''
    Based on some very rough approximation, a function to generate a pressure curve.

    Returns
    -------
    list of float:
        a simaulated pressure curve.
    '''
    return [700 - 1.5*(x) for x in range(400)]


def weight_function_model(x):
    '''
    Based on some very rough approximation, a function that gives a weight for an instant in time.

    Parameters
    ----------
    x: float
        The x value for which weight is desired for.

    Returns
    -------
    float:
        the simulated weight at this instant
    '''
    return 26 - sigmoid_advanced(x, 10, (1/100), 1, top_half_only=True)


def generate_weight_curve():
    '''
    Based on some very rough approximation, a function to generate a weight curve.

    Returns
    -------
    list of float:
        a simaulated weight curve.
    '''
    return [weight_function_model(x) for x in range(400)]


def generate_daq_object():
    '''
    A mock function to generate a realistic DAQ object

    Returns
    -------
    DAQ_raw.DAQRaw:
        a simaulated weight curve.
    '''
    return DAQRaw(range(400), generate_pressure_curve(), generate_weight_curve(),
                  generate_thrust_curve())
