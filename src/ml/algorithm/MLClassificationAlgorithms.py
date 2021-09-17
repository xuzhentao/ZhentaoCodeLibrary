##################################################################
#	Class: 					Machine Learning
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2018/3/16
#	Description: 			Utilize Machine Learning Method in analyzing the MMU sensor's data, and provide prediction.
#	Tested Environment:		Windows 10 (64 bits) w/ Python 3.6
#	Required Libraries:		numpy:			pip install numpy
#							matplotlib: 	pip install matplotlib
#							scikit-learn: 	pip install scikit-learn
##################################################################

import numpy as np
import matplotlib.pyplot as plt


# Class_Machine Learning
# input: None
# Description: Use common machine classifiers (DT, RF, SVM, etc.) to classifier and predict the p-code.
class MLClassificationAlgorithms():

    # constructor.
    def __init__(self, whether_plot=True, whether_mute=False, random_seed=0):
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.Y_test = None
        self.classification_result = None
        self.list_featurename = None
        self.list_labels = None
        self.__hyperparameters__ = None
        self.whether_plot = whether_plot
        self.whether_mute = whether_mute
        self.random_seed = random_seed
        self.__initialize_hyperparameters__()

    # initialize_hyperparameters__()
    # input: noun
    # output: noun
    # change: the self.hyperparameters variable.
    def __initialize_hyperparameters__(self):
        self.__hyperparameters__ = {
            "NC": None,
            "NB": None,
            "DT": {"max_depth": 3},
            "RF": {"max_depth": 4, "random_state": 0},
            "GBC": {"n_estimators": 100, "learning_rate": 1.0, "max_depth": 1, "random_state": 0},
            "AB": {"n_estimators": 100},
            "SVM": {"kernel": "rbf"},
            "SVM_linear": None,
            "MLP": {"solver": 'lbfgs', "hidden_layer_sizes": (50,), "max_iter": 1000}
        }

    # fun_loadData(self, X_train, y_train, X_test, y_test)
    # input: 	X_train: the ndarray of shape NxM
    #		 	y_train: the 1d array of shape N,
    #			X_test: the ndarray of shape N'xM
    #			y_test: the ndarray of shape N',
    # function: load the training and testing data to the class.
    def fun_loadData(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    # fun_loadFeatureName(self, list_featurename)
    # input: 	list_featurename: a list of string, each of which is a name for a certian feature.
    # function: load the training and testing data to the class.
    def fun_loadFeatureName(self, list_featurename):
        self.list_featurename = list_featurename

    # fun_loadLabel
    # input: list_labels: a list of label, each of which represents
    # output: none
    # function: set the list_labels to the private variable.
    # def fun_loadLabel(self, list_labels):
    # 	self.list_labels = list_labels

    # name: classification explore
    # input: none
    # output: list_accuracy, list_classifiername
    # function: try different classifier and return the result.
    def classification_explore(self):

        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        train_X, train_Y, test_X, test_Y = self.X_train, self.y_train, self.X_test, self.y_test

        from sklearn.metrics import accuracy_score

        list_classifierName = []
        list_accuracyscore = []

        from sklearn.neighbors.nearest_centroid import NearestCentroid
        clf = NearestCentroid()
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "NC"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn.naive_bayes import GaussianNB
        clf = GaussianNB()
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "NB"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn import tree
        conf = self.__hyperparameters__['DT']
        clf = tree.DecisionTreeClassifier(max_depth=conf['max_depth'])
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "DT"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]
        # visualize decision tree
        # with open(path_out + "DT/"+"DT_["+ self.pcode +"].dot", "w") as f:
        # 	f = tree.export_graphviz(clf, out_file=f, feature_names = self.list_featurename , class_names = self.list_labels, filled = True, rounded=True)

        from sklearn.ensemble import RandomForestClassifier
        conf = self.__hyperparameters__["RF"]
        clf = RandomForestClassifier(max_depth=conf["max_depth"], random_state=conf["random_state"]);
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        from sklearn.metrics import accuracy_score
        classifier = "RF"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn.ensemble import GradientBoostingClassifier
        conf = self.__hyperparameters__["GBC"]
        clf = GradientBoostingClassifier(n_estimators=conf["n_estimators"], learning_rate=conf["learning_rate"],
                                         max_depth=conf["max_depth"], random_state=conf["random_state"])
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "GBC"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn.ensemble import AdaBoostClassifier
        conf = self.__hyperparameters__['AB']
        clf = AdaBoostClassifier(n_estimators=conf["n_estimators"])
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "AB"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn import svm
        conf = self.__hyperparameters__['SVM']
        clf = svm.SVC(kernel=conf['kernel'])
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "SVM"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn import svm
        clf = svm.LinearSVC()
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "SVM_linear"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        from sklearn.neural_network import MLPClassifier
        conf = self.__hyperparameters__['MLP']
        clf = MLPClassifier(solver=conf['solver'], hidden_layer_sizes=conf['hidden_layer_sizes'],
                            max_iter=conf['max_iter'])
        clf.fit(train_X, train_Y)
        test_pred = clf.predict(test_X)
        classifier = "MLP"
        accuracy = accuracy_score(test_Y, test_pred)
        if not self.whether_mute:
            print(classifier, accuracy)
        list_classifierName += [classifier]
        list_accuracyscore += [accuracy]

        if self.whether_plot:
            import matplotlib.pyplot as plt
            list_accuracyscore = [100 * i for i in list_accuracyscore]
            list_accuracyscore_sort, list_classifierName_sort = zip(
                *sorted(zip(list_accuracyscore, list_classifierName), reverse=False))
            # for classifier, accuracy_score in zip(list_classifierName_sort, list_accuracyscore_sort):
            # 		print (classifier +'\t'+ str(accuracy_score) + '%')
            x = np.arange(len(list_accuracyscore_sort))
            plt.bar(x, height=list_accuracyscore_sort)
            plt.xticks(x, list_classifierName_sort)
            axes = plt.gca()
            axes.set_ylim([0, 100])
            plt.ylabel('Accuracy')
            plt.xlabel("Different Classifier")
            plt.title('The Accuracy of Different Classifier on Testing Data')
            plt.show()
            plt.close()

        self.classification_result = {classifiername: accuracyscore for classifiername, accuracyscore in
                                      zip(list_classifierName, list_accuracyscore)}

        return list_accuracyscore, list_classifierName
