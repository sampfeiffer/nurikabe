import pygame

from level import Level
from position import Position


class Screen:
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 500
    MIN_BORDER = 5

    BLACK = 3 * [0]
    BOARD_COLOR = 3 * [230]  # off-white
    BACKGROUND_COLOR = 3 * [160]  # gray

    def __init__(self, level: Level):
        self.screen = pygame.display.set_mode(size=(Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT))
        pygame.display.set_caption('Nurikabe')
        self.screen.fill(self.BACKGROUND_COLOR)

        self.cell_width = None
        self.font_size = None
        self.set_component_sizes(level)

    def set_component_sizes(self, level: Level) -> None:
        self.set_cell_width(level.width_in_cells, level.height_in_cells)
        self.set_font_size()

    def set_cell_width(self, width_in_cells: int, height_in_cells: int) -> None:
        max_board_width = self.SCREEN_WIDTH - 2 * self.MIN_BORDER
        max_cell_width = int(max_board_width / width_in_cells)

        max_board_height = self.SCREEN_HEIGHT - 2 * self.MIN_BORDER
        max_cell_height = int(max_board_height / height_in_cells)

        self.cell_width = min((max_cell_width, max_cell_height))

    def set_font_size(self) -> None:
        self.font_size = int(0.8 * self.cell_width)

    def get_cell_location(self, board_rect: pygame.Rect, row_number: int, col_number: int) -> Position:
        left = board_rect.left + self.cell_width * col_number
        top = board_rect.top + self.cell_width * row_number
        return Position(left, top)

    @staticmethod
    def update_screen() -> None:
        pygame.display.flip()