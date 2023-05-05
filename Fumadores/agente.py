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