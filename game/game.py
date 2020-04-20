import pyglet
from pyglet.gl import GL_POINTS
from pyglet.gl import GL_TRIANGLES
from pyglet.window import mouse
from pyglet.window import key

from modules.game_assets import GameAssets
from modules.game_state import GameState
from modules.game_object import GameObject
from modules.player import Player
from modules.healthbar import HealthBar
from modules.infectionbar import InfectionBar
from modules.virus import Virus
from modules.virus_spawner import VirusSpawner
from modules.circle_collider import CircleCollider
from modules.polygon_collider import PolygonCollider
from modules.level_handler import LevelHandler
from modules import util


def main():
    window = pyglet.window.Window(1000, 1000, "game title",
                                  resizable=True,
                                  # style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS
                                  )

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()

    # groups - 0 drawn first, 10 drawn last
    groups = []
    for i in range(10):
        groups.append(pyglet.graphics.OrderedGroup(i))

    # load required resources
    assets = GameAssets()

    # background music score
    background_music = assets.audio_assets["ost_music"]
    p = pyglet.media.Player()
    p.queue(background_music)
    p.loop = True
    p.play()

    # common game state for all the game objects
    state = GameState()

    # initialize dummy background and foreground
    state.bkg = GameObject(img=assets.image_assets["img_dummy"],
                                     x=-1, y=-1, batch=main_batch, group=groups[0])
    state.frg = GameObject(img=assets.image_assets["img_dummy"],
                                     x=-1, y=-1, batch=main_batch, group=groups[7])
    state.game_level = -1  # pre launch state

    # keyboard input handler
    key_handler = key.KeyStateHandler()
    window.push_handlers(key_handler)

    # UI - spawn it off screen
    # ui_start = LevelHandler(state, assets, window, groups, x=-1, y=-1,
    #                         batch=main_batch, group=groups[8])
    # window.push_handlers(ui_start)
    # window.push_handlers(ui_start.key_handler)
    game_objects = []

    # add game objects common to all levels
    # health bar
    health_bar = HealthBar(state, assets,
                           x=state.player_life, y=900,
                           batch=main_batch, group=groups[8])
    game_objects.append(health_bar)

    # infection bar
    infection_bar = InfectionBar(state, assets,
                                 x=state.infection_level, y=920,
                                 batch=main_batch, group=groups[8])
    game_objects.append(infection_bar)

    # virus spawner
    virus_spawner = VirusSpawner(state, assets, x=-5, y=0,
                                 batch=main_batch, group=groups[5])
    game_objects.append(virus_spawner)

    vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
    vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
    vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
    vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
    vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]

    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        if state.game_level == 1:
            util.get_gl_polygon(vertices1).draw(GL_TRIANGLES)
            util.get_gl_polygon(vertices2).draw(GL_TRIANGLES)
            util.get_gl_polygon(vertices3).draw(GL_TRIANGLES)
            util.get_gl_polygon(vertices4).draw(GL_TRIANGLES)
            util.get_gl_polygon(vertices5).draw(GL_TRIANGLES)

    def handle_game_launch():
        state.frg.image = assets.image_assets["img_start_screen_A"]
        state.frg.x = 500
        state.frg.y = 500
        state.game_level = 0

    def handle_start_screen():
        if key_handler[key.RIGHT]:
            state.frg.image = assets.image_assets["img_start_screen_B"]
            state.frg.x = 500
            state.frg.y = 500
        if key_handler[key.LEFT]:
            state.frg.image = assets.image_assets["img_start_screen_A"]
            state.frg.x = 500
            state.frg.y = 500
        if key_handler[key.ENTER]:
            state.game_level = 1
            load_stage_1()

    def handle_levels():
        if key_handler[key.N]:
            # delete existing game objects
            state.game_level = 2
            remove_all_non_essential_game_objects()
            load_stage_2()

    def load_stage_1():
        # background and foreground
        state.bkg = GameObject(img=assets.image_assets["img_bkg_level_1"],
                         x=0, y=0, batch=main_batch, group=groups[0])
        state.frg = GameObject(img=assets.image_assets["img_frg_level_1"], x=0, y=0,
                         batch=main_batch, group=groups[7])

        # player
        player = Player(state, assets, x=100, y=400,
                        batch=main_batch, group=groups[5])
        window.push_handlers(player)
        window.push_handlers(player.key_handler)

        # stage - polygon colliders
        vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
        vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
        vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
        vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
        vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]

        polygon1 = PolygonCollider(util.get_points(vertices1), state,
                                   assets, "poly1", group=groups[5])
        polygon2 = PolygonCollider(util.get_points(vertices2), state,
                                   assets, "poly2", group=groups[5])
        polygon3 = PolygonCollider(util.get_points(vertices3), state,
                                   assets, "poly3", group=groups[5])
        polygon4 = PolygonCollider(util.get_points(vertices4), state,
                                   assets, "poly4", group=groups[5])
        polygon5 = PolygonCollider(util.get_points(vertices5), state,
                                   assets, "poly5", group=groups[5])

        # list of all game objects
        game_objects.append(state.bkg)
        game_objects.append(state.frg)

        game_objects.append(player)

        game_objects.append(polygon1)
        game_objects.append(polygon2)
        game_objects.append(polygon3)
        game_objects.append(polygon4)
        game_objects.append(polygon5)

    def load_stage_2():
        print(game_objects)

    def remove_all_non_essential_game_objects():
        for obj in game_objects:
            if obj.type not in ["virus_spawner", "healthbar", "infectionbar"]:
                obj.dead = True
            if obj.type in ["virus"]:
                pyglet.clock.unschedule(obj.release_particle)

    def update(dt):

        if state.game_level == -1:
            handle_game_launch()
        elif state.game_level == 0:
            handle_start_screen()
        elif state.game_level > 0:
            handle_levels()


        # primitive collision detection
        # loop over pairs of game objects
        for i in range(len(game_objects)):
            for j in range(i + 1, len(game_objects)):
                object_one = game_objects[i]
                object_two = game_objects[j]
                # if either of the objects are not dead
                if not object_one.dead and not object_two.dead:
                    # check collision
                    if object_one.collides_with(object_two):
                        # handle collision with each other
                        object_one.handle_collision_with(object_two)
                        object_two.handle_collision_with(object_one)

        objects_to_add = []  # list of new objects to add
        # update positions, state of each object and
        # collect all children that each object may spawn
        for obj in game_objects:
            obj.update_object(dt)       # update the current position and state of objects
            objects_to_add.extend(obj.child_objects)  # add objects that this game object wants to spawn
            obj.child_objects = []  # clear the list

        # remove objects that are dead
        for object_to_remove in [obj for obj in game_objects if obj.dead]:
            object_to_remove.delete()
            game_objects.remove(object_to_remove)

        # add new objects
        game_objects.extend(objects_to_add)

    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()


if __name__ == "__main__":

    main()
