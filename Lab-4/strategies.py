from abc import ABC, abstractmethod
import json
import redis
from kafka import KafkaProducer

class IOutputStrategy(ABC):
    @abstractmethod
    def write(self, data: list):
        pass

class ConsoleStrategy(IOutputStrategy):
    def write(self, data: list):
        print("\n--- ВИВІД ДАНИХ У КОНСОЛЬ ---")
        for row in data:
            print(row)
        print(f"✅ Успішно виведено {len(data)} записів у консоль.\n")

class RedisStrategy(IOutputStrategy):
    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def write(self, data: list):
        print("\n--- ЗАПИС ДАНИХ У REDIS ---")
        for row in data:
            self.client.rpush("chicago_crimes", json.dumps(row))
        print(f"✅ Успішно записано {len(data)} записів у Redis.\n")

class KafkaStrategy(IOutputStrategy):
    def __init__(self, broker, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=[broker],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def write(self, data: list):
        print(f"\n--- ВІДПРАВКА ДАНИХ У KAFKA (Топік: {self.topic}) ---")
        for row in data:
            self.producer.send(self.topic, value=row)
        self.producer.flush()
        print(f"✅ Успішно відправлено {len(data)} записів у Kafka.\n")