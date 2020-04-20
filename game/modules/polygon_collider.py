import pyglet

from modules import game_assets, game_state
from modules.game_object import GameObject

class PolygonCollider(GameObject):
    def __init__(self, vertices, game_state, game_assets, name, *args, **kwargs):
        """
        Initializes the PolygonCollider object
        :param vertices: vertices that define the polygon
        :param game_state: game state
        :param game_assets: game assets
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        """
        images = [game_assets.image_assets["img_circle"]]
        super(PolygonCollider, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state
        self.type = "polygon"
        self.vertices = vertices
        self.collider_type = "polygon"
        self.name = name
        #
        # for v in vertices:
        #     print("{}, {}".format(v.x, v.y))

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
        elif other_object.type == "player":
            print("I {} am colliding with player at {}".format(self.name, self.game_state.player_position))
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
