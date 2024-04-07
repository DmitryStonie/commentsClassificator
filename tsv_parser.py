import numpy as np
import pandas as pd
import re 
import nltk 
from nltk.corpus import stopwords 
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils import shuffle

sample = []
words_num = 300

def process_the_data(file_name_train,file_name_test) :
    sample.clear()
    nltk.download('stopwords')
    dataset_train = pd.read_csv(file_name_train, delimiter = '\t')
    dataset_test = pd.read_csv(file_name_test, delimiter = '\t')
    X_train, y_train = shuffle(dataset_train.iloc[:,0].values, dataset_train.iloc[:,1].values)
    X_test, y_test = shuffle(dataset_test.iloc[:,0].values, dataset_test.iloc[:,1].values)
    X = np.concatenate((X_train,X_test), axis=0)
    y = np.concatenate((y_train,y_test), axis=0)
    corpus = []
    for i in range(len(X)):
        #сохраняем тестовые комментарии для дальнейшего вывода
        if i >= len(X_train):
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

    global words_num
    cv = CountVectorizer(max_features = words_num)
    #Векторизуем данные
    X = cv.fit_transform(corpus).toarray()

    #Подсчитываем частоту употребления слов в позитивных и негативных комментариях
    frequency_negative = np.zeros(words_num)
    frequency_positive = np.zeros(words_num)
    for i in range(len(X)):
        if y[i] == 1: frequency_positive += X[i]
        else: frequency_negative += X[i]
    
    #сохраняем позиции слов которые часто встречаются как в негативных 
    #так и в позитивных комментариях для последующего удаления
    to_del = []
    for i in range(words_num):
        if abs(frequency_positive[i] - frequency_negative[i]) < 20: 
            words_num-=1
            to_del.append(i)
    print(words_num)

    #удаляем слова чтобы получить лучшую точность предсказания
    if (len(to_del) != 0):
        for i in range(len(to_del)-1,-1,-1):
            X = np.delete(X, to_del[i], 1)

    X_train, X_test = X[:len(X_train), :], X[len(X_train):, :]
    y_train, y_test = y[:len(y_train)], y[len(y_train):]



    return X_train, X_test, y_train, y_test



#process_the_data("train_sample.tsv", "test_sample.tsv")