import tensorflow as tf 

tf.enable_eager_execution()

print(tf.executing_eagerly())

print(tf.add(2, 3))