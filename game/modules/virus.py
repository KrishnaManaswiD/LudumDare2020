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
        images = [game_assets.image_assets["img_virus_B"]]
        # TODO make this a sprite later
        super(Virus, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state                # game state object
        self.game_assets = game_assets
        self.type = "virus"                         # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = self.position

        self.life = 100     # life of the virus

        self.seek_player = True
        self.proximity_threshold = 200
        self.seeking_step = 1.2

        self.move_step = 0.5     # Distance by which to move in each key press
        self.game_state.infection_level = min(100, self.game_state.infection_level+self.game_state.infection_by_virus)   # increase infection level
        pyglet.clock.schedule_interval(self.release_particle, 7)

    def release_particle(self, dt):
        if self.game_state.should_fire_new_particles:
            particle = VirusParticle(self.game_state, self.game_assets,
                                     x=self.x, y=self.y, batch=self.batch,
                                     group=self.group)
            particle.velocity_x = random.randrange(-50,50)
            particle.velocity_y = random.randrange(-50,50)
            self.child_objects.append(particle)

    def inflict_damage(self, amount):
        """
        Inflicts damage to the object. If the life of the object reaches 0, the object dies.
        :param amount: amount of damage to inflict
        """
        self.life = max(0, self.life - amount)
        if self.life == 0:
            self.game_state.score += self.game_state.score_inc_virus_killed   # increase score
            pyglet.clock.unschedule(self.release_particle)      # unschedule the release particle function

            # decrease infection level
            self.game_state.infection_level = max(0,
                                                  self.game_state.infection_level - self.game_state.infection_by_virus)

            self.dead = True
        else:
            self.dead = False

    def get_distance_to_player(self):
        player_position = self.game_state.player_position
        return util.distance((player_position[0], player_position[1]),
                             (self.x, self.y))

    def update_object(self, dt):
        self.previous_position = self.position
        if self.seek_player and self.game_state.player_position is not None:
            dist = self.get_distance_to_player()
            if dist < self.proximity_threshold:
                x_dir = (self.game_state.player_position[0] - self.x) / dist
                y_dir = (self.game_state.player_position[1] - self.y) / dist

                self.x += x_dir * self.seeking_step
                self.y += y_dir * self.seeking_step
            else:
                self.x += random.randrange(-1, 2, 2) * self.move_step
                self.y += random.randrange(-1, 2, 2) * self.move_step
                self.rotation += random.randrange(-1, 2, 2) * self.move_step
        else:
            self.x += random.randrange(-1, 2, 2) * self.move_step
            self.y += random.randrange(-1, 2, 2) * self.move_step
            self.rotation += random.randrange(-1, 2, 2) * self.move_step
        self.check_bounds()

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "virus":
            self.dead = False   # two viruses bump away when they collide
            self.position = self.previous_position
        elif other_object.type == "bullet":
            self.inflict_damage(self.game_state.damage_virus_by_bullet)
        elif other_object.type == "player":
            self.inflict_damage(self.game_state.damage_virus_by_player)
        elif other_object.type == "infection":
            self.dead = False

    def check_bounds(self):
        if self.x > 1000:
            self.x = 1000
        if self.y > 1000:
            self.y = 1000
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

