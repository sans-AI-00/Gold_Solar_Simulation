from utils import *
from plotting import *


def one_hour_simulation(production, consumption, charging_power, discharge_power, battery_level, battery_capacity):
    energy_acquired_by_the_battery = 0
    energy_released_by_the_battery = 0
    self_consumption = 0
    external_consumption = 0
    energy_produced = 0
    energy_fed_into_the_network = 0

    energy_produced += production

    if consumption > production:
        residual_consumption = consumption - production
        self_consumption += production
        if residual_consumption >= discharge_power:
            if battery_level > discharge_power:
                residual_consumption -= discharge_power
                energy_released_by_the_battery += discharge_power
                self_consumption += energy_released_by_the_battery
                battery_level -= energy_released_by_the_battery
                external_consumption += residual_consumption
                residual_consumption = 0
            else:
                residual_consumption -= battery_level
                energy_released_by_the_battery += battery_level
                self_consumption += energy_released_by_the_battery
                battery_level -= energy_released_by_the_battery
                external_consumption += residual_consumption
                residual_consumption = 0
        else:
            if battery_level > residual_consumption:
                energy_released_by_the_battery += residual_consumption
                self_consumption += energy_released_by_the_battery
                battery_level -= energy_released_by_the_battery
                residual_consumption = 0
            else:
                energy_released_by_the_battery += battery_level
                self_consumption += energy_released_by_the_battery
                battery_level -= energy_released_by_the_battery
                residual_consumption -= battery_level
                external_consumption += residual_consumption
                residual_consumption = 0
    else:
        residual_production = production - consumption
        self_consumption += consumption
        if residual_production >= charging_power:
            if battery_capacity - battery_level > charging_power:
                residual_production -= charging_power
                energy_acquired_by_the_battery += charging_power
                battery_level += energy_acquired_by_the_battery
                energy_fed_into_the_network += residual_production
                residual_production = 0
            else:
                residual_production -= battery_capacity - battery_level
                energy_acquired_by_the_battery += battery_capacity - battery_level
                battery_level += energy_acquired_by_the_battery
                energy_fed_into_the_network += residual_production
                residual_production = 0
        else:
            if battery_capacity - battery_level > residual_production:
                energy_acquired_by_the_battery += residual_production
                battery_level += energy_acquired_by_the_battery
                residual_production = 0
            else:
                energy_acquired_by_the_battery += residual_production
                battery_level += energy_acquired_by_the_battery
                residual_production -= battery_capacity - battery_level
                energy_fed_into_the_network += residual_production
                residual_production = 0

    if battery_level > battery_capacity:
        print('[DEBUG INFO] battery_level > battery_capacity')
    elif energy_acquired_by_the_battery > charging_power:
        print('[DEBUG INFO] energy_acquired_by_the_battery > charging_power')
    elif energy_released_by_the_battery > discharge_power:
        print('[DEBUG INFO] energy_released_by_the_battery > discharge_power')
    elif self_consumption + external_consumption != consumption:
        print('[DEBUG INFO] self_consumption + external_consumption != consumption')
        print(self_consumption + external_consumption, consumption)

    return {'energy acquired by the battery': energy_acquired_by_the_battery,
            'energy released by the battery': energy_released_by_the_battery,
            'battery level': battery_level,
            'self consumption': self_consumption,
            'external consumption': external_consumption,
            'energy produced': energy_produced,
            'energy fed into the network': energy_fed_into_the_network}


def simulation(production_history, consumption_history, max_charging_power, max_discharge_power, battery_capacity):
    total_energy_acquired_by_the_battery = 0
    total_energy_released_by_the_battery = 0
    total_self_consumption = 0
    total_external_consumption = 0
    total_consumption = 0
    total_energy_produced = 0
    total_energy_fed_into_the_network = 0
    battery_level = 0

    monthly_energy_acquired_by_the_battery_history = []
    monthly_energy_released_by_the_battery_history = []
    monthly_self_consumption_history = []
    monthly_external_consumption_history = []
    monthly_consumption_history = []
    monthly_energy_produced_history = []
    monthly_energy_fed_into_the_network_history = []

    day_count = 0
    for i in range(12):
        monthly_energy_acquired_by_the_battery = 0
        monthly_energy_released_by_the_battery = 0
        monthly_self_consumption = 0
        monthly_external_consumption = 0
        monthly_consumption = 0
        monthly_energy_produced = 0
        monthly_energy_fed_into_the_network = 0
        for j in range(30):
            day_count += 1
            print(f"day {day_count}/360")
            for k in range(24):
                actual_battery_power = battery_power(battery_capacity, battery_level, max_charging_power, max_discharge_power)
                charging_power = actual_battery_power['charging power']
                discharge_power = actual_battery_power['discharge power']
                production = production_history[i][k]
                consumption = consumption_history[i][k]
                monthly_consumption += consumption

                simulation_result = one_hour_simulation(production, consumption, charging_power, discharge_power, battery_level,
                                                        battery_capacity)

                energy_acquired_by_the_battery = simulation_result['energy acquired by the battery']
                energy_released_by_the_battery = simulation_result['energy released by the battery']
                battery_level = simulation_result['battery level']
                self_consumption = simulation_result['self consumption']
                external_consumption = simulation_result['external consumption']
                energy_produced = simulation_result['energy produced']
                energy_fed_into_the_network = simulation_result['energy fed into the network']

                monthly_energy_acquired_by_the_battery += energy_acquired_by_the_battery
                monthly_energy_released_by_the_battery += energy_released_by_the_battery
                monthly_self_consumption += self_consumption
                monthly_external_consumption += external_consumption
                monthly_energy_produced += energy_produced
                monthly_energy_fed_into_the_network += energy_fed_into_the_network

        monthly_energy_acquired_by_the_battery_history.append(monthly_energy_acquired_by_the_battery)
        monthly_energy_released_by_the_battery_history.append(monthly_energy_released_by_the_battery)
        monthly_self_consumption_history.append(monthly_self_consumption)
        monthly_external_consumption_history.append(monthly_external_consumption)
        monthly_consumption_history.append(monthly_consumption)
        monthly_energy_produced_history.append(monthly_energy_produced)
        monthly_energy_fed_into_the_network_history.append(monthly_energy_fed_into_the_network)

        total_energy_acquired_by_the_battery += monthly_energy_acquired_by_the_battery
        total_energy_released_by_the_battery += monthly_energy_released_by_the_battery
        total_self_consumption += monthly_self_consumption
        total_external_consumption += monthly_external_consumption
        total_consumption += monthly_consumption
        total_energy_produced += monthly_energy_produced
        total_energy_fed_into_the_network += monthly_energy_fed_into_the_network

    return {'monthly': [monthly_energy_acquired_by_the_battery_history, monthly_energy_released_by_the_battery_history,
                        monthly_self_consumption_history, monthly_external_consumption_history, monthly_consumption_history,
                        monthly_energy_produced_history, monthly_energy_fed_into_the_network_history],

            'annual': [total_energy_acquired_by_the_battery, total_energy_released_by_the_battery,
                       total_self_consumption, total_external_consumption, total_consumption, total_energy_produced,
                       total_energy_fed_into_the_network]}
########################################################################################################################
########################################################################################################################


if __name__ == '__main__':

    production_history = production_history(kwp=3, orientation=None, tilt=None, loc=LOC_1)

    total_energy = 0
    for i in range(len(production_history)):
        for j in range(len(production_history[i])):
            total_energy += production_history[i][j]
    print(total_energy * 30)

    monthly_consumption = [250 for i in range(12)]
    hours_of_activity = [{'start': 8, 'stop': 24} for i in range(12)]

    consumption_history = consumption_history(monthly_consumption, hours_of_activity)

    result = simulation(production_history, consumption_history, max_charging_power=2, max_discharge_power=2, battery_capacity=5)

    color_list = ['blue', 'blue', 'green', 'red', 'orange', 'yellow', 'green']
    ec_list = ['black', 'black', 'black', 'black', 'black', 'black', 'black']
    ylabel_list = ['energia accumulata (Kwh)', 'inserire titolo', 'energia autoconsumata (Kwh)', 'consumo esterno (Kwh)',
                   'consumo totale (Kwh)', 'energia prodotta (Kwh)', 'energia immessa in rete (Kwh)']
    title_list = ['Energia accumulata mensilmente', 'inserire etichetta asse y', 'Energia autoconsumata mensilmente', 'Consumo esterno mensile',
                   'Consumo totale mensile', 'Energia prodotta mensilmente', 'Energia immessa in rete mensilmente']

    for i in range(len(result['monthly'])):
        plot = hist_plot(result['monthly'][i], ylabel=ylabel_list[i], title=title_list[i], color=color_list[i], ec=ec_list[i])
        plot.savefig(f'hist/fig_{i}.png')




