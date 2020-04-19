import pyglet

from modules.game_assets import GameAssets
from modules.game_state import GameState
from modules.game_object import GameObject


class CircleCollider(GameObject):
    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_circle"]]
        super(CircleCollider, self).__init__(img=images[0], *args, **kwargs)
        self.game_state = game_state
        self.type = "circle"
        self.collider_type = "circle"
        self.collision_radius = self.width/2

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
        elif other_object.type == "polygon":
            self.dead = False
        elif other_object.type == "player":
            self.dead = False
        elif other_object.type == "bullet":
            self.dead = False
        elif other_object.type == "virus":
            self.dead = False
        elif other_object.type == "virus_particle":
            self.dead = False
        elif other_object.type == "infection":
            self.dead = False

    def update_object(self, dt):
        # state change code comes here
        pass
