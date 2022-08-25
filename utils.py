import scipy.integrate as spi
import numpy as np

from global_variables import *

def get_power_function_coef(Etot, Pmax, sunrise, sunset):

    a = sunrise
    b = sunset

    k_a = (Etot - 2 * Pmax * (12 - a))/(2 * (-12 ** 2 + 12 * a + 1/2 * (12 ** 2 - a ** 2)))
    k_b = (Etot - 2 * Pmax * (b - 12))/(2 * (-12 * b + 12 ** 2 + 1/2 * (b ** 2 - 12 ** 2)))
    h_a = Pmax - 12 * k_a
    h_b = Pmax - 12 * k_b

    integrand_a = lambda x : h_a + k_a * x
    integrand_b = lambda x : h_b + k_b * x

    result_a, error_a= spi.quad(integrand_a, a, 12)
    result_b, error_b = spi.quad(integrand_b, 12, b)

    return {'h_a': h_a, 'k_a': k_a, 'h_b': h_b, 'k_b': k_b}

def power_function(coeff, sunrise, sunset, t):

    if t < sunrise or t > sunset:
        return 0
    elif t <= 12:
        return coeff['h_a'] + coeff['k_a'] * t
    elif t > 12:
        return coeff['h_b'] + coeff['k_b'] * t

def avarage_power_function(coeff, sunrise, sunset, t_0, t_1):

    t_values = np.linspace(t_0, t_1, 10000)
    result = 0

    for t_value in t_values:
        result += power_function(coeff, sunrise, sunset, t_value)
    result = result / len(t_values)

    return result

# aggiorna rendendo possibile l'ottenimento del valore da tabella
def get_orientation_and_tilt_coeff(orientation=None, tilt=None, loc=None):

    coeff = 1.1

    return coeff

# genera la produzione dell'impianto per un certo quantitativo di radiazione solare assorbita
# kwp definisce la potenza nominale dell'impianto
# kwh definisce la radiazione solare assorbita
#
# tilt è un coefficiente che dipende dall'inclinazione e dall'orientamento dei pannelli
def production(kwp, kwh, orientation=None, tilt=None, loc=None):
    coeff = get_orientation_and_tilt_coeff(orientation, tilt)
    production = kwp * kwh * coeff * 0.8

    return production

def hourly_production_distribution(kwp, coeff, sunrise, sunset):
    result = []

    for t_0 in range(0,24):
        t_1 = t_0 + 1
        kwh = avarage_power_function(coeff, sunrise, sunset, t_0, t_1)
        result.append(production(kwp, kwh, orientation=None, tilt=None, loc=None))

    return result

def production_history(kwp, orientation=None, tilt=None, loc=None):
    history = []

    for i in range(12):
        Etot = loc['average daily radiation'][i]
        Pmax = loc['maximum daily radiation'][i]
        length_of_day = loc['avarage length of day'][i]
        sunrise = 12 - length_of_day / 2
        sunset = 12 + length_of_day / 2
        coeff = get_power_function_coef(Etot, Pmax, sunrise, sunset)
        history.append(hourly_production_distribution(kwp, coeff, sunrise, sunset))

    return history
########################################################################################################################
########################################################################################################################

def consumption_function(avarage_hourly_consuption, start, stop, t):

    if t < start or t > stop:
        return 0
    else:
        return avarage_hourly_consuption

def hourly_consumption_distribution(daily_consumption, start, stop):
    avarage_hourly_consuption = daily_consumption / (stop - start)
    result = []

    for t in range(1,25):
        result.append(consumption_function(avarage_hourly_consuption, start, stop, t))

    return result

def consumption_history(monthly_consumption, hours_of_activity):
    history = []

    for i in range(12):
        daily_consumption = monthly_consumption[i] / 30
        start = hours_of_activity[i]['start']
        stop = hours_of_activity[i]['stop']
        history.append(hourly_consumption_distribution(daily_consumption, start, stop))

    return history
########################################################################################################################
########################################################################################################################

def battery_power(battery_capacity,battery_level, max_charging_power, max_discharge_power):
    discharge_power = battery_level ** 2 * max_discharge_power / battery_capacity ** 2
    charging_power = max_charging_power * (1 - battery_level ** 2 / battery_capacity ** 2)

    return {'charging power':charging_power, 'discharge power':discharge_power}

########################################################################################################################
########################################################################################################################
if __name__ == '__main__':
    result = production_history(kwp = 3, orientation=None, tilt=None, loc=LOC_1)

    total_energy = 0
    for i in range(len(result)):
        for j in range(len(result[i])):
            total_energy += result[i][j]
    print(total_energy * 30)

    monthly_consumption = [100 for i in range(12)]
    hours_of_activity = [{'start': 8, 'stop': 24} for i in range(12)]

    consumption_history = consumption_history(monthly_consumption, hours_of_activity)

    total_consumption = 0
    for i in range(len(consumption_history)):
        for j in range(len(consumption_history[i])):
            total_consumption += consumption_history[i][j]
    print(total_consumption * 30)



