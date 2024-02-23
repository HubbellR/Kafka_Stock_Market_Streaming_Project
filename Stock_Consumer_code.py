#Code for the consumer of Stock Market Kafka steaming process
from kafka import KafkaConsumer
from time import sleep
from json import dumps, loads
import json
from s3fs import S3FileSystem

consumer = KafkaConsumer(
        'demo_test',
        #Here enter/edit the IP address of the EC2 server being used
        bootstrap_servers = ['16.16.141.101:9092'],
        value_deserializer= lambda x: loads(x.decode('utf-8')),
        api_version=(0, 10, 1))    

#for c in consumer:
#    print(c.value)

s3 = S3FileSystem()

for count, i in enumerate(consumer):
    print(i)
    with s3.open("s3://hwr-stock-market-kafka-proj/stock_market_{}.json".format(count), 'w') as file:
        json.dump(i.value, file)




