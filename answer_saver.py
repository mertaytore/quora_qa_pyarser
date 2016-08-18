from processv2 import QuoraParser
import csv, sys, random
import importlib
parser = QuoraParser()

all_answers = []
infile = open("newtest3train.txt", "r")
outfile = open("outnewtest3.txt", "a")
importlib.reload(sys)
count_answers = 0
for line in infile:
    print(count_answers)
    q, a = parser.get_data(line)
    outfile.write(str(a[0]) + '\n')
    count_answers = count_answers + 1
answer_length = len(all_answers)
infile.close()
outfile.close()
