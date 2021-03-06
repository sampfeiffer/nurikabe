from typing import Optional
import pygame

from level import Level
from pixel_position import PixelPosition
from color import Color
from text_type import TextType


class Screen:
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 500
    MIN_BORDER = 5
    SHOULD_APPLY_ANTI_ALIAS = True

    SOLVER_BUTTON_RECT_WIDTH = 150
    SOLVER_BUTTON_RECT_HEIGHT = 20
    SOLVER_BUTTON_FONT_SIZE = 12

    GAME_STATUS_RECT_WIDTH = int(0.75 * SCREEN_WIDTH)
    GAME_STATUS_RECT_HEIGHT = 30
    PUZZLE_SOLVED_FONT_SIZE = 25
    FONT = 'Courier'

    def __init__(self, level: Level):
        self.screen = pygame.display.set_mode(size=(Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT))
        pygame.display.set_caption('Nurikabe')
        self.screen.fill(Color.GRAY.value)

        self.top_left_of_game_status = self.get_top_left_of_game_status()
        self.cell_width = self.get_cell_width(level.number_of_rows, level.number_of_columns)
        self.top_left_of_board = self.get_top_left_of_board(level.number_of_columns)

        self.font_map = {
            TextType.CELL: self.get_cell_font(),
            TextType.PUZZLE_SOLVED: pygame.font.SysFont(self.FONT, self.PUZZLE_SOLVED_FONT_SIZE),
            TextType.SOLVER_BUTTON: pygame.font.SysFont(self.FONT, self.SOLVER_BUTTON_FONT_SIZE)
        }

    def get_top_left_of_game_status(self) -> PixelPosition:
        left = int((self.SCREEN_WIDTH - self.GAME_STATUS_RECT_WIDTH) / 2)
        top = self.SCREEN_HEIGHT - (self.GAME_STATUS_RECT_HEIGHT + self.MIN_BORDER)
        return PixelPosition(x_coordinate=left, y_coordinate=top)

    def get_cell_width(self, number_of_rows: int, number_of_columns: int) -> int:
        max_board_width = self.SCREEN_WIDTH - 2 * self.MIN_BORDER
        max_cell_width = int(max_board_width / number_of_columns)

        height_for_non_board_components = 2 * self.MIN_BORDER + self.GAME_STATUS_RECT_HEIGHT + \
            self.SOLVER_BUTTON_RECT_HEIGHT
        max_board_height = self.SCREEN_HEIGHT - height_for_non_board_components
        max_cell_height = int(max_board_height / number_of_rows)

        return min((max_cell_width, max_cell_height))

    def get_top_left_of_board(self, number_of_columns: int) -> PixelPosition:
        left_border_size = self.get_actual_left_border_size(number_of_columns)
        return PixelPosition(x_coordinate=left_border_size, y_coordinate=Screen.MIN_BORDER)

    def get_actual_left_border_size(self, number_of_columns: int) -> int:
        actual_board_width = self.cell_width * number_of_columns
        return int((self.SCREEN_WIDTH - actual_board_width) / 2)

    def get_cell_font(self) -> pygame.font.SysFont:
        font_size = self.get_cell_font_size()
        return pygame.font.SysFont(self.FONT, font_size)

    def get_cell_font_size(self) -> int:
        return int(0.8 * self.cell_width)

    def get_cell_location(self, board_rect: pygame.Rect, row_number: int, col_number: int) -> PixelPosition:
        left = board_rect.left + self.cell_width * col_number
        top = board_rect.top + self.cell_width * row_number
        return PixelPosition(x_coordinate=left, y_coordinate=top)

    def draw_rect(self, color: Color, rect: pygame.Rect, width: int, text: Optional[str] = None,
                  text_color: Optional[Color] = None, text_type: TextType = TextType.CELL) -> None:
        pygame.draw.rect(surface=self.screen, color=color.value, rect=rect, width=width)
        if text is not None:
            if text_color is None:
                raise RuntimeError('text_color must be provided if text is provided')
            font = self.font_map[text_type]
            text = font.render(text, self.SHOULD_APPLY_ANTI_ALIAS, text_color.value)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    @staticmethod
    def update_screen() -> None:
        pygame.display.flip()
