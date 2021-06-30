from pdfminer.high_level import extract_text
# from date_extractor import extract_dates
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
import re
import os
from PyPDF2 import PdfFileReader
from pyresparser import ResumeParser
from nltk.corpus import stopwords

# extracting pdf as text
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# phone numbers
def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)

    if phone:
        number = ''.join(phone[0])

        if resume_text.find(number) >= 0 and len(number) < 16:
            return number
    return None


# extracting emails
def extract_emails(resume_text):
    if re.findall(EMAIL_REG, resume_text):
        return re.findall(EMAIL_REG, resume_text)
    
    
# extracting linkedIn
def extract_linkedIn(resume_text):
    new_data = resume_text.split("\n\n")
    for i in new_data:
        if 'linkedin' in i:
            return(i.replace("\n",""))
        

# counting number of pages    
def No_of_pages(file):
    pdf = PdfFileReader(open(file,'rb'))
    return pdf.getNumPages()


# getting total word count of a resume
def total_wordcount(resume_text):
    words = re.findall(r"[^\W_]+", resume_text, re.MULTILINE)
    return len(words)


# extracting different sections 
def sections_of_text(resume_text):
    new_data = resume_text.split("\n\n")
    for i in range(len(new_data)):
        try:
            new_data[i] = new_data[i].replace('\n',' ')
        except:
            pass
    l = []
    HEADINGS = ['SUMMARY','PROFILE','EDUCATION','EXPERIENCE','SKILL','ACHIEVEMENT','HISTORY']
    for x in HEADINGS: 
        for i in new_data:
            if x in i.upper():
                l.append(i.strip())
    sections = {}
    for i in range(len(l)):
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,')

        l[i] = ''.join(filter(whitelist.__contains__, l[i]))
    return l

# checking work history
def work_history(l):
    for i in l:
        if 'EXPERIENCE' in i.upper():
            return 'EXPERIENCE'
    return None

# checking skills
def check_skills(l):
    for i in l:
        if 'SKILL' in i.upper() or 'SKILLS' in i.upper():
            return 'SKILLS'
    return None


# checking education
def check_education(l):
    for i in l:
        if 'EDUCATION' in i.upper() or 'HISTORY' in i.upper():
            return "Education section is there"
    return None


# checking file type
def check_fileType(file_path):
    if file_path.lower().endswith('.pdf'):
        return 'The file type of your resume is: PDF document. \nThis is one of the standard file types used for resumes. Great!'
    else:
        return None


# calculating file size
def file_size(file):
    size = os.path.getsize(file)
    size_kb= size//1000
    return size_kb


# counting personal pronuns
def pronouns():
    iAndMe = 0
    for i in filtered_data.split(" "):
        if i.lower()=="me" or i.lower()=="i":
            iAndMe+=1
    return iAndMe


# counting numbers
def numbers():
    nums = 0
    for i in filtered_data.split(" "):
        if i.isnumeric():
            nums+=1
    return nums


# hard skills
def hardSkills():
    hardSkills = {}
    new_data = ResumeParser(file_path).get_extracted_data()
    skills = new_data['skills']
    for i in skills:
        if filtered_data.count(i.lower())>=2:
            hardSkills[i]=filtered_data.count(i.lower())
    return hardSkills


# common words
def comWords():
    commonWords = {}
    lstStopwords=stopwords.words('english')
    for i in filtered_data.split(" "):
        if filtered_data.count(i.lower())>2 and i not in lstStopwords and i.isalpha():
            commonWords[i]=filtered_data.count(i.lower())
    return commonWords


# achievements
def Achievements():
    for i in filtered_data.split(" "):
        if 'ACHIEVEMENTS' in i.upper() or 'ACHIEVEMENT' in i.upper():
            return 'ACHIEVEMENTS'


# calculating scores
def Scored():
    score = 0
    semanticScore = 0
    lexicalScore = 0
    phone=extract_phone_number(resume_text)
    email=extract_emails(resume_text)
    page_count=No_of_pages(file_path)
    word_count=total_wordcount(resume_text)
    linkedin= extract_linkedIn(resume_text)
    skills=check_skills(l)
    work_experience = work_history(l)
    Education = check_education(l)
    File_type=check_fileType(file_path)
    File_size = file_size(file_path)
    comm_words=comWords()
    num_count=numbers()
    personalPronouns=pronouns()
    hard_skills=hardSkills()
    achievements = Achievements()
    
    if personalPronouns==0:
        lexicalScore+=10
    else:
        print("Personal pronouns like 'I' and 'me' violate standard resume etiquette, so we recommend removing them from your resume.")
    
    if num_count<10 and num_count>0:
        lexicalScore+=5
        print("Your resume contains less numericized data. We recommend you to add more.")
    elif num_count>10:
        lexicalScore+=10
        print("You've done your due diligence to numericize your results. Good stuff!")
    else:
        print("We recommend writing numbers like '3' and '100' in this exact form on your resume, as opposed to spelling them out like 'three' and 'one hundred'. That makes your resume more easily skimmable, and highlights your measurable accomplishments so that they stand out more.")

    if len(comm_words)>15:
        lexicalScore+=10
        print("Your resume contains "+str(len(comm_words)))
    elif len(comm_words)>10 and len(comm_words)<15:
        lexicalScore+=5
        print("Your resume contains "+str(len(comm_words)))

    if len(hard_skills)>=5:
        semanticScore+=8
        print("Your resume contains a total of around "+str(len(hard_skills))+ " hard skills. Awesome!")
    elif len(hard_skills)>0 and len(hard_skills)<=4:
        semanticScore+=4
        print("Your resume contains a total of around "+str(len(hard_skills))+ " hard skills. We recommend listing out all of your hard skills that are relevant to the jobs you're applying for in a separate section on your resume.")

    if achievements == "ACHIEVEMENTS":
        semanticScore+=15
        print('Great, Achievement section was detected in your resume but we still recommend including more bullet points numerically quantifying your contributions at past jobs.')
    else:
        print('Achievement section was not detected in your resume')

    if phone is not None:
        score+=10
        print(f'We have successfully detected your phone number on your resume as: {phone}')
    else:
        print("Phone number is not provided")
        
        
        
    if email is not None:
        score+=10
        print(f"We have successfully detected your e-mail address on your resume as: {email[0]}")
    else:
        print('Email address is not provided')
    
    
    
    if page_count==1:
        score += 10
        print('Your resume contains 1 page.')
    elif page_count == 2:
        score += 5
        print('Your resume contains 2 pages. 1 page Resumes are recommended') 
    else:
        print('Your resume should not be longer than 2 pages')
    
    
    
    if word_count in range(300,1201):
        score+=10
        print(f'Your resume contains {word_count} words')
    else:
        print('Effective range of word count is in between 300 to 1200')
    
    
    
        
    if linkedin is not None:
        score+=10
        print(f'We have successfully detected the URL to your LinkedIn profile as: {linkedin}')
    else:
        print('URL to your linkedin profile is not provided')
        
        
        
    if skills is not None:
        score+=10
        print('SKILLS section was detected in your resume')
        
    else:
        print("SKILLS section was not detected in your resume")
        
        
        
    if work_experience is not None:
        score+=10
        print("WORK EXPERIENCE section was detected in your resume")
    else:
        print('WORK EXPERIENCE section was not detected in your resume')
        
        
    
    if Education is not None:
        score+=10
        print("EDUCATION section was detected in your resume")
    else:
        print('EDUCATION section was not detected in your resume')
        
        
        
    if File_type is not None:
        score+=10
        print(File_type)
    else:
        print('The file type should be PDF document')
        
        
        
    if File_size in range(1025):
        score+=10
        print(f'The file size of your resume is: {File_size} KB')
    else:
        print('Large files can be difficult to download, recommended file size is under 1 MB')      
        
    max_score = 100
    totalScore = int((score/max_score) *40) + int(lexicalScore) + int(semanticScore)
    return totalScore


#     main function
if __name__ == '__main__':

# add name of file
    file_path = "C:/Users/DELL/Downloads/Resume - Sakshi Agrawal.pdf"
    resume_text = extract_text_from_pdf(file_path)
    PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
    EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
    LINKEDIN_REG= re.compile(r'(([a-zA-Z0-9\-])*\.|[linkedin])[linkedin/\-]+\.[a-zA-Z0-9/\-_,&=\?\.;]+[^\.,\s<]')
    data = extract_text_from_pdf(file_path)
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~-'''   
    filtered_data = ""
    for i in data:
        if i[-1] not in punctuations:
            filtered_data = filtered_data + i.lower()
        else:
            filtered_data = filtered_data + i[:-1].lower()
    l = sections_of_text(resume_text)
    
    s = Scored()
    print(f'Your score is: {s}')