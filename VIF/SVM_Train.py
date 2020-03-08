
from sklearn.model_selection import train_test_split

from sklearn.metrics import average_precision_score

from sklearn import metrics
import pickle
from sklearn.svm import SVC
from numpy import genfromtxt
import numpy as np
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

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
clf = SVC(kernel='linear', probability=True, tol=1e-3)  # , verbose = True) #Set the classifier as a support vector machines with

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
#
# plt.title('Receiver Operating Characteristic')
# plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
# plt.legend(loc = 'lower right')
# plt.plot([0, 1], [0, 1],'r--')
# plt.xlim([0, 1])
# plt.ylim([0, 1])
# plt.ylabel('True Positive Rate')
# plt.xlabel('False Positive Rate')
# plt.show()
#








#print(X_test)
#print(y_test)
#print(clf.predict(X_test))

pickle.dump(clf, open('model-svm1.sav', 'wb'))

#
#
# cap = cv2.VideoCapture('dataset/Accidents/subvideos/best/15.mp4')
# frames = []
# vif = ViF()
#
# while True:
#     ret, frame = cap.read()
#
#     if ret:
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         frames.append(gray)
#
#     else:
#         break
#
# obj = ViF()
# feature_vec = obj.process(frames)
# print(clf.predict(feature_vec.reshape(1, 304)))
#
#
#



'''
X, Y = load_bd()

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    X = np.array(X)
    Y = np.array(Y)

    print X.shape
    print Y.shape
    # print Y

    #np.savetxt("X.csv", X, delimiter=",")
    #np.savetxt("Y.csv", Y, delimiter=",")

    clf = SVC(kernel='linear', probability=True, tol=1e-3)  # , verbose = True) #Set the classifier as a support vector machines with

    clf.fit(X_train, y_train)
    #joblib.dump(clf, '../models/ship-svm.pkl')
    pickle.dump(clf, open('../models/ship-svm.sav', 'wb'))

    print "Normal score: ", clf.score(X_test, y_test)
'''