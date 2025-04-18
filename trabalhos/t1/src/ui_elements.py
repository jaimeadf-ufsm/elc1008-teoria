import pygame

class Button:
    def __init__(self, rect, text, action, normal_color, hover_color, click_color):
        self.rect = rect
        self.text = text  
        self.action = action
        self.colors = {
            'normal': normal_color,
            'hover': hover_color,
            'click': click_color
        }
        self.current_color = normal_color
        self.click_effect = False

    def get_text(self):
        return self.text() if callable(self.text) else self.text

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.click_effect:
                self.current_color = self.colors['hover']
            return True
        self.current_color = self.colors['normal']
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.click_effect = True
            return True
        elif event.type == pygame.MOUSEBUTTONUP and self.click_effect:
            self.click_effect = False
            self.action()
            return True
        return False

    def draw(self, surface, font):
        current_color = self.colors['click'] if self.click_effect else self.current_color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.get_text(), True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

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