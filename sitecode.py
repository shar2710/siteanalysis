# perform anaylis on the data from any news article from https://www.ndtv.com/
# IMPORTING LIBRARIES
import pandas as pd  # TO CREATE DATAFRAME
import requests  # TO FETCH WEBSITE CONTENT
from bs4 import BeautifulSoup  # TO PARSE HTML CONTENT
import nltk
from nltk.corpus import stopwords

# with site link as the user input and then fetching the website title and text from the website, and then creating a csv file with the data
# FETCHING WEBSITE CONTENT
url = input("Enter the website link: ")
# converting url into response object
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.find('h1').text
text = soup.find('div', class_='content').text
newfile = title + '\n' + text  # CONCATENATE TITLE AND TEXT
with open(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\newfile.txt", 'w', encoding='utf-8') as f:
    f.write(newfile)

# SAVING THE NEW text FILE
newfile = r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\newfile.txt"

# converting newfile into a dataframe and adding text and title columns
df = pd.DataFrame(columns=['title', 'text'])
df['title'] = [title]
df['text'] = [text]
df.to_csv(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\inputsite.csv", mode='a', index=False, header=False)

#Cleaning using Stop Words Lists
stop_words=set(stopwords.words('english'))
#NUMBER OF SYLLABLES IN A WORD
def count_syllables(word):
    vowels = "aeiouAEIOU"
    count = 0
    prev_char = None  # Initialize prev_char (can be skipped if using approach 2)

    for char in word:
        if prev_char is not None and char in vowels and prev_char not in vowels:
            count += 1
        prev_char = char

    return count


# performing sentiment analysis on the data
# IMPORTING POSITIVE AND NEGATIVE WORDS
positive_words = set()
negative_words = set()
with open(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\positive_words.txt", encoding='utf-8') as f:
    for line in f:
        positive_words.add(line.strip())
with open(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\negative_words.txt", encoding='utf-8') as f:
    for line in f:
        negative_words.add(line.strip())

# INITIALISING VARIABLES 
positive_score = []
negative_score = []
polarity_score = []
subjectivity_score = []
avg_sentence_length=[]
percentage_complex_words=[]
fog_index=[]
avg_words_per_sentence=[]
complex_word_count=[]
word_count=[]
syllable_per_word=[]
personal_pronouns=[]
avg_word_length=[]

#perorfm analysis on the data from the input file
with open(newfile, 'r', encoding='utf-8') as f:
    text = f.read()
    sentences=nltk.sent_tokenize(text)
    words=nltk.word_tokenize(text)
    word_count.append(len(words)) #word count
    sentence_count=len(sentences) 
    for sentence in sentences:
        words=nltk.word_tokenize(sentence)
        avg_words_per_sentence.append(len(words))
        syllable_count=0
        complex_words=0
        personal_pronoun_count=0
        for word in words:
            syllable_count+=count_syllables(word)
            if word in positive_words or word in negative_words:
                complex_words+=1 #complex word count
            if word.lower() in ['i','me','my','mine','we','us','our','ours']:
                personal_pronoun_count+=1 #personal pronoun count

        for i in range(len(df)):
           pos = 0
           neg = 0
           for word in df['title'][i].split():
            if word.lower() in positive_words:
               pos += 1
            if word.lower() in negative_words:
               neg += 1
        positive_score.append(pos)
        negative_score.append(neg)
        polarity_score.append((pos - neg) / (pos + neg + 0.000001))
        subjectivity_score.append((pos + neg) / (len(df['title'][i].split()) + 0.000001))
                #readability analysis
        avg_sentence_length.append(len(words)/sentence_count)
        percentage_complex_words.append(complex_words/len(words))
        fog_index.append(0.4*(avg_sentence_length[-1]+percentage_complex_words[-1]))
        #average word per sentence
        avg_word_length.append(sum(len(word) for word in words)/len(words))
        #syllable per word
        syllable_per_word.append(syllable_count/len(words))
        #syllable per word
        syllable_per_word.append(syllable_count/len(words))
        #average word length
        avg_word_length.append(sum(len(word) for word in words)/len(words))
    

    




'''
STEP 3
OUTPUT DATA STRUCTURE

print(len(positive_score))
print(len(negative_score))
print(len(polarity_score))
print(len(subjectivity_score))
print(len(avg_sentence_length))
print(len(percentage_complex_words))
print(len(fog_index))
print(len(complex_word_count))

print(len(word_count))
print(len(syllable_per_word))
print(len(personal_pronouns))
print(len(avg_word_length))

'''




word_count = len(words)
complex_word_count=len(complex_word_count)
syllable_per_word=len(words)/syllable_count
personal_pronouns=personal_pronoun_count
avg_word_length=sum(len(word) for word in words)/len(words)

# CREATING A DATAFRAME WHICH INCLUDES ALL THE VARIABLES AND All INPUT VARIABLES IN THE INPUT FILE
data={'Link': url,
    'Title': title,
    'Positive Score':positive_score,
    'Negative Score':negative_score,
    'Polarity Score':polarity_score,
    'Subjectivity Score':subjectivity_score,
    'Average Sentence Length':avg_sentence_length,
    'Percentage of Complex Words':percentage_complex_words,
    'Fog Index':fog_index,
    'Average Number of Words Per Sentence':avg_words_per_sentence,
    'Complex Word Count':complex_word_count,
    'Word Count':word_count,
    'Syllable Per Word':syllable_per_word,
    'Personal Pronouns':personal_pronouns,
    'Average Word Length':avg_word_length}


output_df = pd.DataFrame(data)
output_df.to_csv(r"C:\Users\sejal\OneDrive\Documents\NOTES\python projects\siteanalysis\outputsite.csv", mode='a', index=False, header=False)
print("success")