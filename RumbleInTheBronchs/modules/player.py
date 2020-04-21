import math
import pyglet
from pyglet.window import key

from modules.game_object import GameObject
from modules.bullet import Bullet


class Player(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_player_1"],
                  game_assets.image_assets["img_player_2"],
                  game_assets.image_assets["img_player_3"]]
        anim = pyglet.image.Animation.from_image_sequence(images, duration=0.5, loop=True)
        super(Player, self).__init__(img=anim, *args, **kwargs)

        self.game_state = game_state                # game state object
        self.game_assets = game_assets              # game assets object
        self.type = "player"                        # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.image.get_max_height()/2        # collision radius
        self.previous_position = self.position

        self.height_max = 50

        # self.move_step = 10         # Distance by which to move in each key press

        self.rotate_speed = 100
        self.drift_speed = 1
        self.drift_speed_max = 4
        self.drift_speed_min = -4

        self.bullet_speed = 300         # speed with which a bullet is released

        self.bullet_reload_timeout = 0.3    # time in seconds between two bullet shots
        self.bullet_time_current = 0        # time in seconds until next bullet is ready

        self.speed_update_timeout = 0.2     # time in seconds to wait between speed changes
        self.speed_time_current = 0         # time in seconds until speed change is ready

    def inflict_damage(self, amount):
        """
        Inflicts damage to the object. If the life of the object reaches 0, the object dies.
        :param amount: amount of damage to inflict
        """
        self.game_state.player_life = max(0, self.game_state.player_life - amount)
        if self.game_state.player_life == 0:
            self.dead = True
            self.game_assets.audio_assets["snd_player_death"].play()
        else:
            self.dead = False

    def fire(self):
        """
        Creates a new bullet object and adds it to the list of child objects
        """
        bullet_x = self.x
        bullet_y = self.y
        new_bullet = Bullet(self.game_state, self.game_assets,
                            x=bullet_x, y=bullet_y, batch=self.batch,
                            group=self.group)    # mentioning group is important
        new_bullet.velocity_x = self.bullet_speed * math.sin(self.rotation * math.pi / 180)
        new_bullet.velocity_y = self.bullet_speed * math.cos(self.rotation * math.pi / 180)
        new_bullet.rotation = self.rotation
        self.child_objects.append(new_bullet)
        self.game_assets.audio_assets["snd_player_fire"].play()

    def check_bounds(self):
        if self.x > 1000:
            self.x = 1000
        if self.y > 1000:
            self.y = 1000
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def update_object(self, dt):
        self.previous_position = self.position

        # Fire bullets at a minimum interval of self.bullet_reload_time, if space is pressed
        if self.bullet_time_current == 0:
            if self.key_handler[key.SPACE]:
                # fire bullet if space is pressed
                self.fire()
                self.bullet_time_current = self.bullet_reload_timeout  # start countdown
        else:
            self.bullet_time_current = max(0, self.bullet_time_current - dt)

        # update speed at a minimum interval of self.speed_update_time, if up or down are pressed
        if self.speed_time_current == 0:
            if self.key_handler[key.DOWN]:
                self.drift_speed = max(self.drift_speed_min, self.drift_speed-1)
                self.speed_time_current = self.speed_update_timeout     # start countdown

            if self.key_handler[key.UP]:
                self.drift_speed = min(self.drift_speed_max, self.drift_speed+1)
                self.speed_time_current = self.speed_update_timeout     # start countdown
        else:
            self.speed_time_current = max(0, self.speed_time_current - dt)

        # # New controls
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        self.x += self.drift_speed * math.sin(self.rotation * math.pi / 180)
        self.y += self.drift_speed * math.cos(self.rotation * math.pi / 180)

        self.check_bounds()
        # update state with the player's position
        if not self.dead:
            self.game_state.player_position = self.position
        else:
            self.game_state.player_position = None

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
        elif other_object.type == "bullet":
            self.dead = False   # nothing happens if a bullet hits the object
        elif other_object.type == "virus":
            self.inflict_damage(self.game_state.damage_player_by_virus)
            self.position = self.previous_position      # also bounce back
        elif other_object.type == "virus_particle":
            self.inflict_damage(self.game_state.damage_player_by_virus_particle)
        elif other_object.type == "infection":
            self.position = self.previous_position
            self.inflict_damage(self.game_state.damage_player_by_infection)
