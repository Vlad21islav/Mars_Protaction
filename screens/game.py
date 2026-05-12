import random
import time

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from functions import change_config, set_texture, ScoreDisplay, DrawImageButton, config, game_data, path


class GameScreen(Screen):
    def __init__(self, **kwargs):
        self.update_positions()

        self.touch_active = False
        self.touch_direction = 0
        self.move_event = None
        self.game_started = False

        self.texture_cache = {}

        Window.bind(on_resize=self.on_window_resize)
        super().__init__(**kwargs)
        Clock.schedule_interval(self.cycle, 1/60)
        Window.bind(on_key_down=self.on_key_down)
        if platform != 'win' and platform != 'linux' and platform != 'macosx':
            Window.bind(on_touch_down=self.on_touch_start)
            Window.bind(on_touch_up=self.on_touch_end)
        Clock.schedule_interval(self.on_window_resize, 1/3)

        self.mars = DrawImageButton((Window.width // 14, Window.height), (0, 0), path + "images/planets/planet_red_big.png")
        self.add_widget(self.mars)

        self.blit_ship()
        self.blit_bad_ships()
        self.blit_bullets()

        self.score_display = ScoreDisplay()
        self.add_widget(self.score_display)
        Clock.schedule_interval(self.score_display.animate_fire, 0.3)

    def on_window_resize(self, *args):
        self.mars.update_image((Window.width // 14, Window.height), (0, 0))

        self.update_ship()

        self.score_display.update_display()

    def update_positions(self):
        self.ship_y = 50
        bad_planes_count = 5
        self.bad_planes = [[500 // bad_planes_count * i, random.randint(0, 100)] for i in range(0, bad_planes_count)]
        self.bullet_queue = 0
        bullets_count = 10
        self.bullets = [[0, -30] for i in range(0, bullets_count)]
        self.last_spawn_time = time.time()
        self.last_move_time = time.time()

    def cycle(self, dt):
        if self.game_started:
            if time.time() - self.last_spawn_time > 3:
                self.bullets[self.bullet_queue] = [0, self.ship_y]
                if self.bullet_queue == len(self.bullets) - 1:
                    self.bullet_queue = 0
                else:
                    self.bullet_queue += 1
                self.last_spawn_time = time.time()
                self.update_bullets()

            for _ in range(int((time.time() - self.last_move_time) / 0.01)):
                for bullet in self.bullets:
                    if bullet != [0, -30]:
                        bullet[0] += 1
                for pos in self.bad_planes:
                    if pos[0] > 1000:
                        pos[0] = 500
                        self.game_started = False
                        self.manager.current = 'menu'
                    pos[0] += 1
                for bullet_pos in self.bullets:
                    for ship_pos in self.bad_planes:
                        if self.check_collision(ship_pos, bullet_pos):
                            ship_pos[0] = 500
                            ship_pos[1] = random.randint(0, 100)
                            bullet_pos[0] = 0
                            bullet_pos[1] = -30
                            game_data['points'] += 1
                            change_config(config, game_data)
                            self.score_display.update_display(game_data['points'])
                self.last_move_time = time.time()
                self.update_bad_ships()
                self.update_bullets()


    def check_collision(self, ship_pos, bullet_pos):
        self.update_ship_settings()
        self.update_bullets_settings()
        bullet_pos = (bullet_pos[0] + self.ship_padding[0] + ((Window.width - self.ship_size[0] - self.ship_padding[0]) / 1000 * bullet_pos[0]), Window.height / 100 * bullet_pos[1])
        ship_pos = (2 * Window.width -  2 * Window.width / 1000 * ship_pos[0], Window.height - Window.height / 100 * ship_pos[1])
        if (abs((ship_pos[1] + self.bad_ship_size[1] // 2) - (bullet_pos[1] + self.bullet_size[1] // 2)) <= self.bad_ship_size[1] // 2 + self.bullet_size[1] // 2) and \
            (bullet_pos[0] >= ship_pos[0]):
            return True
        return False

    def update_ship_settings(self):
        self.ship_size = (Window.width / 10, Window.height / 5)
        self.ship_padding = (Window.width / 4, Window.height / 100 * self.ship_y)

    def blit_ship(self):
        self.update_ship_settings()

        tex = set_texture(path + f"images/planes/plane{game_data['selected_ship']}.png")

        ship = Image(
            texture = tex,
            size_hint = (None, None),
            size = self.ship_size,
            pos = self.ship_padding,
            allow_stretch = True,
            keep_ratio = False
        )

        self.add_widget(ship)
        self.ship_layout = ship

    def update_ship(self):
        self.update_ship_settings()
        if hasattr(self, "ship_layout"):
            self.ship_layout.texture = set_texture(path + f"images/planes/plane{game_data['selected_ship']}.png")
            self.ship_layout.size = self.ship_size
            self.ship_layout.pos = self.ship_padding

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        scancode = int(scancode)
        if scancode == 26 or scancode == 82:
            self.controle_ship(1)
        elif scancode == 22 or scancode == 81:
            self.controle_ship(-1)

    def controle_ship(self, direction):
        self.update_ship_settings()
        if direction == 1:
            self.ship_y += 1 and self.ship_y < 100 - (self.ship_size[1] / Window.height * 100)
        elif direction == -1 and self.ship_y > 0:
            self.ship_y -= 1
        self.update_ship()

    def on_touch_start(self, window, touch):
        self.touch_active = True
        screen_center = Window.height / 2
        
        if touch.y > screen_center:
            self.touch_direction = 1
        else:
            self.touch_direction = -1
        if self.move_event:
            self.move_event.cancel()
        self.move_event = Clock.schedule_interval(self.continuous_move, 1/20)
    
    def on_touch_end(self, window, touch):
        self.touch_direction = 0
        if self.move_event:
            self.move_event.cancel()
            self.move_event = None
    
    def continuous_move(self, dt):
        if self.touch_direction != 0:
            self.controle_ship(self.touch_direction)

    def update_bad_ships_settings(self):
        self.bad_ship_size = (Window.width / 10, Window.height / 10)

    def blit_bad_ships(self):
        self.update_bad_ships_settings()
        if hasattr(self, "bad_ship_layout"):
            self.remove_widget(self.bad_ship_layout)
        layout = FloatLayout()
        for ship in self.bad_planes:
            tex = set_texture(path + "images/bad_plane.png")

            bad_ship = Image(
                texture = tex,
                size_hint = (None, None),
                size = self.bad_ship_size,
                pos = (2 * Window.width -  2 * Window.width / 1000 * ship[0], Window.height - Window.height / 100 * ship[1]),
                allow_stretch = True,
                keep_ratio = False
            )

            layout.add_widget(bad_ship)
        self.add_widget(layout)
        self.bad_ship_layout = layout

    def update_bad_ships(self):
        self.update_bad_ships_settings()
        if hasattr(self, "bad_ship_layout"):
            for i, ship in enumerate(self.bad_ship_layout.children):
                ship.size = self.bad_ship_size
                ship.pos = (2 * Window.width -  2 * Window.width / 1000 * self.bad_planes[len(self.bad_planes) - i - 1][0], Window.height - Window.height / 100 * self.bad_planes[len(self.bad_planes) - i - 1][1])

    def update_bullets_settings(self):
        self.bullet_size = (Window.width / 25, Window.height / 25)

    def blit_bullets(self):
        self.update_bullets_settings()
        if hasattr(self, "bullet_layout"):
            self.remove_widget(self.bullet_layout)
        layout = FloatLayout()
        for ship in self.bullets:
            tex = set_texture(path + f"images/bullets/bullet{game_data['selected_ship']}.png")

            bullet = Image(
                texture = tex,
                size_hint = (None, None),
                size = self.bullet_size,
                pos = (self.ship_padding[0] + ((Window.width - self.ship_size[0] - self.ship_padding[0]) / 1000 * ship[0]), Window.height / 100 * ship[1]),
                allow_stretch = True,
                keep_ratio = False
            )

            layout.add_widget(bullet)
        self.add_widget(layout)
        self.bullet_layout = layout

    def update_bullets(self):
        self.update_bullets_settings()
        if hasattr(self, "bullet_layout"):
            for i, ship in enumerate(self.bullet_layout.children):
                ship.texture = set_texture(path + f"images/bullets/bullet{game_data['selected_ship']}.png")
                ship.size = self.bullet_size
                ship.pos = (self.ship_padding[0] + ((Window.width - self.ship_size[0] - self.ship_padding[0]) / 1000 * self.bullets[len(self.bullets) - i - 1][0]), Window.height / 100 * self.bullets[len(self.bullets) - i - 1][1])
