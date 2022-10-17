from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.lang.builder import Builder
from kivy import platform
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, Clock
import random

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from transfrom import transfrom, transfrom_2D, transfrom_3D
    from keys import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    v_line = 12
    v_line_spacing = .6
    vertical_lines = []

    H_line = 8
    H_line_spacing = .3
    Horizontal_lines = []

    speed = 1.5
    current_offset_y = 0
    current_y_loop = 0
    score = 0
    high_score = 0
    #scr = 0

    speed_x = 2
    current_speed_x = 0
    current_offset_x = 0

    N_tiles = 6
    tiles = []
    tiles_coordinates = []



    ship = None
    SHIP_HEIGHT = 0.035
    SHIP_WIDTH = .1
    SHIP_BASE = 0.04
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    game_over = False
    game_started = False

    menu_title = StringProperty("G   A   L   E   X   Y")
    menu_title_btn = StringProperty("START")

    bg_title = StringProperty("images/bg 1.jpg")

    score_txt = StringProperty()
    high_score_txt = StringProperty()


    sound_begin  =None
    sound_galexy = None
    sound_gameover_impact = None
    sound_gameover = None
    sound_music = None
    sound_restart = None

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_audio()
        self.init_vertical_line()
        self.init_horizontal_line()
        self.init_tiles()
        self.init_ship()
        self.restart_game()

        #if self.is_desktop():
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.sound_galexy.play()
        self.score += 1

    def init_audio(self):
        self.sound_begin = SoundLoader.load("audio/begin.wav")
        self.sound_galexy = SoundLoader.load("audio/galaxy.wav")
        self.sound_music = SoundLoader.load("audio/music1.wav")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.wav")
        self.sound_gameover = SoundLoader.load("audio/gameover_voice.wav")
        self.sound_restart = SoundLoader.load("audio/restart.wav")
        self.btn_click = SoundLoader.load("audio/btn_click.mp3")

        self.sound_music.volume = 1
        self.sound_begin.volume = .30
        self.sound_galexy.volome = .40
        self.sound_gameover_impact.volume = .5
        self.sound_gameover.volume = .7
        self.sound_restart.volume= .6
        self.btn_click.volume= .9


    def restart_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.tiles_coordinates = []
        self.score = 0
        self.score_txt = " SCORE:" + str(self.score)
        self.start_tiles()
        self.genarate_tiles_coordinate()
        self.game_over = False

    def is_desktop(self):
        if platform in ('linux', 'windows', 'macosx'):
            return True
        return

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 1)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width / 2
        base_y = self.SHIP_BASE * self.height
        ship_half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height
        #
        #    2
        #
        # 1     3
        self.ship_coordinates[0] = (center_x - ship_half_width, base_y)
        self.ship_coordinates[1] = (center_x, base_y + ship_height)
        self.ship_coordinates[2] = (center_x + ship_half_width, base_y)

        x1, y1 = self.transfrom(*self.ship_coordinates[0])
        x2, y2 = self.transfrom(*self.ship_coordinates[1])
        x3, y3 = self.transfrom(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def cheak_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.cheak_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def cheak_ship_collision_with_tile(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_coordinate(ti_x, ti_y)
        xmax, ymax = self.get_tile_coordinate(ti_x + 1, ti_y + 1)
        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.N_tiles):
                self.tiles.append(Quad())

    def start_tiles(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def genarate_tiles_coordinate(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.N_tiles):
            r = random.randint(0, 2)
            start_index = -int(self.v_line / 2) + 1
            end_index = start_index + self.v_line - .63
            if last_x <= start_index:
                r = 1
            if last_x >= end_index - 1:
                r = 2

            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def init_vertical_line(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.v_line):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        center_line_x = self.perspective_point_x
        spacing = self.v_line_spacing * self.width
        offset = index - 0.5
        line_x = center_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_line_spacing * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinate(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.N_tiles):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tile_coordinate(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_coordinate(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            # 2    3
            #
            # 1     4
            x1, y1 = self.transfrom(xmin, ymin)
            x2, y2 = self.transfrom(xmin, ymax)
            x3, y3 = self.transfrom(xmax, ymax)
            x4, y4 = self.transfrom(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_line(self):
        # -1,0,1,2
        start_index = -int(self.v_line / 2) + 1
        for i in range(start_index, start_index + self.v_line):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transfrom(line_x, 0)
            x2, y2 = self.transfrom(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_line(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_line):
                self.Horizontal_lines.append(Line())

    def update_horizontal_line(self):
        start_index = -int(self.v_line / 2) + 1
        end_index = start_index + self.v_line - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.H_line):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transfrom(xmin, line_y)
            x2, y2 = self.transfrom(xmax, line_y)
            self.Horizontal_lines[i].points = [x1, y1, x2, y2]

    def button_click_sound(self,dt):
        self.btn_click.play()

    def User_speed(self, instance):
        if instance.text == 'Hard':
            Clock.schedule_once(self.button_click_sound, .001)
            self.bg_title = "images/bg 2.jpg"
            self.speed = 2.1
        elif instance.text == 'Medium':
            Clock.schedule_once(self.button_click_sound, .001)
            self.bg_title = "images/bg 1.jpg"
            self.speed = 1.6
        elif instance.text == 'Easy':
            Clock.schedule_once(self.button_click_sound, .001)
            self.bg_title = "images/bg 3.jpg"
            self.speed = 1.3


    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            return self.high_score
        else:
            return self.high_score

    def update(self, dt):
        time_factor = dt * 60
        self.update_vertical_line()
        self.update_horizontal_line()
        self.update_tiles()
        self.update_ship()

        if not self.game_over and self.game_started:
            speed_y = self.speed * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = self.H_line_spacing * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score += 1
                self.score_txt = " SCORE : " + str(self.score)
                self.genarate_tiles_coordinate()
            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor

        if not self.cheak_ship_collision() and not self.game_over:
            self.game_over = True
            self.menu_title ="G  A  M  E O  V  E  R"
            self.menu_title_btn = "RESTART"
            self.menu_widget.opacity = 1
            high_score = self.update_score()
            self.high_score_txt = "  HIGH SCORE : " + str(high_score)
            self.sound_music.stop()
            self.sound_gameover_impact.play()
            Clock.schedule_once(self.game_over_sound, .2)
    def game_over_sound(self,dt):
        self.sound_gameover.play()

    def on_menu_button_press(self):
        if self.game_over:
            self.sound_restart.play()
        else:
            self.sound_begin.play()
        self.restart_game()
        self.game_started = True
        self.menu_widget.opacity = 0
        self.sound_music.play()

class GalaxyApp(App):
    pass


GalaxyApp().run()
