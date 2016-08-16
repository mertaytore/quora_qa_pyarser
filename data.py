from processv2 import QuoraParser
import csv
import sys

parser = QuoraParser()
q, a = parser.get_data('https://www.quora.com/What-is-your-job-and-your-salary-Are-you-satisfied-with-your-current-job/answers/26027995')
at = q[0]
if "Answer to" in at[:9]:
    temp = q[0]
    temp = temp[10:]
    q[0] = temp
print(q,a)


with open('data.csv', 'w') as csvfile:
    datawriter = csv.writer(csvfile)
    datawriter.writerow(["Context","Utterance","Label"])
    rows = zip(q, a)
    for row in rows:
        datawriter.writerow(row)
        datawriter.writerow(row)
