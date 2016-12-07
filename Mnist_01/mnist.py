import tensorflow as tf
import numpy as np
import scipy.io as spio

'''���к���'''
def NeuralNetwork():
    data_digits = spio.loadmat('data_digits.mat')
    X = data_digits['X']
    y = data_digits['y']
    m,n = X.shape
    class_y = np.zeros((m,10))      # y��0,1,2,3...9,��Ҫӳ��0/1��ʽ
    for i in range(10):
        class_y[:,i] = np.float32(y==i).reshape(1,-1) 
    
    xs = tf.placeholder(tf.float32, shape=[None,400])  # ������20x20=400��������400��feature
    ys = tf.placeholder(tf.float32, shape=[None,10])   # �����10��
    
    prediction = add_layer(xs, 400, 10, activation_function=tf.nn.softmax) # ���������磬400x10
    #prediction = add_layer(layer1, 25, 10, activation_function=tf.nn.softmax)
 
    #loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-prediction),reduction_indices=[1]))
    loss = tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction),reduction_indices=[1]))  # ������ʧ���������ۺ�������
    train = tf.train.GradientDescentOptimizer(learning_rate=0.5).minimize(loss)     # ʹ���ݶ��½���С����ʧ
    init = tf.initialize_all_variables()   # ��ʼ�����б���
    
    sess = tf.Session()  # ����Session
    sess.run(init)
    
    for i in range(4000): # ����ѵ��4000��
        sess.run(train, feed_dict={xs:X,ys:class_y})  # ѵ��train����������
        if i%50==0:  # ÿ50�������ǰ��׼ȷ��
            print(compute_accuracy(xs,ys,X,class_y,sess,prediction))

'''���һ��������'''
def add_layer(inputs,in_size,out_size,activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size,out_size]))    # Ȩ�أ�in*out 
    biases = tf.Variable(tf.zeros([1,out_size]) + 0.1)  
    Ws_plus_b = tf.matmul(inputs,Weights) + biases   # ����Ȩ�غ�ƫ��֮���ֵ
                                                                                                   
    if activation_function is None:                                                                                               
        outputs = Ws_plus_b                                                                                                                
    else:                                                                                                                              
        outputs = activation_function(Ws_plus_b)    # ���ü�����������                                                                                                                 
    return outputs    


'''����Ԥ��׼ȷ��'''  
def compute_accuracy(xs,ys,X,y,sess,prediction):
    y_pre = sess.run(prediction,feed_dict={xs:X}) 
    correct_prediction = tf.equal(tf.argmax(y_pre,1),tf.argmax(y,1))  #tf.argmax ����ĳ��tensor������ĳһά�ϵ����������ֵ���ڵ�����ֵ,��Ϊ��Ӧ�����֣�tf.equal ��������ǵ�Ԥ���Ƿ���ʵ��ǩƥ��
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32)) # ƽ��ֵ��Ϊ׼ȷ��
    result = sess.run(accuracy,feed_dict={xs:X,ys:y})
    return result    
    
if __name__ == '__main__':
    NeuralNetwork()