#Este tercer archivo tendrá toda la logica de los ataques por turno y asi.
import random
from pokedata import STATS_BASE, Table_Types

class BattleManager:
    def __init__(self, pokemon_jugador, pokemon_enemigo):
        #Se crean 2 variables las cuales contendran al jugador y a la ia enemiga
        self.pokemon_jugador = pokemon_jugador
        self.pokemon_enemigo = pokemon_enemigo

        #Esta parte determina que estamos dentro del apartado "Seleccion de movimiento"
        self.estado = "SELECCION_MOVIMIENTO"  # Siempre empieza aqui
        self.turno = 1                         # Contador de turnos
        self.ganador = None                    # Quien gano al final (None = nadie aun)

        #Aqui se almacenara que movimiento fue el que escogio el jugador
        self.movimiento_jugador = None
        #Aqui se almacenara que movimiento fue el que escogio el Enemigo
        self.movimiento_enemigo = None

        #Log de mensajes para mostrar en pantalla
        #Cada entrada es un string con lo que paso en el turno
        #Por ejemplo: "Giovanni uso Siesta Mortal! Hizo 45 de daño!"
        self.log = []

        #Nos aseguramos de que ambos pokemon empiecen con vida completa
        self.pokemon_jugador.curar_totalmente()
        self.pokemon_enemigo.curar_totalmente()

    #------- METODO PRINCIPAL: lo llamas cada frame desde main.py
    #  Dependiendo del estado en el que te encuentres, hara cosas diferentes, tales como, hacer la batalla, aplicar efectos, etc.
    def actualizar(self, indice_movimiento_jugador=None):
        #Si el estado en el que se encuentra es "Seleccion de movimiento" Esperara hasta que escojas algo
        if self.estado == "SELECCION_MOVIMIENTO":
            # Si el jugador ya eligio un movimiento, avanzamos
            if indice_movimiento_jugador is not None:
                self._registrar_elecciones(indice_movimiento_jugador)
                self.estado = "EJECUTAR_TURNO"
        #Si el jugador ya escogio algo, entrara en la funcion "ejecutar_turno()"
        elif self.estado == "EJECUTAR_TURNO":
            self._ejecutar_turno()

            #Despues de ejecutar el turno, revisamos si alguien perdio
            if self._verificar_fin_batalla():
                self.estado = "BATALLA_TERMINADA"
            else:
                #Si no termino, volvemos a pedir movimiento al jugador
                self.turno += 1
                self.movimiento_jugador = None
                self.movimiento_enemigo = None
                self.estado = "SELECCION_MOVIMIENTO"

        elif self.estado == "BATALLA_TERMINADA":
            # Ya no hacemos nada, main.py se encarga de mostrar el resultado
            pass

    #-----------REGISTRAR ELECCIONES: el jugador elige, la IA tambien
    def _registrar_elecciones(self, indice_movimiento_jugador):
        #Guarda el movimiento del jugador y genera el movimiento de la IA.
        #El indice va del 0 al 3 (4 movimientos por pokemon).
        movimientos_jugador = self.pokemon_jugador._movimientos
        movimientos_enemigo = self.pokemon_enemigo._movimientos

        #Validamos que el indice sea valido
        if 0 <= indice_movimiento_jugador < len(movimientos_jugador):
            self.movimiento_jugador = movimientos_jugador[indice_movimiento_jugador]
        else:
            #Si por alguna razon el indice no es valido, usamos el primero
            self.movimiento_jugador = movimientos_jugador[0]

        # La IA elige al azar un movimiento usando la libreria random
        self.movimiento_enemigo = random.choice(movimientos_enemigo)

    #------------------ EJECUTAR TURNO: aqui se aplica el daño y los efectos
    def _ejecutar_turno(self):
        #Determina quien ataca primero segun la velocidad, luego aplica los movimientos en orden.
        self.log = []  # Limpiamos el log al inicio de cada turno
        self.log.append(f"--- Turno {self.turno} ---")

        # --- Determinamos quien va primero por velocidad ---
        vel_jugador = self.pokemon_jugador.velocidad * self.pokemon_jugador.mods[2]
        vel_enemigo = self.pokemon_enemigo.velocidad * self.pokemon_enemigo.mods[2]

        if vel_jugador >= vel_enemigo:
            #El jugador va primero
            self._aplicar_accion(
                atacante=self.pokemon_jugador,
                defensor=self.pokemon_enemigo,
                movimiento=self.movimiento_jugador,
            )
            #Solo ataca el enemigo si todavia esta vivo
            if self.pokemon_enemigo._hp_actual > 0:
                self._aplicar_accion(
                    atacante=self.pokemon_enemigo,
                    defensor=self.pokemon_jugador,
                    movimiento=self.movimiento_enemigo,
                )
        else:
            #El enemigo va primero
            self._aplicar_accion(
                atacante=self.pokemon_enemigo,
                defensor=self.pokemon_jugador,
                movimiento=self.movimiento_enemigo,
            )
            #Solo ataca el jugador si todavia esta vivo
            if self.pokemon_jugador._hp_actual > 0:
                self._aplicar_accion(
                    atacante=self.pokemon_jugador,
                    defensor=self.pokemon_enemigo,
                    movimiento=self.movimiento_jugador,
                )

    #----------- APLICAR ACCION: un pokemon usa su movimiento
    def _aplicar_accion(self, atacante, defensor, movimiento):
        #Aplica un movimiento: puede ser de daño o de efecto (buff/debuff). Agrega mensajes al log para que main.py los muestre.
        nombre_atacante = atacante._nombre
        nombre_movimiento = movimiento.nombre

        #Verificamos si el movimiento acierta
        if not movimiento.acertar():
            self.log.append(f"{nombre_atacante} uso {nombre_movimiento}... Pero fallo!")
            return  #El movimiento falla, no pasa nada mas

        #Movimiento de efecto (buff o debuff, potencia = 0)
        if movimiento.potencia == 0 and movimiento.efecto is not None:
            # Determinamos a quien afecta el efecto. Los buffs se aplican al atacante, los debuffs al defensor
            if "buff" in movimiento.efecto:
                objetivo = atacante
                nombre_objetivo = nombre_atacante
            else:
                objetivo = defensor
                nombre_objetivo = defensor._nombre

            objetivo.aplicar_efecto(movimiento)

            # Mensajes descriptivos segun el tipo de efecto
            if movimiento.efecto == "buff_ataque":
                self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
                self.log.append(f"El ataque de {nombre_objetivo} subio!")
            elif movimiento.efecto == "debuff_ataque":
                self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
                self.log.append(f"El ataque de {nombre_objetivo} bajo!")
            elif movimiento.efecto == "buff_defensa":
                self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
                self.log.append(f"La defensa de {nombre_objetivo} subio!")
            elif movimiento.efecto == "debuff_defensa":
                self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
                self.log.append(f"La defensa de {nombre_objetivo} bajo!")
            elif movimiento.efecto == "buff_velocidad":
                self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
                self.log.append(f"La velocidad de {nombre_objetivo} subio!")
            elif movimiento.efecto == "debuff_velocidad":
                self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
                self.log.append(f"La velocidad de {nombre_objetivo} bajo!")

        #Movimiento de daño (potencia > 0)
        else:
            #Usamos el calcular_daño que ya tienes en STATS_BASE
            daño = atacante.calcular_daño(atacante, defensor, movimiento)
            defensor.recibir_daño(daño)

            self.log.append(f"{nombre_atacante} uso {nombre_movimiento}!")
            self.log.append(f"Hizo {daño} de daño a {defensor._nombre}!")

            #Mensaje de efectividad
            efectividad = Table_Types.get_effectiveness(movimiento.tipo, defensor._tipo)
            if efectividad >= 2.0:
                self.log.append("Es super efectivo!")
            elif efectividad == 4.0:
                self.log.append("Es ULTRA efectivo!")
            elif efectividad <= 0.5:
                self.log.append("No es muy efectivo...")

            #Mensaje si el pokemon se debilita
            if defensor._hp_actual <= 0:
                self.log.append(f"{defensor._nombre} se debilito!")

    #-------- VERIFICAR FIN DE BATALLA
    def _verificar_fin_batalla(self):
        #Revisa si alguno de los dos pokemon llego a 0 de HP. Si es asi, guarda el ganador y retorna True.
        if self.pokemon_jugador._hp_actual <= 0:
            self.ganador = "ENEMIGO"
            self.log.append(f"Perdiste! {self.pokemon_enemigo._nombre} gano la batalla!")
            return True
        if self.pokemon_enemigo._hp_actual <= 0:
            self.ganador = "JUGADOR"
            self.log.append(f"Ganaste! {self.pokemon_jugador._nombre} gano la batalla!")
            return True
        return False

    #---- METODOS DE CONSULTA: para que main.py pueda leer el estado
    def get_hp_jugador(self):
        #Retorna (hp_actual, hp_maximo) del pokemon del jugador
        return (self.pokemon_jugador._hp_actual, self.pokemon_jugador._hp_max)

    def get_hp_enemigo(self):
        #Retorna (hp_actual, hp_maximo) del pokemon enemigo
        return (self.pokemon_enemigo._hp_actual, self.pokemon_enemigo._hp_max)

    def get_movimientos_jugador(self):
        #Retorna la lista de movimientos del jugador (para mostrar los botones)
        return self.pokemon_jugador._movimientos

    def get_log(self):
        #Retorna los mensajes del ultimo turno
        return self.log

    def batalla_terminada(self):
        #Retorna True si la batalla ya termino
        return self.estado == "BATALLA_TERMINADA"