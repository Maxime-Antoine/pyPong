from random import randint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window


class PongApp(App):

    def build(self):
        game = PongGame()
        game.serve_ball(angle=0)
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


class PongGame(Widget):

    reserve_delay = 1 # sec
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._waiting_for_new_ball = False

    def update(self, dt):
        self.ball.move()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # went of to a side to score point?
        if not self._waiting_for_new_ball:
            if self.ball.x < 0:
                self._player2_scored()
            if self.ball.x > self.width:
                self._player1_scored()

    def serve_ball(self, velocity=(4, 0), angle=None):
        self.ball.center = self.center
        angle = randint(0, 60) if angle is None else angle
        self.ball.velocity = Vector(velocity).rotate(angle)
        self._waiting_for_new_ball = False

    def _player1_scored(self):
        self._waiting_for_new_ball = True
        self.player1.score += 1
        Clock.schedule_once(lambda _: self.serve_ball(velocity=(-4, 0)), self.reserve_delay)

    def _player2_scored(self):
        self._waiting_for_new_ball = True
        self.player2.score += 1
        Clock.schedule_once(lambda _: self.serve_ball(velocity=(4, 0)), self.reserve_delay)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'q':
            self.player1.center_y += 30
        if keycode[1] == 'a':
            self.player1.center_y -= 30
        if keycode[1] == 'up':
            self.player2.center_y += 30
        if keycode[1] == 'down':
            self.player2.center_y -= 30
        return True


class PongBall(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


if __name__ == "__main__":
    PongApp().run()
