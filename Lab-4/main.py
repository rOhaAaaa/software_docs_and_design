import json
from data_reader import CsvReader
from strategies import ConsoleStrategy, RedisStrategy, KafkaStrategy, IOutputStrategy

class DataProcessor:
    def __init__(self, strategy: IOutputStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: IOutputStrategy):
        self._strategy = strategy

    def process_and_output(self, data: list):
        if not data:
            print("Немає даних для виводу.")
            return
        self._strategy.write(data)

def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def get_strategy_from_config(config):
    """Фабричний метод для вибору стратегії на основі конфігу"""
    strategy_name = config.get("output_strategy", "console").lower()

    if strategy_name == "redis":
        return RedisStrategy(host=config["redis_host"], port=config["redis_port"])
    elif strategy_name == "kafka":
        return KafkaStrategy(broker=config["kafka_broker"], topic=config["kafka_topic"])
    else:
        return ConsoleStrategy()

if __name__ == "__main__":
    config = load_config()

    reader = CsvReader(config["dataset_path"])
    crimes_data = reader.read_data(limit=5) 

    strategy = get_strategy_from_config(config)

    processor = DataProcessor(strategy)
    processor.process_and_output(crimes_data)