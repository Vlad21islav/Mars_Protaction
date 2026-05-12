from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

from functions import change_config, set_texture, ImageButton, DrawImageButton, config, game_data, path


class ShipsScreen(Screen):
    def __init__(self, **kwargs):
        Window.bind(on_resize=self.on_window_resize)
        super().__init__(**kwargs)
        Clock.schedule_interval(self.on_window_resize, 1/3)

        self.blit_ships()

        self.update_button_sizes()
        self.back_button = DrawImageButton((self.button_width, self.button_height), (self.button_back_x, self.button_back_y), path + "images/buttons/back.png", on_press=self.on_back_button_press)
        self.add_widget(self.back_button)

    def on_window_resize(self, *args):
        self.update_ships()
        
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

    def update_ships_settings(self):
        self.ships_size = (Window.width / 10, Window.height / 5)
        self.ships_padding_x = Window.width / 150
        self.ships_padding_y = Window.height / 50

    def blit_ships(self):
        layout = FloatLayout()
        self.update_ships_settings()

        for i in range(len(game_data['ships'])):
            image = path + f"images/{'planes' if int(game_data['ships'][len(game_data['ships']) - i - 1]) else 'gray'}/plane{len(game_data['ships']) - i - 1}.png"
            tex = set_texture(image)

            ship = ImageButton(
                texture = tex,
                size_hint = (None, None),
                size = self.ships_size,
                pos = (self.ships_padding_x + (self.ships_size[0] + self.ships_padding_x) * (i % 5), Window.height - (self.ships_size[1] + self.ships_padding_y) * ((i // 5) + 1)),
                allow_stretch = True,
                keep_ratio = False
            )
            ship.bind(on_press=self.select_ship)

            layout.add_widget(ship)

        self.add_widget(layout)
        self.ships_layout = layout

    def select_ship(self, ship):
        if int(game_data['ships'][self.ships_layout.children.index(ship)]):
            game_data['selected_ship'] = self.ships_layout.children.index(ship)
            change_config(config, game_data)
            self.manager.current = 'menu'

    def update_ships(self):
        self.update_ships_settings()
        if hasattr(self, "ships_layout"):
            for i, ship in enumerate(self.ships_layout.children):
                ship.texture = set_texture(path + f"images/{'planes' if int(game_data['ships'][i]) else 'gray'}/plane{i}.png")
                ship.size = self.ships_size
                ship.pos = (self.ships_padding_x + (self.ships_size[0] + self.ships_padding_x) * (i % 5), Window.height - (self.ships_size[1] + self.ships_padding_y) * ((i // 5) + 1))
