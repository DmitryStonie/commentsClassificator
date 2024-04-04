import numpy as np
import pandas as pd
import re 
import nltk 
from nltk.corpus import stopwords 
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def process_the_data(file_name) :
    nltk.download('stopwords')
    dataset = pd.read_csv(file_name, delimiter = ':')
    corpus = [] 
    for i in range(len(dataset['Comment'])):
        #убираем все символы которые не явл буквами 
        comment = re.sub('[^а-яА-Я]', ' ', dataset['Comment'][0])
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
    y = dataset.iloc[:,1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    return X_train, X_test, y_train, y_test