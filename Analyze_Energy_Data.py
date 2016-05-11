from project_methods import *

#import the electrical data, assign to numpy array with sub methods:
power_filename = 'SQL_Data_Exports/CSM_B-36 Main_PWR.csv'
power_data = import_energy_totals(power_filename)

#import the thermal data, assign to numpy array with submethods::
thermal_filename = 'SQL_Data_Exports/CSM_B-36 HW_MBTU.csv'
thermal_data = import_energy_totals(thermal_filename)

#convert continuous energy totals into interval consumption:
power_interval_values = calculate_interval_values(power_data[1,:])
thermal_interval_values = calculate_interval_values(thermal_data[1,:])

#condense the 5-minute thermal energy interval data into 15-min totals, convert to kWh:
thermal_interval_values = condense_and_convert_thermal_to_kwh(power_interval_values, thermal_interval_values)

#Remove unreasonabe values from thermal interval consumption data:
thermal_interval_values = remove_spikes(thermal_interval_values)

#Totalize energy consumption in building by adding electircal energy to thermal energy
totalized_energy_values = totalize_energy_consumption(power_interval_values, thermal_interval_values)

#define the time axis at the timestamps of the electrical series:
times = power_data[0,:]

#plot these series on the same line plot with the optional optional date rage, totalized series, and color arguments:
line_plot_date_range(times, power_interval_values, thermal_interval_values, '1/1/2016', '1/4/2016', totalized_energy_values)

#for both series, identify th the times centered in the highest hours of consumption during the specified interval: 
highest_consumption_intervals(times, power_interval_values, thermal_interval_values, '3/1/2016', '3/8/2016')