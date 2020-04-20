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

class LevelHandler(GameObject):

    def __init__(self, game_state, game_assets, game_window, game_groups, *args, **kwargs):
        """
        Start Screen
        :param game_state:
        :param game_assets:
        :param args:
        :param kwargs:
        """
        super(LevelHandler, self).__init__(img=game_assets.image_assets["img_dummy"], *args, **kwargs)

        self.game_state = game_state
        self.game_assets = game_assets
        self.game_window = game_window
        self.game_groups = game_groups

        self.type = "level_handler"
        self.collider_type = None
        self.key_handler = key.KeyStateHandler()
        self.dead = False

        # initialize dummy background and foreground
        self.game_state.bkg = GameObject(img=self.game_assets.image_assets["img_dummy"],
                                         x=-1, y=-1, batch=self.batch, group=self.game_groups[0])
        self.game_state.frg = GameObject(img=self.game_assets.image_assets["img_dummy"],
                                         x=-1, y=-1, batch=self.batch, group=self.game_groups[7])

    def update_object(self, dt):
        if self.game_state.game_level == -1:
            self.handle_game_launch()
        elif self.game_state.game_level == 0:
            self.handle_start_screen()
        elif self.game_state.game_level >0:
            self.handle_levels()

    def handle_game_launch(self):
        self.game_state.frg.image = self.game_assets.image_assets["img_start_screen_A"]
        self.game_state.frg.x = 500
        self.game_state.frg.y = 500
        self.game_state.game_level = 0

    def handle_start_screen(self):
        if self.key_handler[key.RIGHT]:
            self.game_state.frg.image = self.game_assets.image_assets["img_start_screen_B"]
            self.game_state.frg.x = 500
            self.game_state.frg.y = 500
        if self.key_handler[key.LEFT]:
            self.game_state.frg.image = self.game_assets.image_assets["img_start_screen_A"]
            self.game_state.frg.x = 500
            self.game_state.frg.y = 500
        if self.key_handler[key.ENTER]:
            self.game_state.game_level = 1
            self.load_stage_1()

    def handle_levels(self):
        if self.key_handler[key.N]:
            # delete existing game objects
            self.game_state.game_level = 2
            print("N key pressed")
            self.load_stage_2()

    def load_stage_1(self):
        # background and foreground
        self.game_state.bkg = GameObject(img=self.game_assets.image_assets["img_bkg_level_1"],
                         x=0, y=0, batch=self.batch, group=self.game_groups[0])
        self.game_state.frg = GameObject(img=self.game_assets.image_assets["img_frg_level_1"], x=0, y=0,
                         batch=self.batch, group=self.game_groups[7])

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

        # virus spawner
        virus_spawner = VirusSpawner(self.game_state, self.game_assets, x=-5, y=0,
                                     batch=self.batch, group=self.game_groups[5])

        # stage - polygon colliders
        vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
        vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
        vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
        vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
        vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]

        polygon1 = PolygonCollider(util.get_points(vertices1), self.game_state,
                                   self.game_assets, "poly1", group=self.game_groups[5])
        polygon2 = PolygonCollider(util.get_points(vertices2), self.game_state,
                                   self.game_assets, "poly2", group=self.game_groups[5])
        polygon3 = PolygonCollider(util.get_points(vertices3), self.game_state,
                                   self.game_assets, "poly3", group=self.game_groups[5])
        polygon4 = PolygonCollider(util.get_points(vertices4), self.game_state,
                                   self.game_assets, "poly4", group=self.game_groups[5])
        polygon5 = PolygonCollider(util.get_points(vertices5), self.game_state,
                                   self.game_assets, "poly5", group=self.game_groups[5])

        # list of all game objects
        self.child_objects.append(self.game_state.bkg)
        self.child_objects.append(self.game_state.frg)

        self.child_objects.append(player)
        self.child_objects.append(virus_spawner)

        self.child_objects.append(health_bar)
        self.child_objects.append(infection_bar)

        self.child_objects.append(polygon1)
        self.child_objects.append(polygon2)
        self.child_objects.append(polygon3)
        self.child_objects.append(polygon4)
        self.child_objects.append(polygon5)

    def load_stage_2(self):
        # background and foreground
        self.game_state.bkg = GameObject(img=self.game_assets.image_assets["img_bkg_level_2"],
                         x=0, y=0, batch=self.batch, group=self.game_groups[0])
        self.game_state.frg = GameObject(img=self.game_assets.image_assets["img_frg_level_2"], x=0, y=0,
                         batch=self.batch, group=self.game_groups[7])

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

        # virus spawner
        virus_spawner = VirusSpawner(self.game_state, self.game_assets, x=-5, y=0,
                                     batch=self.batch, group=self.game_groups[5])

        # stage - polygon colliders
        vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
        vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
        vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
        vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
        vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]

        polygon1 = PolygonCollider(util.get_points(vertices1), self.game_state,
                                   self.game_assets, "poly1", group=self.game_groups[5])
        polygon2 = PolygonCollider(util.get_points(vertices2), self.game_state,
                                   self.game_assets, "poly2", group=self.game_groups[5])
        polygon3 = PolygonCollider(util.get_points(vertices3), self.game_state,
                                   self.game_assets, "poly3", group=self.game_groups[5])
        polygon4 = PolygonCollider(util.get_points(vertices4), self.game_state,
                                   self.game_assets, "poly4", group=self.game_groups[5])
        polygon5 = PolygonCollider(util.get_points(vertices5), self.game_state,
                                   self.game_assets, "poly5", group=self.game_groups[5])

        # list of all game objects
        self.child_objects.append(self.game_state.bkg)
        self.child_objects.append(self.game_state.frg)

        self.child_objects.append(player)
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



# level one
vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]


# level two
vertices1 = [403, 0, 343, 122, 173, 46, 151, 1]
vertices2 = [600, 58, 660, 0, 1001, 0, 998, 35, 656, 167]
vertices3 = [1001, 730, 795, 555, 739, 379, 871, 275, 1001, 275]
vertices4 = [1, 742, 0, 193, 170, 269, 204, 500, 123, 701]
vertices5 = [289, 1001, 374, 696, 626, 657, 730, 865, 657, 1000]

# level three
vertices1 = [449, 252, 241, 209, 0, 239, 0, 0, 509, 0]
vertices2 = [1001, 404, 889, 352, 815, 145, 830, 0, 1001, 0]
vertices3 = [187, 601, 286, 489, 440, 532, 591, 509, 652, 627, 600, 739, 320, 742]
vertices4 = [699, 910, 864, 889, 977, 793, 1001, 799, 1001, 1001, 784, 1001]
