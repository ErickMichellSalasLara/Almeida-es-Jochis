import numpy as np, random

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
#Encapsulamos los atributos de la clase, para evitar que se modifiquen directamente desde fuera de la clase, y asi poder controlar mejor el comportamiento de los movimientos, como por ejemplo, si un movimiento tiene una potencia de 0, no deberia hacer daño al pokemon defensor, o si un movimiento tiene una precision de 0, no deberia tener ninguna posibilidad de acertar al pokemon defensor.
class Movement:
    def __init__(self, nombre, tipo, potencia, precision, efecto = None):
        self.nombre = nombre
        self.tipo = tipo
        self.potencia = potencia
        self.precision = precision
        self.efecto = efecto #Se iguala a nada ya que todavia no tenemos un efecto establecido
    # Esta funcion se encarga de determinar si el movimiento acierta o no, dependiendo de la precision del movimiento, y de un numero aleatorio generado entre 1 y 100, si el numero aleatorio es menor o igual a la precision del movimiento, entonces el movimiento acierta, de lo contrario, el movimiento falla.
    def acertar(self):
        return random.randint(1, 100) <= self.precision

#Creamos un diccionario para guardar varios movimientos. Con sus respectivas caracteristicas
#Potencia de ataques: 20-50 debil. 60-90 normal. 100-150 fuerte.
#Los movimientos se los pedi a la Ia ya que eran muchos los que queria agregar
MOVIMIENTOS = {
    # FLOJO
    "Siesta Mortal": Movement("Siesta Mortal", "FLOJO", 110, 60),
    "Bostezo": Movement("Bostezo", "FLOJO", 0, 100, "debuff_velocidad"),
    "Desgano": Movement("Desgano", "FLOJO", 60, 85),
    "Cansancio": Movement("Cansancio", "FLOJO", 0, 100, "debuff_ataque"),

    # MECOSTRONICOS
    "Engranaje Letal": Movement("Engranaje Letal", "MECOSTRONICOS", 90, 85),
    "SolidWorks": Movement("Descarga Técnica", "MECOSTRONICOS", 70, 95),
    "Ajuste Preciso": Movement("Ajuste Preciso", "MECOSTRONICOS", 0, 100, "buff_ataque"),
    "Mandato de Avalos": Movement("Mandato de Avalos", "MECOSTRONICOS", 0, 100, "buff_velocidad"),

    # TICS
    "Refactorizar": Movement("Refactorizar", "TICS", 80, 90),
    "Git Push": Movement("Git Push", "TICS", 100, 75),
    "Compilar": Movement("Compilar", "TICS", 0, 100, "buff_defensa"),
    "Error 404": Movement("Error 404", "TICS", 0, 100, "debuff_defensa"),

    # CHATGIPITY
    "Prompt Avanzado": Movement("Prompt Avanzado", "CHATGIPITY", 85, 90),
    "NO ME GUSTO, HAZLO OTRA VEZ": Movement("NO ME GUSTO, HAZLO OTRA VEZ", "CHATGIPITY", 70, 100),
    "Ram en aumento": Movement("Ram en aumento", "CHATGIPITY", 110, 65),
    "Generar Texto": Movement("Generar Texto", "CHATGIPITY", 0, 100, "buff_ataque"),

    # DUCHA
    "Chorro a Presión": Movement("Chorro a Presión", "DUCHA", 90, 85),
    "Baño": Movement("Baño", "DUCHA", 120, 65),
    "Agua Fría": Movement("Agua Fría", "DUCHA", 0, 100, "debuff_velocidad"),
    "Enjuague": Movement("Enjuague", "DUCHA", 0, 100, "buff_defensa"),

    # FEMBOY
    "Encanto Brillante": Movement("Encanto Brillante", "FEMBOY", 75, 95),
    "Mirada Cute": Movement("Mirada Cute", "FEMBOY", 0, 100, "debuff_ataque"),
    "Aura Fashion": Movement("Aura Fashion", "FEMBOY", 90, 80),
    "Deslumbrar": Movement("Deslumbrar", "FEMBOY", 0, 100, "debuff_defensa"),

    # VIEJA
    "Es solo un amigo": Movement("Es solo un amigo", "VIEJA", 95, 85),
    "Ilusionista": Movement("Ilusionista", "VIEJA", 70, 100),
    "Mirada Juzgadora": Movement("Mirada Juzgadora", "VIEJA", 0, 100, "debuff_ataque"),
    "Controladora": Movement("Grito Histórico", "VIEJA", 0, 100, "debuff_defensa"),

    # INTELIGENTE
    "Cálculo Mental": Movement("Cálculo Mental", "INTELIGENTE", 80, 100),
    "Formulario": Movement("Formulario", "INTELIGENTE", 0, 100, "buff_defensa"),
    "Rezo a San Cristian": Movement("Rezo a San Cristian", "INTELIGENTE", 0, 100, "buff_ataque"),
    "Integral Doble": Movement("Integral Doble", "INTELIGENTE", 120, 70),

    # JOCHIS
    "Orgullo Total": Movement("Orgullo Total", "JOCHIS", 85, 90),
    "Actitud": Movement("Actitud", "JOCHIS", 0, 100, "buff_ataque"),
    "Brillo Propio": Movement("Brillo Propio", "JOCHIS", 0, 100, "buff_velocidad"),
    "Impacto Diva": Movement("Impacto Diva", "JOCHIS", 110, 75),

    # MERCADOFIESTA
    "Organizacion de Evento": Movement("Organizacion de Evento", "MERCADOFIESTA", 90, 85),
    "Canva 2": Movement("Canva 2", "MERCADOFIESTA", 70, 95),
    "Descuento": Movement("Descuento", "MERCADOFIESTA", 0, 100, "buff_defensa"),
    "Little Ceasers": Movement("Little Ceasers", "MERCADOFIESTA", 110, 70),

    # JORNADA_LABORAL
    "Horas Extra": Movement("Horas Extra", "JORNADA_LABORAL", 95, 85),
    "Trabajo Duro": Movement("Trabajo Duro", "JORNADA_LABORAL", 80, 90),
    "Estrés": Movement("Estrés", "JORNADA_LABORAL", 0, 100, "debuff_ataque"),
    "Burnout": Movement("Burnout", "JORNADA_LABORAL", 120, 65),

    # FURROS
    "Furia Salvaje": Movement("Furia Salvaje", "FURROS", 90, 85),
    "Comision de arte": Movement("Instinto Animal", "FURROS", 75, 95),
    "Aullido": Movement("Aullido", "FURROS", 0, 100, "buff_ataque"),
    "Transformación": Movement("Transformación", "FURROS", 0, 100, "buff_velocidad"),
}

# Aplicamos herencia en esta parte y encapsulamiento
class STATS_BASE:
    def __init__(self, nombre, tipo, hp_max, ataque, defensa, velocidad, nivel = 50):
        self.nombre = nombre
        self.tipo = tipo
        self.hp_max = hp_max
        self.hp_actual = hp_max  # Inicializamos el HP actual al maximo
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.nivel = nivel
        self.movimientos = []
        self.mods = np.array([1.0, 1.0, 1.0])  # Modificadores: [ataque, defensa, velocidad]
        
    #Esta funcion sirve para identificar si hay un buff o un debuff
    def aplicar_efecto(self, movimiento):
            if movimiento.efecto == "buff_ataque":
                #Para que el buffeo no sea hacia el infinito, se aplicaran los metodos MAX y MIN. Los cuales limitan estos valores
                #Se hace primero la multiplicación
                self.mods[0] *= 1.2
                #Y luego se limita
                self.mods[0] = min(self.mods[0], 4.0)

            elif movimiento.efecto == "debuff_ataque":
                self.mods[0] *= 0.8
                self.mods[0] = max(self.mods[0], 0.25)

            elif movimiento.efecto == "buff_defensa":
                self.mods[1] *= 1.2
                self.mods[1] = min(self.mods[1], 4.0)

            elif movimiento.efecto == "debuff_defensa":
                self.mods[1] *= 0.8
                self.mods[1] = max(self.mods[1], 0.25)

            elif movimiento.efecto == "buff_velocidad":
                self.mods[2] *= 1.2
                self.mods[2] = min(self.mods[2], 4.0)

            elif movimiento.efecto == "debuff_velocidad":
                self.mods[2] *= 0.8
                self.mods[2] = max(self.mods[2], 0.25)
                
            return self.mods
        
    def calcular_daño(self, atacante, defensor, movimiento):
        #Atacante = El que ataca. Y el ataque es el tipo del personaje
        self.ataque = np.array(atacante.ataque * atacante.mods[0])  # Aplicar mod de ataque
        #Defensor = El que se defiende. Y la defensa es el tipo del personaje
        self.defensa = np.array(defensor.defensa * defensor.mods[1])  # Aplicar mod de defensa
        #Movimiento = El nombre del movimiento, su tipo y la potencia del mismo
        self.potencia = np.array(movimiento.potencia)

        self.efectividad = Table_Types.get_effectiveness(movimiento.tipo, defensor._tipo)
        #Esto es para no oneshotear a todos XD
        self.daño = (self.ataque / self.defensa) * self.potencia * self.efectividad

        return max(1, int(self.daño))
    
    def reset_mods(self):
        #Se resetean los valor por default para que no se queden con los buffos o debuffos anteriores
        self.mods = np.array([1.0, 1.0, 1.0])
        return self.mods
    
    # El hp actual se inicializa al maximo hp, ya que al crear un nuevo pokemon, este estara completamente sano
    def curar_totalmente(self):
        self.hp_actual = self.hp_max
        return self.hp_actual #devuelve la vida completa al crearse un nuevo pokemon o seguir de batalla
    
    # El metodo recibir_daño se encarga de reducir el hp actual del pokemon, y si el hp actual llega a 0, el pokemon se considera debilitado
    def recibir_daño(self, cantidad):
        self.hp_actual = max(0, self.hp_actual - cantidad)
        return self.hp_actual #devuelve la cantidad de daño hecho
        
#------ Clases de los pokemones, cada clase hereda de la clase STATS_BASE, y se le pueden agregar atributos y metodos especificos de cada pokemon, como por ejemplo, los movimientos que puede aprender, las habilidades que tiene etc.------
class Giovanni(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Excadrill base
        # Primero definimos los valores, luego llamamos a super().__init__()
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Giovanni",
            tipo = "FLOJO",
            hp_max = 110,
            ataque = 135,
            defensa = 60,
            velocidad = 88,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gio tendrá
        self._movimientos = [MOVIMIENTOS["Siesta Mortal"], MOVIMIENTOS["Bostezo"], MOVIMIENTOS["Furia Salvaje"], MOVIMIENTOS["Ajuste Preciso"]]
        #--------- Aqui se completa la clase
        
class David(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "David",
            tipo = "CHATGIPITY",
            hp_max = 160,
            ataque = 110,
            defensa = 65,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que David tendrá
        self._movimientos = [MOVIMIENTOS["Prompt Avanzado"], MOVIMIENTOS["Ram en aumento"], MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Deslumbrar"]]
        #--------- Aqui se completa la clase
        
class Erick(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Meowscarada base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Erick",
            tipo = "TICS",
            hp_max = 76,
            ataque = 110,
            defensa = 70,
            velocidad = 123,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Erick tendrá
        self._movimientos = [MOVIMIENTOS["Refactorizar"], MOVIMIENTOS["Git Push"], MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Mandato de Avalos"]]
        #--------- Aqui se completa la clase
        
class Rafa(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Slakoth base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Rafa",
            tipo = "FLOJO",
            hp_max = 60,
            ataque = 60,
            defensa = 60,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Rafa tendrá
        self._movimientos = [MOVIMIENTOS["Siesta Mortal"], MOVIMIENTOS["Bostezo"], MOVIMIENTOS["Furia Salvaje"], MOVIMIENTOS["Compilar"]]
        #--------- Aqui se completa la clase
        
class Joshua(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Typhlosion base
        super().__init__(
            nombre = "Joshua",
            tipo = "CHATGIPITY",
            hp_max = 78,
            ataque = 84,
            defensa = 78,
            velocidad = 100,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Didier tendrá
        self._movimientos = [MOVIMIENTOS["Prompt Avanzado"], MOVIMIENTOS["Ram en aumento"], MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Mirada Cute"]]
        #--------- Aqui se completa la clase
        
class Abraham(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Lapras base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Abraham",
            tipo = "INTELIGENTE",
            hp_max = 130,
            ataque = 85,
            defensa = 80,
            velocidad = 60,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Abraham tendrá
        self._movimientos = [MOVIMIENTOS["Cálculo Mental"], MOVIMIENTOS["Integral Doble"], MOVIMIENTOS["Furia Salvaje"], MOVIMIENTOS["Enjuague"]]
        #--------- Aqui se completa la clase
        
class Andrew(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Exeggutor base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Andrew",
            tipo = "DUCHA",
            hp_max = 95,
            ataque = 95,
            defensa = 85,
            velocidad = 55,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Alberto tendrá
        self._movimientos = [MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Baño"], MOVIMIENTOS["Es solo un amigo"], MOVIMIENTOS["Actitud"]]
        #--------- Aqui se completa la clase
        
class Generico_Diseño(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Delphox base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Generico Diseño",
            tipo = "FURROS",
            hp_max = 75,
            ataque = 69,
            defensa = 72,
            velocidad = 104,
            nivel = 50
        )
        # Ahora agregamos los movimientos que tendrá
        self._movimientos = [MOVIMIENTOS["Furia Salvaje"], MOVIMIENTOS["Comision de arte"], MOVIMIENTOS["Siesta Mortal"], MOVIMIENTOS["Formulario"]]
        #--------- Aqui se completa la clase
        
class Generico_Mercadofiesta(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Kilowattrel base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Generico Mercadofiesta",
            tipo = "MERCADOFIESTA",
            hp_max = 70,
            ataque = 70,
            defensa = 60,
            velocidad = 125,
            nivel = 50
        )
        # Ahora agregamos los movimientos que tendrá
        self._movimientos = [MOVIMIENTOS["Organizacion de Evento"], MOVIMIENTOS["Canva 2"], MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Rezo a San Cristian"]]
        #--------- Aqui se completa la clase
        
class Gato(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Lopunny base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Gato",
            tipo = "FURROS",
            hp_max = 65,
            ataque = 136,
            defensa = 94,
            velocidad = 123,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Gato tendrá
        self._movimientos = [MOVIMIENTOS["Furia Salvaje"], MOVIMIENTOS["Comision de arte"], MOVIMIENTOS["Siesta Mortal"], MOVIMIENTOS["Estrés"]]
        #--------- Aqui se completa la clase
        
class Osmar(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Lucario base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Osmar",
            tipo = "INTELIGENTE",
            hp_max = 70,
            ataque = 110,
            defensa = 70,
            velocidad = 90,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Cálculo Mental"], MOVIMIENTOS["Integral Doble"], MOVIMIENTOS["Furia Salvaje"], MOVIMIENTOS["Brillo Propio"]]
        #--------- Aqui se completa la clase
        
class Morro_Ardido(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Vivillon base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Morro Ardido",
            tipo = "JOCHIS",
            hp_max = 80,
            ataque = 52,
            defensa = 50,
            velocidad = 89,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Orgullo Total"], MOVIMIENTOS["Impacto Diva"], MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Aullido"]]
        #--------- Aqui se completa la clase

class Morra_Castrosa(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Gothitelle base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Morra Castrosa",
            tipo = "VIEJA",
            hp_max = 70,
            ataque = 55,
            defensa = 95,
            velocidad = 65,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Es solo un amigo"], MOVIMIENTOS["Ilusionista"], MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Descuento"]]
        #--------- Aqui se completa la clase
        
class El_Rector(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Snorlax base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "El Rector",
            tipo = "JORNADA_LABORAL",
            hp_max = 105,
            ataque = 150,
            defensa = 90,
            velocidad = 95,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Osmar tendrá
        self._movimientos = [MOVIMIENTOS["Horas Extra"], MOVIMIENTOS["Trabajo Duro"], MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Transformación"]]
        #--------- Aqui se completa la clase
        
class Chechi(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Torkoal base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Chechi",
            tipo = "TICS",
            hp_max = 70,
            ataque = 85,
            defensa = 140,
            velocidad = 20,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Chechi tendrá
        self._movimientos = [MOVIMIENTOS["Refactorizar"], MOVIMIENTOS["Git Push"], MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Ajuste Preciso"]]
        #--------- Aqui se completa la clase
        
class Fabian(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Aegislash base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Fabian",
            tipo = "MECOSTRONICOS",
            hp_max = 70,
            ataque = 140,
            defensa = 50,
            velocidad = 60,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Fabian tendrá
        self._movimientos = [MOVIMIENTOS["Engranaje Letal"], MOVIMIENTOS["SolidWorks"], MOVIMIENTOS["Es solo un amigo"], MOVIMIENTOS["Mandato de Avalos"]]
        #--------- Aqui se completa la clase

class Sigma(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Mega-Lucario base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Sigma",
            tipo = "MECOSTRONICOS",
            hp_max = 70,
            ataque = 165,
            defensa = 95,
            velocidad = 110,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Sigma tendrá
        self._movimientos = [MOVIMIENTOS["Engranaje Letal"], MOVIMIENTOS["SolidWorks"], MOVIMIENTOS["Es solo un amigo"], MOVIMIENTOS["Compilar"]]
        #--------- Aqui se completa la clase

class Diseño_Raro(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Cinderace base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Femboy de Diseño",
            tipo = "FEMBOY",
            hp_max = 80,
            ataque = 116,
            defensa = 75,
            velocidad = 119,
            nivel = 50
        )
        # Ahora agregamos los movimientos tendrá
        self._movimientos = [MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Aura Fashion"], MOVIMIENTOS["Orgullo Total"], MOVIMIENTOS["Error 404"]]
        #--------- Aqui se completa la clase
        
class Youtuber_Generico(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Eelektross base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Folagor",
            tipo = "FEMBOY",
            hp_max = 85,
            ataque = 115,
            defensa = 80,
            velocidad = 50,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Folagor tendrá
        self._movimientos = [MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Aura Fashion"], MOVIMIENTOS["Orgullo Total"], MOVIMIENTOS["Cansancio"]]
        #--------- Aqui se completa la clase

class JabonZote(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Rotom Lavado base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Jabon Zote",
            tipo = "DUCHA",
            hp_max = 70,
            ataque = 65,
            defensa = 130,
            velocidad = 86,
            nivel = 50
        )
        # Ahora agregamos los movimientos que Folagor tendrá
        self._movimientos = [MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Baño"], MOVIMIENTOS["Es solo un amigo"], MOVIMIENTOS["Generar Texto"]]
        #--------- Aqui se completa la clase
        
class Morro_Cachimba(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Quacaval (algo asi xd) base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "CachimbaBoy",
            tipo = "MERCADOFIESTA",
            hp_max = 85,
            ataque = 120,
            defensa = 80,
            velocidad = 85,
            nivel = 50
        )
        # Ahora agregamos los movimientos que CachimbaBoy tendrá
        self._movimientos = [MOVIMIENTOS["Organizacion de Evento"], MOVIMIENTOS["Canva 2"], MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Mirada Juzgadora"]]
        #--------- Aqui se completa la clase
        
class YOVOY(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Coalossal base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "YOVOY",
            tipo = "JOCHIS",
            hp_max = 110,
            ataque = 80,
            defensa = 120,
            velocidad = 30,
            nivel = 50
        )
        # Ahora agregamos los movimientos que YOVOY tendrá
        self._movimientos = [MOVIMIENTOS["Orgullo Total"], MOVIMIENTOS["Impacto Diva"], MOVIMIENTOS["Chorro a Presión"], MOVIMIENTOS["Controladora"]]
        #--------- Aqui se completa la clase
        
class GOTICA(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Grimmsnarl base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Gotica",
            tipo = "VIEJA",
            hp_max = 95,
            ataque = 120,
            defensa = 65,
            velocidad = 60,
            nivel = 50
        )
        # Ahora agregamos los movimientos que CachimbaBoy tendrá
        self._movimientos = [MOVIMIENTOS["Es solo un amigo"], MOVIMIENTOS["Ilusionista"], MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Little Ceasers"]]
        #--------- Aqui se completa la clase
        
class Almeida(STATS_BASE):
    def __init__(self):
        # Se tomaron referencia a stats de Yveltal base
        super().__init__( # Esta linea llama al constructor de la clase padre (STATS_BASE) para inicializar los atributos comunes a todos los pokemones, como el nombre, el tipo, el hp maximo, el ataque, la defensa, la velocidad y el nivel
            nombre = "Almeida",
            tipo = "JORNADA_LABORAL",
            hp_max = 126,
            ataque = 131,
            defensa = 95,
            velocidad = 100,
            nivel = 50
        )
        # Ahora agregamos los movimientos que CachimbaBoy tendrá
        self._movimientos = [MOVIMIENTOS["Horas Extra"], MOVIMIENTOS["Trabajo Duro"], MOVIMIENTOS["Encanto Brillante"], MOVIMIENTOS["Aullido"]]
        #--------- Aqui se completa la clase