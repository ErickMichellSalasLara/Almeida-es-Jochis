# Archivo donde se hara el proyecto
import pygame, sys, numpy as np
from pokedata import Table_Types, Movement, STATS_BASE
from battle import BattleManager
from Trainers import ENTRENADORES, get_equipo_aleatorio, get_lista_pokemon_disponibles

SCREEN_WIDTH = 1280 #Ancho
SCREEN_HEIGHT = 720 # Largo
WHITE = (255, 255, 255) #Blanco
BLACK = (0,   0,   0) #Negro
GOLD = (141, 105, 34) #Oro
YELLOW = (212, 175, 55) #Amarillo
LIGHT_YELLOW = (255, 243, 129) #Amarillo Bajito
DARK = (30,  30,  30) #Grisaceo
RED = (180, 40,  40) #Rojo
GREEN = (40,  160, 40) #Verde
DARK_GREEN = (20, 60, 20) #Verde oscuro
DARK_BLUE = (20, 20, 50) #Azul Oscuro
CYAN = (118, 250, 242) #Cyan
PURPLE = (102, 0, 204) #Purple

pygame.display.set_caption("POKEUTR") #Titulo de la ventana del juego

def get_font(size): #Funcion para obtener la fuente del texto, la cual se usara en el menu y en el juego
    return pygame.font.Font("Fonts/TEXTO_MENU.ttf", size) # Se carga la fuente del texto, y se devuelve la fuente con el tamaño especificado

# Diccionario que mapea nombre de pokemon -> ruta de imagen. Solo los que tienen imagen disponible en Assets/PokeEstudiantes/
IMAGENES_POKEMON = {
    "Chechi":"Assets/PokeEstudiantes/Chechi_.jpg",
    "David":"Assets/PokeEstudiantes/David_.jpeg",
    "Erick":"Assets/PokeEstudiantes/Erick_.jpeg",
    "Fabian":"Assets/PokeEstudiantes/Fabian_.jpeg",
    "Gato":"Assets/PokeEstudiantes/Gato_.jpeg",
    "Sigma":"Assets/PokeEstudiantes/Sigma_.jpeg",
    "Generico Diseño":"Assets/PokeEstudiantes/Generico_diseño.jpg",
    "Abraham":"Assets/PokeEstudiantes/Abraham.png",
    "Almeida":"Assets/PokeEstudiantes/Almeida.png",
    "Andrew":"Assets/PokeEstudiantes/Andrew.jpeg",
    "El Rector":"Assets/PokeEstudiantes/ElRector.jpg",
    "Giovanni":"Assets/PokeEstudiantes/Giovanni.jpeg",
    "Gotica":"Assets/PokeEstudiantes/Gotica.jpeg",
    "Jabon Zote":"Assets/PokeEstudiantes/Jabon.jpg",
    "Joshua":"Assets/PokeEstudiantes/Joshua.jpeg",
    "Morra Castrosa":"Assets/PokeEstudiantes/Morra_Castrosa.jpeg",
    "Morro Ardido":"Assets/PokeEstudiantes/Morro_Ardido.png",
    "CachimbaBoy":"Assets/PokeEstudiantes/Morro_Cachimba.jpg",
    "Femboy de Diseño":"Assets/PokeEstudiantes/Morro_Diseño.jpeg",
    "Generico Mercadofiesta":"Assets/PokeEstudiantes/Morro_Mercadofiesta.png",
    "Osmar":"Assets/PokeEstudiantes/Osmar.jpeg",
    "Rafa":"Assets/PokeEstudiantes/Rafa.jpg",
    "Folagor":"Assets/PokeEstudiantes/Youtuber_Generico.png",
    "YOVOY":"Assets/PokeEstudiantes/YoVoy.jpg",
}

def get_sounds(): #Funcion para cargar los sonidos del juego, la cual se usara en el juego
    pass

#Esta clase nos sirve para los botones del menu, como el boton de jugar, el boton de opciones etc
#La clase la copie y pegue de un video tutorial que encontre en youtube XD
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
#Esta funcion ayuda a dibujar los textos de manera más sencilla
def draw_text(screen, text, font, color, x, y, center=True):
    surf = font.render(text, True, color)
    if center:
        rect = surf.get_rect(center=(x, y))
    else:
        rect = surf.get_rect(topleft=(x, y))
    return screen.blit(surf, rect)

#Esta funcion dibuja un panel
def draw_panel(screen, x, y, width, height, color = LIGHT_YELLOW, alpha=60, border=None):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.fill((*color, alpha))
    screen.blit(surf, (x, y))
    if border:
        pygame.draw.rect(screen, border, (x, y, width, height), 2, border_radius=8)

#Esta funcion sirve para hacer la barra de vida, estuve un rato pensando como hacerlo pero la neta no supe
#ya cuando chat lo hizo se me abrio el tercer ojo xdxd
def draw_hp_bar(screen, x, y, hp_actual, hp_max, width=300, height=20):
    if hp_max > 0:
        ratio = hp_actual / hp_max
    else:
        ratio = 0
    pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height), border_radius=5)
    
    if ratio > 0.5:
        color = GREEN
    elif ratio > 0.25:
        color = LIGHT_YELLOW
    else:
        color = RED
    barra_movible = int(width * ratio)
    if barra_movible > 0:
        pygame.draw.rect(screen, color, (x, y, barra_movible, height), border_radius=5)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=5)
    font_hp = get_font(22)
    texto_hp = font_hp.render(f"{hp_actual} / {hp_max}", True, WHITE)
    screen.blit(texto_hp, (x + width + 10, y))

class Game(object):
    def __init__(self): # Iniciamos la clase
        # Datos del Jugador
        self.state = "MENU" # Estado actual del juego: MENU o PLAY
        self.nombre_jugador = "" # Variable para guardar el nombre del jugador, la cual se usara para referirse a el durante el juego
        self.input_text = "" # Variable para guardar el texto que el jugador ingresa
        self.equipo_jugador = [] #Array donde estaran los pokemons del jugador
        self.pokemon_activo = None
        
        # Datos de la partida
        self.indice_entrenador_actual = 0 #Cuantos entrenadores llevas vencidos
        self.entrenadores = ENTRENADORES #Tomara las propiedades de los entrenadoes y los guarda en la variable entrenadores
        
        # Selección de pokemones manual
        self.todos_los_pokemon = get_lista_pokemon_disponibles() #Guarda todas las clases de Pokemons en la variable
        self.seleccionados_idx = [] #Pokemones seleccionados por el jugador
        self.pagina_seleccion = 0 #Se haran paginas para distribuir a los Pokes
        
        # Batalla
        self.batalla = None
        self.log_batalla = [] #Se imprimiran todos los eventos
        self.esperando_confirmacion = False #Variable donde determina si ya se escogio opcion o no
        self.cursor_movimiento = 0

        # Esto sirve para cargar la imagen una sola vez y no cargarlo de que 60 veces por segundo xd
        # Fondos
        self.background_menu = pygame.image.load("Assets/background_menu.jpg").convert()
        self.background_game_over = pygame.image.load("Assets/fondogameover.png").convert()
        self.background_play = pygame.image.load("Assets/campo_batalla.jpeg").convert()
        
        # Botones
        self.play_img = pygame.image.load("Assets/Play Rect.png")
        self.quit_img = pygame.image.load("Assets/Quit Rect.png")
        
        #Imagenes de Pokemones
    #Funcion para no hacer un monton de lineas de codigo que saque de chat XD
    def ImagenesPokemon(self, nombre, size=(200, 200)):
        ruta = IMAGENES_POKEMON.get(nombre)
        if ruta is None:
            print(f"No hay imagen para: {nombre}")
            return pygame.Surface(size)
        imagen = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(imagen, size)
        
    def MainMenu(self, screen):
        screen.blit(self.background_menu, (0, 0)) # Se carga la imagen de fondo del menu, y se dibuja en la pantalla
        menu_mouse_pos = pygame.mouse.get_pos()
    
        menu_text = get_font(100).render("POKE - UTR", True, GOLD)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH/2, 200)) # Menu rect es el rectangulo del menu, el cual se posiciona en el centro de la pantalla, a 100 pixeles de altura
    
        play_button = Button(image=self.play_img, pos=(SCREEN_WIDTH/2, 400), text_input="PLAY", font=get_font(75), base_color="#d8b265", hovering_color="White")
        quit_button = Button(image=self.quit_img, pos=(SCREEN_WIDTH/2, 550), text_input="QUIT", font=get_font(75), base_color="#d8b265", hovering_color="White")
    
        screen.blit(menu_text, menu_rect) # Se dibuja el texto del menu en la pantalla, usando el rectangulo del menu para posicionarlo
        for button in [play_button, quit_button]: # Se dibujan los botones del menu en la pantalla, usando el metodo update de la clase Button
            button.changeColor(menu_mouse_pos) # Si el mouse esta sobre el boton, se cambia el color del texto del boton, usando el metodo changeColor de la clase Button
            button.update(screen) # Se dibuja el boton en la pantalla, usando el metodo update de la clase Button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # Si se hace click con el mouse
                if play_button.checkForInput(menu_mouse_pos): # Si el mouse esta sobre el boton de play, vamos al estado de juego
                    self.state = "PEDIR_NOMBRE"
                if quit_button.checkForInput(menu_mouse_pos): # Si el mouse esta sobre el boton de quit, se cierra el juego
                    pygame.quit(); sys.exit()
        
        pygame.display.update() # Se actualiza la pantalla para que se dibujen los cambios realizados
    
    def PedirNombre(self, screen):
        screen.blit(self.background_menu, (0, 0))
        draw_panel(screen, 340, 180, 600, 340, border = YELLOW)

        draw_text(screen, "¿Cuál es tu nombre, entrenador?", get_font(50), GOLD, SCREEN_WIDTH//2, 255)
        draw_text(screen, "(Máximo 16 caracteres)", get_font(25), DARK, SCREEN_WIDTH//2, 295)

        # Caja de texto
        pygame.draw.rect(screen, WHITE,  (390, 330, 500, 60), border_radius=8)
        pygame.draw.rect(screen, YELLOW, (390, 330, 500, 60), 3, border_radius=8)
        Nombre_Player = get_font(38).render(self.input_text + "|", True, BLACK)
        screen.blit(Nombre_Player, Nombre_Player.get_rect(center=(640, 360)))

        draw_text(screen, "Presiona ENTER para continuar", get_font(30), DARK, SCREEN_WIDTH//2, 440)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.input_text) > 0:
                    self.nombre_jugador = self.input_text
                    self.input_text = ""
                    self.state = "ELEGIR_MODO"
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif len(self.input_text) < 16 and event.unicode.isprintable():
                    self.input_text += event.unicode

        pygame.display.update()
    #Elegir modo de juego
    def ElegirModo(self, screen):
        screen.blit(self.background_menu, (0, 0))
        mouse = pygame.mouse.get_pos()

        draw_panel(screen, 240, 130, 800, 450, border = YELLOW)
        draw_text(screen, f"¡Hola, {self.nombre_jugador}!", get_font(65), GOLD, SCREEN_WIDTH//2, 210)
        draw_text(screen, "¿Cómo quieres elegir tu equipo?", get_font(45), DARK, SCREEN_WIDTH//2, 275)
        draw_text(screen, "Llevarás 6 pokémon a la batalla", get_font(25), DARK, SCREEN_WIDTH//2, 315)

        button_aleatorio = Button(None, (SCREEN_WIDTH//2 - 190, 420), "  ALEATORIO  ", get_font(36), GOLD, WHITE)
        button_manual    = Button(None, (SCREEN_WIDTH//2 + 190, 420), "   ELEGIR   ", get_font(36), GOLD, WHITE)

        for button in [button_aleatorio, button_manual]: # Se dibujan los botones del menu en la pantalla, usando el metodo update de la clase Button
            button.changeColor(mouse) # Si el mouse esta sobre el boton, se cambia el color del texto del boton, usando el metodo changeColor de la clase Button
            button.update(screen) # Se dibuja el boton en la pantalla, usando el metodo update de la clase Button

        draw_text(screen, "La suerte decide", get_font(20), DARK, SCREEN_WIDTH//2 - 190, 470)
        draw_text(screen, "Tú eliges tus 6", get_font(20), DARK, SCREEN_WIDTH//2 + 190, 470)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_aleatorio.checkForInput(mouse):
                    self.equipo_jugador = get_equipo_aleatorio(6)
                    self.pokemon_activo = self.equipo_jugador[0]
                    self.state = "MAPA_ENTRENADORES"
                if button_manual.checkForInput(mouse):
                    self.seleccionados_idx = []
                    self.pagina_seleccion  = 0
                    self.state = "SELECCION_MANUAL"

        pygame.display.update()

    def SeleccionManual(self, screen):
        screen.blit(self.background_menu, (0, 0))
        mouse = pygame.mouse.get_pos()
        button_previous = None
        button_next = None
        button_ok = None
        
        #Tienes que escoger 6 PokeEstudiantes
        faltantes = 6 - len(self.seleccionados_idx) #Va checando en el array cuantos te falta por escoger
        if faltantes > 0:
            Faltantes_Text = (f"Elige {faltantes} pokémon más")
        else:
            Faltantes_Text = ("¡Equipo completo!")
        draw_text(screen, Faltantes_Text, get_font(38), BLACK, 480, 40)

        # Panel equipo seleccionado (derecha)
        draw_panel(screen, 950, 70, 310, 250, border = RED)
        draw_text(screen, "Tu equipo:", get_font(30), BLACK, 1105, 95)
        
        #Este For imprime los pokemons que hayas escogido en el cuadro
        i = 0
        for idx in self.seleccionados_idx:
            nombre = self.todos_los_pokemon[idx].nombre
                                                        # Esta parte es para ir bajando verticalmente el texto, en forma de lista
            draw_text(screen, f"• {nombre}", get_font(25), BLACK, 960, 122 + i * 32, center = False)
            i += 1
            
        #Aqui haremos la parte de las cartas (paginas) de cada apartado de los pokemones
        #3 columnas, 3 filas = 8 por página
        #Osease tendriamos 3 paginas con 8 pokemons en cada una
        columnas = 3
        card_weight, card_height = 250, 150
        start_x, start_y = 75, 80
        gap_x, gap_y = 15, 10
        por_pagina = 9
        #Para la primera pagina quedaria algo asi: (0 * 8 = 0), los primeros 8 pokemons en el array
        inicio = self.pagina_seleccion * por_pagina
        #Osease, en la primera pagina habrá 8 PokeEstudiantes a escoger
        fin = min(inicio + por_pagina, len(self.todos_los_pokemon))
        #Y aqui solamente se hace el calculo de cuantas paginas totales habrá, teniendo algo:
        # Total = ((24) Ya que hay 24 clases de pokes + 8 - 1) entre entero // 8 = 3. Y asi tendriamos las paginas totales
        total_paginas = (len(self.todos_los_pokemon) + por_pagina - 1) // por_pagina
        #Este for acomodara los pokes en cartas / paginas de 8 en 8 hasta completar las 3 paginas
        
        for poke_idx in range(inicio, fin):
            i = poke_idx - inicio
            #La variable "poke", almacenara el id de todos los pokes que vayan pasando por el for
            poke = self.todos_los_pokemon[poke_idx]
            #Esta parte convertira los numeros en grids. Osease, en columnas y filas
            #Teniendo algo como: i = 0, col = 0 % 4, row = 0 // 4
            #i = 1, col = 1 % 4, row = 1 // 4
            #i = 2, col = 2 % 4, row = 1 // 4. Y asi sucesivamente
            #De manera visual deberia quedar algo como: Fila 0: [0][1][2][3]
            #                                           Fila 0: [4][5][6][7]
            col = i % columnas
            row = i // columnas

            #Esta parte es de las coordenadas, osease donde ira cada poke que estamos acomodando
            #Quedando algo asi:
            #i = 0 → col = 0, row = 0
            #x = 20 + 0 * (220 + 12) = 20
            #y = 80 + 0 * (95 + 10) = 80
            x = start_x + col * (card_weight + gap_x)
            y = start_y + row * (card_height + gap_y)

            ya_selected = poke_idx in self.seleccionados_idx
            if ya_selected:
                color_borde = GREEN
                color_fondo = DARK_GREEN
            else:
                color_borde = YELLOW
                color_fondo = DARK_BLUE

            draw_panel(screen, x, y, card_weight, card_height, color=color_fondo, border=color_borde)

            draw_text(screen, poke.nombre, get_font(30), WHITE, x + card_weight//2, y + 30)
            draw_text(screen, f"Tipo: {poke.tipo}", get_font(25), DARK, x + card_weight//2, y + 79)
            draw_text(screen, f"HP:{poke.hp_max}  ATK:{poke.ataque}  VEL:{poke.velocidad}", get_font(25), DARK, x + card_weight//2, y + 101)

            rect = pygame.Rect(x, y, card_weight, card_height)
            #Si el mouse pasa por encima, se vuelve de color blanco el borde
            if rect.collidepoint(mouse):
                pygame.draw.rect(screen, GREEN, rect, 2, border_radius=8)

        #Pagina en la que estas
        #Si estas en la pagina 1, aparece el boton "anterior"
        if self.pagina_seleccion > 0:
            button_previous = Button(None, (SCREEN_WIDTH//2 - 150, 625), "< ANTERIOR", get_font(28), WHITE, LIGHT_YELLOW)
            button_previous.changeColor(mouse) # Si el mouse esta sobre el boton, se cambia el color del texto del boton, usando el metodo changeColor de la clase Button
            button_previous.update(screen) # Se dibuja el boton en la pantalla, usando el metodo update de la clase Button

        #Si estas en la pagina 1 o 2, aparece el boton "siguiente"
        if self.pagina_seleccion < total_paginas - 1:
            button_next = Button(None, (SCREEN_WIDTH//2 + 150, 625), "SIGUIENTE >", get_font(28), WHITE, LIGHT_YELLOW)
            button_next.changeColor(mouse) # Si el mouse esta sobre el boton, se cambia el color del texto del boton, usando el metodo changeColor de la clase Button
            button_next.update(screen) # Se dibuja el boton en la pantalla, usando el metodo update de la clase Button

        draw_text(screen, f"Página {self.pagina_seleccion+1}/{total_paginas}", get_font(20), WHITE, SCREEN_WIDTH//2, 590)

        #Botón confirmar
        if len(self.seleccionados_idx) == 6:
            button_ok = Button(None, (1105, 580), "¡LISTO!", get_font(36), GREEN, WHITE)
            button_ok.changeColor(mouse) # Si el mouse esta sobre el boton, se cambia el color del texto del boton, usando el metodo changeColor de la clase Button
            button_ok.update(screen) # Se dibuja el boton en la pantalla, usando el metodo update de la clase Button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                #Click en carta del poke
                for poke_idx in range(inicio, fin):
                    #La variable "i" nos sirve para ir ubicando cada parte de los pokes en las cartas
                    i = poke_idx - inicio
                    #Y aqui por ejemplo, al tener columnas = 4, "i" se repetira cada 4 columnas ubicadas
                    col = i % columnas
                    #y al tener aqui al hacer division entera, cada 4 sube de fila, bueno, en este caso baja, ya que positivo es hacia abajo
                    row = i // columnas
                    x = start_x + col * (card_weight + gap_x)
                    y = start_y + row * (card_height + gap_y)
                    #Detectamos si el puntero del mouse esta encima del rectangulo
                    if pygame.Rect(x, y, card_weight, card_height).collidepoint(mouse):
                        #Si ya esta seleccionado la carta del pokemon, se remueve de la carta
                        if poke_idx in self.seleccionados_idx:
                            self.seleccionados_idx.remove(poke_idx)
                        #Si no esta seleccionado, y a parte faltan pokes en el equipo, se agrega
                        elif len(self.seleccionados_idx) < 6:
                            self.seleccionados_idx.append(poke_idx)

                # Paginación para detectar ahora si el click del mouse
                if self.pagina_seleccion > 0:
                    if button_previous and button_previous.checkForInput(mouse):
                        self.pagina_seleccion -= 1 #Va pa atras
                if self.pagina_seleccion < total_paginas - 1:
                    if button_next and button_next.checkForInput(mouse):
                        self.pagina_seleccion += 1 #Va pa delante

                #Boton para confirmar y seguir avanzando
                #Si ya escogiste los 6 pokes, se muestra el boton LISTO!
                if len(self.seleccionados_idx) == 6:
                    #Este if detecta si es que el mouse hizo Click con el botón
                    if button_ok and button_ok.checkForInput(mouse):
                        #Se manda a llamar la variablde del Equipo del Jugador y se le asigna los pokes seleccionados
                        self.equipo_jugador = []
                        for i in self.seleccionados_idx:
                            #Aqui se accede al objeto / clase de pokedata.py y lo busca por su idx (i)
                            clase_poke = type(self.todos_los_pokemon[i])
                            #Una vez encontrado, toma sus caracteristicas y los agrega al equipo del jugador
                            #Tomado ya las caracteristicas, se crea una instancia nueva con estos parentesis
                            #Se podria decir que "Por cada Pokémon seleccionado, crea uno nuevo desde su clase"
                            nuevo_poke = clase_poke()
                            self.equipo_jugador.append(nuevo_poke)
                        self.pokemon_activo = self.equipo_jugador[0]
                        self.state = "MAPA_ENTRENADORES"

        pygame.display.update()

    def MapaEntrenadores(self, screen):
        screen.blit(self.background_play, (0, 0))
        mouse = pygame.mouse.get_pos()
        button_fight = None

        draw_panel(screen, 80, 30, 1120, 660, border = DARK_GREEN)
        draw_text(screen, f"Ruta del Entrenador {self.nombre_jugador}", get_font(50), WHITE, SCREEN_WIDTH//2, 70)
        draw_text(screen, "Derrota a los 5 entrenadores para ganar", get_font(26), DARK, SCREEN_WIDTH//2, 108)

        #Este for recorre todos los entrenadores
        for i in range(len(self.entrenadores)):
            #Accedemos al entrenador actual usando su índice
            #Los entrenadores se nos proporcionan desde Trainers.py
            entrenador = self.entrenadores[i]
            #Posición vertical de cada tarjeta (se separan hacia abajo)
            y_card = 145 + i * 108
            #Creamos una variable para wachar si ya fue derrotado o no el entrenador zzz
            completado = entrenador.derrotado
            #Esta linea te notifica mediante un booleano si el entrenador que sigue, pues sigue o no xd
            #Todo esto por medio de "i". Nota: Solo hay 5 entrenadores, asi que "i" solamente llegara hasta 4
            sigo_o_no = (i == self.indice_entrenador_actual)

            #Colores dependiendo del estado del entrenador
            if completado:
                color_fondo = CYAN
                color_borde = GREEN
            elif sigo_o_no:
                color_fondo = LIGHT_YELLOW
                color_borde = YELLOW
            else:
                color_fondo = DARK_BLUE
                color_borde = DARK

            #Dibujamos la tarjeta del entrenador
            draw_panel(screen, 110, y_card, 1060, 85, color = color_fondo, border = color_borde)

            #Texto del estado
            if completado:
                estado_txt = "DERROTADO :D"
                color_estado = GREEN
            elif sigo_o_no:
                estado_txt = "SIGUIENTE >>>"
                color_estado = LIGHT_YELLOW
            else:
                estado_txt = "NO E, ESPERATE!"
                color_estado = DARK

            #Nombre del entrenador (con número)
            draw_text(screen, f"{i+1}. {entrenador.nombre}", get_font(28), WHITE, 120, y_card + 22, center=False)

            #Estado (derrotado, siguiente o bloqueado)
            draw_text(screen, estado_txt, get_font(28), color_estado, 930, y_card + 33, center=False)

            #Descripción corta (solo la primera línea)
            #Esta linea usa el metodo spli para tomar solo la primera linea de la descripcion
            #Es como, dar una "vista previa" de la descripción
            desc_corta = entrenador.descripcion.split("\n")[0]
            draw_text(screen, desc_corta, get_font(18), DARK, 120, y_card + 55, center=False)

            #Se crea un boton pa pelear si es que todavia no se ha completado el entrenador
            if sigo_o_no and not completado: #Esto regresa un True si es que esta desbloqueado
                button_fight = Button(None, (1120, y_card + 45), "PELEAR", get_font(28), GOLD, WHITE)
                button_fight.changeColor(mouse)
                button_fight.update(screen)
        #Creamos una variable verdadera para checar si todos fueron derrotados
        todos_derrotados = True
        #Se revisa este for el cual dice: "Por cada entrenador en la lista de entrenadores"
        #Osease, va a checar toda la lista pa ver si ya ganaste, y si todavia no, pues a seguirle xdxd
        for entrenador in self.entrenadores:
            if not entrenador.derrotado:
                todos_derrotados = False
                break
        #Si derrotaste a todos, mis respetos ksks
        if todos_derrotados:
            draw_panel(screen, 250, 620, 780, 60, color = DARK, border = YELLOW)
            draw_text(screen, "FELICIDADES:¡ERES EL CAMPEÓN DE LA UTR!", get_font(36), GOLD, SCREEN_WIDTH//2, 650)
            
        #Este for es como los de arriba, solo que este checa si ya derrotaste a los entrenadores
        #Y de no ser asi, pues crea un boton en el siguiente pa empezar la batalla puchamon
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.indice_entrenador_actual < len(self.entrenadores):
                    entrenador_actual = self.entrenadores[self.indice_entrenador_actual]
                    if not entrenador_actual.derrotado:
                        if button_fight and button_fight.checkForInput(mouse):
                            self.state = "DIALOGO_RIVAL"

        pygame.display.update()
        
    def DialogoRival(self, screen):
        screen.blit(self.background_play, (0, 0))
        mouse = pygame.mouse.get_pos()
        #Esta variable se igualara al entrenador al que te vayas a enfrentar usando el indice del for en MapaEntrenadores()
        entrenador = self.entrenadores[self.indice_entrenador_actual]

        draw_panel(screen, 80, 80, 1120, 560, border = YELLOW)
        draw_text(screen, f"¡{entrenador.nombre} quiere pelear!", get_font(50), BLACK, SCREEN_WIDTH//2, 160)
        #Lineas es la varible string que guardara lo pedazos que se recorten de la descripcion de cada entrenador y se dibujara
        #una debajo de la otra con el for.
        lineas = entrenador.descripcion.split("\n")
        for i in range(len(lineas)):
            linea = lineas[i]
            draw_text(screen, linea, get_font(30), WHITE, SCREEN_WIDTH//2, 235 + i * 40)

        # Frase del rival con el nombre del jugador que se inserto al principio
        # Nota: Esto solo se cumple si en la parte de "Trainers.py" se puso un valor para "nombre_jugador"
        frase = entrenador.frase_inicio.format(nombre=self.nombre_jugador)
        draw_panel(screen, 130, 370, 1020, 80, color = GREEN, border = PURPLE)
        draw_text(screen, f'"{frase}"', get_font(30), WHITE, SCREEN_WIDTH//2, 410)

        # Tu equipo vs su equipo
        draw_text(screen, "Tu equipo:", get_font(26), GREEN, 140, 480)
        #Se crea una variable string vacia
        nombres_equipo_jugador = ""
        #Se recorrera cada nombre del equipo y se añadira a la variable creada anteriormente
        for jugador in self.equipo_jugador:
            #Aqui, como es la primera vuelta, se agregara el primer nombre
            if nombres_equipo_jugador == "":
                nombres_equipo_jugador = jugador.nombre
            #Como ya tendra algo aqui, pues se añadira ahora el siguiente pero con un espacio
            else:
                nombres_equipo_jugador += ", " + jugador.nombre
        #Y se dibujan en la pantalla
        draw_text(screen, nombres_equipo_jugador, get_font(24), WHITE, 140, 505, center=False)

        draw_text(screen, "Su equipo:", get_font(26), RED, 140, 545)

        # Lo mismo pero con el equipo rival
        nombres_rival = ""
        for clase in entrenador.pokemon_clases:
            nombre = clase().nombre  # creamos instancia para obtener nombre

            if nombres_rival == "":
                nombres_rival = nombre
            else:
                nombres_rival += ", " + nombre

        draw_text(screen, nombres_rival, get_font(24), WHITE, 140, 570, center=False)

        button_fight_time = Button(None, (SCREEN_WIDTH//2, 680), "¡A PELEAR!", get_font(36), GOLD, WHITE)
        button_fight_time.changeColor(mouse)
        button_fight_time.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_fight_time and button_fight_time.checkForInput(mouse):
                        self.state = "INICIAR_BATALLA"

        pygame.display.update()
    
    def IniciarBatalla(self, screen):
        entrenador = self.entrenadores[self.indice_entrenador_actual]
        # Curamos al equipo del jugador entre batallas
        for equipo in self.equipo_jugador:
            equipo.curar_totalmente()
            equipo.reset_mods()
        equipo_rival = entrenador.get_equipo()
        for poke in equipo_rival:
            poke.curar_totalmente()
            poke.reset_mods()
        # Ahora se pasa la lista de todos los pokemons de los equipos
        self.batalla = BattleManager(self.equipo_jugador, equipo_rival)
        self.log_batalla = []
        self.cursor_movimiento = 0
        #Este booleano es para determinar si el Jugador ya escogio opcion de ataque
        self.esperando_confirmacion = False
        #Este booleano sirve para cambiar de pokemon si es que el Jugador asi lo desea
        #True cuando el jugador presiona C
        self.menu_cambio_abierto = False
        #Cursor del menú de cambio
        self.cursor_cambio = 0
        self.state = "BATALLA"
        
    def Batalla(self, screen):
        screen.blit(self.background_play, (0, 0))
        entrenador = self.entrenadores[self.indice_entrenador_actual]
        #Creamos 2 variables para los pokes que se pelearan. Y se les iguala al primer pokemon
        #de cada "jugador", usando la variabke "batalla" que es igualada a la clase con los
        #respectivos parametros
        pokemon_jugador = self.batalla.pokemon_jugador
        pokemon_enemigo = self.batalla.pokemon_enemigo
        #Hacemos algo similara a arriba pero esta vez para conseguir la vida de cada uno y manejarla
        #en tiempo real
        hp_actual_jugador, hp_maximo_jugador = self.batalla.get_hp_jugador() #Recibe Hp actual y Maximo
        hp_actual_enemigo, hp_maximo_enemigo = self.batalla.get_hp_enemigo()
        movimientos = self.batalla.get_movimientos_jugador() #Da la lista de movimientos del poke
        
        #Parte pa que se dibuje lo del enemigo
        imagen_enemigo = self.ImagenesPokemon(pokemon_enemigo.nombre, (160, 160))
        #Imagen (arriba derecha)
        screen.blit(imagen_enemigo, (900, 120))
        
        #Panel enemigo (a la izquierda de la imagen)
        draw_panel(screen, 120, 80, 320, 110, border = DARK_BLUE)
        draw_text(screen, pokemon_enemigo.nombre, get_font(30), WHITE, 280, 105)
        draw_text(screen, f"Tipo: {pokemon_enemigo.tipo}", get_font(24), DARK, 280, 135)
        draw_hp_bar(screen, 160, 160, hp_actual_enemigo, hp_maximo_enemigo, width = 200)
        
        #Parte para que se dibuje lo del jugador
        imagen_jugador = self.ImagenesPokemon(pokemon_jugador.nombre, (200, 200))
        #Imagen (abajo izquierda)
        screen.blit(imagen_jugador, (120, 360))
        #Panel jugador (a la derecha de la imagen)
        draw_panel(screen, 700, 380, 320, 110, border = DARK_BLUE)
        draw_text(screen, pokemon_jugador.nombre, get_font(30), WHITE, 860, 405)
        draw_text(screen, f"Tipo: {pokemon_jugador.tipo}", get_font(24), DARK, 860, 435)
        draw_hp_bar(screen, 740, 460, hp_actual_jugador, hp_maximo_jugador, width = 200)
        
        #Eventos de la batalla (log) abajo a la derecha
        draw_panel(screen, 50, 520, 1200, 200, border = DARK)
        draw_text(screen, "Registro de batalla:", get_font(30), WHITE, 425, 540)
        #Lista con todos los mensajes de la batalla, las cuales solo se tomaran los ultimos 5 registros
        #Osease los más actualizados:
        #Tomo los últimos 5 eventos del combate y los dibujo en pantalla uno debajo del otro usando un desplazamiento vertical basado en el índice.
        lineas_visibles = self.log_batalla[-5:]
        for i in range(len(lineas_visibles)):
            linea = lineas_visibles[i]
            draw_text(screen, linea, get_font(22), WHITE, 100, 570 + i * 28, center = False)

        #Panel movimientos o menú de cambio (abajo derecha)
        draw_panel(screen, 800, 520, 450, 200, border = DARK_GREEN)
        
        #Esta parte determina si tu pokemon fue abatido o cambiaste de pokemon
        if self.batalla.necesita_cambio_forzado() or self.menu_cambio_abierto:
            #Cambiara de color y de texto dependiendo de lo que se ocupe
            if self.batalla.necesita_cambio_forzado():
                titulo_cambio = "¡ELIGE TU SIGUIENTE POKÉ - ESTUDIANTE!"
                color_id = RED
            else:
                titulo_cambio = "Cambiar Poké - Estudiante:"
                color_id = CYAN
            draw_text(screen, titulo_cambio, get_font(30), color_id , 1020, 540)
            if not self.batalla.necesita_cambio_forzado():
                draw_text(screen, "ESC para cancelar", get_font(15), DARK, 830, 700, center=False)
        
        if self.menu_cambio_abierto:
            # Menú de los Pokes
            for idx in range(len(self.equipo_jugador)):
                poke = self.equipo_jugador[idx]
                #Usaremos un grid para acomodar al equipo, en donde usaremos 2 columnas y 2 filas
                columna = idx // 3
                fila = idx % 3
                
                x = 820 + columna * 180 #Separamos de manera horizontal
                y = 518 + fila * 44 #Y aqui de manera vertical
                
                draw_text(screen, f"[{idx + 1}] {poke.nombre}", get_font(22), CYAN, x, y + 50, center=False)
                draw_text(screen, f"{poke.tipo}", get_font(20), DARK, x, y + 70, center=False)
                
        elif self.batalla.necesita_cambio_forzado():
            # Menú de los Pokes
            for idx in range(len(self.equipo_jugador)):
                poke = self.equipo_jugador[idx]
                #Usaremos un grid para acomodar al equipo, en donde usaremos 2 columnas y 2 filas
                columna = idx // 3
                fila = idx % 3
                
                x = 820 + columna * 180 #Separamos de manera horizontal
                y = 518 + fila * 44 #Y aqui de manera vertical
                
                draw_text(screen, f"[{idx + 1}] {poke.nombre}", get_font(22), RED, x, y + 50, center=False)
                draw_text(screen, f"{poke.tipo}", get_font(20), DARK, x, y + 70, center=False)

        else:
            # Menú de los movimientos
            draw_text(screen, "Movimientos:", get_font(25), WHITE, 1020, 535)
            i = 0
            for idx in range(len(movimientos)):
                mov = movimientos[idx]
                y_mov = 518 + i * 44
                if i == self.cursor_movimiento:
                    color_mov = GOLD
                else:
                    color_mov = WHITE
                    
                if mov.potencia > 0:
                    potencia_txt = f"POT:{mov.potencia}"
                else:
                    potencia_txt = "Efecto"
                    
                i += 1
                draw_text(screen, f"[{i}] {mov.nombre}", get_font(22), color_mov, 820, y_mov + 30, center=False)
                draw_text(screen, f"{potencia_txt}, de Potencia!", get_font(20), DARK, 820, y_mov + 50, center=False)
                draw_text(screen, f" {mov.precision}% de Presición!", get_font(20), DARK, 1070, y_mov + 50, center=False)

        #Instrucciones de la UI
        if self.batalla.batalla_terminada():
            pass
        elif self.batalla.necesita_cambio_forzado():
            draw_text(screen, "↑↓ Mover  |  ENTER para enviar", get_font(20), RED, SCREEN_WIDTH//2, 708)
        elif self.menu_cambio_abierto:
            draw_text(screen, "↑↓ Mover  |  ENTER para cambiar  |  ESC cancelar", get_font(18), DARK_BLUE, SCREEN_WIDTH//2, 708)
        elif self.esperando_confirmacion:
            draw_text(screen, "Presiona ENTER para continuar...", get_font(22), YELLOW, SCREEN_WIDTH//2, 708)
        else:
            draw_text(screen, "↑↓ Mover  |  ENTER/1-4 atacar  |  'C' cambiar pokémon", get_font(20), DARK_BLUE, 500, 708)
        #Este if esta aqui abajo por lo mismo de que tiene al final del pygame.display.update(), que es el responsable
        #de recargar todos los dibujos que se pongan en la pantalla, si lo saco se dibujara todo de que 60 veces por segundo!
        #Y no queremos eso xd. Asi que se quedara en esta logica
        if self.batalla.batalla_terminada():
            draw_panel(screen, 280, 240, 720, 180, DARK, alpha=230, border = GOLD)
            if self.batalla.ganador == "JUGADOR":
                ganador_text = f"¡{self.nombre_jugador} ganó!"
                color_id = GREEN
            else:
                ganador_text = f"¡Perdiste contra {entrenador.nombre}!"
                color_id = RED
            draw_text(screen, ganador_text, get_font(58), color_id, SCREEN_WIDTH//2, 310)
            draw_text(screen, "ENTER para continuar", get_font(30), YELLOW, SCREEN_WIDTH//2, 385)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_batalla_input(event.key)
                

        pygame.display.update()
        
    #Esta funcion estara cargada de todos los inputs que vayamos a usar. Va a ser grande x'd
    def handle_batalla_input(self, key):
        indice_activo = self.batalla.get_indice_activo()
        vivos = self.batalla.get_equipo_vivo()
        
        #Primero procesaremos si es que la batalla ya termino
        if self.batalla.batalla_terminada():
            if key == pygame.K_ESCAPE:
                self.procesar_resultado_batalla()
            return
                    
        #Creamos ahora los inputs para los cambios de pokes
        if self.menu_cambio_abierto:
            pokes_equipo = []
            i = 0
            for i in vivos:
                if i != indice_activo: #Si el poke es diferente del que esta peleando
                    pokes_equipo.append(i)
                i += 1
            
            #If si valida si aun tienes pokes vivos en el equipo
            if not pokes_equipo:
                return
                
            #Si el cursor anda en un poke no vivo xd
            if self.cursor_cambio not in pokes_equipo:
                #mueve el cursor al primero de los vivos
                self.cursor_cambio = pokes_equipo[0]
                
            if key == pygame.K_ESCAPE:
                self.menu_cambio_abierto = False
                self.cursor_cambio = indice_activo
            #Si el boton presionado se encuentra entre la tecla 1 y 6
            elif pygame.K_1 <= key <= pygame.K_6:
                #el indice igualara el num "correcto para un indice", osease entre 0 y 5
                indice = key - pygame.K_1
                if indice in pokes_equipo:
                    #el cursor igualara el num del indice donde se encuentre el poke
                    self.cursor_cambio = indice
                    #y se mandara al campo
                    self.confirmar_cambio(ya_en_juego = False)
                    
            elif key == pygame.K_RETURN:
                if self.cursor_cambio in pokes_equipo:
                    self.confirmar_cambio(ya_en_juego = False)
            return
        
        #Creamos ahora los inputs para los cambios de pokes cuando es obligatorio
        if self.batalla.necesita_cambio_forzado():
            pokes_equipo = []
            for i in vivos:
                if i != indice_activo: #Si el poke es diferente del que esta peleando
                    pokes_equipo.append(i)
            #If si valida si aun tienes pokes vivos en el equipo
            if not pokes_equipo:
                return
                
            #Si el cursor anda en un poke no vivo xd
            if self.cursor_cambio not in pokes_equipo:
                #mueve el cursor al primero de los vivos
                self.cursor_cambio = pokes_equipo[0]
                
            #Si el boton presionado se encuentra entre la tecla 1 y 6
            if pygame.K_1 <= key <= pygame.K_6:
                #el indice igualara el num "correcto para un indice", osease entre 0 y 5
                indice = key - pygame.K_1
                if indice in pokes_equipo:
                    #el cursor igualara el num del indice donde se encuentre el poke
                    self.cursor_cambio = indice
                    #y se mandara al campo
                    self.confirmar_cambio(ya_en_juego = True)
                    
            elif key == pygame.K_RETURN:
                if self.cursor_cambio in pokes_equipo:
                    self.confirmar_cambio(ya_en_juego = True)
            return
            
        #Ahora hacemos la confirmacion de la espera
        if self.esperando_confirmacion:
            if key == pygame.K_RETURN:
                self.esperando_confirmacion = False
                
                self.cursor_movimiento = 0
                self.menu_cambio_abierto = False
                
                nuevos_mensajes = self.batalla.get_log()
                for mensaje in nuevos_mensajes:
                    self.log_batalla.append(mensaje)
            return
        
        #AHORA SI, hacemos la logica para seleccionar el movimiento del pokemon.
        if self.batalla.estado == "SELECCION_MOVIMIENTO":
            #Esta variable almacenara los datos de los movimientos del poke del jugador
            movimientos = self.batalla.get_movimientos_jugador()
            #Si por alguna razon no hay movimientos
            if not movimientos:
                return #Pues se regresa
            
            #Aqui hacemos lo de arriba, un como "circulo" donde no pueda seleccionar un movimiento inexistente
            if key == pygame.K_UP:
                self.cursor_movimiento = (self.cursor_movimiento - 1) % len(movimientos)
            elif key == pygame.K_DOWN:
                self.cursor_movimiento = (self.cursor_movimiento + 1) % len(movimientos)
                #Tecla para cambiar de poke
            elif key == pygame.K_c:
                #abrimos el menu de cambio de poke
                pokes_equipo = []
                #Revisamos cada poke en el equipo que aun siga con vida
                for i in vivos:
                    if i != indice_activo:
                        pokes_equipo.append(i)

                if pokes_equipo:
                    self.menu_cambio_abierto = True
                    self.cursor_cambio = pokes_equipo[0]
                    
            elif key == pygame.K_1:
                #Usamos el primer movimiento
                self.usar_movimiento(0)
            elif key == pygame.K_2:
                #Usamos el segundo movimiento
                self.usar_movimiento(1)
            elif key == pygame.K_3:
                #Usamos el tercer movimiento
                self.usar_movimiento(2)
            elif key == pygame.K_4:
                #Usamos el cuarto movimiento
                self.usar_movimiento(3)
            elif key == pygame.K_RETURN:
                self.usar_movimiento(self.cursor_movimiento)

    #Ya por ultimo creamos una funcion nueva donde ahora si se impriman los resultados y asi completar el loop del main y el juego en si
    def resultado(self, screen):
        mouse = pygame.mouse.get_pos()
        #Creamos una varible para determinar si el jugador Gano o no
        gano_jugador = self.batalla and self.batalla.ganador == "JUGADOR"
        button_continuar = None
        button_menu = None
        
        #si el jugador gano, dibujara un fondo diferente en cada situacion con su repectivo panel
        if gano_jugador:
            screen.blit(self.background_play, (0,0))
            #Si ganamos, el indicie del entrenador se restara 1 faltando asi los qu falten
            indice_entrenador = self.indice_entrenador_actual - 1
        else:
            screen.blit(self.background_game_over, (0,0))
            #Si perdemos, no se resta nada y se deja igual por que, pues no ganamos xd
            indice_entrenador = self.indice_entrenador_actual
            
        draw_panel(screen, 180, 130, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, border = YELLOW)
        #Guardamos dentro de una nueva variable el indice nuevo de los entrenadores faltantes
        entrenador = self.entrenadores[indice_entrenador]
        #Si ganamos, se dibuja el texto encima del panel que ganamos y la linea de derrota del entrenador
        if gano_jugador:
            draw_text(screen, "¡VICTORIA!", get_font(70), GREEN, SCREEN_WIDTH//2, 230)
            frase_derrota = entrenador.frase_derrota.format(nombre = self.nombre_jugador)
            draw_text(screen, f'"{frase_derrota}"', get_font(26), GOLD, SCREEN_WIDTH//2, 330)
            #Si aun faltan entrenadores por pelear, pues dibuja quien sera el siguiente
            if self.indice_entrenador_actual < len(self.entrenadores):
                siguiente = self.entrenadores[self.indice_entrenador_actual]
                draw_text(screen, f"Siguiente rival: {siguiente.nombre}", get_font(28), WHITE, SCREEN_WIDTH//2, 410)
            #Si ya no hay entrenadores restantes, osea que ganaste. Se dibuja que ganaste pues
            else:
                draw_text(screen, "¡¡¡ERES EL CAMPEÓN DE LA UTR!!!", get_font(34), YELLOW, SCREEN_WIDTH//2, 410)
        #Ya si perdiste pues, se dibuja el hecho de que perdiste
        else:
            draw_text(screen, "¡DERROTA!", get_font(70), RED, SCREEN_WIDTH//2, 230)
            draw_text(screen, f"Perdiste contra {entrenador.nombre}", get_font(28), WHITE, SCREEN_WIDTH//2, 330)
            draw_text(screen, "Puedes intentarlo de nuevo", get_font(24), DARK, SCREEN_WIDTH//2, 380)

        #Ahora le preguntamos al jugador que quiere hacer, si seguir jugando o no.
        button_continuar = Button(None, (SCREEN_WIDTH//2, 510), "CONTINUAR", get_font(36), YELLOW, WHITE)
        button_continuar.changeColor(mouse)
        button_continuar.update(screen)
        button_menu = Button(None, (SCREEN_WIDTH//2, 565), "VOLVER AL MENÚ", get_font(28), DARK, WHITE)
        button_menu.changeColor(mouse)
        button_menu.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_continuar.checkForInput(mouse):
                    self.state = "MAPA_ENTRENADORES"
                if button_menu.checkForInput(mouse):
                    self.reset_juego()
                    self.state = "MENU"
                    
    #Haremos una funcion para reiniciar el juego y asi hacer un loop infinito
    def reset_juego(self):
        self.nombre_jugador = "" # Variable para guardar el nombre del jugador, la cual se usara para referirse a el durante el juego
        self.input_text = "" # Variable para guardar el texto que el jugador ingresa
        self.equipo_jugador = [] #Array donde estaran los pokemons del jugador
        self.pokemon_activo = None
        self.indice_entrenador_actual = 0 #Cuantos entrenadores llevas vencidos
        self.seleccionados_idx = []
        self.batalla = None
        self.log_batalla = [] #Se imprimiran todos los eventos
        for maestros in self.entrenadores:
            maestros.derrotado = False

                
    #Esta funcion hara la confirmacion del cambio de Poké, sea intencional o obligatoriamente
    def confirmar_cambio(self, ya_en_juego):
        #Aqui se hace el cambio
        self.batalla.actualizar(indice_cambio = self.cursor_cambio)
        #Este for agregara los mensajes del log uno en uno
        nuevos_mensajes = self.batalla.get_log()
        for mensaje in nuevos_mensajes:
            self.log_batalla.append(mensaje)
        #Cerramos el menu de cambio
        self.menu_cambio_abierto = False
        #Reinicamos el cursor
        self.cursor_movimiento = 0
        if not ya_en_juego:
            self.cursor_movimiento = 0
            self.esperando_confirmacion = True

    def procesar_resultado_batalla(self):
        entrenador_actual = self.entrenadores[self.indice_entrenador_actual]
        if self.batalla.ganador == "JUGADOR":
            entrenador_actual.derrotado = True
            self.indice_entrenador_actual += 1
        self.state = "RESULTADO"
        
    #Creamos la funcion pa usar los movimientos
    def usar_movimiento(self, indice):
        #Aqui haremos que el turno como tal se complete
        #Primero tendriamos que checar que el jugador haya usado un movimiento y si fue asi cual fue
        self.batalla.actualizar(indice_movimiento_jugador = indice)
        #Ahora si depues de confirmar que rollo, hacemos el turno
        if self.batalla.estado == "EJECUTAR_TURNO":
            self.batalla.actualizar()
            #Se crea una variable tipo string que obtendra los registros
            nuevos_mensajes = self.batalla.get_log()
            for mensaje in nuevos_mensajes:
                self.log_batalla.append(mensaje)
        #Aqui ya se manda la confirmacion
        self.esperando_confirmacion = True
        
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("POKEUTR") # Se establece el titulo de la ventana
    clock = pygame.time.Clock() # Se crea un reloj para controlar los frames por segundo del juego

    game = Game() # Se crea una instancia de la clase Game, para poder acceder a sus metodos y atributos
    
    while True:
        if game.state == "MENU":
            game.MainMenu(screen)
            
        if game.state == "PEDIR_NOMBRE":
            game.PedirNombre(screen)
            
        if game.state == "ELEGIR_MODO":
            game.ElegirModo(screen)
            
        if game.state == "SELECCION_MANUAL":
            game.SeleccionManual(screen)
            
        if game.state == "MAPA_ENTRENADORES":
            game.MapaEntrenadores(screen)
            
        if game.state == "DIALOGO_RIVAL":
            game.DialogoRival(screen)

        if game.state == "BATALLA":
            game.Batalla(screen)
            
        if game.state == "INICIAR_BATALLA":
            game.IniciarBatalla(screen)
            
        if game.state == "RESULTADO":
            game.resultado(screen)
            
        clock.tick(60) # Se establece el limite de frames por segundo del juego a 60
    pygame.quit() # Se cierra el juego
    
    
# El if servira solamente para ejecutar la funcion main, y no ejecutar el codigo si se importa este archivo como un modulo
if __name__ == "__main__":
    main()