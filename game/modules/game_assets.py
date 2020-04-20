import pyglet


class GameAssets():

    def __init__(self, *args, **kwargs):
        """
        Initializes the class object.
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        """
        super(GameAssets, self).__init__(*args, **kwargs)

        self.image_assets = dict()        # dictionary of game assets
        self.audio_assets = dict()        # dictionary of audio assets

        self.load_assets()

    def set_anchor_at_centre(self, image):
        """
        Sets the anchor of an image to its centre
        :param image: Image whose anchor has to be set
        """
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    def create_image_asset(self, keyword, file, centered=True):
        """
        Creates an image asset from the specified file and adds it to the
        dictionary of image assets using the specified keyword
        :param keyword: Keyword with which to name the asset
        :param file: File from which to create the asset
        :param centered: Boolean indicating if the anchor has to be centered.
                        Default is True. If False, anchor is at bottom left.
        """
        image_asset = pyglet.resource.image(file)
        if centered:
            self.set_anchor_at_centre(image_asset)
        self.image_assets.update({keyword: image_asset})

    def create_audio_asset(self, keyword, file, streaming=False):
        """
        Creates an audio asset from the specified file and adds it to the
        dictionary of sound assets using the specified keyword
        :param keyword: Keyword with which to name the asset
        :param file: Keyword with which to name the asset
        :param streaming: Boolean indicating if the audio has to be streamed live or pre-loaded
        """
        audio_asset = pyglet.resource.media(file, streaming=streaming)
        self.audio_assets.update({keyword : audio_asset})

    def load_assets(self):
        pyglet.resource.path = ['resources']
        pyglet.resource.reindex()

        # load images
        # self.create_image_asset("img_player", "images/player.png", True)
        self.create_image_asset("img_player_1", "images/player_1.png", True)
        self.create_image_asset("img_player_2", "images/player_2.png", True)
        self.create_image_asset("img_player_3", "images/player_3.png", True)
        self.create_image_asset("img_bkg", "images/bkg_red_1000x1000.png", False)
        self.create_image_asset("img_frg", "images/openCVTest2_transparent.png", False)
        self.create_image_asset("img_circle", "images/circle_100.png", True)
        self.create_image_asset("img_virus", "images/virus.png", True)
        self.create_image_asset("img_virus_A", "images/virus_A.png", True)
        self.create_image_asset("img_virus_B", "images/virus_B.png", True)
        self.create_image_asset("img_virus_C", "images/virus_C.png", True)
        self.create_image_asset("img_virus_D", "images/virus_D.png", True)
        self.create_image_asset("img_virus_particle", "images/virus_particle.png", True)
        self.create_image_asset("img_bullet", "images/bullet.png", True)
        self.create_image_asset("img_bullet_1", "images/bullet_1.png", True)
        self.create_image_asset("img_bullet_2", "images/bullet_2.png", True)
        self.create_image_asset("img_bullet_3", "images/bullet_3.png", True)
        self.create_image_asset("img_health_bar", "images/health_bar.png", True)
        self.create_image_asset("img_infection", "images/infection.png", True)
        self.create_image_asset("img_infection_A_1", "images/infection_A_1.png", True)
        self.create_image_asset("img_infection_A_2", "images/infection_A_2.png", True)

        # load audio
        self.create_audio_asset("bkg_music", "music/bkg.wav", True)
        self.create_audio_asset("ost_music", "music/ost.wav", True)
        self.create_audio_asset("snd_player_death", "sounds/Booming_Rumble.wav", False)
        self.create_audio_asset("snd_player_fire", "sounds/Zap_power_down_1.wav", False)
        self.create_audio_asset("snd_virus_birth", "sounds/Booming_Rumble.wav", False)
        self.create_audio_asset("snd_virus_fire", "sounds/Booming_Rumble.wav", False)
        self.create_audio_asset("snd_virus_death", "sounds/Booming_Rumble.wav", False)
        self.create_audio_asset("snd_infection_birth", "sounds/Booming_Rumble.wav", False)
        self.create_audio_asset("snd_infection_death", "sounds/abstract_atmosphere_083.wav", False)
        self.create_audio_asset("snd_impending_doom", "sounds/Booming_Rumble.wav", False)

