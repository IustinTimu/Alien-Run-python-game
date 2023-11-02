import pygame
from sys import exit
from random import randint


def scor():
    current_time = int(pygame.time.get_ticks()/1000) - time
    score_surface = text_font.render(
        f'Score: {current_time}', False, (36, 172, 177))
    scor_rect = score_surface.get_rect(center=(700, 50))
    window.blit(score_surface, scor_rect)
    return current_time


def rock_movement(rock_list):
    if rock_list:
        for rock_rect in rock_list:
            rock_rect.x -= 9
            window.blit(rock, rock_rect)
        rock_list = [rock for rock in rock_list if rock.x > -100]
        return rock_list
    else:
        return []


def collisions(player, rock):

    if rock:
        for rock_rect in rock:
            if player.colliderect(rock_rect):
                end_game_sound.play()
                return False
    return True


def animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = jump

    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption('ALIEN RUN')
clock = pygame.time.Clock()
text_font = pygame.font.Font('Python/game/fonts/font titlu.ttf', 20)
title_font = pygame.font.Font('Python/game/fonts/font titlu.ttf', 100)


player_walk_1 = pygame.image.load('Python/game/pictures/player_walk_1.png')
player_walk_2 = pygame.image.load('Python/game/pictures/player_walk_2.png')
player_walk = [player_walk_1, player_walk_2]
player_index = 0
jump = pygame.image.load('Python/game/pictures/jump.png')

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(60, 483))
player_gravity = 0

durt = pygame.image.load('Python/game/pictures/spatiu.png')

sky = pygame.image.load('Python/game/pictures/background.jpg')

rock = pygame.image.load('Python/game/pictures/rock_2.png ')
rock_rect = rock.get_rect(bottomright=(600, 510))

rock_rect_list = []

start_screen = pygame.image.load('Python/game/pictures/capsule.png ')

jump_sound = pygame.mixer.Sound('Python/game/sound/jump_music.wav')
jump_sound.set_volume(0.5)

end_game_sound = pygame.mixer.Sound('Python/game/sound/game_over_music.wav')
end_game_sound.set_volume(0.3)

background_sound = pygame.mixer.Sound('Python/game/sound/background_music.wav')
background_sound.set_volume(0.1)

restart_sound = pygame.mixer.Sound('Python/game/sound/restart_game_music.wav')
restart_sound.set_volume(0.1)

is_running = False
time = 0
score = 0
rock_timer = pygame.USEREVENT + 1
pygame.time.set_timer(rock_timer, 900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if is_running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -25
                    jump_sound.play()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_running = True
                rock_rect.left = 800
                time = int(pygame.time.get_ticks()/1000)

            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()

        if event.type == rock_timer and is_running:
            rock_rect_list.append(rock.get_rect(
                bottomright=(randint(800, 1100), 510)))

    if is_running:

        window.blit(sky, (0, 0))
        window.blit(durt, (0, 483))
        score = scor()

        player_gravity += 1.1
        player_rect.y += player_gravity
        if player_rect.bottom >= 480:
            player_rect.bottom = 480
        animation()
        window.blit(player_surface, player_rect)

        rock_rect_list = rock_movement(rock_rect_list)

        is_running = collisions(player_rect, rock_rect_list)

    else:
        window.fill((25, 116, 142))
        window.blit(start_screen, (0, 0))
        rock_rect_list.clear()

        title_surface = title_font.render(f'ALIEN RUN ', False, (36, 172, 177))
        title_rect = title_surface.get_rect(center=(330, 90))
        start_text_surface = text_font.render(
            f'press SPACE to start', False, (36, 172, 177))
        start_text_rect = start_text_surface.get_rect(center=(340, 320))

        quit_text_surface = text_font.render(
            f'press ESC to quit', False, (36, 172, 177))
        quit_text_rect = quit_text_surface.get_rect(center=(340, 370))

        score_message = text_font.render(
            f'Your score: {score}', False, (36, 172, 177))
        score_message_rect = score_message.get_rect(center=(340, 420))
        if score == 0:
            window.blit(title_surface, title_rect)
            window.blit(start_text_surface, start_text_rect)
            window.blit(quit_text_surface, quit_text_rect)
        else:
            window.blit(title_surface, title_rect)
            window.blit(start_text_surface, start_text_rect)
            window.blit(quit_text_surface, quit_text_rect)
            window.blit(score_message, score_message_rect)

        pygame.display.flip()

    pygame.display.update()
    clock.tick(60)
