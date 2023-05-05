import pika
import random
import time
import threading

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar la cola para el agente y los fumadores
channel.queue_declare(queue='agent')
channel.queue_declare(queue='tobacco_smoker')
channel.queue_declare(queue='paper_smoker')
channel.queue_declare(queue='matches_smoker')

# Función para simular el proceso de fumar
def smoke():
    time.sleep(random.randint(1, 3))

# Función que se ejecuta cuando el agente deja los ingredientes en la mesa
def agent():
    while True:
        time.sleep(random.randint(1, 3))
        ingredients = ['tobacco', 'paper', 'matches']
        random.shuffle(ingredients)
        channel.basic_publish(exchange='', routing_key='agent', body=','.join(ingredients).encode())

# Función que se ejecuta cuando el fumador con tabaco está listo para fumar
def tobacco_smoker(ch, method, properties, ingredients):
    if 'paper' in ingredients and 'matches' in ingredients:
        print('Tobacco smoker is smoking')
        smoke()
        channel.basic_publish(exchange='', routing_key='agent', body='tobacco'.encode())

# Función que se ejecuta cuando el fumador con papel está listo para fumar
def paper_smoker(ch, method, properties, ingredients):
    if 'tobacco' in ingredients and 'matches' in ingredients:
        print('Paper smoker is smoking')
        smoke()
        channel.basic_publish(exchange='', routing_key='agent', body='paper'.encode())

# Función que se ejecuta cuando el fumador con cerillas está listo para fumar
def matches_smoker(ch, method, properties, ingredients):
    if 'tobacco' in ingredients and 'paper' in ingredients:
        print('Matches smoker is smoking')
        smoke()
        channel.basic_publish(exchange='', routing_key='agent', body='matches'.encode())

# Asignar las funciones a cada cola
channel.basic_consume(queue='agent', on_message_callback=lambda ch, method, properties, body: [tobacco_smoker(ch, method, properties, body.decode('utf-8').split(',')), paper_smoker(ch, method, properties, body.decode('utf-8').split(',')), matches_smoker(ch, method, properties, body.decode('utf-8').split(','))])
channel.basic_consume(queue='tobacco_smoker', on_message_callback=tobacco_smoker)
channel.basic_consume(queue='paper_smoker', on_message_callback=paper_smoker)
channel.basic_consume(queue='matches_smoker', on_message_callback=matches_smoker)

# Iniciar los procesos
agent_process = threading.Thread(target=agent)
agent_process.start()

channel.start_consuming()

# Cerrar la conexión a RabbitMQ
channel.close()
connection.close()