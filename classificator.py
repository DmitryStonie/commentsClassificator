from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import tsv_parser as par

def naive_bayes(X_train, y_train, X_test):
    model = MultinomialNB(0.1)
    model.fit(X_train, y_train)
    return model.predict(X_test)

def neighbors(X_train, y_train, X_test):
    model = KNeighborsClassifier(5)
    model.fit(X_train, y_train)
    return model.predict(X_test)

def train(model_func):
    X_train, X_test, y_train, y_test = par.process_the_data("dataset.tsv")
    predicted = model_func(X_train,y_train,X_test)
    score_test = accuracy_score(y_test, predicted)
    report = classification_report(y_test, predicted)
    print(score_test)
    print(report)