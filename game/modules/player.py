import pyglet
from pyglet.window import key

from modules.game_object import GameObject
from modules import util

class Player(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_player"]]
        # TODO make this a sprite later
        super(Player, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state                # game state object
        self.type = "player"                        # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = None

        self.move_step = 10     # Distance by which to move in each key press
        self.life = 100         # Life of the player

    def update_object(self, dt):
        self.previous_position = self.position
        if self.key_handler[key.LEFT]:
            self.x -= self.move_step

        if self.key_handler[key.RIGHT]:
            self.x += self.move_step

        if self.key_handler[key.UP]:
            self.y += self.move_step

        if self.key_handler[key.DOWN]:
            self.y -= self.move_step

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            # intersection = util.circles_intersection(self.x, self.y, self.collision_radius, other_object.x, other_object.y, other_object.collision_radius)
            # if self.x < other_object.x and self.y < other_object.y:
            #     self.x = intersection[0] - self.collision_radius
            #     self.y = intersection[1] - self.collision_radius
            # elif self.x > other_object.x and self.y < other_object.y:
            #     self.x = intersection[0] + self.collision_radius
            #     self.y = intersection[1] - self.collision_radius
            # elif self.x > other_object.x and self.y > other_object.y:
            #     self.x = intersection[0] + self.collision_radius
            #     self.y = intersection[1] + self.collision_radius
            # elif self.x < other_object.x and self.y < other_object.y:
            #     self.x = intersection[0] - self.collision_radius
            #     self.y = intersection[1] + self.collision_radius
            self.position = self.previous_position
            print("colliding with circle")
        if other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
            print("colliding with polygon")
