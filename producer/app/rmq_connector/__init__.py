import os
from typing import Union

import pika


class RMQExchangeConnector():
    """RabbitMQ Single Exchange Connector.
    Provides a context manager for a single exchange,
    whose parameters are declared during initialization.
    """
    def __init__(self, exchange: str = '', exchange_type: str = 'fanout'):
        """Create a RMQ connection and initialize exchange parameters.

        Args:
            exchange (str, optional): Exchange name. Defaults to ''.
            exchange_type (str, optional): Exchange type. Defaults to 'fanout'.
                Accepts [fanout, direct, topic], 'headers' won't work
        """
        self.connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=os.environ.get('PIKA_HOST', 'rabbitmq'),
                port=os.environ.get('PIKA_PORT', 5672),
                credentials=pika.PlainCredentials(
                    username=os.environ.get('PIKA_USER', 'fast'),
                    password=os.environ.get('PIKA_PASS', 'fast'),
                ),
            )
        )
        self.exchange = exchange
        self.exchange_type = exchange_type

    def __enter__(self) -> 'RMQExchangeConnector':
        """Initialize the context manager with the creation of the Exchange.

        Returns:
            RMQExchangeConnector: self
        """
        self.channel = self.connection.channel()
        self._create_exchange()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager closing the connection.
        """
        self.connection.close()

    def _create_exchange(self):
        """Create the Exchange based on parameters sent during initialization.
        """
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type,
            durable=True,
        )

    def create_queue(self, queue: str = '', binding_key: Union[str, None] = None) -> str:
        """Create a new Queue for the instance's Exchange.

        Args:
            queue (str, optional): Queue's name. Defaults to '' (random)
            binding_key (str, optional): Binding key. Defaults to None
                If None, Queue's name is used.

        Returns:
            str: Queue's name
        """
        queue = self.channel.queue_declare(
            queue=queue,
            durable=True,
        )
        queue_name = queue.method.queue

        self.channel.queue_bind(
            exchange=self.exchange,
            queue=queue_name,
            routing_key=binding_key or queue_name,
        )
        return queue_name

    def basic_publish(self, body: str, routing_key: str = ''):
        """Publish a message to the broker.

        Args:
            body (str): Message to be published
            routing_key (str, optional): Key to route the message. Defaults to ''
                '' to 'fanout' exchange type
                Queue's name to 'direct' exchange type
                Topic to 'topic' exchange type, e.g. *.error#
        """
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                content_type='',
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            )
        )
