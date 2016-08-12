import urllib.request
import re
import unicodedata
from html.parser import HTMLParser

class QuoraParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dataArray = []
        self.question = ''
        self.lasttag = None
        self.inDiv = False
        self.inData = False
        self.inAns = False
        self.time = 0
        self.inSpan = False

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.lasttag = tag
        if tag == 'div':
            for name, value in attrs:
                if name == 'id':
                    if '_answer_content' in value:
                        print('in answer_content')
                        self.time = self.time + 1
                        self.inDiv = True

        if tag == 'div' and self.inDiv and self.time == 1:
            for name, value in attrs:
                if name == 'class':
                    print(value)
                    if 'content' in value[1]:
                        print('in rendered')
                        self.inSpan = True
                        self.lasttag = tag
                        self.inData = True

        if tag == 'span' and self.inDiv and self.time == 1:
            for name, value in attrs:
                if name == 'class' and value == 'rendered_qtext':
                    self.inSpan = True
                    self.lasttag = tag
                    self.inData = True

        if tag == 'p' and self.inData and self.time == 1:
            for name, value in attrs:
                if name == 'class' and value == 'qtext_para':
                    self.lasttag = tag
                    self.inData = True



    def handle_endtag(self, tag):
        if self.lasttag == 'span' and self.inDiv:
            self.inSpan = False

    def handle_data(self, data):
        if (self.lasttag == 'p' or self.lasttag == 'br' or self.lasttag == 'li' or self.lasttag == 'b' or self.lasttag == 'ul' or self.lasttag == 'i') and self.inData and data.strip() and self.time == 1:
            data = data.replace(u'\xa0',u'')
            self.dataArray.append(data)
        if self.lasttag == 'span' and self.inData and (self.inSpan) and data.strip() and self.time == 1:
            data = data.replace(u'\xa0',u'')
            self.dataArray.append(data)
        if self.lasttag == 'title':
            question = data[:-7]
            print("\nQUESTION: " + question)
            print ('---------------------\n')

parser = QuoraParser()

f = urllib.request.urlopen('https://www.quora.com/What-is-the-best-place-to-live-in-turkey')
data = f.read().decode('utf-8')
parser.feed(data)
parser.dataArray = parser.dataArray[:-7]
print(parser.dataArray)
