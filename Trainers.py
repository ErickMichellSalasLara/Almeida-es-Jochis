import random
from pokedata import (
    Giovanni, David, Erick, Rafa, Didier, Abraham, Alberto,
    Morro_Generico_Diseño, Morro_Generico_Mercadofiesta, Gato,
    Osmar, Morro_Ardido_Generico, Morra_Castrosa,
    El_Rector_Que_No_Es_El_Rector, Chechi, Fabian, Sigma,
    Diseño_Raro, Youtuber_Generico, JabonZote,
    Morro_Cachimba, YOVOY, GOTICA, Almeida
)

#-------- POOL DE TODOS LOS POKEMON DISPONIBLES PARA EL JUGADOR
All_Pokemons = [
    Giovanni, David, Erick, Rafa, Didier, Abraham, Alberto,
    Morro_Generico_Diseño, Morro_Generico_Mercadofiesta, Gato,
    Osmar, Morro_Ardido_Generico, Morra_Castrosa, Chechi,
    Fabian, Sigma, Diseño_Raro, Youtuber_Generico,
    JabonZote, Morro_Cachimba, YOVOY, GOTICA
]

#---------- CLASE ENTRENADOR: representa a un rival con su equipo
class Entrenador:
    def __init__(self, nombre, descripcion, pokemon_clases, frase_inicio, frase_derrota):
        self.nombre = nombre
        self.descripcion = descripcion          # Texto que aparece antes de pelear
        self.pokemon_clases = pokemon_clases    # Lista de clases (no instancias)
        self.frase_inicio = frase_inicio
        self.frase_derrota = frase_derrota
        self.derrotado = False

    #Esta funcion funciona de tal manera que, en self.pokemon_clases, vas a guardar los pokes que se consigan
    #con la "clase()", que es basicamente llamar al constructor de cada Pokemon. Esto crea a los pokes desde 0 con hp full
    def get_equipo(self):
        #Genera instancias frescas del equipo (con HP completo)
        return [clase() for clase in self.pokemon_clases]

    def get_pokemon_actual(self):
        #Para batallas simples (1v1), devuelve solo el primer pokemon
        return self.pokemon_clases[0]()

#--------------- LOS 5 ENTRENADORES EN ORDEN DE DIFICULTAD
ENTRENADORES = [
    #Cada elemento de la lista es un objeto de tipo Entrenador. Entonces básicamente es una lista de 5 entrenadores
    Entrenador(
        nombre="Max - Android's Version",
        descripcion="Un profe que preferiría estar durmiendo.\nSus pokemon son tan flojos como él.",
        pokemon_clases=[Rafa, Giovanni, GOTICA],
        frase_inicio="El morado es malo para las paginas Jovenes. No lo usen!",
        frase_derrota="NOOO!!!. USARAS MORADO AAAAHHH!!"
    ),

    Entrenador(
        nombre="Doña Chole",
        descripcion="Aguas con doña chole.",
        pokemon_clases=[Morra_Castrosa, YOVOY, Diseño_Raro],
        frase_inicio="Ay, ¿en serio me vas a retar? Qué gracioso...",
        frase_derrota="YA NO HAY SERVICIO PARA TI!"
    ),

    Entrenador(
        nombre="Brandon - El GitMan",
        descripcion="Compilará tus esperanzas y las mandará al error 404.\nTiene experiencia depurando rivales.",
        pokemon_clases=[David, Abraham, Alberto, Didier],
        frase_inicio="¡Vamos a ver si tu código sobrevive mis pruebas!",
        frase_derrota="Mmm... encontraste el bug en mi estrategia. Bien jugado."
    ),

    Entrenador(
        nombre="Justes - 'Hola hermano!'",
        descripcion="Aquel que piensa que el mundo gira alrededor de el.\nAcuerdate de la bitacora!",
        pokemon_clases=[Rafa, Morro_Generico_Mercadofiesta, El_Rector_Que_No_Es_El_Rector, Gato, Morro_Ardido_Generico],
        frase_inicio="Acabare esto rapido. Los cigarros no se acaban solos!",
        frase_derrota="Jolines tio, no lo veia venir."
    ),

    Entrenador(
        nombre="Almeida — El Jefe Final",
        descripcion="El entrenador más poderoso de la UTR.\nDice que no es el rector pero claramente lo es.\nEquipo completo. Sin piedad.",
        pokemon_clases=[Almeida, El_Rector_Que_No_Es_El_Rector, Osmar, Sigma, Chechi, JabonZote],
        frase_inicio="Joven {nombre}. Que dijimos de usar Ia?",
        frase_derrota="Vaya, al parecer entendiste tu codigo a la perfección. Felicidades Joven {nombre}"
    ),
]

#----------- FUNCION: obtener pokemon aleatorios para el jugador
def get_equipo_aleatorio(cantidad=6):
    # Devuelve 'cantidad' clases de pokemon al azar del pool del jugador
    seleccionados = random.sample(All_Pokemons, cantidad)
    return [clase() for clase in seleccionados]

#---------- FUNCION: obtener todos los pokemon disponibles con nombre (para mostrar en el menú de selección manual)
def get_lista_pokemon_disponibles():
    #Devuelve instancias de todos los pokemon disponibles para el jugador
    return [clase() for clase in All_Pokemons]