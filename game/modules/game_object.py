import pyglet

from modules import util

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
        self.dead = False           # whether this object has to be removed from screen or not
        self.collision_radius = 0   # circle collider radius
        self.collider_type = None   # "circle" or "polygon"

    def update_object(self, dt):
        """
        Virtual update_object function. This is not named update because the Sprite object has a
        function called update
        """
        pass

    def check_circle_circle_collision(self, other_object):
        collision_distance = self.collision_radius + other_object.collision_radius
        actual_distance = util.distance(self.position, other_object.position)
        return actual_distance <= collision_distance

    def check_point_polygon_collision(self, other_object):
        p = util.Point(self.x, self.y)
        polygon = other_object.vertices
        return util.is_inside_polygon_wn_algorithm(p, polygon)

    def check_polygon_point_collsion(self, other_object):
        p = util.Point(other_object.x, other_object.y)
        polygon = self.vertices
        return util.is_inside_polygon(p, polygon)

    def collides_with(self, other_object):
        if self.collider_type == 'circle' and other_object.collider_type == 'circle':
            return self.check_circle_circle_collision(other_object)
        elif self.collider_type == 'circle' and other_object.collider_type == 'polygon':
            return self.check_point_polygon_collision(other_object)
        elif self.collider_type == 'polygon' and other_object.collider_type == 'circle':
            return self.check_polygon_point_collsion(other_object)

    def handle_collision_with(self, other_object):
        self.dead = False
