import os
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Utils.Variables import dataset, parent_dir
parent_dir = '\\'.join(str(parent_dir).split('\\')[:-2])
current_time = str(time.time())



tensorboard = TensorBoard(log_dir=rf'{parent_dir}'+r'\NBA-Machine-Learning-Sports-Betting\Logs\{}'.format(current_time))
earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
mcp_save = ModelCheckpoint(rf'{parent_dir}\NBA-Machine-Learning-Sports-Betting\Models\Trained-Model-ML-' + current_time, save_best_only=True, monitor='val_loss', mode='min')

con = sqlite3.connect(rf"{parent_dir}\NBA-Machine-Learning-Sports-Betting\Data\dataset.sqlite")
data = pd.read_sql_query(f"select * from \"{dataset}\"", con, index_col="index")
con.close()

scores = data['Score']
margin = data['Home-Team-Win']
data.drop(['Score', 'Home-Team-Win', 'TEAM_NAME', 'Date', 'TEAM_NAME.1', 'Date.1', 'OU', 'OU-Cover'], axis=1, inplace=True)

data = data.values
data = data.astype(float)

x_train = tf.keras.utils.normalize(data, axis=1)
y_train = np.asarray(margin)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu6))
model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=50, validation_split=0.1, batch_size=32,
          callbacks=[tensorboard, earlyStopping, mcp_save])

print('Done')
