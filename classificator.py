from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from prettytable import PrettyTable
import tsv_parser as par
import datetime

def print_results(num,y_test,predicted):
    th = ["Комментарий", "Предсказанная оценка", "Реальная оценка"]
    td = []
    for i in range(num):
        td.append(par.sample[i])
        if predicted[i] == 1: td.append("Позитивный")
        else: td.append("Негативный")
        if y_test[i] == 1: td.append("Позитивный")
        else: td.append("Негативный")

    td = td[:]
    table = PrettyTable(th)
    table._max_width = {"Комментарий":70}
    while td:
        table.add_row(td[:3])
        td = td[3:]
    
    print(table)

def naive_bayes(X_train, y_train, X_test):
    print("Наивный байесовский классификатор")
    model = MultinomialNB()
    start = datetime.datetime.now()
    model.fit(X_train, y_train)
    end = datetime.datetime.now()
    return model.predict(X_test), end-start

def neighbors(X_train, y_train, X_test):
    print("Метод k-близжайших соседей")
    model = KNeighborsClassifier(3)
    start = datetime.datetime.now()
    model.fit(X_train, y_train)
    end = datetime.datetime.now()
    return model.predict(X_test), end-start

def SGD(X_train, y_train, X_test):
    print("Метод градиентного спуска")
    model = SGDClassifier(max_iter=1000)
    start = datetime.datetime.now()
    model.fit(X_train, y_train)
    end = datetime.datetime.now()
    return model.predict(X_test), end-start

def linear_SVC(X_train, y_train, X_test):
    print("Метод опорных векторов")
    model = LinearSVC()
    start = datetime.datetime.now()
    model.fit(X_train,y_train)
    end = datetime.datetime.now()
    return model.predict(X_test), end-start

def decision_tree(X_train, y_train, X_test):
    print("Дерево решений")
    model = DecisionTreeClassifier()
    start = datetime.datetime.now()
    model.fit(X_train,y_train)
    end = datetime.datetime.now()
    return model.predict(X_test), end-start

def MLP(X_train, y_train, X_test):
    print("Многослойный перцептрон")
    model = MLPClassifier(hidden_layer_sizes=10,max_iter=1000)
    start = datetime.datetime.now()
    model.fit(X_train,y_train)
    end = datetime.datetime.now()
    return model.predict(X_test), end-start

def train(model_func):
    #подготавливаем обучающую выборку
    X_train, X_test, y_train, y_test = par.process_the_data("train_sample.tsv", "test_sample.tsv")
    #подготавливаем тестовую выборку
  #  X_test, y_test = par.process_the_data("test_sample.tsv", "test")
    start = datetime.datetime.now
    predicted, time = model_func(X_train,y_train,X_test)
    score_test = accuracy_score(y_test, predicted)
    #Выводим первые 10 комментариев и их оценки
    print_results(10,y_test,predicted)
    #Выводим точность на тестовой выборке
    print(f"\n \033[32;40m Точность на тестовой выборке: {score_test}, время обучения : {time}")
    #Вывод матрицы ошибок
    cm = confusion_matrix(y_test, predicted)
    sns.heatmap(cm,
                annot=True,
                fmt='g',
                xticklabels=['Негативный','Позитивный'],
                yticklabels=['Негативный','Позитивный'])
    plt.ylabel('Prediction',fontsize=13)
    plt.xlabel('Actual',fontsize=13)
    plt.title('Confusion Matrix',fontsize=17)
    plt.show()
