import tensorflow as tf
from tensorflow.python.client import device_lib


def new_session():
    tf.keras.backend.clear_session()
    tf.keras.backend.get_session().close()
    cfg = tf.ConfigProto()
    cfg.gpu_options.allow_growth = True
    tf.keras.backend.set_session(tf.Session(config=cfg))


def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.physical_device_desc for x in local_device_protos if x.device_type == 'GPU']
