import time
from random import *
from os import environ
from sys import platform as _sys_platform
import pygame
import os

path = ''

clock = pygame.time.Clock()


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return 'android'
    elif _sys_platform in ('linux', 'linux2', 'linux3'):
        return 'linux'
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'


pygame.init()

screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)  # flags=pygame.NOFRAME
pygame.display.set_caption('Mars protection')
icon = pygame.image.load(path + 'images/galactic_warships_images/icons/MP_icon.png').convert_alpha()
pygame.display.set_icon(icon)

w, h = pygame.display.get_surface().get_size()
w_difference, h_difference = 1536 / w, 864 / h

bg0 = pygame.transform.scale(
    pygame.image.load(path + 'images/galactic_warships_images/bg/space.jpg').convert_alpha(), (w, h))
bg1 = pygame.transform.scale(
    pygame.image.load(path + 'images/galactic_warships_images/bg/space2.jpg').convert_alpha(), (w, h))

little_size = (100 // w_difference, 100 // w_difference)

all_ships = [
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain0_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain1_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain2_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain3_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain4_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain5_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain6_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain7_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain8_gray.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/gray/p_plain9_gray.png').convert_alpha(), little_size)
]

players_ships = [
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain0.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain1.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain2.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain3.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain4.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain5.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain6.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain7.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain8.png').convert_alpha(), little_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain9.png').convert_alpha(), little_size)
]

big_size = (500 / w_difference, 500 / w_difference)

players_ships_menu = [
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain0.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain1.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain2.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain3.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain4.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain5.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain6.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain7.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain8.png').convert_alpha().convert_alpha(), big_size),
    pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/p_plain/p_plain9.png').convert_alpha().convert_alpha(), big_size)
]

bad_ship = pygame.transform.scale(pygame.image.load(path + 'images/galactic_warships_images/bad_plain/plain.png').
                                  convert_alpha(), little_size)
bad_ship_list = []

bullet_size = (50 / w_difference, 17 / w_difference)

bullet = [
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet01.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet01.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet01.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet11.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet11.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet11.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet21.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet21.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet21.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet31.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet31.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet31.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet41.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet41.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet41.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet51.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet51.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet51.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet61.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet61.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet61.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet71.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet71.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet71.png').convert_alpha(), bullet_size)],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet81.png').convert_alpha(),
                            (30 / w_difference, 30 / w_difference)),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet81.png').convert_alpha(),
                            (30 / w_difference, 30 / w_difference)),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet81.png').convert_alpha(),
                            (30 / w_difference, 30 / w_difference))],
    [pygame.transform.scale(pygame.image.load(
        path + 'images/galactic_warships_images/bullets/bullet91.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet91.png').convert_alpha(), bullet_size),
     pygame.transform.scale(pygame.image.load(
         path + 'images/galactic_warships_images/bullets/bullet91.png').convert_alpha(), bullet_size)]
]

bullet_choice = 0
bullet_choice_max = 2
bullet_choice_stop = False

bullets = []

players_ships_x = 300 // w_difference
players_ships_y = 360 // w_difference

players_ships_speed = 2

bullets_speed = 0.5

bad_ship_speed = 1

big_planet = pygame.transform.scale(pygame.image.load(
    path + 'images/galactic_warships_images/planets/planet_red_big.png').
                                    convert_alpha(), (166 / w_difference, 1019 / w_difference))

bad_ship_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bad_ship_timer, 2000)

bullet_timer = pygame.USEREVENT + 1
pygame.time.set_timer(bullet_timer, 2000)

label = pygame.font.Font(path + 'fonts/planet_font.ttf', int(80 / w_difference))
label2 = pygame.font.Font(path + 'fonts/planet_font.ttf', int(50 / w_difference))
font = pygame.font.Font(path + 'fonts/planet_font.ttf', int(23 / w_difference))

next_label = label.render('дальше', True, 'black')

# 1540, 802
next_label_x = 20 // w_difference
next_label_y = h - 80 // w_difference - 20
next_label_rect = next_label.get_rect(topleft=(next_label_x, next_label_y))
next_label_rect2 = next_label.get_rect(topleft=(next_label_x + 1200, next_label_y))

square_next = pygame.Surface((int(50 * len('дальше') // w_difference), 80 // w_difference))
square_next.fill('yellow')

done_label = label.render('играть', True, 'black')

# 1540, 802
done_label_x = w - 20 - int(42 * len('играть')) // w_difference
done_label_y = h - 20 - 80 // w_difference
done_label_rect = done_label.get_rect(topleft=(done_label_x, done_label_y))

square_done = pygame.Surface((int(42 * len('играть')), 80 // w_difference))
square_done.fill('yellow')

ship_label = label.render('самолёты', True, 'black')

# 1540, 802
ship_label_x = 20 // w_difference
ship_label_y = 20 // w_difference
ship_label_rect = ship_label.get_rect(topleft=(ship_label_x, ship_label_y))

square_ship = pygame.Surface((int(50 * len('самолёты') // w_difference), 80 // w_difference))
square_ship.fill('yellow')

shop = label.render('магазин', True, 'black')
# 1540, 802
shop_label_x = 20 // w_difference
shop_label_y = 120 // w_difference
shop_label_rect = shop.get_rect(topleft=(shop_label_x, shop_label_y))
square_shop = pygame.Surface((int(45 * len('магазин') // w_difference), 80 // w_difference))
square_shop.fill('yellow')

management = label.render('управление', True, 'black')
# 1540, 802
management_label_x = 20 // w_difference
management_label_y = 220 // w_difference
management_label_rect = management.get_rect(topleft=(management_label_x, management_label_y))
square_management = pygame.Surface((int(45 * len('management') // w_difference), 80 // w_difference))
square_management.fill('yellow')

out = label.render('назад', True, 'black')

# 1540, 802
out_x = w - 270 // w_difference
out_y = 20 // w_difference
out_rect = out.get_rect(topleft=(out_x, out_y))

square_out = pygame.Surface((int(50 * len('назад')), 80 // w_difference))
square_out.fill('yellow')

label_up_down = pygame.font.Font(path + 'fonts/planet_font.ttf', int(80 // w_difference))
up_down_x = 1300 // w_difference

control_label = pygame.font.Font(path + 'fonts/planet_font.ttf', int(80 // w_difference))
control_y = 500 // w_difference

joystick = control_label.render('джойстик', True, 'black')
joystick_rect = joystick.get_rect(topleft=(20, control_y))

square_joystick = pygame.Surface((int(47 * len('джойстик') // w_difference), 80 // w_difference))
square_joystick.fill('yellow')

arrows = control_label.render('стрелки', True, 'black')
arrows_rect = arrows.get_rect(topleft=(470, control_y))

square_arrows = pygame.Surface((int(45 * len('стрелки') // w_difference), 80 // w_difference))
square_arrows.fill('yellow')

control = 1

circle_pos = pygame.mouse.get_pos()

sqr_x = int(120 // w_difference)
sqr_y = int(240 // w_difference)

sqr_x2 = int(1300 // w_difference)
sqr_y2 = int(500 // w_difference)

size = 40

play_stop = pygame.font.Font(path + 'fonts/planet_font.ttf', int(80 // w_difference))
play_stop_x = 300 // w_difference
play_stop_y = 20 // w_difference

play = pygame.transform.scale(pygame.image.load(
    path + 'images/galactic_warships_images/buttons/play_button.png').convert_alpha(),
                              (64 // w_difference, 64 // w_difference))
play_rect = play.get_rect(topleft=(play_stop_x + 200 // w_difference, play_stop_y // w_difference))

square_play = pygame.Surface((64 // w_difference, 64 // w_difference))
square_play.fill('yellow')

stop_and_out = pygame.transform.scale(pygame.image.load(
    path + 'images/galactic_warships_images/buttons/stop_button.png').convert_alpha(),
                                      (64 // w_difference, 64 // w_difference))
stop_and_out_rect = stop_and_out.get_rect(topleft=(play_stop_x, play_stop_y))

square_stop_and_out = pygame.Surface((64 // w_difference, 64 // w_difference))
square_stop_and_out.fill('yellow')

stop = pygame.transform.scale(pygame.image.load(
    path + 'images/galactic_warships_images/buttons/pause_button.png').convert_alpha(),
                              (64 // w_difference, 64 // w_difference))
stop_rect = stop.get_rect(topleft=(play_stop_x + 100 // w_difference, play_stop_y))

square_stop = pygame.Surface((64 // w_difference, 64 // w_difference))
square_stop.fill('yellow')

black_planet = pygame.image.load(path + 'images/galactic_warships_images/planets/planet_black.png').convert_alpha()
blue_planet = pygame.image.load(path + 'images/galactic_warships_images/planets/planet_blue.png').convert_alpha()
green_planet = pygame.image.load(path + 'images/galactic_warships_images/planets/planet_green.png').convert_alpha()

score = 0
score_list = [0]

bg_sound = pygame.mixer.Sound(path + 'music/planet_music.mp3')
bg_sound2 = pygame.mixer.Sound(path + 'music/planet_music2.mp3')
bg_sound2.play(loops=-1)
bg_sound.stop()

music_list = 0
music_list2 = 0

gameplay = 3

plain = 0

f = open(path + 'plains.TXT', 'r')
file_contents = f.read()
p = str(file_contents)
f.close()

p_list = []

for some in range(len(p)):
    p_list += str(p[some])

points = 0

f = open(path + 'points.TXT', 'r')
file_contents = f.read()
points += int(file_contents)
f.close()

c = 0

b = 0

cost = 100

p_listTrue = '1' + '0' * (len(p_list) - 1)

ind = 1

color_up = 'yellow'
color_down = 'yellow'

stop_or_play = 0

up_True = 0
down_True = 0

start_time = time.time()
time_int = 1
counter = 0

fps = ''

running = True
while running:

    screen.fill('black')

    p_listTrue = ''
    for x in range(len(p_list)):
        if p_list[x] == '1':
            p_listTrue += '1'
        else:
            p_listTrue += '0'

    if gameplay == 0:

        up_label = label_up_down.render('/\\', True, color_up)
        up_label_rect = up_label.get_rect(topleft=(up_down_x, 500))

        down_label = label_up_down.render('\\/', True, color_down)
        down_label_rect = down_label.get_rect(topleft=(up_down_x, 600))

        screen.fill('black')

        if music_list == 1:
            bg_sound.play(loops=-1)
            music_list = 0
        screen.blit(bg0, (0, 0))
        players_ships_rect = players_ships[plain].get_rect(topleft=(players_ships_x, players_ships_y))
        big_planet_rect = big_planet.get_rect(topleft=(0, -170 // w_difference))
        screen.blit(big_planet, big_planet_rect)

        screen.blit(black_planet, (200, 20))
        screen.blit(blue_planet, (1400, 40))
        screen.blit(green_planet, (400, 680))

        print_score = pygame.font.Font(path + 'fonts/planet_font.ttf', int(20 // w_difference))
        text_score = print_score.render(f'{score} самолётов побеждено!', True, 'green')
        screen.blit(text_score, (10 // w_difference, 30 // w_difference))

        if stop_or_play == 0:
            screen.blit(square_stop, stop_rect)
            screen.blit(stop, stop_rect)
            screen.blit(square_stop_and_out, stop_and_out_rect)
            screen.blit(stop_and_out, stop_and_out_rect)

            mouse = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if stop_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                players_ships_speed = 0
                bullets_speed = 0
                bad_ship_speed = 0
                bullet_choice_stop = True
                stop_or_play = 1

            mouse = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if stop_and_out_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = 1
                bg_sound.stop()
                bg_sound2.play(loops=-1)

        else:
            screen.blit(square_play, play_rect)
            screen.blit(play, play_rect)

            mouse = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            if play_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                players_ships_speed = 2
                bullets_speed = 0.5
                bad_ship_speed = 1
                bullet_choice_stop = False
                stop_or_play = 0

        screen.blit(players_ships[plain], players_ships_rect)

        if bad_ship_list:
            for (i, el) in enumerate(bad_ship_list):
                screen.blit(bad_ship, el)
                el.x -= bad_ship_speed

                if el.x < -50:
                    bad_ship_list.pop(i)

                if big_planet_rect.colliderect(el):
                    gameplay = 1
                    bg_sound.stop()
                    bg_sound2.play(loops=-1)

        if control == 0:

            pygame.draw.rect(screen, 'green',
                             (sqr_x2, sqr_y2, sqr_x, sqr_y))

            pygame.draw.circle(screen, 'red', circle_pos, size)

            if sqr_x2 < list(pygame.mouse.get_pos())[0] < sqr_x2 + sqr_x and sqr_y2 < list(pygame.mouse.get_pos())[
                1] < sqr_y2 \
                    + sqr_y:
                circle_pos = pygame.mouse.get_pos()
            else:
                circle_pos = (sqr_x2 + sqr_x / 2, sqr_y2 + sqr_y / 2)
                pygame.draw.rect(screen, 'green',
                                 (sqr_x2, sqr_y2, sqr_x, sqr_y))
                pygame.draw.circle(screen, 'red', circle_pos, size)

            if list(circle_pos)[1] > round(sqr_y2 + sqr_y / 3 * 2):
                if players_ships_y < h - little_size[0] - 20:
                    players_ships_y += players_ships_speed
            if list(circle_pos)[1] < round(sqr_y2 + sqr_y / 3):
                if players_ships_y > 20:
                    players_ships_y -= players_ships_speed

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            if keys[pygame.K_UP] and players_ships_y > 20:
                up_True = 1
                players_ships_y -= players_ships_speed
            elif keys[pygame.K_DOWN] and players_ships_y < h - little_size[0] - 20:
                down_True = 1
                players_ships_y += players_ships_speed
        else:

            screen.blit(up_label, up_label_rect)
            screen.blit(down_label, down_label_rect)

            if color_up == 'blue':
                color_up = 'yellow'
            if color_down == 'blue':
                color_down = 'yellow'

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            if keys[pygame.K_UP] and players_ships_y > 20 or up_label_rect.collidepoint(mouse) and \
                    pygame.mouse.get_pressed()[0] and players_ships_y > 20:
                color_up = 'blue'
                players_ships_y -= players_ships_speed
            elif keys[pygame.K_DOWN] and players_ships_y < h - little_size[0] - 20 or \
                    down_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] and \
                    players_ships_y < h - little_size[0] - 20:
                color_down = 'blue'
                players_ships_y += players_ships_speed

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet[plain][bullet_choice], (el.x, el.y))
                if bullet_choice >= bullet_choice_max and not bullet_choice_stop:
                    bullet_choice = 0
                elif bullet_choice < bullet_choice_max:
                    bullet_choice += 1

                el.x += bullets_speed

                if el.x > 1700:
                    bullets.pop(i)

                if bad_ship_list:
                    for (index, bad_ship_el) in enumerate(bad_ship_list):
                        if el.colliderect(bad_ship_el):
                            bad_ship_list.pop(index)
                            bullets.pop(i)
                            score += 1

    elif gameplay == 1:

        if music_list2 == 1:
            bg_sound2.play(loops=-1)
            music_list2 = 0

        lose_label1 = label.render(f'твой рекорд {max(score_list)},', True,
                                   (247, 94, 59))
        lose_label2 = label.render(f'сейчас ты заработал {score}', True,
                                   (247, 94, 59))
        score_list.append(score)

        screen.blit(bg1, (0, 0))
        screen.blit(lose_label1, (20, 50))
        screen.blit(lose_label2, (20, 50 + 80))
        screen.blit(square_next, (next_label_x, next_label_y + 10))
        screen.blit(next_label, next_label_rect)

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if next_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]:
            gameplay = 3
            points += score

    elif gameplay == 2:
        screen.blit(bg1, (0, 0))
        screen.blit(square_out, (out_x, out_y + 10))
        screen.blit(out, out_rect)

        for i in range(len(all_ships)):
            if p_list[i] == '0':
                p_ship_rect = all_ships[i].get_rect(topleft=((20 + little_size[0]) * i, 400))
                screen.blit(all_ships[i], p_ship_rect)
            else:
                p_ship_rect = players_ships[i].get_rect(topleft=((20 + little_size[0]) * i, 400))
                screen.blit(players_ships[i], p_ship_rect)
                mouse = pygame.mouse.get_pos()
                keys = pygame.key.get_pressed()
                if p_ship_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                    gameplay = 3
                    plain = i

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if out_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = 3

    elif gameplay == 3:
        screen.blit(bg1, (0, 0))
        screen.blit(square_done, (done_label_x, done_label_y + 10))
        screen.blit(square_ship, (ship_label_x, ship_label_y + 10))
        players_ships_menu_rect = players_ships_menu[plain].get_rect(topleft=(500 // w_difference, 200 // w_difference))
        screen.blit(players_ships_menu[plain], players_ships_menu_rect)
        screen.blit(done_label, done_label_rect)
        screen.blit(ship_label, ship_label_rect)
        screen.blit(square_shop, (shop_label_x, shop_label_y + 10))
        screen.blit(shop, shop_label_rect)
        screen.blit(square_management, (management_label_x, management_label_y + 10))
        screen.blit(management, management_label_rect)

        if len(str(points)) >= 9:
            your_points = f'{str(points)[:8]}...'
        else:
            your_points = points

        points2 = label2.render(f'у тебя {your_points} очков', True,
                                (247, 94, 59))
        screen.blit(points2, (450 // w_difference, 30 // w_difference))  # 1540, 802

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if ship_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = 2

        mouse = pygame.mouse.get_pos()
        if management_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = 6

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if shop_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = 4

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if done_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]:
            gameplay = 0
            players_ships_x = 300
            players_ships_y = 360
            bad_ship_list.clear()
            bullets.clear()
            score = 0
            bg_sound2.stop()
            bg_sound.play(loops=-1)

    elif gameplay == 4:
        screen.blit(bg1, (0, 0))
        box = pygame.transform.scale(
            pygame.image.load(path + 'images/galactic_warships_images/boxes/box.png').
            convert_alpha(), (400 // w_difference, 400 // w_difference))
        box_rect = box.get_rect(topleft=(50 // w_difference, 225 // w_difference))
        screen.blit(box, box_rect)
        screen.blit(square_out, (out_x, out_y + 10))
        screen.blit(out, out_rect)
        box_cost = label2.render(f'бокс стоит {cost} очков', True,
                                 (247, 94, 59))
        screen.blit(box_cost, (0, (50 + 100) // w_difference))

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if out_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = 3

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if box_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] and points >= cost and p_listTrue != '1' \
                * len(p_list):
            ind = randint(1, len(p_list) - 1)
            while p_list[ind] != '0':
                ind = randint(1, len(p_list) - 1)
                b += 1
            b = 0
            p_list[ind] = '1'
            points -= cost
            gameplay = 5

    elif gameplay == 5:
        screen.blit(bg1, (0, 0))
        screen.blit(players_ships_menu[ind], (500, 200))
        screen.blit(square_next, (next_label_x + 1200, next_label_y + 10))
        screen.blit(next_label, (next_label_x + 1200, next_label_y))

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if next_label_rect2.collidepoint(mouse) and pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]:
            gameplay = 4

    elif gameplay == 6:
        screen.blit(bg1, (0, 0))

        screen.blit(square_joystick, (20, control_y + 10))
        screen.blit(joystick, joystick_rect)
        screen.blit(square_arrows, (470, control_y + 10))
        screen.blit(arrows, arrows_rect)
        screen.blit(square_out, (out_x, out_y + 10))
        screen.blit(out, out_rect)

        mouse = pygame.mouse.get_pos()
        if out_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = 3

        mouse = pygame.mouse.get_pos()
        if joystick_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            control = 0
            gameplay = 3
        elif arrows_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            control = 1
            gameplay = 3
    counter += 1
    if (time.time() - start_time) > time_int:
        fps = "FPS: " + str(int(counter / (time.time() - start_time)))
        counter = 0
        start_time = time.time()

    screen.blit(font.render(fps, True, (180, 0, 0)), (0, 0))

    pygame.display.update()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            with open(path + 'points.TXT', "w") as f:
                f.write(str(points))
            with open(path + 'plains.TXT', "w") as f:
                f.write(''.join(p_list))
            running = False
            pygame.quit()

        if gameplay == 0 and event.type == bad_ship_timer and stop_or_play == 0:
            bad_ship_list.append(bad_ship.get_rect(topleft=(1500, randint(20, h - 120))))

        if gameplay == 0 and event.type == bullet_timer and stop_or_play == 0:
            bullets.append(bullet[plain][bullet_choice].get_rect(
                topleft=(players_ships_x + little_size[0], players_ships_y + little_size[0] // 2 - 17 / 2)))