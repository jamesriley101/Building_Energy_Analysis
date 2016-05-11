# Building_Energy_Analysis
Python module for parsing energy data time series from a .csv export, totalizing, 
identifying periods of interest, and plotting results.

This program plots and compares two different energy time-series: the 
electrical energy consumption and thermal energy consumption in a building. 

The electrical energy data was sampled every 15 minutes on even 15-minute 
times (i.e. 04:15:00), whereas the thermal energy was sampled every 5 minutes, 
at arbitraty times (i.e. 13:27:54). In both data series the values 
corresponding to each timestamp represent the totalized consumption over
the entire lifetime of the meter, so they strictly increase. This data
is saved in csv files, with the timestamp as the first field in each row
and the totalized lifetime energy consumption of the meter in the last field. 
Several of these electrical and thermal energy data for four different
buildings are included and can be applied.

**Analyze_Energy_Data** calls several methods to execute the analysis. The files 
are opened and the data is read in to NumPy arrays. **calculate_interval_values**
is called to compute the consumption during each interval from the
difference in totals between each log time (otherwise the plot would be a 
strickly increasing line). **condense_and_convert_thermal_to_kwh** is called to 
combine all of the 5-minute intervals of the thermal data into an array 
representing 15-minute intervals, and convert the energy unit from MBTU to 
kWh. **remove_spikes** is then called to clean the the thermal data (eliminate 
impossibly high/low readingsthat arised from meter configuration and reduce 
the resolution of the plot). The two data series are then totalized, and 
totalized_values can be passed as an optional argument to the plot function.

**line_plot_date_range**, which implements matplotlib, is passed the 
interval data for the electrical meter and the thermal meter, along with 
optional arguments of the totalized series, a specified date range, and the 
respective colors for the lines. 

**highest_consumption_intervals** is passed the interval data for both series and
optional start and and end times, and prints to the console the time centered in 
the hour of highest consumption, for both the electrical and thermal energy series.

File names for import, along with optional plot arguments, are entered in the 
Analyze Energy Data driver file, which imports project_methods.
