import pygame
import random
import math

pygame.init()

# ==========================================
# CONFIGURACIÓN
# ==========================================

ANCHO = 1200
ALTO = 800

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Challenge de Pitágoras")

reloj = pygame.time.Clock()

fuente = pygame.font.SysFont(None, 40)
fuente_pequena = pygame.font.SysFont(None, 32)
fuente_grande = pygame.font.SysFont(None, 72)

# ==========================================
# VARIABLES DEL JUEGO
# ==========================================

hipotenusa = random.randint(50, 150)

entrada_usuario = ""

triangulos_creados = 0
errores = 0

MAX_ERRORES = 3

mensaje = "Ingresa un cateto menor que la hipotenusa."

triangulos = []

game_over = False

# ==========================================
# BUCLE PRINCIPAL
# ==========================================

ejecutando = True

while ejecutando:

    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            # Salir con Q
            if evento.key == pygame.K_q:
                ejecutando = False

            # Salir con ESC
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

            if not game_over:

                # Borrar
                if evento.key == pygame.K_BACKSPACE:
                    entrada_usuario = entrada_usuario[:-1]

                # ENTER
                elif evento.key == pygame.K_RETURN:

                    if entrada_usuario != "":

                        cateto = int(entrada_usuario)

                        # ----------------------------------
                        # VALIDACIONES
                        # ----------------------------------

                        if cateto <= 0:

                            errores += 1

                            mensaje = (
                                "Error: Los lados de un triángulo "
                                "deben ser mayores que cero."
                            )

                        elif cateto >= hipotenusa:

                            errores += 1

                            mensaje = (
                                "Error: Un cateto no puede ser "
                                "mayor o igual que la hipotenusa."
                            )

                        else:

                            otro_cateto = math.sqrt(
                                hipotenusa**2 - cateto**2
                            )

                            triangulos.append(
                                (
                                    cateto,
                                    int(otro_cateto)
                                )
                            )

                            triangulos_creados += 1

                            mensaje = (
                                f"Triángulo válido. "
                                f"Segundo cateto = "
                                f"{otro_cateto:.2f}"
                            )

                            hipotenusa = random.randint(50, 150)

                        entrada_usuario = ""

                        # ----------------------------------
                        # GAME OVER
                        # ----------------------------------

                        if errores >= MAX_ERRORES:
                            game_over = True

                else:

                    if evento.unicode.isdigit():
                        entrada_usuario += evento.unicode

    # ======================================
    # DIBUJAR FONDO
    # ======================================

    pantalla.fill((30, 30, 30))

    # ======================================
    # PANEL SUPERIOR
    # ======================================

    texto1 = fuente.render(
        f"Hipotenusa: {hipotenusa}",
        True,
        (255, 255, 255)
    )

    texto2 = fuente.render(
        f"Cateto: {entrada_usuario}",
        True,
        (255, 255, 0)
    )

    texto3 = fuente.render(
        f"Triángulos creados: {triangulos_creados}",
        True,
        (0, 255, 0)
    )

    texto4 = fuente.render(
        f"Errores: {errores}/{MAX_ERRORES}",
        True,
        (255, 100, 100)
    )

    pantalla.blit(texto1, (20, 20))
    pantalla.blit(texto2, (20, 70))
    pantalla.blit(texto3, (20, 120))
    pantalla.blit(texto4, (20, 170))

    # ======================================
    # MENSAJE
    # ======================================

    color_mensaje = (255, 255, 255)

    if "Error" in mensaje:
        color_mensaje = (255, 80, 80)

    texto_mensaje = fuente_pequena.render(
        mensaje,
        True,
        color_mensaje
    )

    pantalla.blit(texto_mensaje, (20, 220))

    # ======================================
    # LÍNEA SEPARADORA
    # ======================================

    pygame.draw.line(
        pantalla,
        (120, 120, 120),
        (0, 270),
        (ANCHO, 270),
        2
    )

    # ======================================
    # TRIÁNGULOS
    # ======================================

    margen_x = 40
    margen_y = 300

    espacio_horizontal = 40
    espacio_vertical = 40

    x = margen_x
    y = margen_y

    altura_fila = 0

    for base, altura in triangulos:

        ancho_ocupado = base + espacio_horizontal

        if x + ancho_ocupado > ANCHO - 50:

            x = margen_x
            y += altura_fila + espacio_vertical
            altura_fila = 0

        puntos = [
            (x, y),
            (x + base, y),
            (x, y + altura)
        ]

        pygame.draw.polygon(
            pantalla,
            (0, 150, 255),
            puntos
        )

        x += ancho_ocupado

        if altura > altura_fila:
            altura_fila = altura

    # ======================================
    # GAME OVER
    # ======================================

    if game_over:

        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        pantalla.blit(overlay, (0, 0))

        texto_go = fuente_grande.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        texto_info = fuente.render(
            f"Has acumulado {errores} errores",
            True,
            (255, 255, 255)
        )

        texto_score = fuente.render(
            f"Triángulos creados: {triangulos_creados}",
            True,
            (255, 255, 255)
        )

        texto_salir = fuente_pequena.render(
            "Presiona Q para salir",
            True,
            (255, 255, 0)
        )

        pantalla.blit(
            texto_go,
            (
                ANCHO // 2 - texto_go.get_width() // 2,
                250
            )
        )

        pantalla.blit(
            texto_info,
            (
                ANCHO // 2 - texto_info.get_width() // 2,
                350
            )
        )

        pantalla.blit(
            texto_score,
            (
                ANCHO // 2 - texto_score.get_width() // 2,
                400
            )
        )

        pantalla.blit(
            texto_salir,
            (
                ANCHO // 2 - texto_salir.get_width() // 2,
                470
            )
        )

    # ======================================
    # ACTUALIZAR
    # ======================================

    pygame.display.flip()

    reloj.tick(60)

pygame.quit()