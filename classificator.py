from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, accuracy_score
import tsv_parser as par

def print_results(num,y_test,predicted):
    for i in range(num):
        print(f"{par.sample[i]}     {predicted[i]}     {y_test[i]}")

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

def train(model_func):
    X_train, y_train = par.process_the_data("dataset_train.tsv")
    X_test, y_test = par.process_the_data("dataset_train.tsv")
    predicted = model_func(X_train,y_train,X_test)
    print_results(5,y_test,predicted)
    score_test = accuracy_score(y_test, predicted)
    print(score_test)
