#SCIKIT-LEARN
#Simple and efficient tools for predictive data analysis
#Accessible to everybody, and reusable in various contexts
#Built on NumPy, SciPy, and matplotlib
#Open source, commercially usable - BSD license

#pip install -U scikit-learn

#In order to check your installation you can use:
# $python -m pip show scikit-learn  # to see which version and where scikit-learn is installed
# $python -m pip freeze  # to see all packages installed in the active virtualenv
# $python -c "import sklearn; sklearn.show_versions()"

#API REFERENCES https://scikit-learn.org/stable/modules/classes.html


import numpy as np
from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


#pip install mlxtend


#Carico in memoria il dataset Iris.
#Suddivido la matrice del dataset in training ( X_train ) e test ( y_train ).
#Per semplicita prendo soltanto due attributi su quattro.

# preparazione dataset
iris = datasets.load_iris()
X = iris.data[:, [2, 3]]
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# standardizzazione
#Standardize features by removing the mean and scaling to unit variance
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)
X_std = sc.transform(X)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

#A questo punto inizio l'addestramento vero e proprio.
#Importo il modello della regressione logistica ( LogisticRegression ) dai modelli lineari di
#Sklearn.
#Imposto gli iperparametri dell'addestramento nell'oggetto lr.
#Infine avvio l'addestramento con la funzione fit.

# addestramento
#PARAMETER C - float, default=1.0
#Inverse of regularization strength; must be a positive float. 
#Like in support vector machines, smaller values specify stronger regularization.
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C=1000.0, random_state=0)
lr.fit(X_train_std, y_train)

# visualizzazione grafica della classificazione

from mlxtend.plotting import plot_decision_regions

plot_decision_regions(X_test_std, y_test, clf=lr, legend=2)
import matplotlib.pyplot as plt
plt.xlabel('petal length [standardized]')
plt.ylabel('petal width [standardized]')
plt.legend(loc='upper left')
plt.show()

clf = lr
print(clf.score(X_test, y_test))