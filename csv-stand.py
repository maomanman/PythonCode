import csv

csvfile=open('csvfile.csv','w',newline='')

writer=csv.writer(csvfile)

writer.writerow('a')

writer.writerow('b')

csvfile.close()

csvfile=open('csvfile.csv','r',newline='')

txtdata=csvfile.read()

csvfile.close()



