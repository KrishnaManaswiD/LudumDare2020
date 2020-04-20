import pyglet
from pyglet.gl import GL_POINTS
from pyglet.gl import GL_TRIANGLES
from pyglet.window import mouse
from pyglet.window import key
from pyglet import clock

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

    lbl_score = pyglet.text.Label('score: ' + str(state.score),
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=700, y=window.height - 50,
                                  anchor_x='center', anchor_y='center',
                                  batch=main_batch, group=groups[8])

    # vertices1 = [1001, 200, 824, 225, 537, 177, 435, 108, 415, 0, 1001, 0]
    # vertices2 = [0, 272, 0, 0, 255, 0, 232, 73, 45, 266]
    # vertices3 = [256, 481, 375, 364, 606, 334, 697, 447, 627, 599, 402, 623]
    # vertices4 = [576, 1001, 601, 902, 744, 851, 837, 712, 969, 651, 1001, 665, 1001, 1001]
    # vertices5 = [0, 1001, 0, 811, 137, 810, 282, 876, 275, 1001]

    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        # if state.game_level == 1:
            # util.get_gl_polygon(vertices1).draw(GL_TRIANGLES)
            # util.get_gl_polygon(vertices2).draw(GL_TRIANGLES)
            # util.get_gl_polygon(vertices3).draw(GL_TRIANGLES)
            # util.get_gl_polygon(vertices4).draw(GL_TRIANGLES)
            # util.get_gl_polygon(vertices5).draw(GL_TRIANGLES)

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

    def handle_game_over_screen():
        state.frg.image = assets.image_assets["img_game_over"]
        state.frg.x = 500
        state.frg.y = 500
        if key_handler[key.R]:
            state.game_level = 1
            state.infection_level = 0
            state.player_life = 100
            load_stage_1()

    def handle_win_screen():
        state.frg.image = assets.image_assets["img_win"]
        state.frg.x = 500
        state.frg.y = 500
        if key_handler[key.R]:
            state.game_level = 1
            state.infection_level = 0
            state.player_life = 100
            load_stage_1()

    def handle_level_change():
        if state.infection_level < 30:  # if under threshold TODO: make this a variable
            state.game_level += 1  # move to next level
        else:
            state.game_level = -2  # game over

        if state.game_level == 2:
            remove_all_non_essential_game_objects()
            state.infection_level = 0
            load_stage_2()
        if state.game_level == 3:
            state.infection_level = 0
            remove_all_non_essential_game_objects()
            load_stage_3()
        if state.game_level == 4:
            remove_all_non_essential_game_objects()
            handle_win_screen()
        if state.game_level == -2:
            remove_all_non_essential_game_objects()
            handle_game_over_screen()

    def load_stage_1():
        state.time_counter = 0
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

        # health bar
        health_bar = HealthBar(state, assets,
                               x=state.player_life, y=900,
                               batch=main_batch, group=groups[8])


        # infection bar
        infection_bar = InfectionBar(state, assets,
                                     x=state.infection_level, y=970,
                                     batch=main_batch, group=groups[8])

        # virus spawner
        virus_spawner = VirusSpawner(state, assets, x=-5, y=0,
                                     batch=main_batch, group=groups[5])

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

        game_objects.append(health_bar)
        game_objects.append(infection_bar)
        game_objects.append(virus_spawner)

        game_objects.append(polygon1)
        game_objects.append(polygon2)
        game_objects.append(polygon3)
        game_objects.append(polygon4)
        game_objects.append(polygon5)

    def load_stage_2():
        state.time_counter = 0
        # background and foreground
        state.bkg = GameObject(img=assets.image_assets["img_bkg_level_2"],
                               x=0, y=0, batch=main_batch, group=groups[0])
        state.frg = GameObject(img=assets.image_assets["img_frg_level_2"], x=0, y=0,
                               batch=main_batch, group=groups[7])

        # player
        player = Player(state, assets, x=500, y=200,
                        batch=main_batch, group=groups[5])
        window.push_handlers(player)
        window.push_handlers(player.key_handler)

        # health bar
        health_bar = HealthBar(state, assets,
                               x=state.player_life, y=900,
                               batch=main_batch, group=groups[8])

        # infection bar
        infection_bar = InfectionBar(state, assets,
                                     x=state.infection_level, y=970,
                                     batch=main_batch, group=groups[8])

        # virus spawner
        virus_spawner = VirusSpawner(state, assets, x=-5, y=0,
                                     batch=main_batch, group=groups[5])

        # stage - polygon colliders
        vertices1 = [403, 0, 343, 122, 173, 46, 151, 1]
        vertices2 = [600, 58, 660, 0, 1001, 0, 998, 35, 656, 167]
        vertices3 = [1001, 730, 795, 555, 739, 379, 871, 275, 1001, 275]
        vertices4 = [1, 742, 0, 193, 170, 269, 204, 500, 123, 701]
        vertices5 = [289, 1001, 374, 696, 626, 657, 730, 865, 657, 1000]

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

        game_objects.append(health_bar)
        game_objects.append(infection_bar)
        game_objects.append(virus_spawner)

        game_objects.append(polygon1)
        game_objects.append(polygon2)
        game_objects.append(polygon3)
        game_objects.append(polygon4)
        game_objects.append(polygon5)

    def load_stage_3():
        state.time_counter = 0
        # background and foreground
        state.bkg = GameObject(img=assets.image_assets["img_bkg_level_3"],
                               x=0, y=0, batch=main_batch, group=groups[0])
        state.frg = GameObject(img=assets.image_assets["img_frg_level_3"], x=0, y=0,
                               batch=main_batch, group=groups[7])

        # player
        player = Player(state, assets, x=150, y=800,
                        batch=main_batch, group=groups[5])
        window.push_handlers(player)
        window.push_handlers(player.key_handler)

        # health bar
        health_bar = HealthBar(state, assets,
                               x=state.player_life, y=900,
                               batch=main_batch, group=groups[8])

        # infection bar
        infection_bar = InfectionBar(state, assets,
                                     x=state.infection_level, y=970,
                                     batch=main_batch, group=groups[8])

        # virus spawner
        virus_spawner = VirusSpawner(state, assets, x=-5, y=0,
                                     batch=main_batch, group=groups[5])

        # stage - polygon colliders
        vertices1 = [449, 252, 241, 209, 0, 239, 0, 0, 509, 0]
        vertices2 = [1001, 404, 889, 352, 815, 145, 830, 0, 1001, 0]
        vertices3 = [187, 601, 286, 489, 440, 532, 591, 509, 652, 627, 600, 739, 320, 742]
        vertices4 = [699, 910, 864, 889, 977, 793, 1001, 799, 1001, 1001, 784, 1001]

        polygon1 = PolygonCollider(util.get_points(vertices1), state,
                                   assets, "poly1", group=groups[5])
        polygon2 = PolygonCollider(util.get_points(vertices2), state,
                                   assets, "poly2", group=groups[5])
        polygon3 = PolygonCollider(util.get_points(vertices3), state,
                                   assets, "poly3", group=groups[5])
        polygon4 = PolygonCollider(util.get_points(vertices4), state,
                                   assets, "poly4", group=groups[5])

        # list of all game objects
        game_objects.append(state.bkg)
        game_objects.append(state.frg)

        game_objects.append(player)

        game_objects.append(health_bar)
        game_objects.append(infection_bar)
        game_objects.append(virus_spawner)

        game_objects.append(polygon1)
        game_objects.append(polygon2)
        game_objects.append(polygon3)
        game_objects.append(polygon4)

    def remove_all_non_essential_game_objects():
        for obj in game_objects:
            if obj.type in ["virus_spawner"]:
                pyglet.clock.unschedule(obj.spawn_virus)
            if obj.type in ["virus"]:
                pyglet.clock.unschedule(obj.release_particle)
            obj.dead = True

    def update(dt):

        if state.game_level == -1:
            handle_game_launch()
        elif state.game_level == 0:
            handle_start_screen()
        elif state.game_level > 0 and state.time_counter > 5:
            handle_level_change()

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

        # count number of viruses. if more than a set amount, dont add any more
        virus_count = 0
        for obj in game_objects:
            if obj.type in ["virus"]:
                virus_count += 1
        if virus_count > 4:
            state.should_create_new_viruses = False
        else:
            state.should_create_new_viruses = True

        # if infection is max, dont fire off new virus particles
        if state.infection_level >= 100:
            state.should_fire_new_particles = False
        else:
            state.should_fire_new_particles = True

        # update score
        lbl_score.text = 'score: ' + str(state.score)

        state.time_counter += dt

    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()


if __name__ == "__main__":

    main()
