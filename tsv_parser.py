import numpy as np
import pandas as pd
import re 
import nltk 
from nltk.corpus import stopwords 
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

sample = []

def process_the_data(file_name) :
    nltk.download('stopwords')
    dataset = pd.read_csv(file_name, delimiter = ':')
    X, y = shuffle(dataset['Comment'], dataset.iloc[:,1].values)
    corpus = []
    for i in range(len(X)):
        sample.append(X[i])
        #убираем все символы которые не явл буквами 
        comment = re.sub('[^а-яА-Я]', ' ', X[i])
        #переводим в нижний регистр и разделяем на слова
        comment = comment.lower().split()
        ps = SnowballStemmer("russian")
        #удаляем стоп-слова
        comment = [ps.stem(word) for word in comment
                if not word in set(stopwords.words('russian'))] 
        #собираем строку обратно
        comment = ' '.join(comment)  
        #добавляем в корпус
        corpus.append(comment) 

    cv = CountVectorizer(max_features = 1500) 
    X = cv.fit_transform(corpus).toarray() 
    return X, y
