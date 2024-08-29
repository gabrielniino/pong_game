import pygame

# Definir as dimensões da tela
WIDTH = 800
HEIGHT = 600

pygame.init()

# Inicializar o mixer de som
pygame.mixer.init()

# Criar a janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Cores
sky_blue = (142, 202, 230)
blue_green = (33, 158, 188)
prussian_blue = (2, 48, 71)
selective_yellow = (255, 183, 3)
ut_orange = (251, 133, 0)
white = (255, 255, 255)

# Dimensões dos jogadores
rect_w = 30
rect_h = 30
rect_x, rect_y = 10, int(HEIGHT / 2) - rect_h // 2
rect2_x, rect2_y = WIDTH - rect_w - 10, int(HEIGHT / 2) - rect_h // 2

# Posições da bola
ball_x, ball_y = int(WIDTH / 2), int(HEIGHT / 2)
ball_speed_x = 0.3
ball_speed_y = 0.3
ball_radius = 10 

ball_moving = False
paused = False
ball_moved = False

score = 0
score2 = 0

# Fontes
font = pygame.font.SysFont("Arial", 20)
menu_title = pygame.font.SysFont("Arial", 40)
menu_text = pygame.font.SysFont("Arial", 20)
button_font = pygame.font.SysFont("Arial", 30)

# Botões
button_width = 200
button_height = 50
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 2 + 40

# Carregar as imagens
paddle_image = pygame.image.load("assets/images/player_1.png")
paddle_image2 = pygame.image.load("assets/images/player_2.png")
ball_image = pygame.image.load("assets/images/ball.png")
background_image = pygame.image.load("assets/images/texture.jpg")
menu_background_image = pygame.image.load("assets/images/background_menu.jpg")

paddle_image = pygame.transform.scale(paddle_image, (rect_w, rect_h))
paddle_image2 = pygame.transform.scale(paddle_image2, (rect_w, rect_h))
ball_image = pygame.transform.scale(ball_image, (ball_radius * 2, ball_radius * 2))

background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
menu_background_image = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))

# Carregar os sons
pygame.mixer.music.load("assets/sounds/track_sound.mp3")
whistle_sound = pygame.mixer.Sound("assets/sounds/apito.mp3")
goal_sound = pygame.mixer.Sound("assets/sounds/goal.wav") 
ball_kick_sound = pygame.mixer.Sound("assets/sounds/ball_kick.mp3") 
click_menu_sound = pygame.mixer.Sound("assets/sounds/click_menu_sound.mp3") 
menu_music = pygame.mixer.music.load("assets/sounds/track_sound_menu.mp3") 
la_vem_mais_sound = pygame.mixer.Sound("assets/sounds/la_vem_mais.mp3") 
gol_da_alemanha_sound = pygame.mixer.Sound("assets/sounds/gol-da-alemanha-1.mp3")  

def draw_menu():
    screen.blit(menu_background_image, (0, 0))  # Desenhar o fundo do menu
    # title_text = menu_title.render("Pong", True, selective_yellow)
    start_button = pygame.Rect(button_x, button_y, button_width, button_height)
    start_text = button_font.render("Iniciar o jogo", True, prussian_blue)

    pygame.draw.rect(screen, ut_orange, start_button)
    # screen.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2,
    #                          HEIGHT / 2 - title_text.get_height() - 60))
    screen.blit(start_text, (button_x + (button_width - start_text.get_width()) / 2,
                             button_y + (button_height - start_text.get_height()) / 2))

    pygame.display.flip()
    return start_button


def reset_ball():
    global ball_x, ball_y, ball_moving, ball_speed_x, ball_speed_y, paused, ball_moved
    # Resetar a posição da bola e as variáveis de controle
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_moving = False
    ball_speed_x = 0.3
    ball_speed_y = 0.3
    paused = False
    ball_moved = False


def main_game():
    global rect_y, rect2_y, ball_x, ball_y, ball_speed_x, ball_speed_y, ball_moving, score, score2, paused, ball_moved

    pygame.mixer.music.load("assets/sounds/track_sound.mp3")  # Trilha sonora do jogo
    pygame.mixer.music.play(-1)  # -1 significa que a música será repetida indefinidamente

    running = True
    played_la_vem_mais = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not ball_moved:
                        ball_moving = True
                        ball_moved = True
                        whistle_sound.play()
                    else:
                        paused = not paused
                        if not paused:
                            whistle_sound.play()

        # Capturar as teclas pressionadas
        keys = pygame.key.get_pressed()

        # Movimento do jogador da esquerda
        if not paused:
            if keys[pygame.K_w]:
                rect_y -= 1
            if keys[pygame.K_s]:
                rect_y += 1

            if rect_y < 0:
                rect_y = 0
            elif rect_y + rect_h > HEIGHT:
                rect_y = HEIGHT - rect_h

            # Movimento do jogador da direita
            if keys[pygame.K_UP]:
                rect2_y -= 1
            if keys[pygame.K_DOWN]:
                rect2_y += 1

            if rect2_y < 0:
                rect2_y = 0
            elif rect2_y + rect_h > HEIGHT:
                rect2_y = HEIGHT - rect_h

        if ball_moving and not paused:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            if ball_y + ball_radius >= HEIGHT or ball_y - ball_radius <= 0:
                ball_speed_y = -ball_speed_y

            if ball_x + ball_radius >= WIDTH:
                score += 1
                goal_sound.play() 
                reset_ball() 
                played_la_vem_mais = False
                if score == 2:
                    gol_da_alemanha_sound.play()

            if ball_x - ball_radius <= 0:
                score2 += 1
                goal_sound.play()
                reset_ball()
                played_la_vem_mais = False
                if score2 == 2:
                    gol_da_alemanha_sound.play()

            # Colisão com os jogadores
            if ball_speed_x < 0:
                if ball_x - ball_radius <= rect_x + rect_w:
                    if rect_y <= ball_y <= rect_y + rect_h:
                        ball_speed_x = -ball_speed_x * 1.1
                        ball_kick_sound.play()
            else:
                if ball_x + ball_radius >= rect2_x:
                    if rect2_y <= ball_y <= rect2_y + rect_h:
                        ball_speed_x = -ball_speed_x * 1.1
                        ball_kick_sound.play()

            losing_player_extreme_x = rect_x + rect_w + 200 if score2 >= score else rect2_x - 200

            if (score >= 1 or score2 >= 1) and not played_la_vem_mais:
                if (score2 >= score and ball_x - ball_radius <= losing_player_extreme_x) or \
                   (score >= score2 and ball_x + ball_radius >= losing_player_extreme_x):
                    la_vem_mais_sound.play()
                    played_la_vem_mais = True

        # Desenhar o background
        screen.blit(background_image, (0, 0))

        # Desenhar os players e a bola
        screen.blit(paddle_image, (rect_x, rect_y))
        screen.blit(paddle_image2, (rect2_x, rect2_y))
        screen.blit(ball_image, (ball_x - ball_radius, ball_y - ball_radius))

        # Desenhar o placar
        score_text = font.render(str(score), True, ut_orange)
        screen.blit(score_text, (WIDTH / 2 - 40, 10))

        score_text2 = font.render(str(score2), True, ut_orange)
        screen.blit(score_text2, (WIDTH / 2 + 20, 10))

        if not ball_moved:
            start_text = font.render("Pressione SPACE para iniciar", True, white)
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() - 30))

        if paused and ball_moved:
            pause_text = menu_title.render("PAUSE", True, white)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()


menu_active = True
pygame.mixer.music.load("assets/sounds/track_sound_menu.mp3")  # Carregar a trilha sonora do menu
pygame.mixer.music.play(-1)  # -1 significa que a música será repetida indefinidamente

while menu_active:
    start_button = draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                click_menu_sound.play()  # Tocar o som do clique do menu
                pygame.time.wait(500)  # Pequena pausa para garantir que o som seja ouvido antes de iniciar o jogo
                pygame.mixer.music.stop()  # Parar a trilha sonora do menu
                menu_active = False
                main_game()

pygame.quit()
