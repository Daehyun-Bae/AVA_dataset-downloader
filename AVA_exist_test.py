import tensorflow as tf
import sys
import os

TARGET_DIR = './../../data/ava/images/'
LIST_FILE = './ava_ID.csv'
JPG_FORMAT = '.jpg'
default_record = [[""]]
batch = 1000
epoch = 256

def read_list(listfile):
    try:
        list_queue = tf.train.string_input_producer([listfile], name='list_queue')
        textReader = tf.TextLineReader()

        key, value = textReader.read(list_queue)

        ID_list = tf.decode_csv(value, record_defaults=default_record, field_delim=' ')
        return ID_list
    except:
        print('Unexpected Error in reading list file...', sys.exc_info()[1])
        exit()

def get_id_batch(listfile, batch_size):
    _id_list = read_list(listfile)
    batch_id_list = tf.train.batch([_id_list], batch_size=batch_size)
    return batch_id_list

def check_exist(file_id):
    return os.path.isfile(TARGET_DIR + file_id + JPG_FORMAT)

def main():
    fp = open('./../../absent_list.csv', 'w')
    if(os.path.exists(LIST_FILE)): print('file existed..')
    batch_id_list = get_id_batch(LIST_FILE, batch)
    img_id = tf.placeholder(tf.string, [batch, 1])
    with tf.Session() as sess:
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        for i in range(epoch):
            try:
                print('Batch %d' % (i + 1))
                _id = sess.run(batch_id_list)
                IDs = sess.run(img_id, feed_dict={img_id: _id})
                for j in range(batch):
                    if(check_exist(IDs[j][0].decode('utf-8'))):
                        continue
                    else:
                        print(IDs[j][0].decode('utf-8'), 'is not exited...')
                        fp.write(IDs[j][0].decode('utf-8')+'\n')
            except:
                print('Unxpected error...', sys.exc_info()[1])
                exit()
        print('session end')
        coord.request_stop()
        coord.join(threads)
    fp.close()

main()