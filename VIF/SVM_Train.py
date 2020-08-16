from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, precision_score, recall_score, confusion_matrix, precision_recall_curve
from sklearn import metrics
import pickle
from sklearn.svm import SVC
from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt


noAccidents = genfromtxt('data_no_accidents.csv', delimiter=',')
Accidents = genfromtxt('data_accidents.csv', delimiter=',')
maxs = min(noAccidents.shape[0],Accidents.shape[0])
noAccidents = noAccidents[0:maxs, :]
Accidents = Accidents[0:maxs, :]

y_noAccidents = np.zeros(noAccidents.shape[0])
y_noAccidents = y_noAccidents.reshape(noAccidents.shape[0], 1)


y_Accidents = np.ones(Accidents.shape[0])
y_Accidents = y_Accidents.reshape(Accidents.shape[0], 1)

X = np.vstack((noAccidents, Accidents))
y = np.vstack((y_noAccidents, y_Accidents))



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
clf = SVC(kernel='linear', probability=True, tol=1e-3) 

clf.fit(X_train, y_train)
print ("Normal score: ", clf.score(X_test, y_test))



# average presition
y_score = clf.decision_function(X_test)
average_precision = average_precision_score(y_test, y_score)
print('Average precision-recall score: {0:0.2f}'.format(
      average_precision))


precision, recall, _ = precision_recall_curve(y_test, y_score)
#print("precision", precision, "recall", recall)

plt.step(recall, precision, color='b', alpha=0.2,
         where='post')
plt.fill_between(recall, precision, step='post', alpha=0.2,
                 color='b')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
          average_precision))
plt.show()



# ROC
preds = clf.predict(X_test)

tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
print ("Confusion matrix tn, fp, fn, tp ", tn, fp, fn, tp )

print("recall", recall_score(y_test, preds))
print("precision", precision_score(y_test, preds))


fpr, tpr, threshold = metrics.roc_curve(y_test, preds)
roc_auc = metrics.auc(fpr, tpr)


pickle.dump(clf, open('model-svm1.sav', 'wb'))



