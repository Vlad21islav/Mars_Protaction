import configparser
import os
import random
import sys

from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.utils import platform

def update_config():
    """Возвращает конфиг из файла или создаёт его, если он не существует"""
    config = configparser.ConfigParser()

    if not os.path.exists(config_path + 'config.ini'):
        config['player'] = {
            'opened_planes': '1000000000',
            'points': '0',
            'chosen_ship': '0'
        }
        with open(config_path + 'config.ini', 'w') as f:
            config.write(f)
    else:
        config.read(config_path + 'config.ini')

    return config

def change_config(config, game_data):
    """Сохранение конфига"""
    config.set('player', 'opened_planes', ''.join(game_data['ships']))
    config.set('player', 'points', str(game_data['points']))
    config.set('player', 'chosen_ship', str(game_data['selected_ship']))
    
    with open(config_path + 'config.ini', 'w') as f:
        config.write(f)

def set_texture(image_path):
    """Загрузка текстуры с отключёнными фильтрами для пиксельной графики"""
    button_texture = CoreImage(image_path).texture
    button_texture.min_filter = 'nearest'
    button_texture.mag_filter = 'nearest'
    return button_texture

def get_config_dir():
    if hasattr(sys, '_MEIPASS'):
        save_dir = os.path.join(os.environ['APPDATA'], 'MarsProtection')
    else:
        save_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    return save_dir


class ScoreDisplay(Widget):
    """Отдельный виджет для отображения счёта"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.number_widgets = []
        self.fire_widget = None
        
        # Кэшируем текстуры цифр
        self.number_textures = {}
        self.load_number_textures()
        
        # Текстуры огня
        self.fire_textures = []
        self.load_fire_textures()
        
        # Обновляем отображение
        self.update_display()
    
    def load_number_textures(self):
        """Загрузка всех текстур цифр один раз"""
        for i in range(10):
            self.number_textures[str(i)] = set_texture(path + f"images/numbers/{i}.png")
    
    def load_fire_textures(self):
        """Загрузка текстур огня"""
        for i in range(2):
            tex = set_texture(path + f"images/numbers/fire{i + 1}.png")
            self.fire_textures.append(tex)
    
    def update_display(self, score=None):
        """Обновление отображения счёта"""
        self.clear_widgets()
        self.number_widgets.clear()
        
        # Настраиваем размеры
        number_width = Window.width / 80
        number_height = Window.height / 20
        number_padding = Window.width / 150
        start_x = Window.width / 50
        start_y = Window.height / 25
        
        # Создаём цифры
        if score is None:
            score = game_data['points']
        points_str = str(score)
        for i, digit in enumerate(points_str):
            number = Image(
                texture=self.number_textures[digit],
                size_hint=(None, None),
                size=(number_width, number_height),
                pos=(start_x + i * (number_width + number_padding), start_y),
                allow_stretch=True,
                keep_ratio=False
            )
            self.add_widget(number)
            self.number_widgets.append(number)
        
        # Добавляем огонь
        fire_width = Window.width / 40
        fire_height = Window.height / 15
        fire_y = Window.height / 25
        
        self.fire_widget = Image(
            texture=random.choice(self.fire_textures),
            size_hint=(None, None),
            size=(fire_width, fire_height),
            pos=(fire_width + (number_padding + number_width) * len(points_str), fire_y),
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.fire_widget)
    
    def animate_fire(self, dt):
        """Анимация огня"""
        if self.fire_widget:
            self.fire_widget.texture = random.choice(self.fire_textures)


class ImageButton(ButtonBehavior, Image):
    pass


class DrawImageButton(Widget):
    """Быстрое рисование изображения"""
    def __init__(self, size: tuple[int], pos: tuple[int], image_path: str, on_press = None, **kwargs):
        self.image_path = image_path
        self.size = size
        self.pos = pos
        self.on_press = on_press

        super().__init__(**kwargs)

        self.blit_image()

    def blit_image(self):
        tex = set_texture(self.image_path)

        image = ImageButton(
            texture = tex,
            size_hint = (None, None),
            size = self.size,
            pos = self.pos,
            allow_stretch = True,
            keep_ratio = False
        )

        if self.on_press:
            image.bind(on_press=self.on_press)

        self.add_widget(image)
        self.image_layout = image
    
    def update_image(self, size: tuple[int], pos: tuple[int], image_path: str = None):
        if not image_path:
            image_path = self.image_path
        if hasattr(self, "image_layout"):
            self.image_layout.texture = set_texture(image_path)
            self.image_layout.size = size
            self.image_layout.pos = pos


if platform == 'win':
    path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))).replace("\\", "/") + "/"
    config_path = get_config_dir().replace("\\", "/") + "/"
else:
    path = ''
    config_path = ''

config = update_config()
game_data = {
    'ships': list(config.get('player', 'opened_planes')),
    'points': config.getint('player', 'points'),
    'selected_ship': config.getint('player', 'chosen_ship')
}
