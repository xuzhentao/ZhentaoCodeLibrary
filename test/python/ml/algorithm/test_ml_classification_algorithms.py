import numpy as np

from src.python.ml.algorithm.MLClassificationAlgorithms import MLClassificationAlgorithms


def test_ml_algorithm():
    # generate fake data.
    np.random.seed(0)
    X = np.random.randn(100, 10)
    Y = np.random.randint(low=0, high=2, size=(100,))

    # machine learning classifiers.
    ml = MLClassificationAlgorithms(whether_plot=False, whether_mute=False, random_seed=0)
    ml.fun_loadData(X, Y, X, Y)
    list_accuracy, list_classifiers = ml.classification_explore()

    assert ([0.58, 0.67, 0.79, 0.98, 1.0, 1.0, 0.88, 0.63, 1.0] == list_accuracy)
    assert (['NC', 'NB', 'DT', 'RF', 'GBC', 'AB', 'SVM', 'SVM_linear', 'MLP'] == list_classifiers)


if __name__ == "__main__":
    test_ml_algorithm()
