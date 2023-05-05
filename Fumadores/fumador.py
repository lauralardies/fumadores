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