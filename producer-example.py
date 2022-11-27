from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

if __name__=='__main__':
    for e in range(5):
        data = {'number' : e}
        producer.send('numtest', value=data)
        sleep(5)