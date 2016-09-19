from extract import QuoraParser
import importlib, sys

parser = QuoraParser()
importlib.reload(sys)

line = sys.argv[1]
q, a = parser.get_data(line)
print("Question: ", q)
print("Answer: ", a)
