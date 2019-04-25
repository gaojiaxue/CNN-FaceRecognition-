import tensorflow as tf
import numpy as np

traind = np.loadtxt("traindata.txt")
traindata = tf.convert_to_tensor(traind)

train = np.loadtxt("trainresult.txt")
trainlabels=train.reshape(-1,1)   
tt=np.where(trainlabels==69,21,trainlabels) 
trainresult = tf.convert_to_tensor(tt)

testd = np.loadtxt("testdata.txt")
testdata = tf.convert_to_tensor(testd)

test = np.loadtxt("testresult.txt")
testlabels=test.reshape(-1,1)
ee=np.where(testlabels==69,21, testlabels)  
testresult = tf.convert_to_tensor(ee)

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    # pre=np.zeros(len(test))
    pre=tf.argmax(y_pre, 1)
    # np.where(pre==21,69, pre) 
    correct_prediction = tf.equal(pre, v_ys)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs:v_xs, ys: v_ys})
    return result

def weight_variable(shape):
    inital=tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(inital)
def bias_variable(shape):
    inital=tf.constant(0.1,shape=shape)
    return tf.Variable(inital)
#define a 2 dimensional  convolutional neural layer
def conv2d(x,W):
    #strides[buntch=1,x_movement.y_movement,in_channels=1]
    #conv2d(input,filter,strides,pading(SAME,VAILD),name)
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
#pooling 
def max_pool_2x2(x):
    #ksize means windows size
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 1024])
ys = tf.placeholder(tf.float32, [None, 1])
# keep_prob=tf.placeholder(tf.float32)
#reshape(1024=>32x32)
x_image=tf.reshape(xs,[-1,32,32,1])

#conv1 layer
#patch is 5x5,input feature is 1,output(feature in this layer) is 20
W_conv1=weight_variable([5,5,1,20])
b_conv1=bias_variable([20])
h_conv1=tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)#output size=32x32x20
h_pool1=max_pool_2x2(h_conv1)#output size =14x14x32
#conv2 layer
W_conv2=weight_variable([5,5,20,50])
b_conv2=bias_variable([50])
h_conv2=tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)#output size=16x16x50
h_pool2=max_pool_2x2(h_conv2)#output size =8x8x50
#func1 layer
W_fc1=weight_variable([8*8*50,500])
b_fc1=bias_variable([500])
h_pool2_flat=tf.reshape(h_pool2,[-1,8*8*50])
h_fc1=tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)
h_fc1_drop=tf.nn.dropout(h_fc1,0.4)
#func2 layer
W_fc2=weight_variable([500,21])
b_fc2=bias_variable([21])
prediction = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)
predictions=tf.argmax(prediction, 1)
predictions=tf.cast(predictions, tf.float32)
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(predictions), reduction_indices=[1]))
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-predictions), reduction_indices=[1]))
#train 
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)
sess = tf.Session()
init=tf.initialize_all_variables()
sess.run(init)


for i in range(1000): 
    sess.run(train_step, feed_dict={xs:traindata, ys:trainresult})
    if i % 20 == 0:
        #show the train result
      print(compute_accuracy(testdata,testresult))