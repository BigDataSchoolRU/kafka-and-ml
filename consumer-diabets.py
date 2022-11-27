from kafka import KafkaConsumer
from json import loads
import pickle
import pandas as pd
import numpy as np
import requests
import json
import psycopg2

HOST_DB = '0.0.0.0'
PORT = 5432
POSTGRES_USER='unicorn_user'
POSTGRES_PASSWORD='magical_password'
POSTGRES_DB='rainbow_database'

consumer = KafkaConsumer(
                        'diabet_kafka_topic',
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer=lambda x: loads(x.decode('utf-8')))

def add_predict(text):
    # создаем коннектор
    conn = psycopg2.connect(host=HOST_DB, port = 5432, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
    # создаем курсор
    cur = conn.cursor()

    # выполняем SQL запрос
    cur.execute("INSERT INTO ml_predict (predict) VALUES(%s)", (text,))
    
    # все коммитим и закрываем
    conn.commit()
    conn.close()
    cur.close()


if __name__=='__main__':
    for message in consumer:
        message = message.value
        # print(message)
        with open("model.pkl", "rb") as f:
            model_forest = pickle.load(f)
        # print(list(message.values()))
        # print(np.array(list(message.values())))
        # print(np.array(list(message.values())).reshape(1, -1))
        print(model_forest.predict(np.array(list(message.values())).reshape(1, -1)))

        response = requests.post(url = "http://127.0.0.1:8000/model-predict", data = json.dumps(message))
        print(response.text)
        add_predict(response.text)


