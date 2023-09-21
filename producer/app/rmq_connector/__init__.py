import os

import pika


class RMQExchangeConnector():
    def __init__(self, exchange: str = '', exchange_type: str = 'fanout'):
        self.connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=os.environ.get('PIKA_HOST', 'rabbitmq'),
                port=os.environ.get('PIKA_PORT', 5672),
            )
        )
        self.exchange = exchange
        self.exchange_type = exchange_type

    def __enter__(self):
        self.channel = self.connection.channel()
        self._create_exchange()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO read more on https://realpython.com/python-with-statement/
        self.channel.close()

    def _create_exchange(self):
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type,
            durable=True,
        )

    def create_queue(self, queue: str = '') -> str:
        queue = self.channel.queue_declare(
            queue=queue,
            durable=True,
        )
        return queue.method.queue

    def basic_publish(self, routing_key: str, body: str):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                content_type='',
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            )
        )
