import random

import pyglet
from pyglet.window import key

from modules.game_object import GameObject
from modules import util


class VirusParticle(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        :param game_state:
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_virus_particle"]]
        # TODO make this a sprite later
        super(VirusParticle, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state                # game state object
        self.type = "virus_particle"                # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = None

        self.move_step = 0.5     # Distance by which to move in each key press
        self.velocity_x = 0
        self.velocity_y = 0

    def create_infection(self):
        pass

    def update_object(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "virus":
            self.dead = False   # no friendly fire
        elif other_object.type == "player":
            self.dead = True    # kill myself
        elif other_object.type == "bullet":
            self.game_state.increase_score_by(self.game_state.score_inc_virus_particle_killed)
            self.dead = True  # kill myself


