import spacy
spacy.load('en_core_web_sm')
from pdfminer.high_level import extract_text
from pyresparser import ResumeParser
import nltk
from nltk.corpus import stopwords
import re



pdf_path = "ResumeSakshiAgrawal.pdf"
new_data = ResumeParser(pdf_path).get_extracted_data()
skills = new_data['skills']
punctuations = '''!()-[]{};:'",<>./?@#$%^&*~-'''
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


def Achievements(abc):
    for i in abc:
        if 'ACHIEVEMENTS' in i.upper() or 'ACHIEVEMENT' in i.upper():
            return 'ACHIEVEMENTS'
    return None



print(comWords())
print(comSkills())
print(Achievements(abc))

#scores  calculation
def Scored():
    score = 0
    skills= commonSkills()
    Achievement = Achievements(abc)

    if Achievements is not None:
        score+=15
        print('Great, Achievement section was detected in your resume but we still recommend including more bullet points numerically quantifying your contributions at past jobs.')
    else:
        print('Achievement section was not detected in your resume')

    if commonSkills is not None:
        
        if score<6:
            print('''your resume contains less than 5 skills. This is on the low end, so we'd recommend adding a few more soft skills on your resume.''')
        else:
            score+=15
            print('our resume contains more than 5 hard skills. Awesome!')
        
    else:
        print("SKILLS section was not detected in your resume")


    max_score = 30
    return int(score/max_score)

#     main function
if __name__ == '__main__':
    
# add name of file
    file_path = input('ResumeSakshiAgrawal.pdf')#+'.pdf'
    
#     add path of file
    file = input('ResumeSakshiAgrawal.pdf')
    
    resume_text = extract_text_from_pdf(file_path)
    PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    LINKEDIN_REG= re.compile(r'(([a-zA-Z0-9\-])*\.|[linkedin])[linkedin/\-]+\.[a-zA-Z0-9/\-_,&=\?\.;]+[^\.,\s<]')
    
    # abc = sections_of_text(resume_text)
    
    s = Scored()
    print(f'Your score is: {s}')
