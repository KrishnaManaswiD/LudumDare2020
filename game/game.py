import pyglet
from pyglet.gl import GL_POINTS
from pyglet.gl import GL_TRIANGLES
from pyglet.window import mouse

from modules.game_assets import GameAssets
from modules.game_state import GameState
from modules.player import Player
from modules.healthbar import HealthBar
from modules.infectionbar import InfectionBar
from modules.virus import Virus
from modules.virus_spawner import VirusSpawner
from modules.circle_collider import CircleCollider
from modules.polygon_collider import PolygonCollider
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

    # background
    bkg = pyglet.sprite.Sprite(img=assets.image_assets["img_bkg"],
                               x=0, y=0, batch=main_batch, group=groups[0])

    # title
    label = pyglet.text.Label('GAME TITLE',
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width // 2,
                              y=window.height - 50,
                              anchor_x='center', anchor_y='center',
                              batch=main_batch, group=groups[1])

    # common game state for all the game objects
    state = GameState()

    # player
    player = Player(state, assets, x=100, y=400, batch=main_batch, group=groups[5])
    window.push_handlers(player)
    window.push_handlers(player.key_handler)

    # health bar
    health_bar = HealthBar(state, assets, x=state.player_life, y=900,
                           batch=main_batch, group=groups[8])
    # infection bar
    infection_bar = InfectionBar(state, assets, x=state.infection_level, y=920,
                                 batch=main_batch, group=groups[8])

    # create a game level - collection of obstacles
    cells = []
    # for i in range(5):
    #     cells.append(CircleCollider(state, assets, x=i*100, y=100, batch=main_batch, group=groups[5]))

    vertices1 = [1001, 0, 415, 0, 435, 108, 537, 177, 824, 225, 1001, 200]
    vertices2 = [45, 266, 232, 73, 255, 0, 0, 0, 0, 272]
    vertices3 = [402, 623, 627, 599, 697, 447, 606, 334, 375, 364, 256, 481]
    vertices4 = [1001, 1001, 1001, 665, 969, 651, 837, 712, 744, 851, 601, 902, 576, 1001]
    vertices5 = [275, 1001, 282, 876, 137, 810, 0, 811, 0, 1001]

    # vertices = [200, 300, 600, 300, 600, 600, 200, 700]

    # vertices1 = [0, 1000, 0, 600, 100, 600, 300, 800, 300, 1000]
    # vertices2 = [500, 1000, 600, 800, 700, 800, 1000, 600, 1000, 1000]
    # vertices3 = [500, 700, 300, 500, 400, 400, 700, 400, 700, 500]
    # vertices4 = [0, 0, 300, 0, 0, 300]
    # vertices5 = [500, 200, 500, 0, 1000, 0, 1000, 200, 900, 300]

    polygon1 = PolygonCollider(util.get_points(vertices1), state, assets, "poly1", group=groups[5])
    polygon2 = PolygonCollider(util.get_points(vertices2), state, assets, "poly2", group=groups[5])
    # polygon3 = PolygonCollider(util.get_points(vertices3), state, assets, "poly3", group=groups[5])
    polygon4 = PolygonCollider(util.get_points(vertices4), state, assets, "poly4", group=groups[5])
    polygon5 = PolygonCollider(util.get_points(vertices5), state, assets, "poly5", group=groups[5])
    # polygon = PolygonCollider(util.get_points(vertices), state, assets, "poly", group=groups[5])

    frg = pyglet.sprite.Sprite(img=assets.image_assets["img_frg"], x=0, y=0, batch=main_batch, group=groups[7])

    # virus_spawner = VirusSpawner(state, assets, x=-5, y=0,
                                 # batch=main_batch, group=groups[5])
    # virus = Virus(state, assets, x=800, y=500, batch=main_batch, group=groups[5])

    # list of all game objects
    game_objects = [player] + cells + [health_bar, infection_bar] + [polygon1, polygon2, polygon4, polygon5]

    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        # util.get_gl_polygon(vertices1).draw(GL_TRIANGLES)
        # util.get_gl_polygon(vertices2).draw(GL_TRIANGLES)
        # util.get_gl_polygon(vertices3).draw(GL_TRIANGLES)
        # util.get_gl_polygon(vertices4).draw(GL_TRIANGLES)
        # util.get_gl_polygon(vertices5).draw(GL_TRIANGLES)
        # util.get_gl_polygon(vertices).draw(GL_TRIANGLES)

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
