import pandas as pd
from textblob import TextBlob
from googletrans import Translator
from nrclex import NRCLex
import csv

def decade(year):
   rez = (year%100)//10
   if rez == 5:
      return 50
   elif rez == 6:
      return 60
   elif rez == 7:
      return 70
   elif rez == 8:
      return 80
   elif rez == 9:
      return 90
   elif rez == 0:
      return 0
   elif rez == 1:
      return 10


#Reading data
music = pd.read_csv('C:/Users/Maja/Desktop/Data/data.csv')
# print(music) 

#Datatype fix
print(music.info()) 
music = music.astype({'genre':'string'})
music = music.astype({'artist_name':'string'})
music = music.astype({'track_name':'string'})
music = music.astype({'lyrics':'string'})
#print(music.info()) 

music = music.query('1950 <= release_date <= 2019')
music = music.query('genre!=""')
music = music.query('artist_name!=""')
music = music.query('track_name!=""')

music["lyrics_length"]= music["lyrics"].str.len()
music = music.astype({'lyrics_length':'int64'})
music = music.query('lyrics_length > 450')
#music = music.drop(['lyrics_length'], axis=1)

#Adding decade tag
music['decade'] = music['release_date'].apply(lambda year : decade(year))
#print(music.info()) 
#print (music)

# Making genre representation
genres = ['pop', 'reggae', 'hip hop', 'country', 'rock', 'blues', 'jazz']
genre_rep=[]

genre_rep.append(music[music.genre == 'pop'].shape[0])
genre_rep.append(music[music.genre == 'reggae'].shape[0])
genre_rep.append(music[music.genre == 'hip hop'].shape[0])
genre_rep.append(music[music.genre == 'country'].shape[0])
genre_rep.append(music[music.genre == 'rock'].shape[0])
genre_rep.append(music[music.genre == 'blues'].shape[0])
genre_rep.append(music[music.genre == 'jazz'].shape[0])

graph = zip(genres, genre_rep)

with open('genre_representation.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(graph)


#Calculating median lyrics length
list = [0,0,0,0,0,0,0]
number =  [0,0,0,0,0,0,0]

for i, j in music.iterrows():
   if j['genre'] == 'pop':
      list[0]= list[0] + (j['lyrics_length'])
      number[0] = number[0]+ 1
   elif j['genre'] == 'reggae':
      list[1]= list[1] + (j['lyrics_length'])
      number[1] = number[1]+ 1
   elif j['genre'] == 'hip hop':
      list[2]= list[2] + (j['lyrics_length'])  
      number[2] = number[2]+ 1
   elif j['genre'] == 'country':
      list[3]= list[3] + (j['lyrics_length'])
      number[3] = number[3]+ 1
   elif j['genre'] == 'rock':
      list[4]= list[4] + (j['lyrics_length'])
      number[4] = number[4]+ 1
   elif j['genre'] == 'blues':
      list[5]= list[5] + (j['lyrics_length'])
      number[5] = number[5]+ 1
   elif j['genre'] == 'jazz':
      list[6]= list[6] + (j['lyrics_length'])
      number[6] = number[6]+ 1

for i in range (0, 7):
   list[i] = list[i]//number[i]

graph = zip(genres, list)

with open('median_lyrics_length.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(graph)

   
# Extractiong sentiment
music['sentiment'] = music['lyrics'].apply(lambda text: TextBlob(text).sentiment.polarity) 
music.to_csv(r'C:/Users/Maja/Desktop/Data/new.csv')

music_new = pd.read_csv('C:/Users/Maja/Desktop/Data/new.csv')

# Making sentiment - genre relation
genres = ['pop', 'reggae', 'hip hop', 'country', 'rock', 'blues', 'jazz']
list = [0,0,0,0,0,0,0]
number =  [0,0,0,0,0,0,0]

for i, j in music_new.iterrows():
   if j['genre'] == 'pop':
      list[0]= list[0] + (j['sentiment'])
      number[0] = number[0]+ 1
   elif j['genre'] == 'reggae':
      list[1]= list[1] + (j['sentiment'])
      number[1] = number[1]+ 1
   elif j['genre'] == 'hip hop':
      list[2]= list[2] + (j['sentiment'])  
      number[2] = number[2]+ 1
   elif j['genre'] == 'country':
      list[3]= list[3] + (j['sentiment'])
      number[3] = number[3]+ 1
   elif j['genre'] == 'rock':
      list[4]= list[4] + (j['sentiment'])
      number[4] = number[4]+ 1
   elif j['genre'] == 'blues':
      list[5]= list[5] + (j['sentiment'])
      number[5] = number[5]+ 1
   elif j['genre'] == 'jazz':
      list[6]= list[6] + (j['sentiment'])
      number[6] = number[6]+ 1
   
print(list)
for i in range (0, 7):
   list[i] = list[i]/number[i]

print(list)

xmin = min(list) 
xmax=max(list)
for i, x in enumerate(list):
    list[i] = (x-xmin) / (xmax-xmin)
print('Normalized List:',list)

graph = zip(genres, list)

with open('genres_sentiment_text_blob.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(graph)
   
#Making decade - sentiment relation
music_new = pd.read_csv('C:/Users/Maja/Desktop/Data/new.csv')
dict = {}
number =  {}
year_list = []

for i, j in music_new.iterrows():
   if j['decade'] in dict.keys():
      dict[j['decade']] = dict[j['decade']] + (j['sentiment'])
      number[j['decade']] = number[j['decade']] + 1
   else:
      dict[j['decade']] = (j['sentiment'])
      number[j['decade']] = 1
      
  
for i in dict.keys():
   dict[j['decade']] = dict[j['decade']]/number[j['decade']]
   
godine = list(dict.keys())
sentiment = list(dict.values())
print(godine)
print(sentiment)

xmin = min(sentiment) 
xmax=max(sentiment)
for i, x in enumerate(sentiment):
    sentiment[i] = (x-xmin) / (xmax-xmin)
print('Normalized List:', sentiment)

graph = zip(godine, sentiment)

with open('years_sentiment_text_blob.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(graph)

#Extracting emotions
music = pd.read_csv('C:/Users/Maja/Desktop/Data/new.csv')

music['emotions'] = music['lyrics'].apply(lambda text: NRCLex(text).raw_emotion_scores)
music['affect_list'] = music['lyrics'].apply(lambda text: NRCLex(text).affect_list)

dict = {'anger' : 0, 'fear' : 0, 'anticipation' : 0, 'trust' : 0, 'surprise' : 0, 'sadness' : 0, 'joy' : 0, 'disgust' : 0, 'positive' : 0, 'negative' : 0 }
decades = [0,10]

#Making emotions - decade relation
for decade in decades:
   for i, j in music.iterrows():
      if j['decade'] == decade:
         emot = j['emotions']
         affect_list = j['affect_list'] 
         if 'anger' in affect_list:
            dict['anger'] = dict['anger'] + emot['anger'] 
         if 'fear' in affect_list:
            dict['fear'] = dict['fear'] + emot['fear']
         if 'anticipation' in affect_list:
            dict['anticipation'] = dict['anticipation'] + emot['anticipation']
         if 'trust' in affect_list:
            dict['trust'] = dict['trust'] + emot['trust']
         if 'surprise' in affect_list:
            dict['surprise'] = dict['surprise'] + emot['surprise']
         if 'sadness' in affect_list:
            dict['sadness'] = dict['sadness'] + emot['sadness']
         if 'joy' in affect_list:
            dict['joy'] = dict['joy'] + emot['joy']
         if 'disgust' in affect_list:
            dict['disgust'] = dict['disgust'] + emot['disgust']
         if 'positive' in affect_list:
            dict['positive'] = dict['positive'] + emot['positive']
         if 'negative' in affect_list:
            dict['negative'] = dict['negative'] + emot['negative']
         emocija = list(dict.keys())
         vrijednost = list(dict.values())
         graph = zip(emocija, vrijednost)
         with open(str(decade) + '_emotions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(graph)
            dict = dict.fromkeys(dict, 0)
