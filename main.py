import random
import pygame
import pygame.freetype


def move_player():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT


def move_AI():
    if ball.centerx > SCREEN_WIDTH/2 and ball_dx > 0:
        if opponent.bottom < ball.top:
            opponent.y += opponent_speed
        elif opponent.top > ball.bottom:
            opponent.y -= opponent_speed


def move_ball(dx, dy):
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        dy = -dy

    if ball.colliderect(player) and dx < 0:
        pong_sound.play()
        if abs(ball.left - player.right) < 10:
            dx = -dx
        elif abs(ball.top - player.bottom) < 10 and dy < 0:
            dy = -dy
        elif abs(player.top - ball.bottom) < 10 and dy > 0:
            dy = -dy

    if ball.colliderect(opponent) and dx > 0:
        pong_sound.play()
        if abs(ball.right - opponent.left) < 10:
            dx = -dx
        elif abs(ball.top - opponent.bottom) < 10 and dy < 0:
            dy = -dy
        elif abs(opponent.top - ball.bottom) < 10 and dy > 0:
            dy = -dy

    now = pygame.time.get_ticks()
    if now - score_time > pause_len and not game_is_over:
        ball.x += dx
        ball.y += dy

    return dx, dy


def restart_ball(dx, dy):
    ball.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
    dx = random.choice((random.randint(-ball_max_speed, -3),
                       random.randint(3, ball_max_speed)))
    dy = random.choice((random.randint(-ball_max_speed, -3),
                       random.randint(3, ball_max_speed)))

    return dx, dy


def play_sound():
    if player_score == target_score:
        win_sound.play()
    elif opponent_score == target_score:
        lose_sound.play()
    else:
        score_sound.play()


pygame.init()
SCREEN_WIDTH = 1350
SCREEN_HEIGHT = 680

BG_COLOR = (255,255,255)
PADDLE_COLOR = (0, 0, 0)

player = pygame.Rect(10, SCREEN_HEIGHT/2, 10, 100)
opponent = pygame.Rect(SCREEN_WIDTH-20, SCREEN_HEIGHT/2, 10, 100)
ball = pygame.Rect(SCREEN_WIDTH/2-10, SCREEN_HEIGHT/2-10, 20, 20)

player_speed = 0
opponent_speed = 7
ball_max_speed = 11
ball_dx, ball_dy = -7, 7

score_time = 0
pause_len = 1000
player_score, opponent_score = 0, 0
target_score = 1
game_is_over = False
end_text = None 
restart_text = "Press R to Restart"
icon = pygame.image.load('favicon.png')

pong_sound = pygame.mixer.Sound('pong.wav')
score_sound = pygame.mixer.Sound('score.wav')
win_sound = pygame.mixer.Sound('win.wav')
lose_sound = pygame.mixer.Sound('lose.wav')

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping Pong')
pygame.display.set_icon(icon)
main_font = pygame.freetype.Font(None, 42)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_is_over:
                game_is_over = False
                player_score, opponent_score = 0, 0

            if event.key == pygame.K_w:
                player_speed -= 7
            elif event.key == pygame.K_s:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_speed += 7
            elif event.key == pygame.K_s:
                player_speed -= 7

    move_player()
    move_AI()
    ball_dx, ball_dy = move_ball(ball_dx, ball_dy)

    if ball.right <= 0:
        opponent_score += 1
        if opponent_score == target_score:
            game_is_over = True
            end_text = 'YOU LOSE'
    elif ball.left >= SCREEN_WIDTH:
        player_score += 1
        if player_score == target_score:
            game_is_over = True
            end_text = 'YOU WIN!'

    if ball.right <= 0 or ball.left >= SCREEN_WIDTH:
        play_sound()
        ball_dx, ball_dy = restart_ball(ball_dx, ball_dy)
        score_time = pygame.time.get_ticks()

    screen.fill(BG_COLOR)
    main_font.render_to(screen, (SCREEN_WIDTH/3, 20), str(player_score))
    main_font.render_to(screen, (SCREEN_WIDTH/1.5, 20), str(opponent_score))

    pygame.draw.rect(screen, PADDLE_COLOR, player)
    pygame.draw.rect(screen, PADDLE_COLOR, opponent)
    pygame.draw.line(screen, PADDLE_COLOR, (SCREEN_WIDTH/2, 0),
                                (SCREEN_WIDTH/2, SCREEN_HEIGHT))
    pygame.draw.ellipse(screen, PADDLE_COLOR, ball)
    if game_is_over:
        main_font.render_to(screen, (SCREEN_WIDTH/2.6, 100), end_text) 
        main_font.render_to(screen, (SCREEN_WIDTH/3.2, 150), restart_text) 

    clock.tick(60)
    pygame.display.flip()