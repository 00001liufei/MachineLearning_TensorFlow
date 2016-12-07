from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np

'''����������'''
def NeuralNetwork():
    minist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    xs = tf.placeholder(tf.float32,[None,784])
    ys = tf.placeholder(tf.float32,[None,10])
    prediction = add_layer(xs, 784, 10, n_layer=1,activation_function=tf.nn.softmax)
    loss = tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction),reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
    sess = tf.Session()  
    sess.run(tf.initialize_all_variables())
    for i in range(2000):
        batch_xs, batch_ys = minist.train.next_batch(100)  # ����ʹ��SGD����ݶ��½�����Ϊ�������ϴ�ÿ���ó�100������ѵ��
        sess.run(train_step,feed_dict={xs:batch_xs,ys:batch_ys})
        if i%50==0:
            print(compute_accuracy(xs,ys,minist.test.images, minist.test.labels,sess,prediction))
      


'''���һ��'''
def add_layer(inputs,in_size,out_size,n_layer,activation_function=None):
    layer_name = 'layer%s'%n_layer
    with tf.name_scope(layer_name):
        with tf.name_scope('Weights'):
            Weights = tf.Variable(tf.random_normal([in_size,out_size]),name='W')
            tf.histogram_summary(layer_name+'/weights', Weights)
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1,out_size]) + 0.1,name='b')
            tf.histogram_summary(layer_name+'/biases',biases)
        with tf.name_scope('Ws_plus_b'):
            Ws_plus_b = tf.matmul(inputs,Weights) + biases
                                                                                                   
        if activation_function is None:                                                                                               
            outputs = Ws_plus_b                                                                                                                
        else:                                                                                                                             
            outputs = activation_function(Ws_plus_b)                                                                                                                     
        tf.histogram_summary(layer_name+'/outputs',outputs)
        return outputs
'''����׼ȷ��'''
def compute_accuracy(xs,ys,v_xs,v_ys,sess,prediction):
    y_pre = sess.run(prediction,feed_dict={xs:v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre,1),tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    result = sess.run(accuracy,feed_dict={xs:v_xs,ys:v_ys})
    return result


NeuralNetwork()