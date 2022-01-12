import json
from kafka import KafkaProducer
from stream.twitter_stream import TwitterStream
from stream.rules_config import rules
from stream.stream_config import query_params
from utils import safe_factory

KAFKA_TOPIC = "tweets"

if __name__ == "__main__":

    def on_tweet_received(tweet_res):
        print(json.dumps(tweet_res, indent=4, sort_keys=True))
        producer.send(topic=KAFKA_TOPIC, value=tweet_res)

    safe = safe_factory((AttributeError, TypeError), None)

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    stream = TwitterStream()\
        .with_params(query_params)\
        .with_rules(rules)\
        .apply(on_tweet_received)\
        .listen()
