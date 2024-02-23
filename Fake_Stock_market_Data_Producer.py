#Using this code to create data in producer side of Kafka
# Running program will sent stream of data from the local adn referenced .csv file one entry every second 

import pandas as pd
from kafka import KafkaProducer
from time import sleep
from json import dumps
import json

#Enter the IP address of the EC2 server you are using here
producer = KafkaProducer(bootstrap_servers=['16.16.141.101:9092'],
        value_serializer = lambda x:
        dumps(x).encode('utf-8'),
        api_version=(0, 10, 1))

#producer.send('demo_test', value={'hello':'world'})

df_in = pd.read_csv("/home/hubbell/PlayingFiles/Data_Eng/Kafka_Stock_Market_Real_Time_Project_Files/indexProcessed.csv")

df_in.head()

while True:
    dict_stock = df_in.sample(1).to_dict(orient="records")[0]

    producer.send('demo_test', value= dict_stock)
    
    sleep(1)

producer.flush()
