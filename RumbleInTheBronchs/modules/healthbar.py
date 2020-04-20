from modules.game_object import GameObject


class HealthBar(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        img = game_assets.image_assets["img_health_bar"]
        super(HealthBar, self).__init__(img=img, *args, **kwargs)

        self.type = "healthbar"

        self.game_state = game_state
        self.game_assets = game_assets

    def update_object(self, dt):
        self.x = self.game_state.player_life*5

    def handle_collision_with(self, other_object):
        self.dead = False   # the healthbar does not vanish on collision with anything
