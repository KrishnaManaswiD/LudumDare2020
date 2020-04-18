import pyglet


class GameObject(pyglet.sprite.Sprite):
    """
    A class to define a generic object in the game.

    Most objects in the game, i.e. player, enemy, bullet are derived from this class.
    This class itself is derived from the pyglet.sprite.Sprite class
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        """
        super(GameObject, self).__init__(*args, **kwargs)

        # Declaring all the member variables of the class
        self.type = None            # Specifies the type of the object - player, enemy, bullet etc.
        self.child_objects = []     # List of objects that can be spawned by this object
        self.game_state = None      # Game state object

    def update_object(self):
        """
        Virtual update_object function. This is not named update because the Sprite object has a
        function called update
        """
        pass