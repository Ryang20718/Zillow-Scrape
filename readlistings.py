import csv

f = open('redfin.csv')
csv_f = csv.reader(f)


for row in csv_f:
    for col in range(len(row)):
        if(col <= 13 and col >=6 ):
            print(row[col])