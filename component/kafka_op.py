# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import socket
import sys

from confluent_kafka.cimpl import Producer

sys.path.append("./")
sys.setrecursionlimit(10000000)
import json
from configs import kafka
from configs import admin


# Asynchronous writes
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


if admin.use_kafka is True:
    conf = {'bootstrap.servers': kafka.bootstrap_servers,
            'client.id': socket.gethostname()}
    topic = kafka.kafka_topic
    producer = Producer(conf)


def insert_message_to_kafka(msg):
    producer.produce(topic=kafka.kafka_topic, key="key", value=json.dumps(msg).encode(), callback=acked)


kafka_offset_reset = 'earliest'  # latest,earliest,none 首次拉取kafka订阅的模式


def get_message_from_kafka():
    consumer = KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=kafka.client_group_id, auto_offset_reset=kafka_offset_reset,
                             client_id='get_message_from_kafka')
    return consumer


def get_message_from_kafka_independent_listener():
    consumer = KafkaConsumer(kafka.kafka_topic, bootstrap_servers=kafka.bootstrap_servers, group_id=admin.independent_listener_kafka_client_group_id,
                             auto_offset_reset=kafka_offset_reset, client_id='get_message_from_kafka_independent_listener')
    return consumer


if __name__ == "__main__":
    insert_message_to_kafka(msg={'msg': 'test'})
