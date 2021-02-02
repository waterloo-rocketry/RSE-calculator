from DAQ_raw import DAQRaw
from math import e
from matplotlib import pyplot as plt


def sigmoid(x, rise_coefficient):
    k = rise_coefficient
    return 1/(e**(-k*x) + 1)

def sigmoid_advanced(start_x, amplitude, rise_coefficient, cutoff_coefficient, top_half_only):
    primary_factor = sigmoid(start_x, rise_coefficient)
    cutoff_factor = sigmoid(start_x, cutoff_coefficient)

    if top_half_only:
        primary_factor = (2*amplitude*primary_factor - amplitude) 
    else:
        primary_factor *= amplitude

    return primary_factor*cutoff_factor

def thrust_function_model(x):
    y_result = 0
    y_result += sigmoid_advanced(x, 150, (1/3), 1, top_half_only = True)
    y_result += sigmoid_advanced(x - 25, 350, (1/5), (1/2), top_half_only = False)
    y_result -= sigmoid_advanced(x- 50, 230, (1/50), 1,  top_half_only = True)
    y_result -= sigmoid_advanced(x - 200, 270, (1/30), 1,  top_half_only = True)

    return y_result

def generate_thrust_curve():
    return [thrust_function_model(x) for x in range(400)]

def generate_pressure_curve():
    return [700 - 1.5*(x) for x in range(400)]

def weight_function_model(x):
    return 26 - sigmoid_advanced(x, 10, (1/100), 1, top_half_only = True)

def generate_weight_curve():
    return [weight_function_model(x) for x in range(400)]

def generate_daq_object():
    return DAQRaw(range(400), generate_pressure_curve(), generate_weight_curve(),
            generate_thrust_curve())

def display_thrust_curve():
    plt.plot(list(range(400)), generate_thrust_curve())
    plt.show()
    generate_daq_object()
