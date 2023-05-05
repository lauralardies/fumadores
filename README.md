# fumadores

Mi dirección de GitHub para este repositorio es la siguiente: [GitHub](https://github.com/lauralardies/fumadores)
https://github.com/lauralardies/fumadores

## Breve introducción
Este ejercicio nos presenta el problema de los fumadores y cómo resolverlo.

¿En qué consiste el **problema de los fumadores**? En un grupo de fumadores cada fumador tiene determinados recursos, pero esos recursos no son todos los que necesita para alcanzar su objetivo (fumar). Por lo tanto, el fumador necesita de los recursos de los otros fumadores del grupo. Este problema es el típico ejemplo de exclusión mutua/interbloqueo, puesto que tienes un recurso y se lo das a otro para tu beneficio de que el otro te de su recurso, pero te quedas en la misma situación de antes ya que has perdido el recurso que previamente tenías. 

Para este problema hemos hecho uso del m´ódulo RabbitMQ.

## Código
Todos los archivos están guardados en la carpeta `Fumadores`.

### Código `agente.py`
```
import time, random

class Agent():
    def __init__(self, channel):
        self.channel = channel

    def agent(self):
        '''
        Función que se ejecuta cuando el agente deja los ingredientes en la mesa
        '''
        while True:
            time.sleep(random.randint(1, 3))
            ingredients = ['tobacco', 'paper', 'matches']
            random.shuffle(ingredients)
            self.channel.basic_publish(exchange='', routing_key='agent', body=','.join(ingredients).encode())
```

### Código `fumador.py`
```
import time, random

class Smoker():
    def __init__(self, channel):
        self.channel = channel

    def smoke(self):
        '''
        Función para simular el proceso de fumar
        '''
        time.sleep(random.randint(1, 3))

    def tobacco_smoker(self, ch, method, properties, ingredients):
        '''
        Función que se ejecuta cuando el fumador con tabaco está listo para fumar
        '''
        if 'paper' in ingredients and 'matches' in ingredients:
            print('Tobacco smoker is smoking')
            self.smoke()
            self.channel.basic_publish(exchange='', routing_key='agent', body='tobacco'.encode())

    def paper_smoker(self, ch, method, properties, ingredients):
        '''
        Función que se ejecuta cuando el fumador con papel está listo para fumar
        '''
        if 'tobacco' in ingredients and 'matches' in ingredients:
            print('Paper smoker is smoking')
            self.smoke()
            self.channel.basic_publish(exchange='', routing_key='agent', body='paper'.encode())

    def matches_smoker(self, ch, method, properties, ingredients):
        '''
        Función que se ejecuta cuando el fumador con cerillas está listo para fumar
        '''
        if 'tobacco' in ingredients and 'paper' in ingredients:
            print('Matches smoker is smoking')
            self.smoke()
            self.channel.basic_publish(exchange='', routing_key='agent', body='matches'.encode())
```

### Código `main.py`
```
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
```

### Código `run.py`
```
from main import main

if __name__ == '__main__':
    main()
```
