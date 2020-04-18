import pyglet

from modules import game_assets, game_state
from modules.game_object import GameObject

class PolygonCollider(GameObject):
    def __init__(self, vertices, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param vertices: vertices that define the polygon
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_circle"]]
        super(PolygonCollider, self).__init__(img=images[0], *args, **kwargs)
        self.game_state = game_state
        self.type = "polygon"
        self.vertices = vertices
        self.collider_type = "polygon"

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            pass
        if other_object.type == "player":
            self.dead = False


    def update_object(self, dt):
        # state change code comes here
        pass
