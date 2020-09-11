######################################################################################
#	Class: 					Feature Significance Ranking
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2018/7/6
#	Description: 			Utilize the Logistic Regression to Rank the features.
#	Tested Environment:		Windows 10 (64 bits) w/ Python 3.6
#	Required Libraries:		numpy:			pip install numpy
#							matplotlib: 	pip install matploblit
#							tensorflow:		pip install tensorflow
#							time, random, os: built-in libraries
######################################################################################



import pickle
import numpy as np
from sklearn import linear_model, datasets


class Class_MachineLearningFeatureRanking():

	def __init__(self):
		self.nd2_X = None
		self.nd_y = None
		self.list_feature = None

	def fun_loadData(self,nd2_X, nd_y, list_feature):
		self.nd2_X = nd2_X
		self.nd_y = nd_y
		self.list_feature = list_feature

	def fun_normalize(self):
		nd2_X_mean = np.mean(self.nd2_X,axis  = 0)
		nd2_x_std  = np.std(self.nd2_X, axis = 0)
		nd2_x_std[nd2_x_std == 0] = 1
		self.nd2_X = (self.nd2_X - nd2_X_mean) / nd2_x_std

	def fun_calcRank_LogisticRegression(self):
		
		logreg = linear_model.LogisticRegression(C=1e5)
		logreg.fit(self.nd2_X, self.nd_y)
		nd1_weights = np.array(logreg.coef_[0])
		list_tuple_featurename_weights = list(zip(self.list_feature, nd1_weights ))
		list_tuple_featurename_weights.sort(key = lambda x:x[1])
		return list_tuple_featurename_weights


# #sample call

# if __name__ == "__main__":

# 	nd2_X = np.random.randn(10000,10)
# 	nd_y = np.random.randn(10000,)

# 	nd_y[nd_y >0] = 1
# 	nd_y[nd_y <=0] = 0

# 	nd2_X[nd_y == 0,0] = np.random.randn()
# 	nd2_X[nd_y == 1,0] = 2 + np.random.randn()

# 	fr = Class_MachineLearningFeatureRanking()
# 	fr.fun_loadData(nd2_X = nd2_X, nd_y = nd_y, list_feature = [str(i) for i in range(10)])
# 	print(fr.fun_calcRank_LogisticRegression())
























