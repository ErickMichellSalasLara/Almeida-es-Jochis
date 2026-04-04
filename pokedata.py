import numpy as np

class Table_Types:
    EFECTIVIDAD = {
        "DUCHA": {"TICS": 2.0, "MECOSTRONICOS": 2.0, "CHATGIPITY": 4.0, "FEMBOY": 0.5, "VIEJA": 0.5},
        "FEMBOY": {"DUCHA": 2.0,"MERCADOFIESTA": 2.0,"TICS": 0.5,"MECOSTRONICOS": 0.5},
        "TICS": {"FEMBOY": 2.0,"MERCADOFIESTA": 2.0,"DUCHA": 0.5,"INTELIGENTE": 0.5,"JORNADA_LABORAL": 0.5, "FURROS": 2.0},
        "VIEJA": {"FLOJO": 4.0,"TICS": 2.0,"MECOSTRONICOS": 2.0,"DUCHA": 0.5, "FURROS": 2.0},
        "FLOJO": {"VIEJA": 0.5,"JORNADA_LABORAL": 0.5,"INTELIGENTE": 0.5},
        "INTELIGENTE": {"FLOJO": 2.0,"MERCADOFIESTA": 2.0,"JORNADA_LABORAL": 2.0,"CHATGIPITY": 0.5, "FURROS": 0.5},
        "CHATGIPITY": {"TICS": 2.0,"MECOSTRONICOS": 2.0,"INTELIGENTE": 0.5,"DUCHA": 0.5},
        "JOCHIS": {"FEMBOY": 2.0,"VIEJA": 2.0,"MECOSTRONICOS": 2.0,"TICS": 0.5,"INTELIGENTE": 0.5, "FURROS": 0.5},
        "MECOSTRONICOS": {"MERCADOFIESTA": 2.0,"DUCHA": 0.5,"FEMBOY": 0.5,"JORNADA_LABORAL": 0.5},
        "MERCADOFIESTA": {"FEMBOY": 2.0,"TICS": 0.5,"JOCHIS": 0.5, "FURROS": 0.5},
        "JORNADA_LABORAL": {"TICS": 2.0,"MECOSTRONICOS": 2.0,"FLOJO": 4.0,"MERCADOFIESTA": 2.0,"INTELIGENTE": 0.5,"CHATGIPITY": 0.5, "FURROS": 2.0},
        "FURROS": {"INTELIGENTE": 2.0,"MERCADOFIESTA": 2.0,"JOCHIS": 2.0,"TICS": 0.5,"JORNADA_LABORAL": 0.5,"VIEJA": 0.5},
    }
    
    def get_effectiveness(tipo_atacante, tipo_defensor):
        # Si el tipo atacante no tiene una efectividad definida contra el tipo defensor, se devuelve 1.0 (efectividad normal)
        return Table_Types.EFECTIVIDAD.get(tipo_atacante, {}).get(tipo_defensor, 1.0)

#Creamos una clase para clasificar los movimientos de los pokemones, cada movimiento tiene un nombre, un tipo, una potencia y una precision, la cual se usara para calcular el daño que hace el movimiento al pokemon defensor
class Movements:
    def __init__(self, nombre, tipo, potencia, precision):
        self.nombre = nombre
        self.tipo = tipo
        self.potencia = potencia
        self.precision = precision

#Creamos un diccionario para guardar varios movimientos. Con sus respectivas caracteristicas
MOVIMIENTOS = {
    #Se añade el nombre y se "iguala" a los datos de la instancia de la clase Movements. (nombre, tipo, potencia y precision)
    "Mega Puño": Movements("Mega Puño", "FLOJO", 80, 85),
    "Golpe Cuerpo": Movements("Golpe Cuerpo", "MECOSTRONICOS", 85, 100),
    "Miados": Movements("Miados", "TICS", 65, 100),
    "Prompt": Movements("Prompt", "CHATGIPITY", 75, 90),
}

# Aplicamos herencia en esta parte
class STATS_BASE:
    def __init__(self, nombre, tipo, hp_max, ataque, defensa, velocidad, nivel = 50):
        self._nombre = nombre
        self._tipo = tipo
        self._hp_max = hp_max
        self._hp_actual = hp_max  # Inicializamos el HP actual al maximo
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self._nivel = nivel
        self._movimientos = []
        
    # El hp actual se inicializa al maximo hp, ya que al crear un nuevo pokemon, este estara completamente sano
    def curar_totalmente(self):
        self._hp_actual = self._hp_max
    # El metodo recibir_daño se encarga de reducir el hp actual del pokemon, y si el hp actual llega a 0, el pokemon se considera debilitado
    def recibir_daño(self, cantidad):
        self._hp_actual = max(0, self._hp_actual - cantidad)
        
#------ Clases de los pokemones, cada clase hereda de la clase STATS_BASE, y se le pueden agregar atributos y metodos especificos de cada pokemon, como por ejemplo, los movimientos que puede aprender, las habilidades que tiene etc.------
class Giovanni(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class David(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "David",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Erick(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Erick",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Rafa(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Didier(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Didier",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Abraham(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Alberto(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Morro_Generico_Diseño(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Morro_Generico_Mercadofiesta(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Gato(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Osmar(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class Morro_Ardido_Generico(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase

class Morra_Castrosa(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase
        
class El_Rector_Que_No_Es_El_Rector(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Mega Puño"], MOVIMIENTOS["Golpe Cuerpo"], MOVIMIENTOS["Miados"], MOVIMIENTOS["Prompt"]]
        #--------- Aqui se completa la clase