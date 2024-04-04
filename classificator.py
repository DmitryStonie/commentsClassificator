from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
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
    table._max_width = {"Комментарий":50}
    while td:
        table.add_row(td[:3])
        td = td[3:]
    
    print(table)
 

def naive_bayes(X_train, y_train, X_test):
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model.predict(X_test)

def neighbors(X_train, y_train, X_test):
    model = KNeighborsClassifier(3)
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
    X_train, y_train = par.process_the_data("train_sample.tsv")
    X_test, y_test = par.process_the_data("train_sample.tsv")
    predicted = model_func(X_train,y_train,X_test)
    score_test = accuracy_score(y_test, predicted)
    print_results(10,y_test,predicted)
    print(f"\n \033[32;40m Точность на тестовой выборке: {score_test}")
