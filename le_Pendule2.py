import sys
import pygame
import math
import random
import json
import os

# -------------------------------------------------------------------------
# 1. GLOBAL & INIT
# -------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
BLUE  = (0,   0, 255)
RED   = (255, 0,   0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Pendule - Full-Screen Emoji Celebration")

SCOREBOARD_FILE = "data/scoreboard.json"
SCOREBOARD = {}  # loaded from scoreboard.json

GAME_SETTINGS = {
    "music_on": True,
    "music_volume": 1.0,
}

# -------------------------------------------------------------------------
# 2. LOAD/SAVE SCOREBOARD
# -------------------------------------------------------------------------
def load_scoreboard():
    global SCOREBOARD
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r", encoding="utf-8") as f:
            SCOREBOARD = json.load(f)
    else:
        SCOREBOARD = {}

def save_scoreboard():
    with open(SCOREBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(SCOREBOARD, f, indent=2)

# -------------------------------------------------------------------------
# 3. RESOURCE LOADING
# -------------------------------------------------------------------------
def load_image(path, size=None):
    """Load an image from disk, optionally scale it, or quit if missing."""
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except FileNotFoundError as e:
        print(f"Error loading image: {e}")
        pygame.quit()
        sys.exit()

def load_sound(path):
    """Load a sound or return None if missing."""
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound: {e}")
        return None

# IMAGES
background_img = load_image("img/sky.png")
platform_img   = load_image("img/laplateforme.png", (400, 200))
sea_img        = load_image("img/sea.png")
wave_img       = load_image("img/flot.png")
man_img        = load_image("img/man.png", (80, 120))
pendulum_img   = load_image("img/pend.png", (50, 50))
fish_img       = load_image("img/fish.png", (150, 150))

heart_plain_b  = load_image("img/heartbp.png", (30, 30))
heart_empty_b  = load_image("img/heartbv.png", (30, 30))
heart_plain_r  = load_image("img/heartrp.png", (30, 30))
heart_empty_r  = load_image("img/heartrv.png", (30, 30))


# Load 20 emojis, each scaled to full-screen
emoji_images = []
for i in range(1, 21):
    fname = f"img/emoji{i}.png"  # e.g. "emoji1.png", "emoji2.png", ...
    emoji_images.append(load_image(fname, (WIDTH, HEIGHT)))

# SOUNDS
try:
    pygame.mixer.music.load("snd/background_music.mp3")
    pygame.mixer.music.play(-1)
except FileNotFoundError:
    print("Warning: background_music.mp3 not found.")

pulse_sound          = load_sound("snd/pulse.wav")      # "beating" sound for each emoji
correct_sound        = load_sound("snd/correct.wav")
incorrect_sound      = load_sound("snd/incorrect.wav")
strike_sound         = load_sound("snd/strike.wav")
splash_sound         = load_sound("snd/splash.wav")
win_sound            = load_sound("snd/win.wav")        # Loop this on "You Win!"
lose_sound           = load_sound("snd/lose.wav")
chrono_endanger_sound= load_sound("snd/chronoendanger.wav")

# FONTS
font       = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)
tiny_font  = pygame.font.Font(None, 22)

# BIG pixel font for "YOU WIN!" in blue
try:
    pixel_font_big = pygame.font.Font("pixel_font.ttf", 100)
except FileNotFoundError:
    print("pixel_font.ttf not found, falling back to default.")
    pixel_font_big = pygame.font.Font(None, 100)

# -------------------------------------------------------------------------
# 4. WORD LISTS (Expanded to 100 words)
# -------------------------------------------------------------------------
easy_words = [
    # PYTHON BASICS
    ("python",         "A high-level language known for readability.", "Created by Guido van Rossum in 1991."),
    ("variable",       "A named reference to a value.",               "Python variables can hold any type."),
    ("string",         "Sequence of characters in Python.",           "Enclosed by single, double, or triple quotes."),
    ("integer",        "Whole number type in Python.",                "Examples: 0, 42, -5."),
    ("float",          "Number with decimal part.",                   "Examples: 3.14, 2.0."),
    ("boolean",        "Represents True or False.",                   "Named after mathematician George Boole."),
    ("list",           "Ordered, changeable sequence in Python.",     "Defined with square brackets []."),
    ("dictionary",     "Key-value pairs in Python.",                  "Defined with curly braces {} and colons."),
    ("tuple",          "Immutable sequence in Python.",               "Similar to a list but unchangeable."),
    ("set",            "Unordered collection of unique elements.",    "Uses curly braces { } or set() constructor."),
    ("loop",           "Repeats code a number of times.",             "Use 'for' or 'while' in Python."),
    ("function",       "A reusable block of code in Python.",         "Defined with 'def' and may return values."),
    ("module",         "A file containing Python code.",              "Can be imported with import keyword."),
    ("package",        "A directory of Python modules.",              "Often contains an __init__.py file."),
    ("class",          "Blueprint for creating objects.",             "Enables OOP in Python."),
    ("object",         "An instance of a class.",                     "Has attributes and methods."),
    ("import",         "Used to load modules in Python.",             "Example: 'import math'."),
    ("print",          "Outputs text to the console.",                "In Python 3: print('Hello')."),
    ("if",             "Checks a condition before running code.",     "Often used with else or elif."),
    ("elif",           "Else-if to chain multiple conditions.",       "Comes between if and else."),
    ("else",           "The fallback if all conditions fail.",        "Used at the end of an if-elif chain."),
    ("input",          "Gets user input from console.",               "Returns string; cast it if you need int/float."),
    ("exception",      "Error event that disrupts normal flow.",      "Handled with try-except blocks."),
    ("try",            "Block of code to test for errors.",           "Paired with except for error handling."),
    ("except",         "Catches exceptions that occur in try block.", "Allows graceful error handling."),
    ("while",          "Runs code while a condition is True.",        "Use 'break' to exit early."),
    ("for",            "Iterates over a sequence.",                   "Example: for x in range(5)."),
    ("range",          "Generates a sequence of numbers.",            "Often used in for loops."),
    ("break",          "Exits the nearest loop.",                     "Used within loops to stop iteration."),
    ("continue",       "Skips to the next iteration of the loop.",    "Ignores the rest of the current loop body."),
    ("pass",           "Does nothing; a placeholder.",                "Used when a statement is required syntactically."),
    ("lambda",         "An anonymous inline function in Python.",     "Typically used in short callbacks."),
    ("listcomprehension", "Concise way to create lists.",             "Syntax: [expr for x in iterable if condition]."),
    ("slice",          "Extracts a portion of a list or string.",      "Syntax: list[start:stop:step]."),
    ("enumerate",      "Adds a counter to an iterable.",               "Returns index and value."),
    ("zip",            "Aggregates elements from multiple iterables.", "Creates tuples pairing elements."),
    ("map",            "Applies a function to all items in an iterable.", "Returns a map object."),
    ("filter",         "Filters items in an iterable based on a function.", "Returns a filter object."),
    ("reduce",         "Applies a rolling computation to sequential pairs.", "Requires functools."),
    ("docstring",      "String literals used for documentation.",      "Placed right after function/class definitions."),
    ("assert",         "Used for debugging purposes.",                "Raises AssertionError if condition is False."),
    ("del",            "Deletes objects.",                             "Can remove elements from lists or delete variables."),
    ("global",         "Declares a variable as global.",              "Allows modification of global variables inside functions."),
    ("nonlocal",       "Declares a variable as nonlocal.",            "Used in nested functions to modify outer scope variables."),
    ("yield",          "Produces a generator.",                        "Used in functions to return a generator instead of a single value."),
    ("decorator",      "A Python feature to modify function behavior.", "Uses @ syntax above a function."),
    ("generator",      "Creates iterators with 'yield'.",              "Used for lazy iteration to save memory."),
    ("contextmanager", "Python's 'with' statement extension.",         "Decorate with '@contextmanager'."),
    ("classmethod",    "Method bound to the class, not instance.",     "Uses @classmethod decorator."),
    ("staticmethod",   "Method not bound to class or instance.",       "Uses @staticmethod decorator."),
    ("property",       "Allows class methods to be accessed like attributes.", "Uses @property decorator."),
    ("inheritance",    "Mechanism where a class can inherit attributes and methods from another.", "Supports code reusability."),
    ("polymorphism",   "Ability to present the same interface for different underlying forms.", "Common in OOP."),
    ("encapsulation",  "Bundling data with methods that operate on that data.", "Helps in hiding the internal state."),
    ("abstraction",    "Simplifying complex reality by modeling classes appropriate to the problem.", "Focuses on essential qualities."),
    ("super",          "Used to call methods from a parent class.",   "Syntax: super().method()"),
]

hard_words = [
    # ADVANCED PYTHON
    ("decorator",       "A Python feature to modify function behavior.",  "Uses @ syntax above a function."),
    ("metaclass",       "A class of a class in Python.",                  "Lets you customize class creation."),
    ("generator",       "Creates iterators with 'yield'.",                "Used for lazy iteration to save memory."),
    ("contextmanager",  "Python's 'with' statement extension.",           "Decorate with '@contextmanager'."),
    ("typehinting",     "Annotating function params for clarity.",        "Optional in Python but improves readability."),
    ("multiprocessing", "Runs code across multiple processes in Python.", "Bypasses GIL constraints on multi-core."),
    ("threading",       "Runs tasks concurrently in Python threads.",     "Limited by GIL but good for I/O wait."),
    ("comprehension",   "Concise way to build lists, sets, or dicts.",    "Syntax: [expr for x in iterable]."),
    ("lambda",          "An anonymous inline function in Python.",        "Typically used in short callbacks."),
    ("__init__",        "Constructor method in Python classes.",          "Called when creating an instance."),
    ("__repr__",        "Unambiguous object representation.",             "Helpful for debugging/logging."),
    ("__str__",         "String version of object, user-friendly.",       "Used with str() or print()."),
    ("__name__",        "Special variable that stores module name.",      "Value is '__main__' if file is run directly."),
    ("__file__",        "Special variable storing module's path.",        "Lets you locate resources relative to script."),
    ("global",          "Keyword to modify global variables inside a func.", "Often best avoided for clarity."),
    ("__slots__",       "Limits dynamic attribute creation in classes.",  "Improves memory usage for many objects."),
    ("unittest",        "Built-in Python testing framework.",             "Defines TestCase classes and methods."),
    ("hypothesis",      "Property-based testing library in Python.",      "Generates random inputs to find edge cases."),
    ("asyncio",         "Python’s async concurrency framework.",          "Manages tasks, events, coroutines."),
    ("pickle",          "Module for serializing and de-serializing Python objects.", "Used for saving objects to files."),
    ("json",            "Module for working with JSON data in Python.",  "Provides easy encoding and decoding."),
    ("pickle",          "Module for serializing and de-serializing Python objects.", "Used for saving objects to files."),
    ("closure",         "A function object that has access to variables in its lexical scope.", "Enables data hiding."),
    ("iterable",        "An object capable of returning its members one at a time.", "Supports iteration in loops."),
    ("iterator",        "An object representing a stream of data.",        "Used in for loops and comprehensions."),
    ("monkeypatching",  "Dynamically modifying or extending code at runtime.", "Often used in testing."),
    ("serialization",   "Process of converting an object into a format that can be stored or transmitted.", "Includes pickle and json."),
    ("deserialization", "Reconstructing objects from serialized data.",    "Opposite of serialization."),
    ("memoization",     "Caching results of expensive function calls.",    "Improves performance by avoiding redundant computations."),
    ("reflection",      "Ability of a program to inspect and modify its own structure and behavior.", "Used in dynamic programming."),
    ("dynamictyping",   "Type checking happens at runtime.",              "Contrasts with static typing."),
    ("ducktyping",      "An object's suitability is determined by the presence of certain methods and properties.", "Type is determined by behavior."),
    ("descriptors",     "Protocol for managing the attributes of objects.", "Used in properties and type annotations."),
    ("metaprogramming", "Writing programs that write or manipulate other programs.", "Enhances flexibility and reusability."),
    ("abstractmethod",  "Method declared but not implemented in base class.", "For advanced OOP patterns."),
    ("property",        "Allows class methods to be accessed like attributes.", "Uses @property decorator."),
    ("type",            "Built-in metaclass for creating classes.",      "Used in metaclass programming."),
    ("memoryview",      "Provides a way to access the memory of other binary objects without copying.", "Enhances performance."),
    ("frozenset",       "Immutable version of a set.",                     "Cannot be modified after creation."),
    ("asyncdef",        "Defines an asynchronous function in Python.",     "Used with await for concurrency."),
    ("await",           "Pauses the coroutine until the awaited task is done.", "Used within async functions."),
    ("yieldfrom",       "Delegates part of a generator's operations to another generator.", "Simplifies generator delegation."),
    ("asynchronous",    "Non-blocking operations allowing multiple tasks to run concurrently.", "Used in asyncio and async/await."),
    ("decorators",      "Functions that modify the behavior of other functions or classes.", "Enhance code modularity and reusability."),
    ("slots",           "Used to declare a fixed set of attributes in a class.", "Reduces memory overhead."),
    ("pickleprotocol",  "Version of the pickle serialization protocol.", "Determines compatibility."),
    ("importlib",       "Module providing a rich API for interacting with the import system.", "Used for dynamic imports."),
    ("sys",             "Module providing access to variables and functions strongly tied to the interpreter.", "Used for system-specific parameters."),
    ("os",              "Module providing a portable way of using operating system dependent functionality.", "Used for file and directory operations."),
    ("pathlib",         "Module offering classes representing filesystem paths with semantics appropriate for different operating systems.", "Enhances path manipulations."),
    ("functools",       "Module for higher-order functions and operations on callable objects.", "Includes decorators like lru_cache."),
    ("itertools",       "Module providing functions creating iterators for efficient looping.", "Includes product, permutations, combinations."),
    ("collections",     "Module implementing specialized container datatypes.", "Includes namedtuple, deque, defaultdict."),
    ("heapq",           "Module providing heap queue algorithms.",         "Used for priority queues."),
    ("bisect",          "Module for array bisection algorithms.",          "Used for maintaining sorted lists."),
    ("operator",        "Module providing efficient functions corresponding to the intrinsic operators of Python.", "Used for functional programming."),
    ("copy",            "Module providing shallow and deep copy operations.", "Important for duplicating objects."),
    ("abc",             "Module for defining Abstract Base Classes.",    "Used to create interfaces."),
    ("enum",            "Module for creating enumerated constants.",      "Enhances code readability."),
    ("typing",          "Module providing support for type hints.",      "Includes List, Dict, Optional, etc."),
    ("dataclasses",     "Module providing a decorator and functions for automatically adding special methods to classes.", "Simplifies class definitions."),
    ("secrets",         "Module for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.", "Enhances security."),
    ("hashlib",         "Module providing a common interface to many secure hash and message digest algorithms.", "Used for hashing data."),
    ("ssl",             "Module providing access to Transport Layer Security (often known as Secure Sockets Layer) encryption and peer authentication facilities for network sockets.", "Enhances network security."),
    ("socket",          "Module providing access to the BSD socket interface.", "Used for network communication."),
    ("select",          "Module providing access to I/O completion facilities.", "Used for multiplexing I/O."),
]

# -------------------------------------------------------------------------
# 5. SCORE/BOARD UTILS
# -------------------------------------------------------------------------
def get_top3_scores():
    """Return the top 3 (name, score) from the scoreboard."""
    all_scores = [(name, data["score"]) for name, data in SCOREBOARD.items()]
    sorted_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)
    return sorted_scores[:3]

def get_best_score():
    """Return (best_player_name, best_score). If none, (None, 0)."""
    if not SCOREBOARD:
        return (None, 0)
    best_name = None
    best_val  = 0
    for nm, dt in SCOREBOARD.items():
        if dt["score"] > best_val:
            best_val = dt["score"]
            best_name= nm
    return (best_name, best_val)

# -------------------------------------------------------------------------
# 6. CLASSES
# -------------------------------------------------------------------------
class Man:
    """Handles the player's character logic."""
    def __init__(self, x, y, platform_width):
        self.x = x
        self.y = y
        self.platform_width= platform_width
        self.velocity_y= 0
        self.direction= 1
        self.move_distance= platform_width * 0.2

        # Victory Animation
        self.victory_mode  = False
        self.victory_phase = 0
        self.victory_scale = 1.0
        self.target_scale  = 1.3
        self.scale_incr    = 0.01

        self.vx_up = 0
        self.vy_up = 0

    def draw(self, surface):
        scaled_w = int(man_img.get_width() * self.victory_scale)
        scaled_h = int(man_img.get_height() * self.victory_scale)
        scaled_man = pygame.transform.smoothscale(man_img, (scaled_w, scaled_h))
        surface.blit(scaled_man, (self.x, self.y))

    def move(self):
        self.x += self.direction * self.move_distance

    def fall(self):
        self.velocity_y += 0.5
        self.y += self.velocity_y


class PendulumGame:
    """
    Manages a single round of the "Le Pendule" game.

    WIN Flow:
      1) Man does 3-phase victory.
      2) Show full-screen emojis (20).
      3) Show "YOU WIN!" => loop `win_sound` until user decides (Continue/Main Menu).
    """
    def __init__(self, difficulty, username):
        self.username = username
        self.difficulty= difficulty

        # Choose word from correct list
        if difficulty=="easy":
            wlist = easy_words
            self.timer_enabled= False
        else:
            wlist = hard_words
            self.timer_enabled= True

        chosen= random.choice(wlist)
        self.word= chosen[0].lower()
        self.hint= chosen[1]
        self.fact= chosen[2]

        # Build guessed-word array
        self.guessed_word= ["_"] * len(self.word)
        if difficulty=="easy" and len(self.word) > 1:
            self.guessed_word[0] = self.word[0]
            self.guessed_word[-1] = self.word[-1]

        self.failures= 0
        self.max_failures= 5
        self.score= 0

        # Timer
        self.time_limit= 30000
        self.start_time= pygame.time.get_ticks()
        self.chrono_warning_played= False

        # Sea
        self.sea_y= HEIGHT - sea_img.get_height()

        # Waves
        self.wave_x= 0
        self.wave_dir= 1
        self.wave_speed= 2
        self.wave_min= -wave_img.get_width()
        self.wave_max= 0

        # Platform
        self.platform_rect= pygame.Rect(
            WIDTH//2 - 200,
            self.sea_y - 200,
            400, 100
        )

        # Man
        self.man= Man(
            self.platform_rect.x,
            self.platform_rect.y - man_img.get_height(),
            self.platform_rect.width
        )

        # Pendulum
        self.pivot_x= WIDTH//2
        self.pivot_y= 0
        self.rod_length= 180
        self.pendulum_angle= 0.0
        self.pendulum_angle_vel= 0.02
        self.pendulum_angle_max= math.radians(20)
        self.strike_in_progress= False
        self.pendulum_x= self.pivot_x
        self.pendulum_y= self.pivot_y + self.rod_length

        # Game states
        self.man_move_done= False
        self.man_falling= False
        self.game_ended= False
        self.game_won= False
        self.walking_to_fish= False
        self.fish_x= self.platform_rect.right + 20
        self.fish_y= self.sea_y - 10
        self.fish_eating= False
        self.fish_midway= False
        self.fish_returned= False
        self.fish_swimming= False
        self.fish_speed= 2
        self.fish_dir= -1

        self.end_buttons_visible= False
        self.continue_button_rect= None
        self.menu_button_rect= None

        # Hearts
        self.hearts= [heart_plain_b]*3 + [heart_plain_r]*2
        self.clock= pygame.time.Clock()
        self.running= True

        # Full-screen Emojis
        self.emoji_images = emoji_images
        self.emoji_sequence_active = False
        self.emoji_index = 0
        self.emoji_interval = 500  # ms between emojis
        self.emoji_last_time = 0
        self.emoji_finished = False
        self.emoji_start_delay = 500
        self.emoji_finish_start = 0

        # Win Sound Looping
        self.win_sound_looping = False

    def run(self):
        """Main game loop for one round."""
        if not GAME_SETTINGS["music_on"]:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.set_volume(GAME_SETTINGS["music_volume"])
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)

        while self.running:
            self.clock.tick(60)
            if not self.handle_events():
                break

            if self.emoji_sequence_active:
                self.update_emoji_sequence()
            else:
                self.update()

            self.draw(screen)
            pygame.display.flip()

            # If user completes the word => man victory
            if "_" not in self.guessed_word and not self.game_ended and not self.man.victory_mode:
                pygame.mixer.music.stop()
                if win_sound:
                    win_sound.play()
                self.man.victory_mode= True

        return  # back to main_menu

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the user closes the window, stop any looping win sound
                if self.win_sound_looping and win_sound:
                    win_sound.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if (not self.game_ended
                    and not self.walking_to_fish
                    and not self.man_falling
                    and not self.man.victory_mode
                    and not self.emoji_sequence_active):

                    letter= event.unicode.lower()
                    if letter.isalpha() and len(letter) == 1:
                        self.process_guess(letter)

            # If end screen is visible, check button clicks
            if self.end_buttons_visible and event.type== pygame.MOUSEBUTTONDOWN:
                x,y= event.pos
                # The user decided => stop looping the win sound
                if self.win_sound_looping and win_sound:
                    win_sound.stop()
                    self.win_sound_looping = False

                if self.continue_button_rect and self.continue_button_rect.collidepoint(x,y):
                    self.__init__(self.difficulty, self.username)
                elif self.menu_button_rect and self.menu_button_rect.collidepoint(x,y):
                    self.running= False

        return True

    def process_guess(self, letter):
        """Check if guessed letter is in the word; update states and hearts."""
        if letter in self.word and letter not in self.guessed_word:
            if correct_sound:
                correct_sound.play()
            for i, c in enumerate(self.word):
                if c == letter and self.guessed_word[i] == "_":
                    self.guessed_word[i] = letter
                    self.score += 10
        else:
            if incorrect_sound:
                incorrect_sound.play()
            self.failures += 1
            self.strike_in_progress = True
            self.man_move_done = False
            if strike_sound:
                strike_sound.play()

            if self.failures <= 3:
                self.hearts[self.failures-1] = heart_empty_b
            else:
                self.hearts[self.failures-1] = heart_empty_r

            if self.failures == self.max_failures:
                if splash_sound:
                    splash_sound.play()

    def show_lose_end_screen(self):
        self.game_ended= True
        self.game_won= False
        self.end_buttons_visible= True
        self.setup_end_buttons()
        self.update_scoreboard(False)

    def show_win_end_screen(self):
        """
        Called after emoji sequence finishes => 
        user sees the final "YOU WIN!" overlay.
        We'll loop the `win_sound` until the user decides.
        """
        self.game_ended= True
        self.game_won= True
        self.end_buttons_visible= True
        self.setup_end_buttons()
        self.update_scoreboard(True)

        # Start looping the win sound
        if win_sound:
            win_sound.play(loops=-1)
            self.win_sound_looping = True

    def setup_end_buttons(self):
        self.continue_button_rect= pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50)
        self.menu_button_rect    = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 140, 200, 50)

    def update_scoreboard(self, win):
        if self.username not in SCOREBOARD:
            SCOREBOARD[self.username] = {"wins":0, "losses":0, "score":0}
        if win:
            SCOREBOARD[self.username]["wins"] += 1
        else:
            SCOREBOARD[self.username]["losses"] += 1
        SCOREBOARD[self.username]["score"] += self.score
        save_scoreboard()

    def update(self):
        """Update all game states: pendulum, waves, man, fish, etc."""
        if self.timer_enabled and not self.game_ended and not self.man.victory_mode:
            elapsed = pygame.time.get_ticks() - self.start_time
            remain  = self.time_limit - elapsed
            if remain <= 0:
                if chrono_endanger_sound and self.chrono_warning_played:
                    chrono_endanger_sound.stop()
                self.failures = self.max_failures
                self.walking_to_fish = True
            elif remain <= 10000 and not self.chrono_warning_played:
                self.chrono_warning_played= True
                if chrono_endanger_sound:
                    chrono_endanger_sound.play()

        # Waves
        self.wave_x += self.wave_speed * self.wave_dir
        if self.wave_x > self.wave_max:
            self.wave_x= self.wave_max
            self.wave_dir= -1
        elif self.wave_x < self.wave_min:
            self.wave_x= self.wave_min
            self.wave_dir= 1

        # Pendulum
        if (not self.strike_in_progress) and (not self.man.victory_mode):
            self.pendulum_angle += self.pendulum_angle_vel
            if self.pendulum_angle > self.pendulum_angle_max:
                self.pendulum_angle= self.pendulum_angle_max
                self.pendulum_angle_vel= -self.pendulum_angle_vel
            elif self.pendulum_angle < -self.pendulum_angle_max:
                self.pendulum_angle= -self.pendulum_angle_max
                self.pendulum_angle_vel= -self.pendulum_angle_vel
            self.update_pendulum_pos()

        # Strike
        if self.strike_in_progress and not self.game_won:
            dx= self.man.x - self.pendulum_x
            step= 5 if dx > 0 else -5
            if abs(dx) > 5:
                self.pendulum_x += step
            else:
                self.pendulum_x= self.man.x
                self.strike_in_progress= False
                if not self.man_move_done:
                    self.man.move()
                    self.man_move_done= True
                if self.failures == self.max_failures:
                    self.walking_to_fish= True

        # Fish scenario
        if self.walking_to_fish and not self.man_falling:
            if abs(self.man.x - self.fish_x) > 3:
                step= 4 if self.fish_x > self.man.x else -4
                self.man.x += step
            else:
                self.walking_to_fish= False
                self.man_falling= True

        if self.man_falling and not self.game_ended and not self.game_won:
            self.man.fall()
            if not self.fish_returned:
                if not self.fish_eating:
                    self.fish_eating= True
                if not self.fish_midway:
                    if self.fish_y > (self.man.y + man_img.get_height()//2):
                        self.fish_y -= 4
                    else:
                        self.fish_midway= True
                        self.man.y=2000
                else:
                    self.fish_y += 4
                    if self.fish_y >= self.sea_y + 20:
                        self.fish_returned= True
                        self.fish_swimming= True
                        if lose_sound:
                            lose_sound.play()
                        self.show_lose_end_screen()

            if self.fish_swimming:
                self.update_fish_swim()

        # Man victory
        if self.man.victory_mode and not self.game_ended:
            self.update_man_victory()

    def update_man_victory(self):
        """3-phase victory. After man is off-screen, start emojis."""
        sea_level = self.sea_y - (man_img.get_height() * self.man.victory_scale)
        if self.man.victory_phase == 0:
            if self.man.victory_scale < self.man.target_scale:
                self.man.victory_scale += self.man.scale_incr
            else:
                self.man.victory_phase= 1
        elif self.man.victory_phase == 1:
            if self.man.y < sea_level:
                self.man.y += 5
            else:
                self.man.victory_phase= 2
                finalX= WIDTH + 100
                finalY= -200
                dx= finalX - self.man.x
                dy= finalY - self.man.y
                length= math.hypot(dx, dy)
                if length != 0:
                    speed= 5.0
                    self.man.vx_up= speed * (dx / length)
                    self.man.vy_up= speed * (dy / length)
                else:
                    self.man.vx_up= 0
                    self.man.vy_up= -5
        else:
            # Flight
            self.man.x += self.man.vx_up
            self.man.y += self.man.vy_up
            scaled_h= man_img.get_height() * self.man.victory_scale
            scaled_w= man_img.get_width() * self.man.victory_scale
            if (self.man.x > WIDTH + scaled_w) or (self.man.y + scaled_h < 0):
                self.man.victory_mode= False
                self.start_emoji_sequence()

    def start_emoji_sequence(self):
        self.emoji_sequence_active = True
        self.emoji_index = 0
        self.emoji_last_time = pygame.time.get_ticks()
        self.emoji_finished = False

    def update_emoji_sequence(self):
        """After the last emoji, show the final Win screen => loop music."""
        if self.emoji_finished:
            now = pygame.time.get_ticks()
            if now - self.emoji_finish_start >= self.emoji_start_delay:
                self.show_win_end_screen()
                self.emoji_sequence_active = False
            return

        now = pygame.time.get_ticks()
        if now - self.emoji_last_time >= self.emoji_interval:
            self.emoji_index += 1
            self.emoji_last_time = now
            if pulse_sound:
                pulse_sound.play()

            if self.emoji_index >= len(self.emoji_images):
                self.emoji_finished = True
                self.emoji_finish_start = pygame.time.get_ticks()

    def update_pendulum_pos(self):
        px = self.pivot_x + self.rod_length * math.sin(self.pendulum_angle)
        py = self.pivot_y + self.rod_length * math.cos(self.pendulum_angle)
        self.pendulum_x = px
        self.pendulum_y = py

    def update_fish_swim(self):
        self.fish_x += self.fish_dir * self.fish_speed
        if self.fish_x < 0:
            self.fish_x= 0
            self.fish_dir= 1
        elif self.fish_x > (WIDTH - fish_img.get_width()):
            self.fish_x= WIDTH - fish_img.get_width()
            self.fish_dir= -1

    def draw_end_buttons(self, surface):
        """Draw the translucent overlay with end-of-game info & buttons."""
        overlay= pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0,0))

        if self.game_won:
            msg_surf = pixel_font_big.render("YOU WIN!", True, BLUE)
        else:
            msg_surf = pixel_font_big.render("GAME OVER!", True, WHITE)

        msg_rect = msg_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 70))

        pygame.draw.rect(surface, RED, msg_rect.inflate(30, 30), width=5)
        surface.blit(msg_surf, msg_rect)

        word_text= font.render(f"The word was: {self.word}", True, WHITE)
        fact_text= font.render(f"Fact: {self.fact}", True, WHITE)

        surface.blit(word_text, (WIDTH//2 - word_text.get_width()//2, HEIGHT//2 - 20))
        surface.blit(fact_text, (WIDTH//2 - fact_text.get_width()//2, HEIGHT//2 + 30))

        pygame.draw.rect(surface, (80,80,80), self.continue_button_rect)
        pygame.draw.rect(surface, (80,80,80), self.menu_button_rect)

        c_text= font.render("Continue", True, WHITE)
        m_text= font.render("Main Menu", True, WHITE)

        surface.blit(c_text, (self.continue_button_rect.centerx - c_text.get_width()//2,
                              self.continue_button_rect.centery - c_text.get_height()//2))
        surface.blit(m_text, (self.menu_button_rect.centerx - m_text.get_width()//2,
                              self.menu_button_rect.centery - m_text.get_height()//2))

    def draw(self, surface):
        """
        If emoji sequence is active, draw the current emoji full-screen.
        Otherwise, draw normal game or end overlay.
        """
        if self.emoji_sequence_active:
            if self.emoji_index < len(self.emoji_images):
                current_emoji = self.emoji_images[self.emoji_index]
                surface.blit(current_emoji, (0, 0))

            if self.end_buttons_visible:
                self.draw_end_buttons(surface)
            return

        # Normal game background
        surface.blit(background_img, (0,0))
        surface.blit(sea_img, (0, HEIGHT - sea_img.get_height()))
        wave_y= (HEIGHT - sea_img.get_height()) - wave_img.get_height()//2
        surface.blit(wave_img, (self.wave_x, wave_y))
        surface.blit(wave_img, (self.wave_x + wave_img.get_width(), wave_y))

        surface.blit(platform_img, self.platform_rect.topleft)

        # Pendulum
        pygame.draw.line(surface, BLUE,
                         (self.pivot_x, self.pivot_y),
                         (self.pendulum_x, self.pendulum_y),
                         3)
        bx= self.pendulum_x - pendulum_img.get_width()//2
        by= self.pendulum_y - pendulum_img.get_height()//2
        surface.blit(pendulum_img, (bx, by))

        # Man
        if self.man.y < 2000:
            self.man.draw(surface)

        # Fish
        surface.blit(fish_img, (self.fish_x, self.fish_y))

        # Hearts
        for i, h in enumerate(self.hearts):
            surface.blit(h, (50 + i*50, 20))

        # Guessed word
        gw_txt= font.render(" ".join(self.guessed_word), True, WHITE)
        surface.blit(gw_txt, (50, HEIGHT - 50))

        if not self.game_ended and not self.man.victory_mode and not self.emoji_sequence_active:
            hint_txt= small_font.render(f"Hint: {self.hint}", True, WHITE)
            surface.blit(hint_txt, (50, HEIGHT - 80))

        # Scoreboard
        usr_txt= small_font.render(f"Player: {self.username}", True, WHITE)
        surface.blit(usr_txt, (WIDTH//2 - usr_txt.get_width()//2, 20))

        sc_txt= small_font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(sc_txt, (WIDTH - 120, 20))

        best_name, best_val = get_best_score()
        y_offset_for_logo = 50
        if best_name:
            if best_name != self.username:
                best_txt= tiny_font.render(f"Best Score: {best_name} ({best_val})", True, WHITE)
            else:
                best_txt= tiny_font.render(f"Best Score: YOU! ({best_val})", True, WHITE)
            surface.blit(best_txt, (WIDTH - 200, y_offset_for_logo))
            y_offset_for_logo += 30  # shift down

        # "designed by RCA"
        rca_text= tiny_font.render("Designed by RCA ", True, WHITE)
        surface.blit(rca_text, (WIDTH - 200, y_offset_for_logo))

        # Timer if Hard
        if self.timer_enabled and not self.game_ended and not self.man.victory_mode:
            elapsed= pygame.time.get_ticks() - self.start_time
            remain_ms= self.time_limit - elapsed
            remain_s= max(0, remain_ms // 1000)
            t_txt= font.render(f"Time: {remain_s}s", True, WHITE)
            surface.blit(t_txt, (WIDTH//2 - 40, 60))

        # End overlay
        if self.end_buttons_visible:
            self.draw_end_buttons(surface)

# -------------------------------------------------------------------------
# 7. NAME PICK / ADD WORD
# -------------------------------------------------------------------------
def text_input_prompt(prompt):
    """Show a prompt and let user type text. Return typed string or None if ESC."""
    user_text= ""
    while True:
        screen.fill(BLACK)
        p_surf= font.render(prompt + user_text, True, WHITE)
        screen.blit(p_surf, (50, HEIGHT//2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_RETURN:
                    if user_text.strip() == "":
                        return "Player1"
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text= user_text[:-1]
                else:
                    user_text += event.unicode

def pick_name_menu():
    """Let user pick an existing name from scoreboard or create a new one."""
    existing_names= list(SCOREBOARD.keys())
    while True:
        screen.fill(BLACK)
        title_surf= font.render("Pick a Name or Click NEW", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 50))

        btn_width, btn_height= 200, 40
        x_base= 50
        y_base= 150
        name_buttons= []
        for i, nm in enumerate(existing_names):
            rect= pygame.Rect(x_base, y_base + i*(btn_height+10), btn_width, btn_height)
            name_buttons.append((rect, nm))
            pygame.draw.rect(screen, (80,80,80), rect)
            nm_surf= small_font.render(nm, True, WHITE)
            screen.blit(nm_surf, (rect.centerx - nm_surf.get_width()//2,
                                  rect.centery - nm_surf.get_height()//2))

        new_btn_rect= pygame.Rect(400, 200, btn_width, btn_height)
        pygame.draw.rect(screen, (120,80,80), new_btn_rect)
        new_txt= small_font.render("NEW NAME", True, WHITE)
        screen.blit(new_txt, (new_btn_rect.centerx - new_txt.get_width()//2,
                              new_btn_rect.centery - new_txt.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y= event.pos
                for rect, nm in name_buttons:
                    if rect.collidepoint(x, y):
                        return nm
                if new_btn_rect.collidepoint(x, y):
                    new_name= text_input_prompt("Enter new name (ESC to cancel): ")
                    if new_name is None:
                        break
                    return new_name

def add_new_words_menu():
    """Add a new word/hint/fact to easy_words or hard_words."""
    while True:
        screen.fill(BLACK)
        t= font.render("Add New Word", True, WHITE)
        i= small_font.render("Press E (Easy) or H (Hard). Press B to go back.", True, WHITE)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 100))
        screen.blit(i, (WIDTH//2 - i.get_width()//2, 200))
        pygame.display.flip()

        chosen_list= None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    chosen_list= easy_words
                elif event.key == pygame.K_h:
                    chosen_list= hard_words
                elif event.key == pygame.K_b:
                    return
        if chosen_list is not None:
            w= text_input_prompt("Enter new word (ESC to cancel): ")
            if w is None:
                continue
            h= text_input_prompt("Enter hint (ESC to cancel): ")
            if h is None:
                continue
            f= text_input_prompt("Enter fact (ESC to cancel): ")
            if f is None:
                f= "No special fact."
            chosen_list.append((w.lower(), h, f))

def main_menu():
    """Show the main menu with options: Easy, Hard, Add Word, Quit."""
    while True:
        screen.blit(background_img, (0,0))

        t  = font.render("Le Pendule", True, WHITE)
        e  = font.render("Easy", True, WHITE)
        hd = font.render("Hard", True, WHITE)
        aw = font.render("Add Word", True, WHITE)
        q  = font.render("Quit", True, WHITE)

        screen.blit(t,  (WIDTH//2 - t.get_width()//2, 100))
        screen.blit(e,  (WIDTH//2 - e.get_width()//2, 250))
        screen.blit(hd, (WIDTH//2 - hd.get_width()//2, 320))
        screen.blit(aw, (WIDTH//2 - aw.get_width()//2, 390))
        screen.blit(q,  (WIDTH//2 - q.get_width()//2, 460))

        # top3
        top3= get_top3_scores()
        top3_txt= small_font.render("Top 3 Scores:", True, WHITE)
        screen.blit(top3_txt, (50, 50))
        y_off= 80
        for i, (nm, sc) in enumerate(top3):
            line= small_font.render(f"{i+1}) {nm} - {sc}", True, WHITE)
            screen.blit(line, (50, y_off))
            y_off += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y= event.pos
                btn_width= 120
                center_x= WIDTH//2 - btn_width//2

                # Easy
                if center_x <= x <= center_x + btn_width and 250 <= y <= 300:
                    username= pick_name_menu()
                    if username:
                        game= PendulumGame("easy", username)
                        game.run()
                # Hard
                if center_x <= x <= center_x + btn_width and 320 <= y <= 370:
                    username= pick_name_menu()
                    if username:
                        game= PendulumGame("hard", username)
                        game.run()
                # Add Word
                if center_x <= x <= center_x + btn_width and 390 <= y <= 440:
                    add_new_words_menu()
                # Quit
                if center_x <= x <= center_x + btn_width and 460 <= y <= 510:
                    pygame.quit()
                    sys.exit()

# -------------------------------------------------------------------------
# 8. MAIN
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Check for difficulty argument
    if len(sys.argv) > 1:
        difficulty = sys.argv[1]
    else:
        difficulty = "easy"  # Default to easy if not provided

    load_scoreboard()
    username = "Joueur"  # Replace with actual username selection logic if necessary
    game = PendulumGame(difficulty, username)
    game.run()
    save_scoreboard()