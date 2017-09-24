from kivy.app import App
from kivy.uix.widget import Widget


class PongGame(object):
    pass


class PongApp(App):
    def Build(self):
        return PongGame()


if __name__ == "__main__":
    PongApp().run()
