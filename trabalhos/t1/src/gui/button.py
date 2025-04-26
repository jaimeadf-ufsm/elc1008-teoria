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