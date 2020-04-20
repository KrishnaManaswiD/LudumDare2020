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
        self.damage_virus_by_bullet = 34
        self.damage_virus_by_player = 10

        self.damage_player_by_virus = 30
        self.damage_player_by_virus_particle = 10
        self.damage_player_by_infection = 40

        self.damage_infection_by_bullet = 25

        # add all score increments here All game objects will use these variables
        self.score_inc_virus_killed = 25
        self.score_inc_virus_particle_killed = 10
        self.score_inc_infection_killed = 25

        # player posiiton
        self.player_position = None

        # healths
        self.player_life = 100
        self.human_life = 100

        # infection levels
        self.infection_level = 0
        self.infection_by_virus = 5
        self.infection_by_infection = 15

        # game levels
        self.game_level = -1

        # level transition toggle
        self.is_time_to_change_level = False

        # foreground and background
        self.bkg = None
        self.frg = None

        # toggles for spawning new viruses and particles
        self.should_create_new_viruses = True
        self.should_fire_new_particles = True

        self.time_counter = 0
        self.level_time = 2  # seconds
