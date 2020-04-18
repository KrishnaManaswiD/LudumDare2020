import pyglet

from modules import game_assets, game_object, game_state

class Cell(GameObject):
    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_player"]]
        super(Player, self).__init__(img=images[0], *args, **kwargs)
        self.game_state = game_state
        self.type = "cell"
