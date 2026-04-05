# Archivo donde se hara el proyecto
import pygame, sys, random
from pokedata import Table_Types, Movement, STATS_BASE
from battle import BattleManager
from Trainers import ENTRENADORES, get_equipo_aleatorio, get_lista_pokemon_disponibles

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
YELLOW = (212, 175, 55)
GRAY   = (160, 160, 160)
DARK   = (30,  30,  30)
RED    = (180, 40,  40)
GREEN  = (40,  160, 40)
MOSTAZA = (220, 180, 0)

pygame.display.set_caption("POKEUTR")

def get_font(size):
    return pygame.font.Font("Fonts/TEXTO_MENU.ttf", size)

# Diccionario que mapea nombre de pokemon -> ruta de imagen
# Solo los que tienen imagen disponible en Assets/PokeEstudiantes/
IMAGENES_POKEMON = {
    "Chechi":  "Assets/PokeEstudiantes/Chechi_.jpeg",
    "David":   "Assets/PokeEstudiantes/David_.jpeg",
    "Erick":   "Assets/PokeEstudiantes/Erick_.jpeg",
    "Fabian":  "Assets/PokeEstudiantes/Fabian_.jpeg",
    "Gato":    "Assets/PokeEstudiantes/Gato_.jpeg",
    "Sigma":   "Assets/PokeEstudiantes/Sigma_.jpeg",
    "Morro Generico Diseño":      "Assets/PokeEstudiantes/Morro_Generico.jpeg",
    "Morro Generico Mercadofiesta": "Assets/PokeEstudiantes/Morro_Generico.jpeg",
}

# ──────────────────────────────────────────────
#  CLASE BUTTON (igual que la tuya original)
# ──────────────────────────────────────────────
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
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and \
           position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# ──────────────────────────────────────────────
#  HELPERS DE DIBUJO
# ──────────────────────────────────────────────
def draw_text(screen, text, font, color, x, y, center=True):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)

def draw_hp_bar(screen, x, y, hp_actual, hp_max, width=300, height=20):
    ratio = hp_actual / hp_max if hp_max > 0 else 0
    pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height), border_radius=5)
    if ratio > 0.5:
        color = GREEN
    elif ratio > 0.25:
        color = MOSTAZA
    else:
        color = RED
    barra_ancho = int(width * ratio)
    if barra_ancho > 0:
        pygame.draw.rect(screen, color, (x, y, barra_ancho, height), border_radius=5)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=5)
    font_hp = get_font(18)
    texto_hp = font_hp.render(f"{hp_actual} / {hp_max}", True, WHITE)
    screen.blit(texto_hp, (x + width + 10, y))

def draw_panel(screen, x, y, width, height, color=(20, 20, 40), alpha=200, border=None):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.fill((*color, alpha))
    screen.blit(surf, (x, y))
    if border:
        pygame.draw.rect(screen, border, (x, y, width, height), 2, border_radius=8)

def cargar_imagen_pokemon(nombre, size=(200, 200)):
    """Carga la imagen de un pokemon si existe, sino devuelve None"""
    ruta = IMAGENES_POKEMON.get(nombre)
    if ruta:
        try:
            img = pygame.image.load(ruta).convert()
            return pygame.transform.scale(img, size)
        except:
            return None
    return None


# ══════════════════════════════════════════════════════════════
#  CLASE PRINCIPAL DEL JUEGO
# ══════════════════════════════════════════════════════════════
class Game(object):
    # Estados posibles del juego:
    # "MENU"              → Pantalla de inicio
    # "PEDIR_NOMBRE"      → Input del nombre del entrenador
    # "ELEGIR_MODO"       → ¿Aleatorio o manual?
    # "SELECCION_MANUAL"  → El jugador elige sus pokemon uno por uno
    # "MAPA_ENTRENADORES" → Lista de los 5 entrenadores a vencer
    # "DIALOGO_RIVAL"     → Dialogo antes de pelear con el rival
    # "BATALLA"           → La pelea en si
    # "RESULTADO"         → Gano o perdio

    def __init__(self):
        # ── Datos del jugador ──
        self.state           = "MENU"
        self.nombre_jugador  = ""
        self.input_text      = ""
        self.equipo_jugador  = []
        self.pokemon_activo  = None

        # ── Datos de la campaña ──
        self.indice_entrenador_actual = 0
        self.entrenadores = ENTRENADORES

        # ── Selección manual ──
        self.todos_los_pokemon = get_lista_pokemon_disponibles()
        self.seleccionados_idx = []
        self.pagina_seleccion  = 0

        # ── Batalla ──
        self.batalla               = None
        self.log_batalla           = []
        self.esperando_confirmacion = False
        self.cursor_movimiento     = 0

        # ── Assets: fondos ──
        self.bg_menu     = pygame.image.load("Assets/background_menu.jpg").convert()
        self.bg_batalla  = pygame.image.load("Assets/campo_batalla.jpeg").convert()
        self.bg_gameover = pygame.image.load("Assets/fondogameover.png").convert()

        # ── Assets: botones del menu ──
        self.play_img = pygame.image.load("Assets/Play Rect.png")
        self.quit_img = pygame.image.load("Assets/Quit Rect.png")

    # ══════════════════════════════════════════
    #  MENU PRINCIPAL
    # ══════════════════════════════════════════
    def MainMenu(self, screen):
        screen.blit(self.bg_menu, (0, 0))
        mouse = pygame.mouse.get_pos()

        titulo = get_font(100).render("POKE - UTR", True, "#8d6922")
        screen.blit(titulo, titulo.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        play_btn = Button(self.play_img, (SCREEN_WIDTH//2, 400), "PLAY", get_font(75), "#d8b265", "White")
        quit_btn = Button(self.quit_img, (SCREEN_WIDTH//2, 550), "QUIT", get_font(75), "#d8b265", "White")

        for btn in [play_btn, quit_btn]:
            btn.changeColor(mouse)
            btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.checkForInput(mouse):
                    self.state = "PEDIR_NOMBRE"
                if quit_btn.checkForInput(mouse):
                    pygame.quit(); sys.exit()

        pygame.display.update()

    # ══════════════════════════════════════════
    #  PEDIR NOMBRE AL JUGADOR
    # ══════════════════════════════════════════
    def PedirNombre(self, screen):
        screen.blit(self.bg_menu, (0, 0))
        draw_panel(screen, 340, 180, 600, 340, border=YELLOW)

        draw_text(screen, "¿Cuál es tu nombre, entrenador?", get_font(32), YELLOW, SCREEN_WIDTH//2, 255)
        draw_text(screen, "(Máximo 16 caracteres)", get_font(20), GRAY, SCREEN_WIDTH//2, 295)

        # Caja de texto
        pygame.draw.rect(screen, WHITE,  (390, 330, 500, 60), border_radius=8)
        pygame.draw.rect(screen, YELLOW, (390, 330, 500, 60), 3, border_radius=8)
        nombre_surf = get_font(38).render(self.input_text + "|", True, BLACK)
        screen.blit(nombre_surf, nombre_surf.get_rect(center=(640, 360)))

        draw_text(screen, "Presiona ENTER para continuar", get_font(23), GRAY, SCREEN_WIDTH//2, 440)

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

    # ══════════════════════════════════════════
    #  ELEGIR MODO: aleatorio o manual
    # ══════════════════════════════════════════
    def ElegirModo(self, screen):
        screen.blit(self.bg_menu, (0, 0))
        mouse = pygame.mouse.get_pos()

        draw_panel(screen, 240, 130, 800, 450, border=YELLOW)
        draw_text(screen, f"¡Hola, {self.nombre_jugador}!", get_font(55), YELLOW, SCREEN_WIDTH//2, 210)
        draw_text(screen, "¿Cómo quieres elegir tu equipo?", get_font(30), WHITE, SCREEN_WIDTH//2, 275)
        draw_text(screen, "Llevarás 6 pokémon a la batalla", get_font(22), GRAY, SCREEN_WIDTH//2, 315)

        btn_aleatorio = Button(None, (SCREEN_WIDTH//2 - 190, 420), "  ALEATORIO  ", get_font(36), GRAY, YELLOW)
        btn_manual    = Button(None, (SCREEN_WIDTH//2 + 190, 420), "   ELEGIR   ", get_font(36), GRAY, YELLOW)

        btn_aleatorio.changeColor(mouse); btn_aleatorio.update(screen)
        btn_manual.changeColor(mouse);    btn_manual.update(screen)

        draw_text(screen, "La suerte decide", get_font(20), GRAY, SCREEN_WIDTH//2 - 190, 470)
        draw_text(screen, "Tú eliges tus 6", get_font(20), GRAY, SCREEN_WIDTH//2 + 190, 470)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_aleatorio.checkForInput(mouse):
                    self.equipo_jugador = get_equipo_aleatorio(6)
                    self.pokemon_activo = self.equipo_jugador[0]
                    self.state = "MAPA_ENTRENADORES"
                if btn_manual.checkForInput(mouse):
                    self.seleccionados_idx = []
                    self.pagina_seleccion  = 0
                    self.state = "SELECCION_MANUAL"

        pygame.display.update()

    # ══════════════════════════════════════════
    #  SELECCIÓN MANUAL DE POKEMON
    # ══════════════════════════════════════════
    def SeleccionManual(self, screen):
        screen.blit(self.bg_menu, (0, 0))
        mouse = pygame.mouse.get_pos()

        faltantes = 6 - len(self.seleccionados_idx)
        titulo_txt = f"Elige {faltantes} pokémon más" if faltantes > 0 else "¡Equipo completo!"
        draw_text(screen, titulo_txt, get_font(38), YELLOW, 480, 40)

        # Panel equipo seleccionado (derecha)
        draw_panel(screen, 950, 70, 310, 250, border=YELLOW)
        draw_text(screen, "Tu equipo:", get_font(24), YELLOW, 1105, 95)
        for i, idx in enumerate(self.seleccionados_idx):
            nombre = self.todos_los_pokemon[idx]._nombre
            draw_text(screen, f"• {nombre}", get_font(19), WHITE, 960, 122 + i * 32, center=False)

        # Grid de cartas (4 columnas, 2 filas = 8 por página)
        cols   = 4
        card_w, card_h = 220, 95
        start_x, start_y = 20, 80
        gap_x, gap_y = 12, 10
        por_pagina = 8
        inicio = self.pagina_seleccion * por_pagina
        fin    = min(inicio + por_pagina, len(self.todos_los_pokemon))
        total_paginas = (len(self.todos_los_pokemon) + por_pagina - 1) // por_pagina

        for i, poke_idx in enumerate(range(inicio, fin)):
            poke = self.todos_los_pokemon[poke_idx]
            col  = i % cols
            row  = i // cols
            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)

            ya_sel      = poke_idx in self.seleccionados_idx
            color_borde = GREEN if ya_sel else YELLOW
            color_fondo = (20, 60, 20) if ya_sel else (20, 20, 50)

            draw_panel(screen, x, y, card_w, card_h, color=color_fondo, border=color_borde)
            draw_text(screen, poke._nombre,              get_font(20), WHITE, x + card_w//2, y + 18)
            draw_text(screen, f"Tipo: {poke._tipo}",    get_font(16), GRAY,  x + card_w//2, y + 42)
            draw_text(screen, f"HP:{poke._hp_max}  ATK:{poke.ataque}  VEL:{poke.velocidad}",
                      get_font(14), GRAY, x + card_w//2, y + 64)

            rect = pygame.Rect(x, y, card_w, card_h)
            if rect.collidepoint(mouse):
                pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)

        # Paginación
        if self.pagina_seleccion > 0:
            btn_prev = Button(None, (100, 580), "< ANTERIOR", get_font(26), GRAY, YELLOW)
            btn_prev.changeColor(mouse); btn_prev.update(screen)
        if self.pagina_seleccion < total_paginas - 1:
            btn_next = Button(None, (350, 580), "SIGUIENTE >", get_font(26), GRAY, YELLOW)
            btn_next.changeColor(mouse); btn_next.update(screen)

        draw_text(screen, f"Página {self.pagina_seleccion+1}/{total_paginas}", get_font(20), GRAY, SCREEN_WIDTH//2, 590)

        # Botón confirmar
        if len(self.seleccionados_idx) == 6:
            btn_ok = Button(None, (1105, 580), "¡LISTO!", get_font(36), GREEN, WHITE)
            btn_ok.changeColor(mouse); btn_ok.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click en carta
                for i, poke_idx in enumerate(range(inicio, fin)):
                    col = i % cols; row = i // cols
                    x = start_x + col * (card_w + gap_x)
                    y = start_y + row * (card_h + gap_y)
                    if pygame.Rect(x, y, card_w, card_h).collidepoint(mouse):
                        if poke_idx in self.seleccionados_idx:
                            self.seleccionados_idx.remove(poke_idx)
                        elif len(self.seleccionados_idx) < 6:
                            self.seleccionados_idx.append(poke_idx)

                # Paginación
                if self.pagina_seleccion > 0:
                    if Button(None, (100, 580), "< ANTERIOR", get_font(26), GRAY, YELLOW).checkForInput(mouse):
                        self.pagina_seleccion -= 1
                if self.pagina_seleccion < total_paginas - 1:
                    if Button(None, (350, 580), "SIGUIENTE >", get_font(26), GRAY, YELLOW).checkForInput(mouse):
                        self.pagina_seleccion += 1

                # Confirmar
                if len(self.seleccionados_idx) == 6:
                    if Button(None, (1105, 580), "¡LISTO!", get_font(36), GREEN, WHITE).checkForInput(mouse):
                        self.equipo_jugador = [
                            type(self.todos_los_pokemon[i])()
                            for i in self.seleccionados_idx
                        ]
                        self.pokemon_activo = self.equipo_jugador[0]
                        self.state = "MAPA_ENTRENADORES"

        pygame.display.update()

    # ══════════════════════════════════════════
    #  MAPA DE ENTRENADORES
    # ══════════════════════════════════════════
    def MapaEntrenadores(self, screen):
        screen.blit(self.bg_menu, (0, 0))
        mouse = pygame.mouse.get_pos()

        draw_panel(screen, 80, 30, 1120, 660, border=YELLOW)
        draw_text(screen, f"Ruta del Entrenador {self.nombre_jugador}", get_font(40), YELLOW, SCREEN_WIDTH//2, 70)
        draw_text(screen, "Derrota a los 5 entrenadores para ganar", get_font(24), GRAY, SCREEN_WIDTH//2, 108)

        for i, entrenador in enumerate(self.entrenadores):
            y_card    = 145 + i * 98
            completado = entrenador.derrotado
            es_actual  = (i == self.indice_entrenador_actual)

            color_fondo = (20, 60, 20) if completado else ((40, 40, 80) if es_actual else (20, 20, 40))
            color_borde = GREEN if completado else (YELLOW if es_actual else GRAY)

            draw_panel(screen, 110, y_card, 1060, 85, color=color_fondo, border=color_borde)

            estado_txt = "✓ DERROTADO" if completado else ("► SIGUIENTE" if es_actual else "Bloqueado")
            draw_text(screen, f"{i+1}. {entrenador.nombre}", get_font(28), WHITE, 120, y_card + 22, center=False)
            draw_text(screen, estado_txt, get_font(22),
                      GREEN if completado else (YELLOW if es_actual else GRAY),
                      900, y_card + 22, center=False)

            desc_corta = entrenador.descripcion.split("\n")[0]
            draw_text(screen, desc_corta, get_font(18), GRAY, 120, y_card + 55, center=False)

            # Botón PELEAR solo para el entrenador actual
            if es_actual and not completado:
                btn = Button(None, (1090, y_card + 42), "PELEAR", get_font(24), YELLOW, WHITE)
                btn.changeColor(mouse); btn.update(screen)

        # Si ganó todo
        if all(e.derrotado for e in self.entrenadores):
            draw_panel(screen, 250, 620, 780, 60, color=(10,10,10), border=YELLOW)
            draw_text(screen, "🏆 ¡ERES EL CAMPEÓN DE LA UTR! 🏆", get_font(36), YELLOW, SCREEN_WIDTH//2, 650)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.indice_entrenador_actual < len(self.entrenadores):
                    entrenador_actual = self.entrenadores[self.indice_entrenador_actual]
                    if not entrenador_actual.derrotado:
                        i      = self.indice_entrenador_actual
                        y_card = 145 + i * 98
                        btn    = Button(None, (1090, y_card + 42), "PELEAR", get_font(24), YELLOW, WHITE)
                        if btn.checkForInput(mouse):
                            self.state = "DIALOGO_RIVAL"

        pygame.display.update()

    # ══════════════════════════════════════════
    #  DIALOGO DEL RIVAL (antes de pelear)
    # ══════════════════════════════════════════
    def DialogoRival(self, screen):
        screen.blit(self.bg_batalla, (0, 0))
        mouse  = pygame.mouse.get_pos()
        entrenador = self.entrenadores[self.indice_entrenador_actual]

        draw_panel(screen, 80, 80, 1120, 560, border=YELLOW)
        draw_text(screen, f"¡{entrenador.nombre} quiere pelear!", get_font(42), YELLOW, SCREEN_WIDTH//2, 160)

        lineas = entrenador.descripcion.split("\n")
        for i, linea in enumerate(lineas):
            draw_text(screen, linea, get_font(24), WHITE, SCREEN_WIDTH//2, 235 + i * 38)

        # Frase del rival con el nombre del jugador interpolado
        frase = entrenador.frase_inicio.format(nombre=self.nombre_jugador)
        draw_panel(screen, 130, 370, 1020, 80, color=(10, 10, 30), border=GRAY)
        draw_text(screen, f'"{frase}"', get_font(26), YELLOW, SCREEN_WIDTH//2, 410)

        # Tu equipo vs su equipo
        draw_text(screen, "Tu equipo:", get_font(22), GREEN, 140, 480)
        nombres_j = "  |  ".join([p._nombre for p in self.equipo_jugador])
        draw_text(screen, nombres_j, get_font(18), WHITE, 140, 505, center=False)

        draw_text(screen, "Su equipo:", get_font(22), RED, 140, 545)
        nombres_r = "  |  ".join([c()._nombre for c in entrenador.pokemon_clases])
        draw_text(screen, nombres_r, get_font(18), WHITE, 140, 570, center=False)

        btn = Button(None, (SCREEN_WIDTH//2, 660), "¡A PELEAR!", get_font(36), YELLOW, WHITE)
        btn.changeColor(mouse); btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.checkForInput(mouse):
                    self._iniciar_batalla()

        pygame.display.update()

    def _iniciar_batalla(self):
        """Prepara el BattleManager con el equipo completo del jugador vs el del entrenador"""
        entrenador = self.entrenadores[self.indice_entrenador_actual]
        # Curamos al equipo del jugador entre batallas
        for p in self.equipo_jugador:
            p.curar_totalmente()
            p.reset_mods()
        pokemon_rival = entrenador.get_pokemon_actual()
        # Ahora pasamos la lista COMPLETA del equipo, no solo el primero
        self.batalla  = BattleManager(self.equipo_jugador, pokemon_rival)
        self.log_batalla            = []
        self.cursor_movimiento      = 0
        self.esperando_confirmacion = False
        self.menu_cambio_abierto    = False  # True cuando el jugador presiona C
        self.cursor_cambio          = 0      # Cursor del menú de cambio
        self.state = "BATALLA"

    # ══════════════════════════════════════════
    #  PANTALLA DE BATALLA
    # ══════════════════════════════════════════
    def Batalla(self, screen):
        screen.blit(self.bg_batalla, (0, 0))
        if self.batalla is None:
            return

        poke_j = self.batalla.pokemon_jugador
        poke_e = self.batalla.pokemon_enemigo
        hp_j_actual, hp_j_max = self.batalla.get_hp_jugador()
        hp_e_actual, hp_e_max = self.batalla.get_hp_enemigo()
        movimientos = self.batalla.get_movimientos_jugador()

        # ── Imagen del pokemon enemigo (arriba izquierda) ──
        img_enemigo = cargar_imagen_pokemon(poke_e._nombre, (160, 160))
        if img_enemigo:
            screen.blit(img_enemigo, (40, 30))

        # ── Panel info enemigo ──
        draw_panel(screen, 210, 30, 420, 110, border=YELLOW)
        draw_text(screen, poke_e._nombre, get_font(30), YELLOW, 420, 58)
        draw_text(screen, f"Tipo: {poke_e._tipo}", get_font(20), GRAY, 420, 88)
        draw_hp_bar(screen, 220, 108, hp_e_actual, hp_e_max, width=220)

        # ── Imagen del pokemon jugador (abajo derecha) ──
        img_jugador = cargar_imagen_pokemon(poke_j._nombre, (160, 160))
        if img_jugador:
            screen.blit(img_jugador, (1075, 310))

        # ── Panel info jugador ──
        draw_panel(screen, 650, 330, 415, 110, border=YELLOW)
        draw_text(screen, poke_j._nombre, get_font(30), YELLOW, 858, 358)
        draw_text(screen, f"Tipo: {poke_j._tipo}", get_font(20), GRAY, 858, 388)
        draw_hp_bar(screen, 660, 408, hp_j_actual, hp_j_max, width=220)

        # ── Minibarra del equipo (arriba derecha, muestra HP de los 6) ──
        draw_panel(screen, 640, 155, 425, 165, border=GRAY)
        draw_text(screen, "Equipo:", get_font(18), YELLOW, 650, 170, center=False)
        equipo = self.batalla.get_equipo_jugador()
        idx_activo = self.batalla.get_indice_activo()
        for i, p in enumerate(equipo):
            y_eq = 188 + i * 22
            color_nombre = YELLOW if i == idx_activo else (GRAY if p._hp_actual <= 0 else WHITE)
            estado = "✓" if i == idx_activo else ("✗" if p._hp_actual <= 0 else f"{p._hp_actual}HP")
            draw_text(screen, f"{p._nombre[:14]}", get_font(16), color_nombre, 650, y_eq, center=False)
            draw_text(screen, estado, get_font(16), color_nombre, 990, y_eq, center=False)

        # ── Panel log (abajo izquierda) ──
        draw_panel(screen, 20, 470, 740, 230, border=GRAY)
        draw_text(screen, "Registro de batalla:", get_font(20), YELLOW, 380, 490)
        lineas_visibles = self.log_batalla[-5:]
        for i, linea in enumerate(lineas_visibles):
            draw_text(screen, linea, get_font(19), WHITE, 380, 515 + i * 34)

        # ── Panel movimientos o menú de cambio (abajo derecha) ──
        draw_panel(screen, 775, 470, 490, 230, border=GRAY)

        # Si hay cambio forzado o el jugador abrió el menú de cambio
        if self.batalla.necesita_cambio_forzado() or self.menu_cambio_abierto:
            titulo_cambio = "¡ELIGE TU SIGUIENTE POKÉMON!" if self.batalla.necesita_cambio_forzado() else "Cambiar pokémon:"
            draw_text(screen, titulo_cambio, get_font(18), RED if self.batalla.necesita_cambio_forzado() else YELLOW, 1020, 490)
            for i, p in enumerate(equipo):
                y_p = 515 + i * 32
                if p._hp_actual <= 0:
                    draw_text(screen, f"[{i+1}] {p._nombre[:16]}  DEBILITADO", get_font(17), GRAY, 785, y_p, center=False)
                else:
                    color = YELLOW if i == self.cursor_cambio else WHITE
                    draw_text(screen, f"[{i+1}] {p._nombre[:16]}  {p._hp_actual}HP", get_font(17), color, 785, y_p, center=False)
            if not self.batalla.necesita_cambio_forzado():
                draw_text(screen, "ESC para cancelar", get_font(15), GRAY, 785, 690, center=False)
        else:
            # Menú normal de movimientos
            draw_text(screen, "Movimientos:", get_font(20), YELLOW, 1020, 490)
            for i, mov in enumerate(movimientos):
                y_mov     = 518 + i * 44
                color_mov = YELLOW if i == self.cursor_movimiento else WHITE
                pot_txt   = f"POT:{mov.potencia}" if mov.potencia > 0 else "Efecto"
                draw_text(screen, f"[{i+1}] {mov.nombre}", get_font(19), color_mov, 785, y_mov, center=False)
                draw_text(screen, f"{pot_txt}  {mov.precision}%", get_font(16), GRAY, 785, y_mov + 20, center=False)

        # ── Instrucciones ──
        if self.batalla.batalla_terminada():
            pass  # Se maneja abajo
        elif self.batalla.necesita_cambio_forzado():
            draw_text(screen, "↑↓ Mover  |  ENTER para enviar", get_font(20), RED, SCREEN_WIDTH//2, 708)
        elif self.menu_cambio_abierto:
            draw_text(screen, "↑↓ Mover  |  ENTER para cambiar  |  ESC cancelar", get_font(18), GRAY, SCREEN_WIDTH//2, 708)
        elif self.esperando_confirmacion:
            draw_text(screen, "Presiona ENTER para continuar...", get_font(22), YELLOW, SCREEN_WIDTH//2, 708)
        else:
            draw_text(screen, "↑↓ Mover  |  ENTER/1-4 atacar  |  C cambiar pokémon", get_font(18), GRAY, SCREEN_WIDTH//2, 708)

        # ── Overlay fin de batalla ──
        if self.batalla.batalla_terminada():
            draw_panel(screen, 280, 240, 720, 180, color=(10,10,10), alpha=230, border=YELLOW)
            ganador_txt = f"¡{self.nombre_jugador} ganó!" if self.batalla.ganador == "JUGADOR" else "¡Perdiste!"
            draw_text(screen, ganador_txt, get_font(55),
                      GREEN if self.batalla.ganador == "JUGADOR" else RED, SCREEN_WIDTH//2, 310)
            draw_text(screen, "ENTER para continuar", get_font(26), YELLOW, SCREEN_WIDTH//2, 385)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                self._handle_batalla_input(event.key)

        pygame.display.update()

    def handle_batalla_input(self, key):
        equipo    = self.batalla.get_equipo_jugador()
        idx_activo = self.batalla.get_indice_activo()

        # Si la batalla terminó, ENTER lleva al resultado
        if self.batalla.batalla_terminada():
            if key == pygame.K_RETURN:
                self._procesar_resultado_batalla()
            return

        # ── Menú de cambio FORZADO (pokémon debilitado) ──
        if self.batalla.necesita_cambio_forzado():
            vivos = [i for i, p in enumerate(equipo) if p._hp_actual > 0]
            if not vivos:
                return
            if key == pygame.K_UP:
                # Mover cursor solo entre los vivos
                pos_actual = vivos.index(self.cursor_cambio) if self.cursor_cambio in vivos else 0
                self.cursor_cambio = vivos[(pos_actual - 1) % len(vivos)]
            elif key == pygame.K_DOWN:
                pos_actual = vivos.index(self.cursor_cambio) if self.cursor_cambio in vivos else 0
                self.cursor_cambio = vivos[(pos_actual + 1) % len(vivos)]
            elif key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                idx = key - pygame.K_1
                if idx in vivos:
                    self.cursor_cambio = idx
                    self._confirmar_cambio(forzado=True)
            elif key == pygame.K_RETURN:
                if self.cursor_cambio in vivos:
                    self._confirmar_cambio(forzado=True)
            return

        # ── Menú de cambio VOLUNTARIO ──
        if self.menu_cambio_abierto:
            vivos = [i for i, p in enumerate(equipo) if p._hp_actual > 0 and i != idx_activo]
            if key == pygame.K_ESCAPE:
                self.menu_cambio_abierto = False
                self.cursor_cambio = idx_activo
            elif key == pygame.K_UP:
                pos_actual = vivos.index(self.cursor_cambio) if self.cursor_cambio in vivos else 0
                self.cursor_cambio = vivos[(pos_actual - 1) % len(vivos)] if vivos else idx_activo
            elif key == pygame.K_DOWN:
                pos_actual = vivos.index(self.cursor_cambio) if self.cursor_cambio in vivos else 0
                self.cursor_cambio = vivos[(pos_actual + 1) % len(vivos)] if vivos else idx_activo
            elif key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                idx = key - pygame.K_1
                if idx < len(equipo) and equipo[idx]._hp_actual > 0 and idx != idx_activo:
                    self.cursor_cambio = idx
                    self._confirmar_cambio(forzado=False)
            elif key == pygame.K_RETURN:
                if self.cursor_cambio != idx_activo and equipo[self.cursor_cambio]._hp_actual > 0:
                    self._confirmar_cambio(forzado=False)
            return

        # ── Esperar confirmación entre turnos ──
        if self.esperando_confirmacion:
            if key == pygame.K_RETURN:
                self.esperando_confirmacion = False
            return

        # ── Selección normal de movimiento ──
        if self.batalla.estado == "SELECCION_MOVIMIENTO":
            movimientos = self.batalla.get_movimientos_jugador()
            if key == pygame.K_UP:
                self.cursor_movimiento = (self.cursor_movimiento - 1) % len(movimientos)
            elif key == pygame.K_DOWN:
                self.cursor_movimiento = (self.cursor_movimiento + 1) % len(movimientos)
            elif key == pygame.K_c:
                # Abrir menú de cambio voluntario
                vivos_sin_activo = [i for i, p in enumerate(equipo) if p._hp_actual > 0 and i != idx_activo]
                if vivos_sin_activo:
                    self.menu_cambio_abierto = True
                    self.cursor_cambio = vivos_sin_activo[0]
            elif key == pygame.K_1: self._ejecutar_movimiento(0)
            elif key == pygame.K_2: self._ejecutar_movimiento(1)
            elif key == pygame.K_3: self._ejecutar_movimiento(2)
            elif key == pygame.K_4: self._ejecutar_movimiento(3)
            elif key == pygame.K_RETURN:
                self._ejecutar_movimiento(self.cursor_movimiento)

    def _confirmar_cambio(self, forzado):
        """Ejecuta el cambio de pokémon, voluntario o forzado"""
        self.batalla.actualizar(indice_cambio=self.cursor_cambio)
        self.log_batalla.extend(self.batalla.get_log())
        self.menu_cambio_abierto = False
        self.cursor_movimiento   = 0
        if not forzado:
            self.esperando_confirmacion = True

    def _ejecutar_movimiento(self, indice):
        """Ejecuta el turno completo: registra elección y aplica resultados"""
        # Fase 1: registrar la elección del jugador
        self.batalla.actualizar(indice_movimiento_jugador=indice)
        # Fase 2: ejecutar el turno (daño, efectos, etc.)
        if self.batalla.estado == "EJECUTAR_TURNO":
            self.batalla.actualizar()
            self.log_batalla.extend(self.batalla.get_log())
        self.esperando_confirmacion = True

    def _procesar_resultado_batalla(self):
        entrenador_actual = self.entrenadores[self.indice_entrenador_actual]
        if self.batalla.ganador == "JUGADOR":
            entrenador_actual.derrotado = True
            self.indice_entrenador_actual += 1
        self.state = "RESULTADO"

    # ══════════════════════════════════════════
    #  PANTALLA DE RESULTADO
    # ══════════════════════════════════════════
    def Resultado(self, screen):
        mouse = pygame.mouse.get_pos()
        gano_jugador = self.batalla and self.batalla.ganador == "JUGADOR"

        if gano_jugador:
            screen.blit(self.bg_batalla, (0, 0))
        else:
            screen.blit(self.bg_gameover, (0, 0))

        draw_panel(screen, 180, 130, 920, 460, border=YELLOW)

        # Índice del entrenador que acabamos de pelear
        idx_peleado = self.indice_entrenador_actual - 1 if gano_jugador else self.indice_entrenador_actual
        idx_peleado = max(0, min(idx_peleado, len(self.entrenadores) - 1))
        entrenador  = self.entrenadores[idx_peleado]

        if gano_jugador:
            draw_text(screen, "¡VICTORIA!", get_font(70), GREEN, SCREEN_WIDTH//2, 230)
            frase_derrota = entrenador.frase_derrota.format(nombre=self.nombre_jugador)
            draw_text(screen, f'"{frase_derrota}"', get_font(26), YELLOW, SCREEN_WIDTH//2, 330)

            if self.indice_entrenador_actual < len(self.entrenadores):
                siguiente = self.entrenadores[self.indice_entrenador_actual]
                draw_text(screen, f"Siguiente rival: {siguiente.nombre}", get_font(28), WHITE, SCREEN_WIDTH//2, 410)
            else:
                draw_text(screen, "¡¡¡ERES EL CAMPEÓN DE LA UTR!!!", get_font(34), YELLOW, SCREEN_WIDTH//2, 410)
        else:
            draw_text(screen, "¡DERROTA!", get_font(70), RED, SCREEN_WIDTH//2, 230)
            draw_text(screen, f"Perdiste contra {entrenador.nombre}", get_font(28), WHITE, SCREEN_WIDTH//2, 330)
            draw_text(screen, "Puedes intentarlo de nuevo", get_font(24), GRAY, SCREEN_WIDTH//2, 380)

        btn_continuar = Button(None, (SCREEN_WIDTH//2, 510), "CONTINUAR", get_font(36), YELLOW, WHITE)
        btn_menu      = Button(None, (SCREEN_WIDTH//2, 565), "VOLVER AL MENÚ", get_font(28), GRAY,   WHITE)

        btn_continuar.changeColor(mouse); btn_continuar.update(screen)
        btn_menu.changeColor(mouse);      btn_menu.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_continuar.checkForInput(mouse):
                    self.state = "MAPA_ENTRENADORES"
                if btn_menu.checkForInput(mouse):
                    self._reset_juego()
                    self.state = "MENU"

        pygame.display.update()

    def _reset_juego(self):
        """Resetea todo el progreso para empezar de nuevo"""
        self.nombre_jugador  = ""
        self.input_text      = ""
        self.equipo_jugador  = []
        self.pokemon_activo  = None
        self.indice_entrenador_actual = 0
        self.seleccionados_idx = []
        self.batalla = None
        self.log_batalla = []
        for e in self.entrenadores:
            e.derrotado = False


# ══════════════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ══════════════════════════════════════════════════════════════
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("POKEUTR")
    clock = pygame.time.Clock()

    game = Game()

    while True:
        if   game.state == "MENU":               game.MainMenu(screen)
        elif game.state == "PEDIR_NOMBRE":        game.PedirNombre(screen)
        elif game.state == "ELEGIR_MODO":         game.ElegirModo(screen)
        elif game.state == "SELECCION_MANUAL":    game.SeleccionManual(screen)
        elif game.state == "MAPA_ENTRENADORES":   game.MapaEntrenadores(screen)
        elif game.state == "DIALOGO_RIVAL":       game.DialogoRival(screen)
        elif game.state == "BATALLA":             game.Batalla(screen)
        elif game.state == "RESULTADO":           game.Resultado(screen)
        clock.tick(60)

if __name__ == "__main__":
    main()