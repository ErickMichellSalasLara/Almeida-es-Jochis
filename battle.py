#Este tercer archivo tendrá toda la logica de los ataques por turno y asi.
import random
from pokedata import STATS_BASE, Table_Types

class BattleManager:
    def __init__(self, equipo_jugador, equipo_enemigo):
        #Se crean 2 variables las cuales contendran al jugador y a la ia enemiga
        self.equipo_enemigo = equipo_enemigo
        self.equipo_jugador = equipo_jugador
        self.indice_activo = 0
        self.indice_activo_enemigo = 0
        self.pokemon_jugador = self.equipo_jugador[self.indice_activo]
        self.pokemon_enemigo = self.equipo_enemigo[self.indice_activo_enemigo]

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

    #------- METODO PRINCIPAL: lo llamas cada frame desde main.py
    
    #  Dependiendo del estado en el que te encuentres, hara cosas diferentes, tales como, hacer la batalla, aplicar efectos, etc.
    def actualizar(self, indice_movimiento_jugador = None, indice_cambio = None):
        #indice_movimiento_jugador → 0-3, el jugador eligió atacar
        #indice_cambio             → 0-5, el jugador eligió cambiar de pokémon
        if self.estado == "SELECCION_MOVIMIENTO":
            # El jugador quiere cambiar de pokémon voluntariamente
            if indice_cambio is not None:
                self.cambiar_pokemon(indice_cambio, ya_en_juego = True)
                # Cambiar gasta el turno: la IA igual ataca
                self.solo_ataca_enemigo()
                if self.verificar_fin_batalla():
                    self.estado = "BATALLA_TERMINADA"
                else:
                    self.turno += 1
                    self.estado = "SELECCION_MOVIMIENTO"

            # El jugador escoge un movimiento
            elif indice_movimiento_jugador is not None:
                self.registrar_elecciones(indice_movimiento_jugador)
                self.estado = "EJECUTAR_TURNO"

        elif self.estado == "EJECUTAR_TURNO":
            self.ejecutar_turno()

            # Revisamos si el pokemon del jugador se debilitó
            if self.verificar_fin_batalla():
                    self.estado = "BATALLA_TERMINADA"

        elif self.estado == "FORZAR_CAMBIO":
            # Esperamos en este estado hasta que main.py llame con indice_cambio
            if indice_cambio is not None:
                self.cambiar_pokemon(indice_cambio, ya_en_juego = False)
                # Después del cambio forzado NO ataca la IA, solo continuamos
                self.turno += 1
                self.movimiento_jugador = None
                self.movimiento_enemigo = None
                self.estado = "SELECCION_MOVIMIENTO"

        elif self.estado == "BATALLA_TERMINADA":
            pass

    def cambiar_pokemon(self, indice, ya_en_juego = True):
        #Cambia el pokémon activo del jugador por el del índice indicado
        if indice < 0 or indice >= len(self.equipo_jugador):
            return
        nuevo = self.equipo_jugador[indice]
        if nuevo.hp_actual <= 0:
            return  # No se puede cambiar a un pokémon debilitado
        if indice == self.indice_activo and ya_en_juego:
            return  # Ya está en el campo

        anterior = self.pokemon_jugador.nombre
        self.indice_activo = indice
        self.pokemon_jugador = self.equipo_jugador[self.indice_activo]

        if ya_en_juego:
            self.log = [f"¡{anterior} vuelve! ¡Adelante, {self.pokemon_jugador.nombre}!"]
        else:
            self.log = [f"¡{anterior} se debilitó!", f"¡Elige tu siguiente pokémon!",
                        f"¡Adelante, {self.pokemon_jugador.nombre}!"]
            
    def cambiar_pokemon_enemigo(self):
        # La IA busca el siguiente pokémon vivo en su equipo y lo manda al campo
        for i in range(len(self.equipo_enemigo)):
            if self.equipo_enemigo[i].hp_actual > 0:
                #se guarda aqui el nombre del pokemon al cual se debilito
                pokemon_debilitado = self.pokemon_enemigo.nombre
                #se iguala el indice de la lista de los pokemons de la ia
                self.indice_activo_enemigo = i
                #Se manda al primer pokemon vivo de la ia
                self.pokemon_enemigo = self.equipo_enemigo[self.indice_activo_enemigo]
                self.log.append(f"¡{pokemon_debilitado} se debilitó!")
                self.log.append(f"¡El rival envía a {self.pokemon_enemigo.nombre}!")
                return True
        # Si llegamos aquí, todos los pokémon del enemigo están debilitados
        return False
        
    def solo_ataca_enemigo(self):
        #Cuando el jugador cambia voluntariamente, la IA aprovecha para atacar
        self.movimiento_enemigo = random.choice(self.pokemon_enemigo.movimientos)
        self.aplicar_accion(
            atacante=self.pokemon_enemigo,
            defensor=self.pokemon_jugador,
            movimiento=self.movimiento_enemigo,
        )
        
    #-----------REGISTRAR ELECCIONES: el jugador elige, la IA tambien
    def registrar_elecciones(self, indice_movimiento_jugador):
        #Guarda el movimiento del jugador y genera el movimiento de la IA.
        #El indice va del 0 al 3 (4 movimientos por pokemon).
        movimientos_jugador = self.pokemon_jugador.movimientos
        movimientos_enemigo = self.pokemon_enemigo.movimientos

        #Validamos que el indice sea valido
        if 0 <= indice_movimiento_jugador < len(movimientos_jugador):
            self.movimiento_jugador = movimientos_jugador[indice_movimiento_jugador]
        else:
            #Si por alguna razon el indice no es valido, usamos el primero
            self.movimiento_jugador = movimientos_jugador[0]

        # La IA elige al azar un movimiento usando la libreria random
        self.movimiento_enemigo = random.choice(movimientos_enemigo)

    #------------------ EJECUTAR TURNO: aqui se aplica el daño y los efectos
    def ejecutar_turno(self):
        #Determina quien ataca primero segun la velocidad, luego aplica los movimientos en orden.
        self.log = []  # Limpiamos el log al inicio de cada turno
        self.log.append(f"--- Turno {self.turno} ---")

        #Determinamos quien va primero por velocidad
        vel_jugador = self.pokemon_jugador.velocidad * self.pokemon_jugador.mods[2]
        vel_enemigo = self.pokemon_enemigo.velocidad * self.pokemon_enemigo.mods[2]

        if vel_jugador >= vel_enemigo:
            #El jugador va primero
            self.aplicar_accion(
                atacante=self.pokemon_jugador,
                defensor=self.pokemon_enemigo,
                movimiento=self.movimiento_jugador,
            )
            #Solo ataca el enemigo si todavia esta vivo
            if self.pokemon_enemigo.hp_actual > 0:
                self.aplicar_accion(
                    atacante=self.pokemon_enemigo,
                    defensor=self.pokemon_jugador,
                    movimiento=self.movimiento_enemigo,
                )
        else:
            #El enemigo va primero
            self.aplicar_accion(
                atacante=self.pokemon_enemigo,
                defensor=self.pokemon_jugador,
                movimiento=self.movimiento_enemigo,
            )
            #Solo ataca el jugador si todavia esta vivo
            if self.pokemon_jugador.hp_actual > 0:
                self.aplicar_accion(
                    atacante=self.pokemon_jugador,
                    defensor=self.pokemon_enemigo,
                    movimiento=self.movimiento_jugador,
                )

    #----------- APLICAR ACCION: un pokemon usa su movimiento
    def aplicar_accion(self, atacante, defensor, movimiento):
        #Aplica un movimiento: puede ser de daño o de efecto (buff/debuff). Agrega mensajes al log para que main.py los muestre.
        nombre_atacante = atacante.nombre
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
                nombre_objetivo = defensor.nombre

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
            self.log.append(f"Hizo {daño} de daño a {defensor.nombre}!")

            #Mensaje de efectividad
            efectividad = Table_Types.get_effectiveness(movimiento.tipo, defensor.tipo)
            if efectividad == 4.0:
                self.log.append("Es ULTRA efectivo!")
            elif efectividad == 2.0:
                self.log.append("Es super efectivo!")
            elif efectividad <= 0.5:
                self.log.append("No es muy efectivo...")
            #Mensaje si el pokemon se debilita
            if defensor.hp_actual <= 0:
                self.log.append(f"{defensor.nombre} se debilito!")

    #-------- VERIFICAR FIN DE BATALLA
    def verificar_fin_batalla(self):
        # Si el pokemon del jugador muere
        if self.pokemon_jugador.hp_actual <= 0:
            vivos = self.get_equipo_vivo()

            if not vivos:
                # Ya no tienes pokémon, pues pierdes
                self.ganador = "ENEMIGO"
                self.log.append("¡No te quedan más pokémon! ¡Perdiste!")
                return True
            else:
                #Si aun hay pokes, pues se cambia al siguiente
                self.estado = "FORZAR_CAMBIO"
                return False

        # Ya si el equipo del enemigo no trae nada, ganas
        if self.pokemon_enemigo.hp_actual <= 0:
            self.ganador = "JUGADOR"
            self.log.append(f"¡Ganaste! {self.pokemon_jugador.nombre} ganó la batalla!")
            return True

        return False

    #---- METODOS DE CONSULTA: para que main.py pueda leer el estado
    def get_hp_jugador(self):
        #Retorna (hp_actual, hp_maximo) del pokemon del jugador
        return (self.pokemon_jugador.hp_actual, self.pokemon_jugador.hp_max)

    def get_hp_enemigo(self):
        #Retorna (hp_actual, hp_maximo) del pokemon enemigo
        return (self.pokemon_enemigo.hp_actual, self.pokemon_enemigo.hp_max)

    def get_movimientos_jugador(self):
        #Retorna la lista de movimientos del jugador (para mostrar los botones)
        return self.pokemon_jugador.movimientos

    def get_log(self):
        #Retorna los mensajes del ultimo turno
        return self.log

    def batalla_terminada(self):
        #Retorna True si la batalla ya termino
        return self.estado == "BATALLA_TERMINADA"
    
    def necesita_cambio_forzado(self):
        #Retorna True si el pokémon activo se debilitó y hay que elegir otro
        return self.estado == "FORZAR_CAMBIO"

    def get_equipo_vivo(self):
        #Se crea un array para meter a los pokes que sigan vivos
        indices_vivos = []
        #Se recorre cada poke del equipo del jugador para determinar cuales siguen vivos
        for i in range(len(self.equipo_jugador)):
            if self.equipo_jugador[i].hp_actual > 0:
                indices_vivos.append(i)
        return indices_vivos

    def get_equipo_jugador(self):
        #Retorna el equipo completo para mostrarlo en pantalla
        return self.equipo_jugador

    def get_indice_activo(self):
        return self.indice_activo