import pyglet
from pyglet.gl import GL_POINTS
from pyglet.gl import GL_TRIANGLES
from pyglet.window import mouse

from modules.game_assets import GameAssets
from modules.game_state import GameState
from modules.player import Player
from modules.virus import Virus
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

    # backgroung
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
    player = Player(state, assets, x=500, y=500, batch=main_batch, group=groups[5])
    window.push_handlers(player)
    window.push_handlers(player.key_handler)

    # create a game level - collection of obstacles
    cells = []
    for i in range(5):
        cells.append(CircleCollider(state, assets, x=i*100, y=100, batch=main_batch, group=groups[5]))

    verts = []
    verts.append(util.Point(700, 500))
    verts.append(util.Point(900, 500))
    verts.append(util.Point(800, 800))
    polygon = PolygonCollider(verts, state, assets)

    glvertices = pyglet.graphics.vertex_list(3, ('v2i', [700, 500, 900, 500, 800, 800]),
                                          ('c3b', [100,200,200, 100,200,200, 100,200,200]))


    virus = Virus(state, assets, x=100, y=700, batch=main_batch, group=groups[5])
    # list of all game objects
    game_objects = [player] + cells + [polygon] + [virus]

    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        glvertices.draw(GL_TRIANGLES)

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
        for objects_to_remove in [obj for obj in game_objects if obj.dead]:
            objects_to_remove.delete()
            game_objects.remove(objects_to_remove)

        # add new objects
        game_objects.extend(objects_to_add)

    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()


if __name__ == "__main__":

    main()
