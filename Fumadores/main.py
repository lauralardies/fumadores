import pika, threading
from fumador import *
from agente import *

def main():
    # Conexión a RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    class_agent = Agent(channel)
    class_smoker = Smoker(channel)

    # Declarar la cola para el agente y los fumadores
    channel.queue_declare(queue='agent')
    channel.queue_declare(queue='tobacco_smoker')
    channel.queue_declare(queue='paper_smoker')
    channel.queue_declare(queue='matches_smoker')

    # Asignar las funciones a cada cola
    channel.basic_consume(queue='agent', on_message_callback=lambda ch, method, properties, body: [class_smoker.tobacco_smoker(ch, method, properties, body.decode('utf-8').split(',')), class_smoker.paper_smoker(ch, method, properties, body.decode('utf-8').split(',')), class_smoker.matches_smoker(ch, method, properties, body.decode('utf-8').split(','))])
    channel.basic_consume(queue='tobacco_smoker', on_message_callback=class_smoker.tobacco_smoker)
    channel.basic_consume(queue='paper_smoker', on_message_callback=class_smoker.paper_smoker)
    channel.basic_consume(queue='matches_smoker', on_message_callback=class_smoker.matches_smoker)

    # Iniciar los procesos
    agent_process = threading.Thread(target=class_agent.agent)
    agent_process.start()

    channel.start_consuming()

    # Cerrar la conexión a RabbitMQ
    channel.close()
    connection.close()