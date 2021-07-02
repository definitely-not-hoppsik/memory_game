import pygame
import sys
import random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
COLORS = {'red': (255, 0, 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255),
          'cyan': (0, 255, 255),
          'magenta': (255, 0, 255),
          'gray': (128, 128, 128),
          'silver': (192, 192, 192),
          'maroon': (128, 0, 0),
          'olive': (128, 128, 0),
          'purple': (128, 0, 128)}


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CARD_SIZE = 80


def game_quit():
    pygame.quit()
    sys.exit()


def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('cannot load an image')
        raise SystemExit(message)
    image = image.convert_alpha()
    return image, image.get_rect()


class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, hidden_color) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.color = WHITE
        self.hidden_color = hidden_color
        self.width = 80
        self.height = 80
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_current_color(self):
        return self.image.get_colorkey()

    def get_hidden_color(self):
        return self.hidden_color

    def hide_color(self):
        self.image.fill(self.color)

    def show_color(self):
        self.image.fill(self.hidden_color)


class Game:
    def __init__(self) -> None:
        self.cards = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.turned_cards = pygame.sprite.Group()
        self.cards_rows = 4
        self.cards_columns = 5
        self.board_x = 50
        self.board_y = 50
        self.board_space = 10

    def get_cards(self):
        return self.cards

    def show_hidden_after_click(self, mouse_sprite_location):
        for card in self.cards:
            if pygame.sprite.collide_rect(mouse_sprite_location, card):
                print('h9')
                print(card.get_current_color())
                card.show_color()
                self.turned_cards.add(card)
                print(card.get_current_color())

        print(self.turned_cards)

        if len(self.turned_cards) > 2:
            turned_card_colors = []
            for card in self.turned_cards:
                turned_card_colors.append(card.get_hidden_color)
                # TODO

            if turned_card_colors[0] == turned_card_colors[1]:
                card.hide_color()

            self.turned_cards.empty()

    def make_cards(self):
        list_of_colors = [rgb for color, rgb in COLORS.items()]
        list_of_colors += list_of_colors
        random.shuffle(list_of_colors)

        # TODO
        for i in range(0, self.cards_rows*2, 2):
            for j in range(0, self.cards_columns*2, 2):
                card = Card(self.board_x + self.board_x*i,
                            self.board_y + self.board_y*j,
                            list_of_colors[i+j])
                self.cards.add(card)

    def make_sprites(self):
        self.all_sprites.add(self.cards)
        print(self.cards)

    def draw_sprites(self):
        self.all_sprites.update()
        self.all_sprites.draw(surface)


class Sprite_mouse_location(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, 1, 1)

    def update(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        self.rect.x = mouse_position[0]
        self.rect.y = mouse_position[1]


# pygame variables
pygame.init()
window_width = 1024
window_height = 768
surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('memory game')
clock = GAME_TIME.Clock()

# game variables
game = Game()
game.make_cards()
game.make_sprites()
mouse_sprite_location = Sprite_mouse_location()

while True:

    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            game_quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.show_hidden_after_click(mouse_sprite_location)

    surface.fill(BLACK)
    game.draw_sprites()
    mouse_sprite_location.update()

    clock.tick(30)
    pygame.display.update()
