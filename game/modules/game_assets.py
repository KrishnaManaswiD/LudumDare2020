import pyglet


class GameAssets():

    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        super(GameAssets, self).__init__(*args, **kwargs)

    def set_anchor_at_centre(image):
        """
        Sets the anchor of an image to its centre
        :param image: Image whose anchor has to be set
        """
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    def load_image_asset_and_center(self, file):
        """
        Loads an image asset from the specified file and centers it anchor point
        :param file: File which has to be loaded as an asset
        :return: Image asset
        """
        asset = pyglet.resource.image(file)
        self.set_anchor_at_centre(asset)
        return asset



def load_resources():
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    # load images
    img_player = pyglet.resource.image("images/player.png")

