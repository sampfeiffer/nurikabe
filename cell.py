from typing import Optional
import pygame

from screen import Screen
from cell_state import CellState
from position import Position


class Cell:
    CENTER_DOT = '\u2022'

    def __init__(self, row_number: int, col_number: int, initial_value: Optional[int], cell_location: Position,
                 screen: Screen):
        self.row_number = row_number
        self.col_number = col_number
        self.initial_value = initial_value
        self.cell_location = cell_location
        self.screen = screen

        self.is_clickable = self.initial_value is None
        self.cell_state = CellState.EMPTY

        self.rect = self.get_rect()
        self.font = pygame.font.SysFont('Courier', self.screen.font_size)

        self.draw_initial_value()

    def get_rect(self) -> pygame.Rect:
        width = self.screen.cell_width
        height = self.screen.cell_width
        return pygame.Rect(self.cell_location.x_coordinate, self.cell_location.y_coordinate, width, height)

    def draw_initial_value(self) -> None:
        self.draw_empty_cell()
        if self.initial_value is not None:
            text = self.font.render(str(self.initial_value), True, Screen.BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            self.screen.screen.blit(text, text_rect)

    def draw_empty_cell(self) -> None:
        pygame.draw.rect(surface=self.screen.screen, color=Screen.BOARD_COLOR, rect=self.rect, width=0)  # background
        pygame.draw.rect(surface=self.screen.screen, color=Screen.BLACK, rect=self.rect, width=1)  # border

    def draw_wall_cell(self) -> None:
        pygame.draw.rect(surface=self.screen.screen, color=Screen.BLACK, rect=self.rect, width=0)

    def draw_non_wall_cell(self) -> None:
        self.draw_empty_cell()  # first clear out the cell
        text = self.font.render(self.CENTER_DOT, True, Screen.BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.screen.blit(text, text_rect)

    def update_cell_state(self, new_cell_state: CellState) -> None:
        self.cell_state = new_cell_state
        if new_cell_state is CellState.EMPTY:
            self.draw_empty_cell()
        elif new_cell_state is CellState.WALL:
            self.draw_wall_cell()
        elif new_cell_state is CellState.NON_WALL:
            self.draw_non_wall_cell()
        else:
            raise RuntimeError('This should not be possible')

    def is_inside_cell(self, event_position: Position) -> bool:
        return self.rect.collidepoint(event_position.coordinates)

    def handle_cell_click(self) -> None:
        if not self.is_clickable:
            return

        new_cell_state = self.cell_state.get_next_in_cycle()
        self.update_cell_state(new_cell_state)