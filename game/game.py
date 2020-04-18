import pyglet
from pyglet.window import mouse

from modules.game_assets import GameAssets
from modules.game_state import GameState
from modules.player import Player

def main():
    window = pyglet.window.Window(1000, 1000, "game title",
                                  resizable=True,
                                  # style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS
                                  )

    # Store objects in a batch to load them efficiently
    main_batch = pyglet.graphics.Batch()

    # load required resources
    assets = GameAssets()

    # backgroung
    bkg = pyglet.sprite.Sprite(img=assets.image_assets["img_bkg"],
                               x=0, y=0, batch=main_batch)

    # title
    label = pyglet.text.Label('GAME TITLE',
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width // 2,
                              y=window.height - 50,
                              anchor_x='center', anchor_y='center',
                              batch=main_batch)

    state = GameState()
    player = Player(state, assets, x=500, y=500, batch=main_batch)
    window.push_handlers(player)

    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()

    pyglet.app.run()

if __name__ == "__main__":
    main()
