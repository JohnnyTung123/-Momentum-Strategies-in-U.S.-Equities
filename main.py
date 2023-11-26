# importing the module
import csv
import math
from scipy import stats
from ma import gen_signal

# Define result_file as a global variable
result_file = 'result.csv'

# Initialize lists to store Buy, Sell, and Buy-Sell values
buy_values = []
sell_values = []
buy_sell_values = []

# Write header to result file
with open(result_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Test', 'N(Buy)', 'N(Sell)', 'Buy', 'Sell', 'Buy-Sell'])
    
def analyze_trb_strategy(dataset, period, band):
    # generating signal by input the file , period and band
    gen_signal(dataset, period, band)
    
    with open(dataset[:-4] + '_signal.csv') as f:
        csvr = csv.reader(f)
        alldata = [line for line in csvr]
        alldata.pop(0)
         # get the number of buy signal
        number_buy_signal = len([line for line in alldata if int(line[2]) == 1])
    
    with open(dataset[:-4] + '_signal.csv') as f:
        csvr = csv.reader(f)
        alldata = [line for line in csvr]
        alldata.pop(0)
         # get the number of sell signal
        number_sell_signal = len([line for line in alldata if int(line[2]) == -1])
        
    with open(dataset) as f:
        csvr = csv.reader(f)
        alldata = [line for line in csvr]
        alldata.pop(0)
        # calculate the daily return 
        unconditional_return = [math.log(float(alldata[i+1][5]) / float(alldata[i][5])) for i in range(len(alldata) - 1)] 

    with open(dataset[:-4] + '_signal.csv') as f:
        csvr = csv.reader(f)
        alldata = [line for line in csvr]
        alldata.pop(0)
        # calculate the return of the buy days 
        buy_signal_return = [math.log(float(alldata[i+1][1]) / float(alldata[i][1])) for i in range(len(alldata) - 1) if int(alldata[i][2]) == 1]
        # calculate the mean buy
        mean_buy = sum(buy_signal_return) / len(buy_signal_return)
        # buy_signal = [alldata[i] for i in range(len(alldata) - 1) if int(alldata[i][2]) == 1]
        
    with open(dataset[:-4] + '_signal.csv') as f:
        csvr = csv.reader(f)
        alldata = [line for line in csvr]
        alldata.pop(0)
        # calculate the return of the sell days 
        sell_signal_return = [math.log(float(alldata[i+1][1]) / float(alldata[i][1])) for i in range(len(alldata) - 1) if int(alldata[i][2]) == -1]
        # calculate the mean sell
        mean_sell = sum(sell_signal_return) / len(sell_signal_return)
        # sell_signal = [alldata[i] for i in range(len(alldata) - 1) if int(alldata[i][2]) == -1]
        
    buy_sell_difference = mean_buy - mean_sell
    
    # Append Buy, Sell, and Buy-Sell values to lists
    buy_values.append(mean_buy)
    sell_values.append(mean_sell)
    buy_sell_values.append(buy_sell_difference)
        
    # t-test
    p_value_buy = stats.ttest_ind(unconditional_return, buy_signal_return, equal_var=True)[1]
    p_value_sell = stats.ttest_ind(unconditional_return, sell_signal_return, equal_var=True)[1]
    p_value_buy_sell = stats.ttest_ind(buy_signal_return, sell_signal_return, equal_var=True)[1] 
        
    # Write results to CSV
    with open(result_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([f"{dataset},{period},{band}", number_buy_signal, number_sell_signal,
                             f"{mean_buy} ({p_value_buy})", f"{mean_sell} ({p_value_sell})", f"{buy_sell_difference} ({p_value_buy_sell})"])

# use ^IXIC to test the strategy
datasets = ['^IXIC.csv']
# datasets = ['^IXIC.csv', 'HSI.csv', 'TSLA.csv']

for dataset in datasets:
    analyze_trb_strategy(dataset, 50, 0)
    analyze_trb_strategy(dataset, 50, 0.01)
    analyze_trb_strategy(dataset, 150, 0)
    analyze_trb_strategy(dataset, 150, 0.1)
    analyze_trb_strategy(dataset, 200, 0)
    analyze_trb_strategy(dataset, 200, 0.1)

    # Calculate averages
    avg_buy = sum(buy_values) / len(buy_values)
    avg_sell = sum(sell_values) / len(sell_values)
    avg_buy_sell = sum(buy_sell_values) / len(buy_sell_values)

    with open(result_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Average', '', '', f"{avg_buy}", f"{avg_sell}", f"{avg_buy_sell}"])
        
    # empty the list
    buy_values = []
    sell_values = []
    buy_sell_values = []
        
    


