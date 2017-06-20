import unittest
import importlib, sys

from fetcher.extract import QuoraParser

def test_answer_fetch():

    parser = QuoraParser()
    importlib.reload(sys)

    lines = ("https://www.quora.com/How-do-I-prepare-for-the-Google-Summer-of-Code-GSoC", \
             "https://www.quora.com/How-should-I-respond-to-my-boss-who-fired-me-via-email")

    q, a = parser.get_data(lines[0])
    q2, a2 = parser.get_data(lines[1])

    print(a)
    assert a != None or a.strip() != ""
    assert a2 != None or a2.strip() != ""
