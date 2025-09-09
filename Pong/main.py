# NOTE: THIS FILE CONTAINS THE MAIN CLASS OF THE GAME WHICH IS RESPONSIBLE FOR RUNNING AND STOPPING THE GAME WITH THE MAIN GAME LOOP
# ------------------------------------------------------------------------------------------------------------------------------------

import sys
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_COLOR, PADDLE_COLOR, PLAYER_WIDTH, PLAYER_HEIGHT
from ball import Ball
from player import Player
from divider import Divider

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen_centery = screen.get_rect().centery
    pygame.display.set_caption("Ping Pong")


    ball = Ball(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, 8, PADDLE_COLOR)
    paddle_left = Player(20, (screen_centery - (PLAYER_HEIGHT//2)), PADDLE_COLOR, PLAYER_WIDTH, PLAYER_HEIGHT)
    paddle_right = Player(WINDOW_WIDTH - 35, (screen_centery - (PLAYER_HEIGHT//2)), PADDLE_COLOR, PLAYER_WIDTH, PLAYER_HEIGHT)
    divider = Divider(screen)

    players = pygame.sprite.Group()
    players.add(paddle_left)
    players.add(paddle_right)
    ball.starting_direction()

    FPS = 60
    clock = pygame.time.Clock()

    player1_score = 0
    player2_score = 0
    game_over = False

    pygame.font.init()
    score_font = pygame.font.SysFont(None, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        
        if not game_over:
            keys = pygame.key.get_pressed()
            paddle_left.update_player_pos(keys, WINDOW_HEIGHT, 'left')
            paddle_right.update_player_pos(keys, WINDOW_HEIGHT, 'right')

            ball.move()

            # Scoring
            if ball.rect.left <= 0:
                player2_score += 1
                ball.reset_ball()
                paddle_left.reset_position()
                paddle_right.reset_position()

                if player2_score >= 11:
                    game_over = True

            if ball.rect.right > WINDOW_WIDTH:
                player1_score += 1
                ball.reset_ball()
                paddle_left.reset_position()
                paddle_right.reset_position()

                if player1_score >= 11:
                    game_over = True
            
            # Improved paddle collisions using the new method
            if paddle_left.image.colliderect(ball.rect) and ball.speed_x < 0:
                ball.paddle_collision(paddle_left.image, True)

            if paddle_right.image.colliderect(ball.rect) and ball.speed_x > 0:
                ball.paddle_collision(paddle_right.image, False)

        screen.fill(BOARD_COLOR)
        ball.draw(screen)
        divider.draw(screen)

        player1_text = score_font.render(str(player1_score), True, PADDLE_COLOR)
        player2_text = score_font.render(str(player2_score), True, PADDLE_COLOR)

        if game_over:
            paddle_left.reset_position()
            paddle_right.reset_position()
           
            winner_caption = ""
            if player1_score >= 11:
                winner_caption = "PLAYER 1 WINS!"
            else:
                winner_caption = "PLAYER 2 WINS!"

            winner_text = score_font.render(winner_caption, True, PADDLE_COLOR)
            winner_rect = winner_text.get_rect(center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(winner_text, winner_rect)

        screen.blit(player1_text, (WINDOW_WIDTH*0.25, 20))
        screen.blit(player2_text, (WINDOW_WIDTH*0.75, 20))

        # drawing the right and left players on their respective position
        for player in players:
            player.draw(screen)

        # update the screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

run_game()
