#perform sentimal anaylis on the data from a website
#IMPORTING LIBRARIES
import pandas as pd #TO CREATE DATAFRAME
import requests #TO FETCH WEBSITE CONTENT
from bs4 import BeautifulSoup #TO PARSE HTML CONTENT


#with site link as the user input and then fetching the website title and text from the website, and then creating a csv file with the data
#FETCHING WEBSITE CONTENT
url=input("Enter the website link: ")
#converting url into response object
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')
title=soup.find('h1').text
text=soup.find('div',class_='post-content').text
newfile=title+'\n'+text #CONCATENATE TITLE AND TEXT
with open(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\newfile.txt",'w') as f:
    f.write(newfile)


#SAVING THE NEW text FILE
newfile=r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\newfile.txt"

#converting newfile into a dataframe
df=pd.DataFrame({'title':[newfile]})
df.to_csv(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\inputsite.txt",index=False)




#performing sentiment analysis on the data
#IMPORTING POSITIVE AND NEGATIVE WORDS
positive_words=set()  
negative_words=set()
with open(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\positive_words.txt") as f:
  for line in f:
    positive_words.add(line.strip())
with open(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\negative_words.txt") as f:
  for line in f:
    negative_words.add(line.strip())

#INITIALISING VARIABLES FOR SENTIMENTAL ANALYSIS
positive_score=[]
negative_score=[]
polarity_score=[]
subjectivity_score=[]

#reading the newtext file and performing sentiment analysis
for i in range(len(df)):
    pos=0
    neg=0
    for word in df['title'][i].split():
        if word.lower() in positive_words:
            pos+=1
        if word.lower() in negative_words:
            neg+=1
    positive_score.append(pos)
    negative_score.append(neg)
    polarity_score.append((pos-neg)/(pos+neg+0.000001))
    subjectivity_score.append((pos+neg)/(len(df['title'][i].split())+0.000001))

    

    
'''
STEP 3
OUTPUT DATA STRUCTURE
'''
#CREATING A DATAFRAME WHICH INCLUDES ALL THE VARIABLES AND All INPUT VARIABLES IN THE INPUT FILE
data={'Title':title,
      'Positive Score':positive_score,
      'Negative Score':negative_score,
      'Polarity Score':polarity_score,
      'Subjectivity Score':subjectivity_score}

#SAVING THE OUTPUT DATA TO A CSV FILE OR EXCEL
df=pd.DataFrame(data)
df.to_csv(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\outputsite.csv",index=False)
print("success")










