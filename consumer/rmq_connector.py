import os
from typing import Union, Callable

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
                connection_attempts=10,
                retry_delay=5,
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
        self.channel.stop_consuming()
        self.channel.close()
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

    def basic_consume(self, queue_name: str, callback: Callable, auto_ack: bool = True):
        """Consume messages from a queue.

        Args:
            queue_name (str): Queue's name
            callback (Callable): Callback dispatched on message
            auto_ack (bool, optional): Auto acknowledgment. Defaults to True.
                If False, callback must handle acknowledgment
        """
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=auto_ack,
        )

    def start_consuming(self):
        """Dispatch basic_consume callbacks until all consumers are cancelled.
        """
        self.channel.start_consuming()
