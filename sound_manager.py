import pygame

class Sound_Manager:
    def __init__(self):
        pygame.mixer.init()
        
        self.SONIDOS = {
            #Sonidos generales
            "fallo": pygame.mixer.Sound("Assets/Sonidos/HUH.mp3"),
            "bonk": pygame.mixer.Sound("Assets/Sonidos/Bonk.mp3"),
            "celebracion": pygame.mixer.Sound("Assets/Sonidos/YEEEEII.mp3"),
            "NoEffective": pygame.mixer.Sound("Assets/Sonidos/NoEffective.mp3"),
            "x2Effective": pygame.mixer.Sound("Assets/Sonidos/x2Effective.mp3"),
            "x4SuperEffective": pygame.mixer.Sound("Assets/Sonidos/x4SuperEffective.mp3"),
            "Cambio": pygame.mixer.Sound("Assets/Sonidos/Cambio.mp3"),
            
            #Cambios de stats
            "buff": pygame.mixer.Sound("Assets/Sonidos/SubidaStats.mp3"),
            "debuff": pygame.mixer.Sound("Assets/Sonidos/BajadaStats.mp3"),
            #Sonidos para movimientos especificos
            "Git Push": pygame.mixer.Sound("Assets/Sonidos/fart-with-reverb.mp3"),
            "Aura Fashion": pygame.mixer.Sound("Assets/Sonidos/Awkard.mp3"),
            "Descuento": pygame.mixer.Sound("Assets/Sonidos/Camera Shutter.mp3"),
            "Bostezo": pygame.mixer.Sound("Assets/Sonidos/Bostezo.mp3"),
            "Impacto Diva": pygame.mixer.Sound("Assets/Sonidos/don-onepiece.mp3"),
            "Transformación": pygame.mixer.Sound("Assets/Sonidos/katon.mp3"),
            "Mirada Juzgadora": pygame.mixer.Sound("Assets/Sonidos/latigazo.mp3"),
            "Desgano": pygame.mixer.Sound("Assets/Sonidos/Raul.mp3"),
            "Mirada Cute": pygame.mixer.Sound("Assets/Sonidos/rizz-sounds.mp3"),
            "Horas Extra": pygame.mixer.Sound("Assets/Sonidos/Sukuna.mp3"),
            "SolidWorks": pygame.mixer.Sound("Assets/Sonidos/tuco-get-out.mp3"),
        }

        self.MUSICA = {
            "main": "Assets/Sonidos/Main_Theme.mp3",
            "victoria": "Assets/Sonidos/Theme_Victory.mp3",
            "derrota": "Assets/Sonidos/BobEsponjaSad.mp3"
        }
    #Hacemos una funcion para mandar a llamar los sonidos con solo esto.
    def play(self, nombre):
        if nombre in self.SONIDOS:
            pygame.mixer.music.set_volume(0.1)
            self.SONIDOS[nombre].play()
            pygame.mixer.music.set_volume(0.2)
            
    def play_musica(self, nombre):
        if nombre in self.MUSICA:
            pygame.mixer.music.load(self.MUSICA[nombre])
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
            
    #Funcion para llamar los sonidos por movimiento especifico
    def play_movimiento(self, movimiento):
        if movimiento.nombre in self.SONIDOS:
            self.SONIDOS[movimiento.nombre].play()
        elif movimiento.efecto:
            if "buff" in movimiento.efecto:
                self.SONIDOS["buff"].play()
            elif "debuff" in movimiento.efecto:
                self.SONIDOS["debuff"].play()
            else:
                self.SONIDOS["bonk"].play()
        else:
            self.SONIDOS["bonk"].play()