
#Classe com dados sobre velocidades, capacidades, descréscimo de velocidade dos meios de transporte

#NOTA: inventei uma classe nova, para poder testar com muito mais encomendas
from cmath import inf


class Stats:
    transportes = ['bicicleta','mota','carro','camiao']
    base_vel = { # metros / min
            'bicicleta': 166.6667,
            'mota': 583.3333,
            'carro': 833.3333,
            'camiao': 766.6666
        }
    max_peso = { # em kg
            'bicicleta': 5.0,
            'mota': 20.0,
            'carro': 100.0, 
            'camiao': 3500.0         
        }

    max_volume = { # em cm^3   inventado
        'bicicleta': 120,
        'mota': 200,
        'carro': 5000,
        'camiao': 20000
    }
    vel_decr_peso = { # decrescimo de metros/minuto conforme kg
        'bicicleta': 10,
        'mota': 8.3333,
        'carro': 1.6666,
        'camiao': 0.0833
    }

    consumo = { # g C02/m  inventado
        'bicicleta': 0,
        'mota': 0.115,
        'carro': 0.200,
        'camiao': 0.500
    }

    rating_decr_atraso = [
        (5,5),
        (10,4),
        (15,3),
        (30,2),
        (60,1),
        (inf,0)
        # abaixo disso é 0 rating
    ]
    deliver_delay = 2 # definimos que o tempo de fazer uma entrega num local era arbitrariamente 2min
