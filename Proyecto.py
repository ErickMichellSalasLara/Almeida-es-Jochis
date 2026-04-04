# Archivo donde se hara el proyecto
import pygame, random, sys

SCREEN_WIDTH = 1280 #Ancho
SCREEN_HEIGHT = 720 #Largo
WHITE = (255, 255, 255) #Blanco
BLACK = (0, 0, 0) #Negro

pygame.display.set_caption("POKEUTR") #Titulo de la ventana del juego

def get_font(size): #Funcion para obtener la fuente del texto, la cual se usara en el menu y en el juego
    return pygame.font.Font("Fonts/TEXTO_MENU.ttf", size) # Se carga la fuente del texto, y se devuelve la fuente con el tamaño especificado

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

class Pokemon:
    def __init__(self, nombre, tipo, vida, ataques):
        self.nombre = nombre
        self.tipo = tipo
        self.vida = vida
        self.ataques = ataques
    pass

class Game(object):
    def __init__(self): # Iniciamos la clase
        self.game_over = False # Variable para saber si el juego se ha terminado o no
        self.score = 0 # Variable para llevar la puntuacion del jugador
        self.all_sprite_list = pygame.sprite.Group() # Creamos una lista de sprites, la cual se usara para dibujar todos los sprites en la pantalla, usando el metodo draw de la clase Group de Pygame
        
        # Esto sirve para cargar la imagen una sola vez y no cargarlo de que 60 veces por segundo xd
        self.background_menu = pygame.image.load("Assets/background_menu.jpg").convert()
        self.play_img = pygame.image.load("Assets/Play Rect.png")
        self.quit_img = pygame.image.load("Assets/Quit Rect.png")
        self.background_game_over = pygame.image.load("Assets/fondogameover.png").convert()
        
    def display_frame(self, screen):
        screen.fill(WHITE)
        
        if self.game_over:
            screen.blit(self.background_game_over, (0, 0))
            font = pygame.font.SysFont("Fonts/TEXTO_MENU.ttf", 25)
            text = font.render("Game Over!.", True, "#7c2626")
            text2 = font.render("Press enter to play again. Score: " + str(self.score), True, "#be6236")
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, (center_x, center_y))
            screen.blit(text2, (center_x, center_y + 30))
        if not self.game_over:
            self.all_sprite_list.draw(screen) # Dibujamos todos los sprites en la pantalla, usando el metodo draw de la clase Group de Pygame
        pygame.display.flip() # Actualizamos la pantalla para que se dibujen los cambios realizados


    #Esta funcion será toda mi logica del juego.
    def play(self):
        # Aqui se hara el codigo del juego, como la logica del juego, el movimiento de los personajes, las colisiones etc
        while not self.game_over:
            
        
            pass
    def MainMenu(self, screen):
        screen.blit(self.background_menu, (0, 0)) # Se carga la imagen de fondo del menu, y se dibuja en la pantalla
        menu_mouse_pos = pygame.mouse.get_pos()
    
        menu_text = get_font(100).render("POKE - UTR", True, "#8d6922")
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
                if play_button.checkForInput(menu_mouse_pos): # Si el mouse esta sobre el boton de play, se llama a la funcion main, la cual es la funcion principal del juego
                    main()
                if quit_button.checkForInput(menu_mouse_pos): # Si el mouse esta sobre el boton de quit, se cierra el juego
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update() # Se actualiza la pantalla para que se dibujen los cambios realizados
        pass

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("POKEUTR") # Se establece el titulo de la ventana
    
    done = False
    clock = pygame.time.Clock() # Se crea un reloj para controlar los frames por segundo del juego

    game = Game() # Se crea una instancia de la clase Game, para poder acceder a sus metodos y atributos
    
    while not done:
        game.MainMenu(screen) # Se llama a la funcion MainMenu de la clase Game, para mostrar el menu del juego
        clock.tick(60) # Se establece el limite de frames por segundo del juego a 60
    pygame.quit() # Se cierra el juego
    
    
# El if servira solamente para ejecutar la funcion main, y no ejecutar el codigo si se importa este archivo como un modulo
if __name__ == "__main__":
    main()