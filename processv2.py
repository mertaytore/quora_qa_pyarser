import urllib.request
import re, sys
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
        self.inSpan = False
        self.time = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.lasttag = tag
        if tag == 'div':
            for name, value in attrs:
                if name == 'id':
                    if '_answer_content' in value:
                        self.time = self.time + 1
                        self.inDiv = True

        if tag == 'div' and self.inDiv and self.time == 1:
            for name, value in attrs:
                if name == 'class':
                    if 'content' in value[1]:
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
            self.question = data[:-7]

    def get_data(self, url):
        #initializations
        parser = QuoraParser()
        f = urllib.request.urlopen(url)
        data = f.read().decode('utf-8')
        parser.feed(data)

        question = []
        answer = []
        answer_string = ''

        # finding the index for full answer
        index = 0
        for i in range(len(parser.dataArray)):
            index = i
            if parser.dataArray[i] == ' · ':
                break
        parser.dataArray = parser.dataArray[:index]

        # Leaving answer empty if there is no answer
        if not parser.dataArray == []:
            parser.dataArray.append('__eou__')

        for data in parser.dataArray:
            answer_string += str(data) + ' '
        answer.append(answer_string)

        # Formatting question
        parser.question += '__eou__ __eot__'
        question.append(parser.question)

        return question, answer
