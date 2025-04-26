import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, 20)
        self.handle_rect = pygame.Rect(x, y - 5, 15, 30)
        self.min = min_val
        self.max = max_val
        self.val = initial_val
        self.dragging = False
        self.update_handle()

    def update_handle(self):
        ratio = (self.val - self.min) / (self.max - self.min)
        x = self.rect.left + ratio * self.rect.width
        self.handle_rect.centerx = x

    def update_value(self, mouse_pos):
        x = max(self.rect.left, min(mouse_pos[0], self.rect.right))
        self.val = self.min + ((x - self.rect.left) / self.rect.width) * (self.max - self.min)
        self.update_handle()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos)

    def draw(self, surface, font):
        pygame.draw.rect(surface, (100, 100, 100), self.rect, border_radius=5)

        pygame.draw.rect(surface, (70, 130, 180), self.handle_rect, border_radius=3)
        pygame.draw.rect(surface, (0, 0, 0), self.handle_rect, 1, border_radius=3)

        text = font.render(f"{int(self.val)}", True, (0, 0, 0))
        surface.blit(text, (self.rect.right + 10, self.rect.centery - 10))