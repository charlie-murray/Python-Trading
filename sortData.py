import csv
from csv import writer
from posixpath import split

def loaderFunction():
    f = open('Historical_Data.csv', 'w+')
    f.close()
    with open('all_stocks_5yr.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        currentStock = ''
        currentList = []
        dates = []
        x = 1
        for row in spamreader:
            strSplit = row[0].split(',')
            if currentStock == '':
                currentStock = strSplit[6]
                currentList.append(strSplit[6])
                currentList.append(strSplit[4])
                if x == 1:
                    dates.append('')
                    dates.append(strSplit[0])
            elif currentStock == strSplit[6]:
                currentList.append(strSplit[4])
                if x == 1:
                    dates.append(strSplit[0])
            else:
                with open('Historical_Data.csv', 'a', newline='') as f_object:
                    write_object = writer(f_object)
                    if x == 1:
                        write_object.writerow(dates)
                    write_object.writerow(currentList)
                    f_object.close()
                currentList.clear()
                currentStock = strSplit[6]
                currentList.append(strSplit[6])
                currentList.append(strSplit[4])
                x += 1  
            
if __name__ == '__main__':
    # sortData.py executed as script
    loaderFunction()
            