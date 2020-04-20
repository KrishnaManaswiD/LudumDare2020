import random
import pyglet

from modules.game_object import GameObject
from modules.game_state import GameState
from modules.game_assets import GameAssets
from modules.virus import Virus

class VirusSpawner(GameObject):

    def __init__(self, game_state, game_assets, spawn_locations, *args, **kwargs):
        """
        Class that spawns viruses
        :param game_state:
        :param game_assets:
        :param args:
        :param kwargs:
        """
        img = game_assets.image_assets["img_spawner"]
        super(VirusSpawner, self).__init__(img=img, *args, **kwargs)

        self.game_state = game_state
        self.game_assets = game_assets
        self.type = "virus_spawner"

        self.collider_type = None

        self.spawn_frequency = 8
        pyglet.clock.schedule_interval(self.spawn_virus, self.spawn_frequency)

        self.spawn_locations = spawn_locations

    def spawn_virus(self, dt):
        """
        Spawns a virus if not at max limit
        """
        if self.game_state.should_create_new_viruses:
            location_index = random.randint(0, len(self.spawn_locations)-1)
            virus_location = self.spawn_locations[location_index]
            virus = Virus(self.game_state, self.game_assets,
                          x=virus_location[0], y = virus_location[1],
                          batch=self.batch, group=self.group)
            self.child_objects.append(virus)
            self.game_assets.audio_assets["snd_virus_birth"].play()

    def handle_collision_with(self, other_object):
        self.dead = False