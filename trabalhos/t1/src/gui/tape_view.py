import pygame

from tape import Tape
from mark import format_mark

CELL_SIZE = 50
CELL_PADDING = 2

COLORS = {
    'background': (220, 220, 220),
    'cell': (255, 255, 255),
    'highlight': (255, 230, 153),
    'text': (0, 0, 0),
    'index': (100, 100, 100),
    'head': (220, 20, 60)
}

class TapeView:
    def __init__(self, tape: Tape, y_position: int, label: str, visible_cells=16):
        self.tape = tape
        self.y_position = y_position
        self.label = label
        self.visible_cells = visible_cells
        
    def draw(self, screen, title_font, regular_font, small_font):
        self._draw_label(screen, title_font)
        self._draw_tape_background(screen)
        self._draw_cells(screen, regular_font)
        self._draw_head(screen)
        self._draw_indices(screen, small_font)
        
    def _draw_label(self, screen, font):
        label_surface = font.render(self.label, True, COLORS['text'])
        screen.blit(label_surface, (50, self.y_position - 20))
        
    def _draw_tape_background(self, screen):
        tape_width = self.visible_cells * CELL_SIZE
        tape_rect = pygame.Rect(50, self.y_position + 30, tape_width, CELL_SIZE)
        pygame.draw.rect(screen, COLORS['background'], tape_rect)
        pygame.draw.rect(screen, COLORS['text'], tape_rect, 2)
        
    def _draw_cells(self, screen, font):
        start_pos = max(0, self.tape.head - self.visible_cells // 2)
        for i in range(self.visible_cells):
            cell_pos = start_pos + i
            x = 50 + i * CELL_SIZE
            self._draw_single_cell(screen, font, cell_pos, x)
            
    def _draw_single_cell(self, screen, font, cell_pos, x):
        cell_rect = pygame.Rect(x, self.y_position + 30, CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING)
        color = COLORS['highlight'] if cell_pos == self.tape.head else COLORS['cell']
        pygame.draw.rect(screen, color, cell_rect)
        pygame.draw.rect(screen, COLORS['text'], cell_rect, 1)
        
        value = format_mark(self.tape.content.get(cell_pos, "B"))

        text = font.render(str(value), True, COLORS['text'])
        screen.blit(text, text.get_rect(center=cell_rect.center))
        
    def _draw_head(self, screen):
        start_pos = max(0, self.tape.head - self.visible_cells // 2)
        head_x = 50 + (self.tape.head - start_pos) * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.polygon(screen, COLORS['head'], [
            (head_x, self.y_position + 20),
            (head_x - 7, self.y_position + 10),
            (head_x + 7, self.y_position + 10)
        ])
        
    def _draw_indices(self, screen, font):
        start_pos = max(0, self.tape.head - self.visible_cells // 2)
        for i in range(self.visible_cells):
            cell_pos = start_pos + i
            x = 50 + i * CELL_SIZE + CELL_SIZE // 2
            text = font.render(str(cell_pos), True, COLORS['index'])
            screen.blit(text, text.get_rect(center=(x, self.y_position + 30 + CELL_SIZE + 15)))