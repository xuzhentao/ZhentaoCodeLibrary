import numpy as np

from src.ml.featureimportance.FeatureImportanceLogisticRegression import FeatureImportanceLogisticRegression


def test_feature_importance_logistic_regression():
    np.random.seed(0)
    nd2_X = np.random.randn(10000, 10)
    nd_y = np.random.randn(10000, )

    nd_y[nd_y > 0] = 1
    nd_y[nd_y <= 0] = 0

    nd2_X[nd_y == 0, 0] = np.random.randn()
    nd2_X[nd_y == 1, 0] = 2 + np.random.randn()

    fr = FeatureImportanceLogisticRegression()
    fr.fun_loadData(nd2_X=nd2_X, nd_y=nd_y, list_feature=[str(i) for i in range(10)])
    res = fr.fun_calcRank_LogisticRegression()

    assert (['0', '9', '4', '5', '7', '1', '6', '8', '3', '2'] == [i[0] for i in res])


if __name__ == "__main__":
    test_feature_importance_logistic_regression()
