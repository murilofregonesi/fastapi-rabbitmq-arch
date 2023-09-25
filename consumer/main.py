from dotenv import load_dotenv

from rmq_connector import RMQExchangeConnector
from callbacks import (
    user_info_callback,
    user_error_callback,
    oder_info_callback,
    oder_error_callback,
)


load_dotenv()

if __name__ == '__main__':
    with RMQExchangeConnector(exchange='producer_log', exchange_type='topic') as rmq:
        user_info_queue = rmq.create_queue(queue='user.info', binding_key='user.*')
        user_error_queue = rmq.create_queue(queue='user.error', binding_key='user.error')
        oder_info_queue = rmq.create_queue(queue='order.info', binding_key='order.*')
        oder_error_queue = rmq.create_queue(queue='order.error', binding_key='order.error')

        rmq.basic_consume(user_info_queue, user_info_callback)
        rmq.basic_consume(user_error_queue, user_error_callback)
        rmq.basic_consume(oder_info_queue, oder_info_callback)
        rmq.basic_consume(oder_error_queue, oder_error_callback)

        try:
            print('Consumer started...')
            rmq.start_consuming()
        except KeyboardInterrupt:
            print('...Consumer stopped')
