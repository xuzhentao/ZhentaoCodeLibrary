import numpy as np
import tensorflow.compat.v1 as tf

from src.python.ml.algorithm.CNNClassificationAlgorithm import CNNClassificationAlgorithm

tf.disable_v2_behavior()
import tempfile


def test_cnn_network():
    io_dir = tempfile.mkdtemp()

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    nd2_X = np.reshape(x_train, [x_train.shape[0], 28, 28, 1])[:1000]
    nd_y = np.zeros((y_train.shape[0], 10))[:1000]
    for i in range(nd_y.shape[0]):
        nd_y[i, y_train[i]] = 1
    from sklearn.model_selection import train_test_split
    nd2_X_train, nd2_X_test, nd_y_train, nd_y_test = train_test_split(nd2_X, nd_y, random_state=0)
    cnn = CNNClassificationAlgorithm(float_weightSTD=0.005, total_epoches=3, batch_size=50, io_dir=io_dir,
                                     random_seed=0)
    cnn.fun_loadData(nd2_X_train, nd_y_train, nd2_X_test, nd_y_test)
    cnn.fit()
    nd_y_test_pred = cnn.predict(nd2_X_test)
    # plt.imshow(nd2_X_test[0, :, :, 0])
    # plt.show()
    print(np.argmax(nd_y_test_pred, axis=1))
    print(np.argmax(nd_y_test, axis=1))


if __name__ == "__main__":
    test_cnn_network()
