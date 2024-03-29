from modules.game_object import GameObject


class InfectionBar(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        img = game_assets.image_assets["img_infection_bar"]
        super(InfectionBar, self).__init__(img=img, *args, **kwargs)

        self.type = "infectionbar"

        self.game_state = game_state
        self.game_assets = game_assets

    def update_object(self, dt):
        self.x = self.game_state.infection_level*5

    def handle_collision_with(self, other_object):
        self.dead = False   # the infectionbar does not vanish on collision with anything
