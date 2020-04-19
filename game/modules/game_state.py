class GameState(object):
    """
    Class that maintains the state of the game
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: additional positional arguments
        :param kwargs: additional keyword arguments
        """
        super(GameState, self).__init__(*args, **kwargs)

        # Declaring all the member variables of the class
        self.score = 0      # game score

        # add all damages here. All game objects will use these variables
        self.damage_virus_by_bullet = 20

        # add all score increments here All game objects will use these variables

    def get_score(self):
        """
        Returns the current score
        :return: self.score
        """
        return self.score

    def increase_score_by(self, value):
        """
        Increases the score by the specified value
        :param value: Value to increase the score by.
        """
        self.score += value
