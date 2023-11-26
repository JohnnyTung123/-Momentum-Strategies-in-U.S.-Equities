import csv 

def gen_signal(filename, period, band):
    # period must be greater than 50 days
    if period < 50:
        print('period must be greater than 50 days')
        return
    # band must be greater than or equal to 0
    if band < 0:
        print('band must be greater than or equal to 0')
        return
    
    """
    this code genereate signals and write to csv
    data is the filename downloaded from YHF
    band is the percent band to generate signals
    period is the number of days to calculate the local max and min
    """
    
    # e.g. HSI.csv -> HSI_signal.csv
    outfilename = filename[0:-4] + '_signal' + filename[-4:]
    # print(outfilename, 'period =', period)
    # print(outfilename, 'band =', band)
    
    # open the new file in write mode
    csvw = csv.writer(open(outfilename, 'w'))
    csvw.writerow(['Date', 'Adj Close', 'Signal'])
    
    # open the original file in read mode
    with open(filename) as f:
        csvr = csv.reader(f)
        pricelist = []
        
        for i, line in enumerate(csvr):
            if i > 0:
                price = float(line[5])
                # check there are n (period) prices in the list to get the local max and min 
                if len(pricelist) > period:
                    # get the local max and min
                    maxprice = max(pricelist[-period:])
                    minprice = min(pricelist[-period:])
                    
                    if price > maxprice * (1 + band/100):
                        signal = 1 # buy
                        
                    elif price < minprice * (1 - band/100):
                        signal = -1 # sell
                        
                    else:
                        signal = 0 # no signal
                        
                else:
                    signal = 0 # no max and min, no signal
                
                pricelist.append(price) # add the price to the list
                csvw.writerow([line[0], line[5], signal])
                    
                    
                    
                    
                    
                    
                
           
        
        
        
        
    
    