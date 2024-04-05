from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from prettytable import PrettyTable
import tsv_parser as par

def print_results(num,y_test,predicted):
    th = ["Комментарий", "Предсказанная оценка", "Реальная оценка"]
    td = []
    for i in range(num):
        td.append(par.sample[i])
        if predicted[i] == 1: td.append("Хорошо")
        else: td.append("Плохо")
        if y_test[i] == 1: td.append("Хорошо")
        else: td.append("Плохо")

    td = td[:]
    table = PrettyTable(th)
    table._max_width = {"Комментарий":70}
    while td:
        table.add_row(td[:3])
        td = td[3:]
    
    print(table)

def naive_bayes(X_train, y_train, X_test):
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model.predict(X_test)

def neighbors(X_train, y_train, X_test):
    model = KNeighborsClassifier(5)
    model.fit(X_train, y_train)
    return model.predict(X_test)

def SGD(X_train, y_train, X_test):
    model = SGDClassifier(max_iter=1000)
    model.fit(X_train, y_train)
    return model.predict(X_test)

def SVC(X_train, y_train, X_test):
    model = LinearSVC()
    model.fit(X_train,y_train)
    return model.predict(X_test)

def train(model_func):
    #подготавливаем обучающую выборку
    X_train, y_train = par.process_the_data("train_sample.tsv")
    #подготавливаем тестовую выборку
    X_test, y_test = par.process_the_data("test_sample.tsv")
    predicted = model_func(X_train,y_train,X_test)
    score_test = accuracy_score(y_test, predicted)
    #Выводим первые 10 комментариев и их оценки
    print_results(10,y_test,predicted)
    #Выводим точность на тестовой выборке
    print(f"\n \033[32;40m Точность на тестовой выборке: {score_test}")
    #Вывод матрицы ошибок
    cm = confusion_matrix(y_test, predicted)
    sns.heatmap(cm,
                annot=True,
                fmt='g',
                xticklabels=['Плохо','Хорошо'],
                yticklabels=['Плохо','Хорошо'])
    plt.ylabel('Prediction',fontsize=13)
    plt.xlabel('Actual',fontsize=13)
    plt.title('Confusion Matrix',fontsize=17)
    plt.show()
