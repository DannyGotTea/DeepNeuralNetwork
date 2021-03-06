from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
	return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

w_conv1 = weight_variable([5,5,1,32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

w_conv2 = weight_variable([5,5,32,64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

w_fullyC1 = weight_variable([7 * 7 * 64, 1024])
b_fullyC1 = bias_variable([1024])

h_pool2_flat  = tf.reshape(h_pool2, [-1, 7 * 7 * 64])

h_fullyC1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fullyC1) + b_fullyC1)

keep_prob = tf.placeholder(tf.float32)

h_fullyC1_drop = tf.nn.dropout(h_fullyC1, keep_prob)

w_fullyC2 = weight_variable([1024, 10])
b_fullyC2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fullyC1_drop, w_fullyC2) + b_fullyC2)

cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))

print correct_prediction

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess.run(tf.initialize_all_variables())


for i in range(20000):
  batch = mnist.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print mnist.test.images.shape
print mnist.test.labels.shape
print("test accuracy %g"%accuracy.eval(feed_dict={
	x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))




































