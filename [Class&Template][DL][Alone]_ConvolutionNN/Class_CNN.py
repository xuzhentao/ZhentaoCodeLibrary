######################################################################################
#	Class: 					CNN
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2018/3/16
#	Description: 			Utilize Machine Learning Method in analyzing the MMU sensor's data, and provide prediction.
#	Tested Environment:		Windows 10 (64 bits) w/ Python 3.6
#	Required Libraries:		numpy:			pip install numpy
#							matplotlib: 	pip install matploblit
#							tensorflow:		pip install tensorflow
#							time, random, os: built-in libraries
######################################################################################

import random

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


class Class_CNN():

    # initialize.
    def __init__(self, float_weightSTD=0.005, total_epoches=2, batch_size=100):

        # the weight and bias term.
        self.weights = {}
        self.biases = {}
        self.float_weightSTD = float_weightSTD
        self.__initializeWeight__()  # intialize the weight and biases

        # training configuration.
        self.total_epoches = total_epoches
        self.batch_size = batch_size

        # training data.
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.Y_test = None

    # load the data input this class.
    def fun_loadData(self, X_train, y_train, X_test, y_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    # name: get_batch_data
    # input: x and y
    # output: the batched x and y
    # function: select a subset of the data (batch size of the data.)
    def get_batch_data(self, x, y):
        int_N = x.shape[0]
        random_index = random.sample(range(int_N), self.batch_size)
        batch_x = x[random_index]
        batch_y = y[random_index]
        return batch_x, batch_y

    def __initializeWeight__(self):

        self.weights = {
            'wc1': tf.Variable(tf.random_normal([5, 5, 1, 5], stddev=self.float_weightSTD)),
            'wc2': tf.Variable(tf.random_normal([5, 5, 5, 10], stddev=self.float_weightSTD)),
            'wc3': tf.Variable(tf.random_normal([5, 5, 10, 10], stddev=self.float_weightSTD)),
            'wc4': tf.Variable(tf.random_normal([6, 6, 10, 10], stddev=self.float_weightSTD))}
        self.biases = {
            'bc1': tf.Variable(tf.random_normal([5], stddev=self.float_weightSTD)),
            'bc2': tf.Variable(tf.random_normal([10], stddev=self.float_weightSTD)),
            'bc3': tf.Variable(tf.random_normal([10], stddev=self.float_weightSTD)),
            'bc4': tf.Variable(tf.random_normal([10], stddev=self.float_weightSTD))
        }

    # Create some wrappers for simplicity
    def layer_conv2d(self, x, W, b, pad='SAME'):
        # Conv2D wrapper, with bias and relu activation
        x = tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding=pad)
        x = tf.nn.bias_add(x, b)
        return x

    def layer_relu(self, x):
        return tf.nn.relu(x)

    def layer_maxpool(self, x):
        return tf.layers.max_pooling2d(inputs=x, pool_size=[2, 2], strides=[2, 2])

    def layer_linear(self, x, W, b):
        int_N = x.shape[0]
        int_input = x.shape[1] * x.shape[2]

        x = tf.reshape(tensor=x, shape=[int_N, int_input])
        print(int_N)
        print(int_input)

        return tf.matmul(x, W) + b

    def layer_softmax(self, x):
        return tf.nn.softmax(x)

    def forward_propogation(self, x):
        # forward propogation.
        print("INITIAL:    \t", x.shape)
        conv1 = self.layer_conv2d(x, self.weights['wc1'], self.biases['bc1'], 'VALID')
        relu1 = self.layer_relu(conv1)
        print("CONV->ReLU->:\t", relu1.shape)

        conv2 = self.layer_conv2d(relu1, self.weights['wc2'], self.biases['bc2'], 'VALID')
        relu2 = self.layer_relu(conv2)
        print("CONV->ReLU->:\t", relu2.shape)

        max2 = self.layer_maxpool(relu2)

        conv3 = self.layer_conv2d(max2, self.weights['wc3'], self.biases['bc3'], 'VALID')
        relu3 = self.layer_relu(conv3)
        print("CONV->ReLU->:\t", relu3.shape)

        conv4 = self.layer_conv2d(relu3, self.weights['wc4'], self.biases['bc4'], 'VALID')
        conv4 = tf.reshape(conv4, (-1, conv4.shape[3]))
        print("CONV------->:\t", conv4.shape)

        output = tf.nn.softmax(conv4)
        print("SIGM------->:\t", output.shape, "[OUTPUT]")

        return output

    def predict(self, nd2_X_test):

        x = tf.placeholder(tf.float32, shape=(None, 28, 28, 1))
        pred = self.forward_propogation(x)

        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver.restore(sess, './trained_session.ckpt')

            pred_v = sess.run(pred, feed_dict={x: nd2_X_test})
            print(pred_v[:5])

            def fun_toonehot(i):
                nd_onehot = [0] * 10
                nd_onehot[int(i)] = 1
                return nd_onehot

            prev_v_onehot = np.array([fun_toonehot(i) for i in np.argmax(pred_v, axis=1).reshape((-1,))])
            return prev_v_onehot

    def fit(self):

        # the place holder for the neural entwork.
        # x = tf.placeholder(tf.float32, shape = (self.batch_size, 121,136,1))# G Model Year
        x = tf.placeholder(tf.float32, shape=(None, 28, 28, 1))
        y = tf.placeholder(tf.float32, shape=(None, 10))

        pred = self.forward_propogation(x)

        # binary classification use this.
        # cost = tf.reduce_mean(	tf.square( pred - y )	) #MSE ERROR
        cost = tf.reduce_mean(-tf.reduce_sum(y * tf.log(pred)))  # CROSS EMTROPY ERROR.

        # define optimizer.
        optimizer = tf.train.AdamOptimizer().minimize(cost)

        # the list to collect the loss during the trianing process.
        list_train_loss = []
        list_test_loss = []
        list_train_accuracy = []
        list_test_accuracy = []

        with tf.Session() as sess:

            sess.run(tf.global_variables_initializer())

            for epoch in range(self.total_epoches):

                train_loss = []
                train_accu = []

                for i in range(int(self.X_train.shape[0] / self.batch_size)):
                    # get batch
                    batch_x_train, batch_y_train = self.get_batch_data(self.X_train, self.y_train)

                    # train & result
                    _, pred_value_train, cost_value_train = sess.run([optimizer, pred, cost],
                                                                     feed_dict={x: batch_x_train, y: batch_y_train})
                    train_accuracy = np.sum([int(i == j) for i, j in zip(np.argmax(batch_y_train, axis=1),
                                                                         np.argmax(pred_value_train, axis=1))]) / \
                                     pred_value_train.shape[0]

                    train_loss += [cost_value_train]
                    train_accu += [train_accuracy]

                # calculate the single epoch loss and accuracy.
                avg_train_loss = np.mean(train_loss)
                avg_train_accu = np.mean(train_accu)

                # test result
                batch_x_test, batch_y_test = self.get_batch_data(self.X_test, self.y_test)
                pred_value_test, cost_value_test = sess.run([pred, cost], feed_dict={x: batch_x_test, y: batch_y_test})
                test_accuracy = np.sum([int(i == j) for i, j in
                                        zip(np.argmax(batch_y_test, axis=1), np.argmax(pred_value_test, axis=1))]) / \
                                pred_value_test.shape[0]

                # record the accuracy and loss.
                list_train_loss += [avg_train_loss]
                list_test_loss += [cost_value_test]
                list_train_accuracy += [avg_train_accu]
                list_test_accuracy += [test_accuracy]

                # print the result.
                print(str(epoch) + '/' + str(
                    self.total_epoches) + "\t[Loss(train),\tLoss(test),\tAccu(train),\tAccu(test)] = [" + str(
                    avg_train_loss) + '\t' + str(cost_value_test) + '\t' + str(avg_train_accu) + '\t' + str(
                    test_accuracy) + ']')

            saver = tf.train.Saver()
            saver.save(sess, './trained_session.ckpt')


# Sample Call.
if __name__ == "__main__":
    from tensorflow.examples.tutorials.mnist import input_data

    mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
    nd2_X = mnist.train.images.reshape((mnist.train.images.shape[0], 28, 28, 1))[:20000]
    nd_y = mnist.train.labels[:20000]
    from sklearn.model_selection import train_test_split

    nd2_X_train, nd2_X_test, nd_y_train, nd_y_test = train_test_split(nd2_X, nd_y)

    cnn = Class_CNN(float_weightSTD=0.005, total_epoches=3, batch_size=50)
    cnn.fun_loadData(nd2_X_train, nd_y_train, nd2_X_test, nd_y_test)

    cnn.fit()

    nd_y_test_pred = cnn.predict(nd2_X_test)
    plt.imshow(nd2_X_test[0, :, :, 0])
    plt.show()
    print(np.argmax(nd_y_test_pred, axis=1))
    print(np.argmax(nd_y_test, axis=1))
