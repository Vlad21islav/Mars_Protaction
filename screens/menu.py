from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from functions import set_texture, ScoreDisplay, DrawImageButton, path, game_data


class MenuScreen(Screen):
    def __init__(self, **kwargs): 
        Window.bind(on_resize=self.on_window_resize)
        super().__init__(**kwargs)
        Clock.schedule_interval(self.on_window_resize, 1/3)

        self.score_display = ScoreDisplay()
        self.add_widget(self.score_display)
        Clock.schedule_interval(self.score_display.animate_fire, 0.3)

        self.blit_chosen_ship()

        self.update_button_sizes()
        self.ships_button = DrawImageButton((self.button_width, self.button_height), (self.button_ships_x, self.button_ships_y), path + "images/buttons/ships.png", on_press=self.on_ships_button_press)
        self.add_widget(self.ships_button)
        self.store_button = DrawImageButton((self.button_width, self.button_height), (self.button_store_x, self.button_store_y), path + "images/buttons/store.png", on_press=self.on_store_button_press)
        self.add_widget(self.store_button)
        self.play_button = DrawImageButton((self.button_width, self.button_height), (self.button_play_x, self.button_play_y), path + "images/buttons/play.png", on_press=self.on_play_button_press)
        self.add_widget(self.play_button)

    def on_window_resize(self, *args):
        self.score_display.update_display()

        self.update_chosen_ship()

        self.update_button_sizes()
        self.ships_button.update_image((self.button_width, self.button_height), (self.button_ships_x, self.button_ships_y))
        self.store_button.update_image((self.button_width, self.button_height), (self.button_store_x, self.button_store_y))
        self.play_button.update_image((self.button_width, self.button_height), (self.button_play_x, self.button_play_y))
        

    def update_button_sizes(self):
        self.button_height = Window.height / 7
        self.button_width = Window.width / 3

        self.button_x_padding = Window.width / 150
        self.button_y_padding = Window.height / 50

        self.button_ships_x = self.button_x_padding
        self.button_ships_y = Window.height - (self.button_y_padding + self.button_height)

        self.button_store_x = self.button_x_padding
        self.button_store_y = Window.height - 2 * (self.button_y_padding + self.button_height)

        self.button_play_x = Window.width - self.button_x_padding - self.button_width
        self.button_play_y = self.button_y_padding

    def on_ships_button_press(self, button):
        self.manager.current = 'ships'
    
    def on_store_button_press(self, button):
        self.manager.current = 'store'
    
    def on_play_button_press(self, button):
        self.manager.current = 'game'
        self.manager.get_screen('game').update_positions()
        self.manager.get_screen('game').game_started = True

    def update_chosen_ship_settings(self):
        self.chosen_ship_size = (Window.width / 4, Window.height / 2)
        self.chosen_ship_padding = (Window.width - Window.width / 150 - Window.width / 3, Window.height - (Window.height / 7 + self.chosen_ship_size[1]))

    def blit_chosen_ship(self):
        
        self.update_chosen_ship_settings()

        tex = set_texture(path + f"images/planes/plane{game_data['selected_ship']}.png")

        ship = Image(
            texture = tex,
            size_hint = (None, None),
            size = self.chosen_ship_size,
            pos = self.chosen_ship_padding,
            allow_stretch = True,
            keep_ratio = False
        )

        self.add_widget(ship)
        self.ship_layout = ship
    
    def update_chosen_ship(self):
        self.update_chosen_ship_settings()
        if hasattr(self, "ship_layout"):
            self.ship_layout.texture = set_texture(path + f"images/planes/plane{game_data['selected_ship']}.png")
            self.ship_layout.size = self.chosen_ship_size
            self.ship_layout.pos = self.chosen_ship_padding