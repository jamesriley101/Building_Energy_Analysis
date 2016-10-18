import numpy as np
import csv
import dateutil.parser
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plb

#Methods
def import_energy_totals(filename):
    csv_in = open(filename, 'r')
    reader = csv.reader(csv_in)
    times = []
    values = []
    for row in reader:
        times.append(dateutil.parser.parse(row[0]))
        values.append(float(row[4]))
    csv_in.close()
    return np.array([times, values])

def calculate_interval_values(values):
    interval_values = np.empty([len(values)], dtype=float)
    for i in range(len(values)):
        if i == 0:
            interval_values[i] = values[1] - values[0]
        else:
            interval_values[i] = values[i] - values[i - 1]
    return interval_values

def condense_and_convert_thermal_to_kwh(power_interval_values, thermal_interval_values):
    thermal_combined_kwh = np.zeros([len(power_interval_values)])
    tlogs_per_plog = int(len(thermal_interval_values) / len(power_interval_values)) + 1
    i = 0
    for i in range(len(thermal_combined_kwh) - 10):
        for j in range(tlogs_per_plog):
            thermal_combined_kwh[i] += thermal_interval_values[i * tlogs_per_plog + j]
    thermal_combined_kwh =  thermal_combined_kwh * .29 * 1000
    return thermal_combined_kwh

def remove_spikes(data):
    for i in range(len(data)):
        if i == 1:
            if np.abs(data[i]) > 100:
                data[i] = 1
        elif np.abs(data[i]) > np.abs(data[i - 1] * 100 + 25) or np.abs(data[i]) > 100:
            data[i] = data[i - 1]
    return data

def totalize_energy_consumption(power_data, thermal_data):
    return power_data + thermal_data

def line_plot_date_range(times, power_data, thermal_data, start_date, end_date, totalized_data=None, power_color='red', thermal_color='blue', total_color='green'):
    plb.plot(times, power_data, color=power_color, label='Electricity Consumption (kWh)')
    plb.plot(times, thermal_data[0:len(times)], color=thermal_color, alpha=0.5, label='Thermal Energy Consumption (kWh)')
    if totalized_data is not None:
        plb.plot(times, totalized_data[0:len(times)], color=total_color, label='Totalized Energy Consumption (kWh)')
    plb.xlim(dateutil.parser.parse(start_date), dateutil.parser.parse(end_date))
    plb.ylim(0,85)
    plb.legend(loc='upper right')
    plb.show()

def highest_consumption_hours_centered(times, power_data, thermal_data, start_time='2/1/2016', end_time='2/8/2016'):
    start_time = dateutil.parser.parse(start_time)
    end_time = dateutil.parser.parse(end_time)
    window = np.ones([4]) * .25
    power_moving_avg = np.convolve(power_data, window, 'same')
    thermal_moving_avg = np.convolve(thermal_data, window, 'same')
    local_power_max_index = np.argmax(power_moving_avg[np.where(np.logical_and(times > start_time, times < end_time))]) + np.where(times==start_time)[0][0]
    local_thermal_max_index = np.argmax(thermal_moving_avg[np.where(np.logical_and(times > start_time, times < end_time))]) + np.where(times==start_time)[0][0]
    print("The hour of maximum power consumption in this time range was centered on %s" % times[local_power_max_index])
    print("The hour of maximum thermal energy consumption in this time range was centered on %s" % times[local_thermal_max_index])
    return

