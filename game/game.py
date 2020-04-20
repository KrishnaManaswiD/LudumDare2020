import pyglet
from pyglet.gl import GL_POINTS
from pyglet.gl import GL_TRIANGLES
from pyglet.window import mouse
from pyglet.window import key

from modules.game_assets import GameAssets
from modules.game_state import GameState
from modules.player import Player
from modules.healthbar import HealthBar
from modules.infectionbar import InfectionBar
from modules.virus import Virus
from modules.virus_spawner import VirusSpawner
from modules.circle_collider import CircleCollider
from modules.polygon_collider import PolygonCollider
from modules.ui import StartScreen
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

    # # start_screen
    ui_start = StartScreen(state, assets, window, groups, x=500, y=500,
                                 batch=main_batch, group=groups[8])
    window.push_handlers(ui_start)
    window.push_handlers(ui_start.key_handler)
    game_objects = [ui_start]

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

    def update(dt):
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
