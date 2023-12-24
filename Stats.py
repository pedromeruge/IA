
#Classe com dados sobre velocidades, capacidades, descréscimo de velocidade dos meios de transporte
class Stats:
    def __init__(self):
        self.transportes = ['bicicleta','mota','carro']
        self.base_vel = { # metros / min
            'bicicleta': 166.6667,
            'mota': 583.3333,
            'carro': 833.3333
        }
        self.max_peso = { # em kg
            'bicicleta': 5.0,
            'mota': 20.0,
            'carro': 100.0            
        }

        self.max_volume = { # em cm^3   inventado
            'bicicleta': 120,
            'mota': 200,
            'carro': 5000  
        }
        self.vel_decr_peso = { # decrescimo de metros/minuto conforme kg
            'bicicleta': 10,
            'mota': 8.3333,
            'carro': 1.6666
        }

        self.consumo = { # g C02/m  inventado
            'bicicleta': 0,
            'mota': 0.115,
            'carro': 0.200
        }

        self.rating_decr_atraso = [
            (5,5),
            (10,4),
            (15,3),
            (30,2),
            (60,1)
            # abaixo disso é 0 rating
        ]
        self.deliver_delay = 2 # definimos que o tempo de fazer uma entrega num local era arbitrariamente 2min
