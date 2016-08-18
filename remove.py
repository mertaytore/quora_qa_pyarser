import sys

lines_seen = set() # holds lines already seen
outfile = open("newtest3.txt", "a")
for line in open("test3.txt", "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
