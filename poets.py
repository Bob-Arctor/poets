import os
import numpy as np 
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

poems_path = 'poems'

target = []
data = []

for file in os.listdir(poems_path):
    f = open(os.path.join(poems_path,file), 'r')
    poet = ''.join([i for i in file[:-4] if not i.isdigit()])
    data.append(f.read())
    target.append(poet)
    
text_clf = Pipeline([('vect', CountVectorizer(encoding='koi8-r')),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),])
#text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 3),token_pattern=r'\b\w+\b', min_df=1)), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.33, random_state=42)

text_clf = text_clf.fit(X_train, y_train)

parameters = {'vect__ngram_range': [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9)], 
                'tfidf__use_idf': (True, False), 
                'clf__alpha': (1e-2, 1e-3),}
                
gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
gs_clf = gs_clf.fit(X_train, y_train)

for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
    
print(gs_clf.best_score_)

predicted = gs_clf.predict(X_test)
print(np.mean(predicted == y_test))
for i, j in zip(y_test, predicted):
    print('%s --> %s'%(i,j))

print(metrics.classification_report(y_test, predicted))
print(metrics.confusion_matrix(y_test, predicted))