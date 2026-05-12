import random

from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

from functions import change_config, set_texture, ScoreDisplay, ImageButton, DrawImageButton, config, game_data, path


class StoreScreen(Screen):
    def __init__(self, **kwargs):
        Window.bind(on_resize=self.on_window_resize)
        super().__init__(**kwargs)
        Clock.schedule_interval(self.on_window_resize, 1/3)

        self.score_display = ScoreDisplay()
        self.add_widget(self.score_display)
        Clock.schedule_interval(self.score_display.animate_fire, 0.3)

        self.blit_box()

        self.update_button_sizes()
        self.back_button = DrawImageButton((self.button_width, self.button_height), (self.button_back_x, self.button_back_y), path + "images/buttons/back.png", on_press=self.on_back_button_press)
        self.add_widget(self.back_button)

    def on_window_resize(self, *args):
        self.update_box()
        
        self.score_display.update_display()

        self.update_button_sizes()
        self.back_button.update_image((self.button_width, self.button_height), (self.button_back_x, self.button_back_y))

    def update_button_sizes(self):
        self.button_height = Window.height / 7
        self.button_width = Window.width / 3

        self.button_x_padding = Window.width / 150
        self.button_y_padding = Window.height / 50

        self.button_back_x = Window.width - self.button_x_padding - self.button_width
        self.button_back_y = Window.height - (self.button_y_padding + self.button_height)

    def on_back_button_press(self, button):
        self.manager.current = 'menu'

    def update_box_settings(self):
        self.box_size = (Window.width / 3, Window.height / 2)
        self.box_padding = (0, (Window.height - self.box_size[1]) / 2)

    def blit_box(self):
        self.update_box_settings()

        tex = set_texture(path + f"images/boxes/mythic.png")

        box = ImageButton(
            texture = tex,
            size_hint = (None, None),
            size = self.box_size,
            pos = self.box_padding,
            allow_stretch = True,
            keep_ratio = False
        )

        box.bind(on_press=self.open_box)

        self.add_widget(box)
        self.box_layout = box

    def update_box(self):
        self.update_box_settings()
        if hasattr(self, "box_layout"):
            self.box_layout.texture = set_texture(path + f"images/boxes/mythic.png")
            self.box_layout.size = self.box_size
            self.box_layout.pos = self.box_padding

    def open_box(self, box):
        if game_data['points'] >= 100 and '0' in game_data['ships']:
            while True:
                new_ship = random.randint(0, len(game_data['ships']) - 1)
                if game_data['ships'][new_ship] == '0':
                    game_data['ships'][new_ship] = '1'
                    game_data['points'] -= 100
                    change_config(config, game_data)
                    break