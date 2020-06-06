import tensorflow as tf
from tensorflow.keras import models,layers,callbacks,metrics,backend, losses #pylint: disable=import-error
import numpy as np

#from https://github.com/Separius/BERT-keras/blob/master/transformer/layers.py

class LayerNormalization(layers.Layer):  #pragma: no cover
    def __init__(self, eps: float = 1e-5, **kwargs) -> None:
        self.eps = eps
        super().__init__(**kwargs)

    def build(self, input_shape):
        self.gamma = self.add_weight(name='gamma', shape=input_shape[-1:],  trainable=True)
        self.beta = self.add_weight(name='beta', shape=input_shape[-1:], trainable=True)
        super().build(input_shape)

    def call(self, x, **kwargs): 
        u = backend.mean(x, axis=-1, keepdims=True)
        s = backend.mean(backend.square(x - u), axis=-1, keepdims=True)
        z = (x - u) / backend.sqrt(s + self.eps)
        return self.gamma * z + self.beta

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        config = {
            'eps': self.eps,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class Gelu(layers.Layer): #pragma: no cover
    def call(self, inputs, **kwargs):
        return inputs * 0.5 * (1.0 + tf.math.erf(inputs / np.sqrt(2.0)))
    def get_config(self):
        return super().get_config()

def full_model(seq_len,
               vocab_size,
               embedding_dim = 128,
               d_hid = 128*4,
               num_heads = 8,
               num_layers = 4
             ):

    inp_layer = layers.Input(batch_shape=(None,seq_len),name='input')

    inp_embeddings = layers.Embedding(input_dim =vocab_size,
                                   output_dim = embedding_dim,
                                   name = f"input_embedding")(inp_layer)

    cur_block = layers.Conv1D(filters=d_hid,
                              kernel_size=1,
                              padding='same',
                              name=f"FF_initial")(inp_embeddings)

    for i in range(num_layers):

        # transformer block

        head_outputs = list()

        for head in range(num_heads):

            query = layers.Conv1D(filters=embedding_dim,
                                  kernel_size=1,
                                  padding='same',
                                  name=f"query_{i}_{head}")(cur_block)

            value = layers.Conv1D(filters=embedding_dim,
                                  kernel_size=1,
                                  padding='same',
                                  name=f"value_{i}_{head}")(cur_block)

            head_outputs.append(layers.Attention(use_scale=True,name=f"attended_{i}_{head}")([query,value]))

        attended_result = layers.Concatenate(name=f"attention_result_{i}")(head_outputs)
        attended_gelu = Gelu(name=f"gelu_{i}")(attended_result)
        ff = layers.Conv1D(filters=d_hid,
                           kernel_size=1,
                           padding='same',
                           name=f"FF_{i}")(attended_gelu)

        ff_normed = LayerNormalization(name=f'layer_norm_{i}')(ff)


        # add output of transformer block to previous state
        cur_block = layers.Add(name=f"Add_{i}")([cur_block,ff_normed])


    penult = layers.Conv1D(filters=d_hid,
                           kernel_size=1,
                           padding='same',
                           name=f"penultimate_FF")(cur_block)
    penult_gelu = Gelu(name=f"penultimate_gelu")(penult)
    penult_normed = LayerNormalization(name=f'penult_norm')(penult_gelu)


    out_layer = layers.Dense(vocab_size,activation='softmax',name=f"output")(penult_normed)



    mdl = models.Model(inputs=[inp_layer],outputs=[out_layer])
    return mdl


