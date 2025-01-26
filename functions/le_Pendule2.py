import pygame
import math
import random
import sys

# -------------------------------------------------------------------------
# 1. GLOBAL CONSTANTS & INIT
# -------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le Pendule - Cord from Top & Enhanced Scoreboard with Larger Word List")

SCOREBOARD = {}  # e.g. { "Alice": { "wins": 2, "losses":1, "score":150 }, ... }
GAME_SETTINGS = {
    "music_on": True,
    "music_volume": 1.0,
}

# -------------------------------------------------------------------------
# 2. RESOURCE LOADING
# -------------------------------------------------------------------------
def load_image(path, size=None):
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except FileNotFoundError as e:
        print(f"Error loading image: {e}")
        pygame.quit()
        sys.exit()

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound: {e}")
        return None

# IMAGES
background_img = load_image("sky.png")
platform_img   = load_image("laplateforme.png", (400, 200))
sea_img        = load_image("sea.png")
wave_img       = load_image("flot.png")
man_img        = load_image("man.png", (80, 120))
pendulum_img   = load_image("pend.png", (50, 50))
fish_img       = load_image("fish.png", (60, 100))

heart_plain_b  = load_image("heartbp.png", (30, 30))
heart_empty_b  = load_image("heartbv.png", (30, 30))
heart_plain_r  = load_image("heartrp.png", (30, 30))
heart_empty_r  = load_image("heartrv.png", (30, 30))

# SOUNDS
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)
except FileNotFoundError:
    print("Warning: background_music.mp3 not found.")

correct_sound   = load_sound("correct.wav")
incorrect_sound = load_sound("incorrect.wav")
strike_sound    = load_sound("strike.wav")
splash_sound    = load_sound("splash.wav")
win_sound       = load_sound("win.wav")
lose_sound      = load_sound("lose.wav")

# FONTS
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 26)
tiny_font = pygame.font.Font(None, 22)

# -------------------------------------------------------------------------
# 3. WORD LISTS (Expanded to >50 words each)
# -------------------------------------------------------------------------
easy_words = [
    ("algorithm",    "Step-by-step procedure for solving a problem."),
    ("binary",       "A system of numerical notation with base 2."),
    ("code",         "Instructions written in a programming language."),
    ("data",         "Information processed or stored by a computer."),
    ("debug",        "To find and fix errors in code."),
    ("array",        "A collection of items stored at contiguous memory locations."),
    ("boolean",      "A data type with two possible values: true or false."),
    ("comment",      "Text in code ignored by the compiler/interpreter."),
    ("compile",      "To transform code into an executable form."),
    ("function",     "A reusable block of code that performs a task."),
    ("variable",     "A named storage location for a value."),
    ("string",       "A sequence of characters."),
    ("integer",      "A whole number, positive, negative, or zero."),
    ("float",        "A real (floating-point) number."),
    ("loop",         "A structure that repeats a block of code."),
    ("iteration",    "A single pass through a loop."),
    ("list",         "A dynamic collection of items in Python."),
    ("tuple",        "An immutable sequence of items in Python."),
    ("dictionary",   "A key-value mapping in Python."),
    ("queue",        "A FIFO structure for data (first-in, first-out)."),
    ("stack",        "A LIFO structure (last-in, first-out)."),
    ("pointer",      "A variable that stores a memory address."),
    ("reference",    "An alias or pointer-like concept in high-level languages."),
    ("git",          "A distributed version control system."),
    ("github",       "A platform for hosting Git repositories."),
    ("shell",        "A command-line interface to an operating system."),
    ("script",       "A file containing code to be executed."),
    ("syntax",       "The rules that define a language's structure."),
    ("token",        "A lexical unit in parsing or compiling."),
    ("operator",     "A symbol that tells the compiler/interpreter to perform a task."),
    ("operand",      "A value on which an operator acts."),
    ("character",    "A single letter or symbol in text."),
    ("keyword",      "A reserved word with special meaning in a language."),
    ("logic",        "A branch dealing with formal principles of reasoning."),
    ("condition",    "A boolean expression used to control flow."),
    ("package",      "A namespace that organizes classes or modules."),
    ("import",       "A statement that brings in external code."),
    ("module",       "A file containing Python definitions and statements."),
    ("runtime",      "The period when a program is executing."),
    ("exception",    "An event that disrupts normal flow of instructions."),
    ("handle",       "To deal with or manage an exception."),
    ("class",        "A blueprint for objects in object-oriented programming."),
    ("object",       "An instance of a class."),
    ("constructor",  "A special method to initialize a newly created object."),
    ("method",       "A function that belongs to a class."),
    ("docstring",    "A string used to describe a function/module/class."),
    ("hash",         "A function that maps data to a fixed-size output."),
    ("index",        "An integer position in a sequence."),
    ("bit",          "A binary digit (0 or 1)."),
    ("byte",         "A unit of data, typically 8 bits."),
    ("server",       "A computer or program that provides services to other devices."),
    ("client",       "A program or device that accesses a service on a server."),
    ("port",         "A communication endpoint for network services."),
]

hard_words = [
    ("asymptotic",    "Behavior of a function as it approaches a limit."),
    ("heuristic",     "A problem-solving approach with practical methods."),
    ("polymorphism",  "A function that can operate on multiple types."),
    ("recursion",     "A function that calls itself."),
    ("syntax",        "The rules that define a language's structure."),
    ("memoization",   "An optimization technique storing function results."),
    ("backtracking",  "A DFS approach to solving constraints systematically."),
    ("serialization", "Converting an object into a storable/transmittable format."),
    ("deserialization","Reading a serialized object to recreate it in memory."),
    ("combinatorics", "Branch of math focusing on counting, arrangement, combination."),
    ("cryptography",  "Securing information by transforming it in an unreadable form."),
    ("interpreter",   "Executes code line-by-line (Python, Ruby, etc.)."),
    ("compiler",      "Translates code into machine code or bytecode."),
    ("monad",         "A structure that represents computations (in functional prog)."),
    ("lambda",        "An anonymous function, often used as a short inline expression."),
    ("bigodata",      "Branch of CS dealing with large data sets (big data)."),
    ("distributed",   "Describes systems spread across multiple machines."),
    ("cloud",         "Remote servers on the internet storing and accessing data."),
    ("container",     "A lightweight OS-level virtualization method (Docker)."),
    ("microservices", "An architectural style building an app as a suite of services."),
    ("refactoring",   "Restructuring existing code without changing its behavior."),
    ("immutability",  "Once created, data cannot be changed."),
    ("concurrency",   "Running multiple tasks simultaneously or in overlapping time."),
    ("parallelism",   "Executing multiple tasks at literally the same time."),
    ("deadlock",      "A situation where tasks wait indefinitely for resources."),
    ("starvation",    "A process never gets required resources to proceed."),
    ("throughput",    "Rate of successful message delivery over a channel."),
    ("latency",       "Delay between cause and effect, e.g. data transfer time."),
    ("scalability",   "The ability of a system to handle growth."),
    ("responsiveness","How quickly a system responds to input."),
    ("serialization", "Converting in-memory objects to a storable format."),
    ("idempotent",    "An operation that can be applied multiple times without change."),
    ("transaction",   "A database concept that groups operations into a single unit."),
    ("cursor",        "A DB pointer to a set of rows returned by a query."),
    ("restful",       "An architectural style for web services using HTTP requests."),
    ("websocket",     "A protocol for two-way communication over one TCP connection."),
    ("agile",         "A project management/Dev method favoring iterative development."),
    ("kanban",        "A lean method to manage and improve work across systems."),
    ("scrum",         "An agile framework to manage iterative tasks/complex projects."),
    ("pipeline",      "A set of data processing stages connected in series."),
    ("orchestration", "Automated arrangement, coordination, management of systems."),
    ("containerization","Packaging software with dependencies into a container."),
    ("hypervisor",    "Software that creates and runs virtual machines."),
    ("machinelearning","A subset of AI letting systems learn from data."),
    ("deepneuralnet", "An artificial neural network with multiple layers."),
    ("regression",    "A statistical approach for modeling relationships in data."),
    ("classification","Labeling items into categories from input data."),
    ("quicksort",     "An efficient divide-and-conquer sorting algorithm."),
    ("mergesort",     "A stable divide-and-conquer sorting algorithm."),
    ("bubblesort",    "A simple, but inefficient sorting algorithm."),
    ("bfs",           "Breadth-first search in graphs/trees."),
    ("dfs",           "Depth-first search in graphs/trees."),
    ("dijkstra",      "An algorithm for shortest paths in weighted graphs."),
    ("bellmanford",   "A DP-based algorithm for shortest paths with negative edges."),
    ("floydwarshall", "An algorithm to find shortest paths among all pairs of nodes."),
]

# -------------------------------------------------------------------------
# 6. HELPER SCOREBOARD FUNCTIONS
# -------------------------------------------------------------------------
def get_top3_scores():
    """
    Returns a list of (name, score) sorted desc by score, up to 3 items.
    """
    all_scores = [(name, data["score"]) for name, data in SCOREBOARD.items()]
    sorted_scores = sorted(all_scores, key=lambda x: x[1], reverse=True)
    return sorted_scores[:3]

def get_best_score():
    """
    Returns (best_name, best_score) for highest scoring player, or (None, 0) if none exist.
    """
    if not SCOREBOARD:
        return (None, 0)
    best_name = None
    best_scr = 0
    for name, data in SCOREBOARD.items():
        if data["score"] > best_scr:
            best_scr = data["score"]
            best_name = name
    return (best_name, best_scr)

# -------------------------------------------------------------------------
# 7. CLASSES
# -------------------------------------------------------------------------
class Man:
    """Represents the man on the platform or falling."""
    def __init__(self, x, y, platform_width):
        self.x = x
        self.y = y
        self.width = man_img.get_width()
        self.height = man_img.get_height()
        self.platform_width = platform_width
        self.velocity_y = 0
        self.direction = 1
        self.move_distance = platform_width * 0.2

    def draw(self, surface):
        surface.blit(man_img, (self.x, self.y))

    def move(self):
        self.x += self.direction * self.move_distance

    def fall(self):
        self.velocity_y += 0.5
        self.y += self.velocity_y


class PendulumGame:
    """
    Main logic:
      - Blue line from pivot => center of pendulum
      - 5 strikes => last triggers fish scenario
      - Win => man flies up until he disappears
      - Scoreboard with top3 in menu & best score displayed in game
    """
    def __init__(self, difficulty, username):
        self.username = username
        self.difficulty = difficulty
        # Word selection
        wlist = easy_words if difficulty == "easy" else hard_words
        chosen = random.choice(wlist)
        self.word, self.hint = chosen[0].lower(), chosen[1]
        self.guessed_word = ["_"] * len(self.word)
        if difficulty == "easy" and len(self.word) > 1:
            self.guessed_word[0] = self.word[0]
            self.guessed_word[-1] = self.word[-1]

        self.failures = 0
        self.max_failures = 5
        self.score = 0

        # Sea & wave
        self.sea_y = HEIGHT - sea_img.get_height()
        self.wave_x = 0
        self.wave_speed = 2

        # Platform
        self.platform_rect = pygame.Rect(
            WIDTH // 2 - 200,
            self.sea_y - 200,
            400,
            100
        )

        # Man at left edge
        self.man = Man(
            self.platform_rect.x,
            self.platform_rect.y - man_img.get_height(),
            self.platform_rect.width
        )

        # Pendulum pivot top-center
        self.pivot_x = WIDTH // 2
        self.pivot_y = 0
        # Pendulum init position (just for visuals)
        self.pendulum_x = self.pivot_x - 50
        self.pendulum_y = 100
        self.strike_in_progress = False
        self.man_move_done = False
        self.man_falling = False
        self.man_on_pendulum = False
        self.game_ended = False
        self.game_won = False

        # 5th => fish
        self.walking_to_fish = False

        # Fish
        self.fish_x = self.platform_rect.right + 20
        self.fish_y = self.sea_y + 20
        self.fish_eating = False
        self.fish_midway = False
        self.fish_returned = False
        self.fish_swimming = False
        self.fish_speed = 2
        self.fish_dir = -1

        # new: man_flying_up => if user wins => man goes up
        self.man_flying_up = False

        self.hearts = [heart_plain_b] * 3 + [heart_plain_r] * 2
        self.end_buttons_visible = False
        self.continue_button_rect = None
        self.menu_button_rect = None

        self.clock = pygame.time.Clock()

    def run(self):
        if not GAME_SETTINGS["music_on"]:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.set_volume(GAME_SETTINGS["music_volume"])
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)

        running = True
        while running:
            self.clock.tick(60)
            running = self.handle_events()
            self.update()
            self.draw(screen)
            pygame.display.flip()

            # Instead of calling end screen immediately when user guesses all letters,
            # we set self.man_flying_up = True => man floats up
            if "_" not in self.guessed_word and not self.game_ended and not self.man_flying_up:
                # user completed the word => man flies up
                self.man_flying_up = True

                # STOP background music
                pygame.mixer.music.stop()

                # then play win sound
                if win_sound:
                    win_sound.play()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if (not self.game_ended and not self.walking_to_fish
                    and not self.man_falling and not self.man_flying_up):
                    letter = event.unicode.lower()
                    if letter.isalpha() and len(letter) == 1:
                        self.process_guess(letter)

            if self.end_buttons_visible and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.continue_button_rect and self.continue_button_rect.collidepoint(x, y):
                    self.__init__(self.difficulty, self.username)
                elif self.menu_button_rect and self.menu_button_rect.collidepoint(x, y):
                    return False

        return True

    def process_guess(self, letter):
        if letter in self.word and letter not in self.guessed_word:
            if correct_sound:
                correct_sound.play()
            for i, c in enumerate(self.word):
                if c == letter and self.guessed_word[i] == "_":
                    self.guessed_word[i] = letter
                    self.score += 10
        else:
            # incorrect
            if incorrect_sound:
                incorrect_sound.play()
            self.failures += 1

            # a horizontal "strike" from pendulum_x => man.x
            self.strike_in_progress = True
            self.man_move_done = False
            if strike_sound:
                strike_sound.play()

            # hearts
            if self.failures <= 3:
                self.hearts[self.failures - 1] = heart_empty_b
            elif self.failures <= 5:
                self.hearts[self.failures - 1] = heart_empty_r

            if self.failures == self.max_failures:
                # fish scenario after strike
                if splash_sound:
                    splash_sound.play()

    def show_lose_end_screen(self):
        self.game_ended = True
        self.game_won = False
        self.end_buttons_visible = True
        self.setup_end_buttons()
        self.update_scoreboard(win=False)

    def show_win_end_screen(self):
        self.game_ended = True
        self.game_won = True
        self.end_buttons_visible = True
        self.setup_end_buttons()
        self.update_scoreboard(win=True)

    def setup_end_buttons(self):
        self.continue_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)
        self.menu_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50)

    def update_scoreboard(self, win):
        if self.username not in SCOREBOARD:
            SCOREBOARD[self.username] = {"wins": 0, "losses": 0, "score": 0}
        if win:
            SCOREBOARD[self.username]["wins"] += 1
        else:
            SCOREBOARD[self.username]["losses"] += 1
        SCOREBOARD[self.username]["score"] += self.score

    def update(self):
        # if strike => move pendulum => man.x
        if self.strike_in_progress and not self.game_won:
            dx = self.man.x - self.pendulum_x
            step = 5 if dx > 0 else -5
            if abs(dx) > 5:
                self.pendulum_x += step
            else:
                self.pendulum_x = self.man.x
                self.strike_in_progress = False
                if not self.man_move_done:
                    self.man.move()
                    self.man_move_done = True
                if self.failures == self.max_failures:
                    self.walking_to_fish = True

        # fish scenario => man walks => fish => man falls => fish leaps
        if self.walking_to_fish and not self.man_falling:
            if abs(self.man.x - self.fish_x) > 3:
                step = 4 if self.fish_x > self.man.x else -4
                self.man.x += step
            else:
                self.walking_to_fish = False
                self.man_falling = True

        if self.man_falling and not self.game_won:
            self.man.fall()
            if not self.fish_returned:
                if not self.fish_eating:
                    self.fish_eating = True
                if not self.fish_midway:
                    if self.fish_y > (self.man.y + self.man.height // 2):
                        self.fish_y -= 4
                    else:
                        self.fish_midway = True
                        self.man.y = 2000
                else:
                    self.fish_y += 4
                    if self.fish_y >= self.sea_y + 20:
                        self.fish_returned = True
                        self.fish_swimming = True
                        if lose_sound:
                            lose_sound.play()
                        self.show_lose_end_screen()
            if self.fish_swimming:
                self.update_fish_swim()

        # if man_flying_up => man goes up until vanish => end screen
        if self.man_flying_up and not self.game_ended:
            self.man.y -= 3
            if self.man.y + self.man.height < 0:
                self.show_win_end_screen()

        # fish free swim
        if self.fish_swimming:
            self.update_fish_swim()

    def update_fish_swim(self):
        self.fish_x += self.fish_dir * self.fish_speed
        if self.fish_x < 0:
            self.fish_x = 0
            self.fish_dir = 1
        elif self.fish_x > WIDTH - fish_img.get_width():
            self.fish_x = WIDTH - fish_img.get_width()
            self.fish_dir = -1

    def draw_end_buttons(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        msg = "You Win!" if self.game_won else "Game Over!"
        end_text = font.render(msg, True, WHITE)
        word_text = font.render(f"The word was: {self.word}", True, WHITE)
        hint_text = font.render(f"Hint: {self.hint}", True, WHITE)

        surface.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 70))
        surface.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2 - 20))
        surface.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 30))

        pygame.draw.rect(surface, (80, 80, 80), self.continue_button_rect)
        pygame.draw.rect(surface, (80, 80, 80), self.menu_button_rect)

        c_text = font.render("Continue", True, WHITE)
        m_text = font.render("Main Menu", True, WHITE)

        surface.blit(c_text, (self.continue_button_rect.centerx - c_text.get_width() // 2,
                              self.continue_button_rect.centery - c_text.get_height() // 2))
        surface.blit(m_text, (self.menu_button_rect.centerx - m_text.get_width() // 2,
                              self.menu_button_rect.centery - m_text.get_height() // 2))

    def draw(self, surface):
        # background
        surface.blit(background_img, (0, 0))

        # sea
        surface.blit(sea_img, (0, self.sea_y))
        # wave
        wave_y = self.sea_y - wave_img.get_height() // 2
        surface.blit(wave_img, (self.wave_x, wave_y))
        surface.blit(wave_img, (self.wave_x + wave_img.get_width(), wave_y))
        self.wave_x -= self.wave_speed
        if self.wave_x <= -wave_img.get_width():
            self.wave_x = 0

        # platform
        surface.blit(platform_img, self.platform_rect.topleft)

        # cord: pivot => center of pendulum
        pend_cx = self.pendulum_x + pendulum_img.get_width() // 2
        pend_cy = self.pendulum_y + pendulum_img.get_height() // 2
        pygame.draw.line(surface, BLUE, (self.pivot_x, self.pivot_y), (pend_cx, pend_cy), 3)

        # pendulum
        surface.blit(pendulum_img, (self.pendulum_x, self.pendulum_y))

        # man
        if self.man.y < 2000:
            self.man.draw(surface)

        # fish
        surface.blit(fish_img, (self.fish_x, self.fish_y))

        # hearts
        for i, h in enumerate(self.hearts):
            surface.blit(h, (50 + i * 50, 20))

        # guessed word
        gw_txt = font.render(" ".join(self.guessed_word), True, WHITE)
        surface.blit(gw_txt, (50, HEIGHT - 50))

        # hint
        hint_txt = small_font.render(f"Hint: {self.hint}", True, WHITE)
        surface.blit(hint_txt, (50, HEIGHT - 80))

        # scoreboard
        usr_txt = small_font.render(f"Player: {self.username}", True, WHITE)
        surface.blit(usr_txt, (WIDTH // 2 - usr_txt.get_width() // 2, 20))

        # current user score
        sc_txt = small_font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(sc_txt, (WIDTH - 120, 20))

        # best overall score
        best_name, best_scr = get_best_score()
        if best_name:
            if best_name != self.username:
                best_txt = tiny_font.render(f"Best Score: {best_name} ({best_scr})", True, WHITE)
            else:
                best_txt = tiny_font.render(f"Best Score: YOU! ({best_scr})", True, WHITE)
            surface.blit(best_txt, (WIDTH - 200, 50))

        if self.end_buttons_visible:
            self.draw_end_buttons(surface)


# -------------------------------------------------------------------------
# 6. HELPER MENUS & FUNCTIONS
# -------------------------------------------------------------------------
def enter_user_name():
    name = ""
    prompt_text = "Enter your name: "
    while True:
        screen.fill(BLACK)
        p_surf = font.render(prompt_text + name, True, WHITE)
        screen.blit(p_surf, (50, HEIGHT // 2 - 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() == "":
                        name = "Player1"
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15:
                        name += event.unicode

def text_input_prompt(prompt):
    user_text = ""
    while True:
        screen.fill(BLACK)
        surf = font.render(prompt + user_text, True, WHITE)
        screen.blit(surf, (50, HEIGHT // 2 - 20))
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
                        return None
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

def get_word_and_hint():
    w = text_input_prompt("Enter new word (ESC to cancel): ")
    if w is None:
        return (None, None)
    h = text_input_prompt("Enter hint (ESC to cancel): ")
    if h is None:
        return (None, None)
    return (w.lower(), h)

def add_new_words_menu():
    while True:
        screen.fill(BLACK)
        t = font.render("Add New Word", True, WHITE)
        i = small_font.render("Press E (Easy) or H (Hard). Press B to go back.", True, WHITE)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 100))
        screen.blit(i, (WIDTH // 2 - i.get_width() // 2, 200))
        pygame.display.flip()

        chosen_list = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    chosen_list = easy_words
                elif event.key == pygame.K_h:
                    chosen_list = hard_words
                elif event.key == pygame.K_b:
                    return
        if chosen_list is not None:
            w, h = get_word_and_hint()
            if w is not None and h is not None:
                chosen_list.append((w, h))
            continue

def main_menu():
    while True:
        screen.blit(background_img, (0, 0))

        t = font.render("Le Pendule", True, WHITE)
        e = font.render("Easy", True, WHITE)
        hd = font.render("Hard", True, WHITE)
        aw = font.render("Add Word", True, WHITE)
        q = font.render("Quit", True, WHITE)

        screen.blit(t,  (WIDTH // 2 - t.get_width() // 2, 100))
        screen.blit(e,  (WIDTH // 2 - e.get_width() // 2, 250))
        screen.blit(hd, (WIDTH // 2 - hd.get_width() // 2, 320))
        screen.blit(aw, (WIDTH // 2 - aw.get_width() // 2, 390))
        screen.blit(q,  (WIDTH // 2 - q.get_width() // 2, 460))

        # Show top 3 scoreboard
        top3 = get_top3_scores()
        top3_txt = small_font.render("Top 3 Scores:", True, WHITE)
        screen.blit(top3_txt, (50, 50))
        y_off = 80
        for i, (nm, sc) in enumerate(top3):
            line = small_font.render(f"{i+1}) {nm} - {sc}", True, WHITE)
            screen.blit(line, (50, y_off))
            y_off += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                btn_width = 120
                center_x = WIDTH // 2 - btn_width // 2
                if center_x <= x <= center_x + btn_width and 250 <= y <= 300:
                    username = enter_user_name()
                    game = PendulumGame("easy", username)
                    game.run()
                if center_x <= x <= center_x + btn_width and 320 <= y <= 370:
                    username = enter_user_name()
                    game = PendulumGame("hard", username)
                    game.run()
                if center_x <= x <= center_x + btn_width and 390 <= y <= 440:
                    add_new_words_menu()
                if center_x <= x <= center_x + btn_width and 460 <= y <= 510:
                    pygame.quit()
                    sys.exit()

# -------------------------------------------------------------------------
# 7. MAIN
# -------------------------------------------------------------------------
if __name__ == "__main__":
    main_menu()
