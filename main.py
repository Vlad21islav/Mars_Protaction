from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import platform

from functions import path

from screens.menu import MenuScreen
from screens.ships import ShipsScreen
from screens.store import StoreScreen
from screens.game import GameScreen


if platform == 'win' or platform == 'linux' or platform == 'macosx':
    Window.size = (900, 450)


class GameApp(App):
    def build(self):
        return Builder.load_file(path + 'game.kv')


if __name__ == '__main__':
    GameApp().run()