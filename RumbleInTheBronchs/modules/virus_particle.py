from pyglet.window import key

from modules.game_object import GameObject
from modules.infection import Infection


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
        self.game_assets = game_assets
        self.type = "virus_particle"                # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = self.position

        self.move_step = 0.5     # Distance by which to move in each key press
        self.velocity_x = 0
        self.velocity_y = 0

    def create_infection(self):
        infection = Infection(self.game_state, self.game_assets, x=self.x, y=self.y, batch=self.batch, group=self.group)
        self.child_objects.append(infection)
        self.game_assets.audio_assets["snd_infection_birth"].play()

    def check_bounds(self):
        if self.x > 1000:
            self.dead = True
        if self.y > 1000:
            self.dead = True
        if self.x < 0:
            self.dead = True
        if self.y < 0:
            self.dead = True

    def update_object(self, dt):
        self.previous_position = self.position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "polygon":
            self.position = self.previous_position
            self.create_infection()
            self.dead = True
        elif other_object.type == "virus":
            self.dead = False   # no friendly fire
        elif other_object.type == "virus_particle":
            self.dead = False  # no friendly fire
        elif other_object.type == "player":
            self.dead = True    # kill myself
        elif other_object.type == "bullet":
            self.game_state.score += self.game_state.score_inc_virus_particle_killed
            self.dead = True  # kill myself
        elif other_object.type == "infection":
            self.dead = False
