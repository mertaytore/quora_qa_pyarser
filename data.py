from processv2 import QuoraParser
import csv, sys, random
import importlib
parser = QuoraParser()

def create_train_csv():
    print('enter train')
    count = 0
    outfile = open("newtest3train.txt", "r")
    csvfile = open('train.csv', 'a')
    datawriter = csv.writer(csvfile)
    #datawriter.writerow(["Context","Utterance","Label"])

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
    print('exit train')

def create_valid_csv():
    count = 0
    length = 0
    outfile = open("newtest3valid.txt", "r")
    distractorfile =  open("outnewtest3.txt", "r")
    csvfile = open('valid.csv', 'a')
    datawriter = csv.writer(csvfile)
    datawriter.writerow(["Context","Ground Truth Utterance","Distractor_0","Distractor_1","Distractor_2","Distractor_3","Distractor_4","Distractor_5","Distractor_6","Distractor_7","Distractor_8"])
    rand_num = 0

    for line in outfile:
        count = count + 1
        q, gtu = parser.get_data(line)

        while (length < 9):
            rand_num = random.randrange(0, answer_length)
            #initialize random_distractor
            for i in range(answer_length):
                random_distractor = distractorfile.readline()
                if i == rand_num:
                    break
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
    distractorfile.close()

def create_test_csv():
    count = 0
    length = 0
    outfile = open("newtest3.txt", "r")
    csvfile = open('test.csv', 'a')
    distractorfile =  open("outnewtest3.txt", "r")
    datawriter = csv.writer(csvfile)
    datawriter.writerow(["Context","Ground Truth Utterance","Distractor_0","Distractor_1","Distractor_2","Distractor_3","Distractor_4","Distractor_5","Distractor_6","Distractor_7","Distractor_8"])

    for line in outfile:
        count = count + 1
        q, gtu = parser.get_data(line)
        while (length < 9):
            rand_num = random.randrange(0, answer_length)
            #initialize random_distractor
            for i in range(answer_length):
                random_distractor = distractorfile.readline()
                if i == rand_num:
                    break
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
    distractorfile.close()



answer_length = 4750
importlib.reload(sys)
print('before train')
create_train_csv()
print('after train')
create_valid_csv()
create_test_csv()
