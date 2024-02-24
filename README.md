# Kafka Stock Market Streaming Project
## Project Overview
 The purpose of this Kafka stock market streaming project is to illustrate how one could create a full
 end to end streaming solution using a simulated streaming input API, a Kafka runtime running on am AWS
 EC2 server, S3 storage buckets, AWS Glue, and AWS Athena, so that this data stream can be indefintely stored
 and queried using SQL using minimal overhead. The project uses a Kafka instance running on an EC2 Server
 along with S3 result storage to pipe input streaming data into storage which is later crawled and queried using
 AWS Glue and Athena.

 The project proceeds with the following dataflow:

Stock Market Real time API/ CSV file (if not willing to pay for API) --> Producer python program (on local machine) -->
Kafka instance on AWS EC2 server --> Consumer python program (on local machine) --> Result Storage in Amazon S3 Bucket
--> Crawled using AWS Glue crawler --> Queried from Amazon Athena --> From here the relational databsase structure can be manipulated ans safely stored to perform whatever is necessary.

 It should be noted that this is an implementation of a project posted by github user darshilparmar,
 which is documented here: <br />
--> https://github.com/darshilparmar/stock-market-kafka-data-engineering-project <br />
--> https://www.youtube.com/watch?v=KerNf0NANMo

I am posting this project to take note of steps I needed to take to make this solution work in addition to 
resources cited, both for my own future benefit, and for anyone else who might be having trouble creating this
solution. 

## General Steps for completing Project
1. The first step would to install Kafka into the EC2 machine. Log into the AWS Account, and launch a new instane.
Name the instance whatever you want. I personally came into trouble when using the t3.nano machine type, as its 1 GB of
RAM was insufficuent. I would recomment using something with at least 2 GB of RAM, such as the t3.small node size. I used
the dafault Amazon Linus OS.

do not forget to create the key pair .pem file, and store it somewhere safe. 

2. Once the EC2 instance is running, note the ec2 public web link, and log into the ec2 machine ussing something like
   'ssh -i "Key_pair_name.pem" ec2-user@EC2_public_web_link_provided_in_EC2_instance_Details'

3.  Install Kafak onto the ec2 machine. The specific version you should use will vary a it gets updated, but on February 2024,
   I would run something like "wget https://downloads.apache.org/kafka/3.6.1/kafka_2.12-3.6.1.tgz
tar -xvf kafka_2.12-3.6.1.tgz". Search this apache downloads ans see what is available.

4.  Do not forget to install java onto the server. I did this using "sudo yum install java-17-amazon-corretto-devel". Use whatever
   is current.

5. Start the zookeeper node within the new kafka software directory. Do this by running this within the kafka directory:
bin/zookeeper-server-start.sh config/zookeeper.properties. You run this first before beginning the general kafka instance
because zookeeper is the master node without which kafka would not function. You need to run zookeeper before Kafka.

7.  Now you can start the Kafka instance using bin/kafka-server-start.sh config/server.properties .
do not try reallocting memory for the kafka server using the KAFKA_HEAP_OPTS command as others recommend. As long as your node
generally has at least 2GB of ram generally, everything will be fine, and this reallocation caused my kafka instance to fail.

8. You will see that the Kafka server references the local IP address of the EC2 machine. You want to switch this to the public
   IP address. You do this by navigating th the config/server.properties file, and uncomment and change the advertized.listeners= line.
   It shoudl look something like this :
   advertised.listeners=PLAINTEXT://Your_Public_EC2_Server_IP_Address:9092
   

10. Restart Both Zookeeper and kafka servers. IP address should now be shows as public ec2 ip in kafka.

11. In ec2 security, create new inbound rule to allow all traffic for either anywhere or your specific IP ddress (latter is safer for obvious reasons).

12.  connect to ec2 machine in two other terminals. Here you will create a producer input console using:
bin/kafka-topics.sh --create --topic demo_testing) --bootstrap-server {Put the Public IP of your EC2 Instance:9092} --replication-factor 1 --partitions 1
This makes the console a good place to input text as input from the producer stand point. This is all to confirm that the system works properly.

14.  ssh into the ec2 server from another console/commandline window using:
bin/kafka-console-consumer.sh --topic demo_testing2 --bootstrap-server {Put the Public IP of your EC2 Instance:9092}

At this point, anything typed into the producer window will output into the consumer window after a short delay. This should work, and with that you, know that the kafka server is working and anything inputted into the producer console outputs into the consumer console.

15.   Implement the attached producer python script to better manage the input stream being inputted into Kafka. These python scripts can be hosted on the ec2 server to serve as a better long term solution relative to a local machine. 

16.    Create an AWS S3 storage bucket where you would like your output to be stored.

17. Implement the attached consumer python script to see output, and to redirect output to S3 storage, which 
    You should be able to see the stream come into the S3 storage. If you do not, carefully make sure that Kafka is running properly, and
    that all previous steps have been completed properly. Missing any of these steps results in a failure. If all else fails, create a new EC2 server and begin from scratch if you cannot pinpoint cause of failure.

18. Create an IAM role for the Glue crawler. Give it admin access, assigning it a memorable name. 

19.   Set up an AWS Glue crawler using the IAM role previously set up, directing it to the functioning S3 bucket (whole bucket). 

20.  Create a second S3 bucket to host SQL tables, and query these table using AWS Athena. 

21. That is it! Using this solution would be a great way to quickly store and analyze many kinds of streaming data. In this case, we are using fake stock data to simulate real streaming input through some API. 

22. Please let me know if anything is missing or could be improved. Don't be shy. Thank you!
