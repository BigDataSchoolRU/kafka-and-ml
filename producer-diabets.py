from time import sleep
from json import dumps
from kafka import KafkaProducer
import pandas as pd
from sklearn import datasets

# Load the dataset
diabetes = datasets.load_diabetes(as_frame=True)


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

if __name__=='__main__':
    for num in range(10):
        data = dict(pd.DataFrame(diabetes['data']).iloc[num])
        print(data)
        producer.send('diabet_kafka_topic', value=data)
        sleep(10)