"""health_bar"""

import pyglet
from modules.game_object import GameObject
from modules.game_assets import GameAssets

class HealthBar(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        img =  game_assets.image_assets["img_health_bar"]
        super(HealthBar, self).__init__(img=img, *args, **kwargs)
        self.scale_y = 5
        self.type = "healthbar"

    def update_health(self, health):
        self.x = (health * 9) - 450

    def handle_collision_with(self, other_object):
        self.dead = False   # the healthbar does not vanish on collision with anything