from processv2 import QuoraParser
import csv, sys, random

parser = QuoraParser()

'''lines_seen = set() # holds lines already seen
outfile = open("newtest3.txt", "a")
for line in open("test3.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()'''

def create_train_csv():
    count = 0
    outfile = open("newtest3train.txt", "r")
    csvfile = open('train.csv', 'a')
    datawriter = csv.writer(csvfile)
    datawriter.writerow(["Context","Utterance","Label"])

    for line in outfile:
        count = count + 1
        q, a = parser.get_data(line)
        at = q[0]
        if "Answer to" in at[:9]:
            temp = q[0]
            temp = temp[10:]
            q[0] = temp
        #print(q,a)

        rows = zip(q, a, '1')
        for row in rows:
            datawriter.writerow(row)
        print(str(count) + 'train.csv')
    outfile.close()
def create_valid_csv():
    count = 0
    length = 0
    outfile = open("newtest3valid.txt", "r")
    csvfile = open('valid.csv', 'a')
    datawriter = csv.writer(csvfile)
    datawriter.writerow(["Context","Ground Truth Utterance","Distractor_0","Distractor_1","Distractor_2","Distractor_3","Distractor_4","Distractor_5","Distractor_6","Distractor_7","Distractor_8"])

    for line in outfile:
        count = count + 1
        q, gtu = parser.get_data(line)
        while (length < 9):
            random_distractor = all_answers[random.randrange(0, answer_length)][0]
            d0 = random_distractor.split(".")
            length = len(d0)
        for i in range(9):
            if not '__eou__' in d0[i]:
                d0[i] += " __eou__"

        str0, str1, str2, str3, str4, str5, str6, str7, str8 = [], [], [], [], [], [], [], [], []
        str0.append(d0[0])
        str1.append(d0[1])
        str2.append(d0[2])
        str3.append(d0[3])
        str4.append(d0[4])
        str5.append(d0[5])
        str6.append(d0[6])
        str7.append(d0[7])
        str8.append(d0[8])

        at = q[0]
        if "Answer to" in at[:9]:
            temp = q[0]
            temp = temp[10:]
            q[0] = temp

        rows = zip(q, gtu, str0, str1, str2, str3, str4, str5, str6, str7, str8)
        for row in rows:
            datawriter.writerow(row)
        print(str(count) + 'valid.csv')
        length = 0
    outfile.close()

def create_test_csv():
    count = 0
    length = 0
    outfile = open("newtest3.txt", "r")
    csvfile = open('test.csv', 'a')
    datawriter = csv.writer(csvfile)
    datawriter.writerow(["Context","Ground Truth Utterance","Distractor_0","Distractor_1","Distractor_2","Distractor_3","Distractor_4","Distractor_5","Distractor_6","Distractor_7","Distractor_8"])

    for line in outfile:
        count = count + 1
        q, gtu = parser.get_data(line)
        while (length < 9):
            random_distractor = all_answers[random.randrange(0, answer_length)][0]
            d0 = random_distractor.split(".")
            length = len(d0)
        for i in range(9):
            if not '__eou__' in d0[i]:
                d0[i] += " __eou__"

        str0, str1, str2, str3, str4, str5, str6, str7, str8 = [], [], [], [], [], [], [], [], []
        str0.append(d0[0])
        str1.append(d0[1])
        str2.append(d0[2])
        str3.append(d0[3])
        str4.append(d0[4])
        str5.append(d0[5])
        str6.append(d0[6])
        str7.append(d0[7])
        str8.append(d0[8])

        at = q[0]
        if "Answer to" in at[:9]:
            temp = q[0]
            temp = temp[10:]
            q[0] = temp

        rows = zip(q, gtu, str0, str1, str2, str3, str4, str5, str6, str7, str8)
        for row in rows:
            datawriter.writerow(row)
        print(str(count) + 'test.csv')
        length = 0
    outfile.close()


all_answers = []
outfile = open("newtest3.txt", "r")
for line in outfile:
    q, a = parser.get_data(line)
    all_answers.append(a)
answer_length = len(all_answers)

create_train_csv()
create_valid_csv()
create_test_csv()
