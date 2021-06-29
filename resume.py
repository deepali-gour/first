import spacy
spacy.load('en_core_web_sm')
from pdfminer.high_level import extract_text
from pyresparser import ResumeParser
import nltk
from nltk.corpus import stopwords

pdf_path = "resume/resume.pdf"
new_data = ResumeParser(pdf_path).get_extracted_data()
skills = new_data['skills']
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~-'''
lstStopwords=stopwords.words('english')
commonWords = {}
commonSkills = {}

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)
data = extract_text_from_pdf(pdf_path)
# listOfData = data.split(" ")
abc = ""
for i in data:
    if i[-1] not in punctuations:
       abc = abc + i.lower()
    else:
        abc = abc + i[:-1].lower()

def pronouns():
    iAndMe = 0
    for i in abc:
        if i.lower()=="me" or i.lower()=="i":
            iAndMe+=1
    return iAndMe

def numbers():
    nums = 0
    for i in abc:
        if i.isnumeric():
            nums+=1
    return nums

def comWords():
    for i in abc.split(" "):
        if abc.count(i.lower())>2 and i not in lstStopwords and i.isalpha():
            commonWords[i]=abc.count(i.lower())
    return commonWords

def comSkills():
    for i in skills:
        if abc.count(i.lower())>=2:
            commonSkills[i]=abc.count(i.lower())
    return commonSkills
print(comWords())
print(numbers())
print(pronouns())
print(comSkills())