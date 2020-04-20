import random
import pyglet
from pyglet.window import key
from modules.game_object import GameObject
from modules.game_state import GameState
from modules.game_assets import GameAssets

from modules.player import Player
from modules.healthbar import HealthBar
from modules.infectionbar import InfectionBar
from modules.virus import Virus
from modules.virus_spawner import VirusSpawner
from modules.circle_collider import CircleCollider
from modules.polygon_collider import PolygonCollider

from modules import util


class StartScreen(GameObject):

    def __init__(self, game_state, game_assets, game_window, game_groups, *args, **kwargs):
        """
        Start Screen
        :param game_state:
        :param game_assets:
        :param args:
        :param kwargs:
        """
        self.img = [game_assets.image_assets["img_start_screen_A"],
               game_assets.image_assets["img_start_screen_B"]]
        super(StartScreen, self).__init__(img=self.img[0], *args, **kwargs)

        self.game_state = game_state
        self.game_assets = game_assets
        self.game_window = game_window
        self.game_groups = game_groups

        self.type = "ui"
        self.collider_type = None
        self.key_handler = key.KeyStateHandler()
        self.dead = False

    def update_object(self, dt):
        if self.key_handler[key.RIGHT]:
            self.image = self.img[1]
        if self.key_handler[key.LEFT]:
            self.image = self.img[0]
        if self.key_handler[key.ENTER]:
            self.game_state.game_level = 1
            self.load_stage_1()
            self.dead = True    # kill myself

    def load_stage_1(self):
        # background
        bkg = pyglet.sprite.Sprite(img=self.game_assets.image_assets["img_bkg"],
                                   x=0, y=0, batch=self.batch, group=self.game_groups[0])

        # player
        player = Player(self.game_state, self.game_assets, x=100, y=400,
                        batch=self.batch, group=self.game_groups[5])
        self.game_window.push_handlers(player)
        self.game_window.push_handlers(player.key_handler)

        # health bar
        health_bar = HealthBar(self.game_state, self.game_assets,
                               x=self.game_state.player_life, y=900,
                               batch=self.batch, group=self.game_groups[8])
        # infection bar
        infection_bar = InfectionBar(self.game_state, self.game_assets,
                                     x=self.game_state.infection_level, y=920,
                                     batch=self.batch, group=self.game_groups[8])

        # create a game level - collection of obstacles
        # cells = []
        # for i in range(5):
        #     cells.append(CircleCollider(state, assets, x=i*100, y=100, batch=main_batch, group=groups[5]))

        vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
        vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
        vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
        vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
        vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]

        # vertices1 = [0, 1000, 0, 600, 100, 600, 300, 800, 300, 1000]
        # vertices2 = [500, 1000, 600, 800, 700, 800, 1000, 600, 1000, 1000]
        # vertices3 = [500, 700, 300, 500, 400, 400, 700, 400, 700, 500]
        # vertices4 = [0, 0, 300, 0, 0, 300]
        # vertices5 = [500, 200, 500, 0, 1000, 0, 1000, 200, 900, 300]

        polygon1 = PolygonCollider(util.get_points(vertices1), self.game_state, self.game_assets, "poly1", group=self.game_groups[5])
        polygon2 = PolygonCollider(util.get_points(vertices2), self.game_state, self.game_assets, "poly2", group=self.game_groups[5])
        polygon3 = PolygonCollider(util.get_points(vertices3), self.game_state, self.game_assets, "poly3", group=self.game_groups[5])
        polygon4 = PolygonCollider(util.get_points(vertices4), self.game_state, self.game_assets, "poly4", group=self.game_groups[5])
        polygon5 = PolygonCollider(util.get_points(vertices5), self.game_state, self.game_assets, "poly5", group=self.game_groups[5])

        frg = pyglet.sprite.Sprite(img=self.game_assets.image_assets["img_frg"], x=0, y=0,
                                   batch=self.batch, group=self.game_groups[7])

        virus_spawner = VirusSpawner(self.game_state, self.game_assets, x=-5, y=0,
                                     batch=self.batch, group=self.game_groups[5])

        # list of all game objects
        self.child_objects.append(player)
        # self.child_objects.append(cells)
        self.child_objects.append(virus_spawner)
        self.child_objects.append(health_bar)
        self.child_objects.append(infection_bar)
        self.child_objects.append(polygon1)
        self.child_objects.append(polygon2)
        self.child_objects.append(polygon3)
        self.child_objects.append(polygon4)
        self.child_objects.append(polygon5)

    def handle_collision_with(self, other_object):
        self.dead = False