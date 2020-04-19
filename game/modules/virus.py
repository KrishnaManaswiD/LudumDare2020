import random

import pyglet
from pyglet.window import key

from modules.game_object import GameObject
from modules.virus_particle import VirusParticle
from modules import util


class Virus(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        :param game_state:
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_virus"]]
        # TODO make this a sprite later
        super(Virus, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state                # game state object
        self.game_assets = game_assets
        self.type = "virus"                         # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = None

        self.life = 100     # life of the virus

        self.move_step = 0.5     # Distance by which to move in each key press
        pyglet.clock.schedule_interval(self.release_particle, 7)

    def release_particle(self, dt):
        particle = VirusParticle(self.game_state, self.game_assets, x=self.x, y=self.y, batch=self.batch, group=self.group)
        particle.velocity_x = random.randrange(-50,50)
        particle.velocity_y = random.randrange(-50,50)
        self.child_objects.append(particle)

    def inflict_damage(self, amount):
        """
        Inflicts damage to the object. If the life of the object reaches 0, the object dies.
        :param amount: amount of damage to inflict
        """
        self.life -= amount
        if self.life <= 0:
            self.game_state.increase_score_by(self.game_state.score_inc_virus_killed)   # increase score
            pyglet.clock.unschedule(self.release_particle)      # unschedule the release particle function
            self.dead = True
        else:
            self.dead = False

    def update_object(self, dt):
        self.previous_position = self.position
        self.x += random.randrange(-1, 2, 2) * self.move_step
        self.y += random.randrange(-1, 2, 2) * self.move_step
        self.rotation += random.randrange(-1, 2, 2) * self.move_step

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "virus":
            self.dead = False
        elif other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "bullet":
            self.inflict_damage(self.game_state.damage_virus_by_bullet)
        elif other_object.type == "player":
            self.inflict_damage(self.game_state.damage_virus_by_player)

