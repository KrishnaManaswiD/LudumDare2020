import pyglet
from pyglet.window import key

from modules.game_object import GameObject

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

        self.move_step = 10     # Distance by which to move in each key press
        self.life = 100         # Life of the player

    def update_object(self):
        if self.key_handler[key.LEFT]:
            self.x -= self.move_step

        if self.keyHandler[key.RIGHT]:
            self.x += self.move_step

        if self.keyHandler[key.UP]:
            self.y += self.move_step

        if self.keyHandler[key.DOWN]:
            self.y -= self.move_step