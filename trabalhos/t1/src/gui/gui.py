import sys
import copy
import pygame

from gui.button import Button
from gui.slider import Slider
from gui.tape_view import TapeView 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 60

class GUI:
    def __init__(self, simulator, all_transitions):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("T1 - Guilherme, Jaime e Luís")
        self.font = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        self.original_simulator = simulator
        self.simulator = copy.deepcopy(self.original_simulator)
        self.all_transitions = all_transitions
        self.simulation_steps = []
        self.current_step = 0
        self.running = False
        self.animation_frame = 0
        self.clock = pygame.time.Clock()
        
        self.precompute_simulation_steps()
        
        self.buttons = self.create_buttons()
        self.slider = Slider(900, WINDOW_HEIGHT - 130, 200, 30, 600, 60)
        self.hovered_button = None

        self.tape_guis = [
            TapeView(self.simulation_steps[0]["tapes"][0], 170, "Working Tape"),
            TapeView(self.simulation_steps[0]["tapes"][1], 310, "History Tape"),
            TapeView(self.simulation_steps[0]["tapes"][2], 450, "Output Tape")
        ]

    def create_buttons(self):
        button_width = 130
        button_y = WINDOW_HEIGHT - 70
        return [
            Button(pygame.Rect(50, button_y, button_width, 50),
                "First", self.go_to_first_step,
                BLUE, (100, 150, 200), (40, 110, 160)),
            Button(pygame.Rect(50 + button_width + 20, button_y, button_width, 50),
                "Previous", self.previous_step,
                BLUE, (100, 150, 200), (40, 110, 160)),
            Button(pygame.Rect(50 + (button_width + 20) * 2, button_y, button_width, 50),
            lambda: "Pause" if self.running else "Play",  
            self.toggle_play,
            DARK_BLUE if self.running else BLUE,
            (80, 225, 80) if self.running else (100, 150, 200),
            (40, 160, 40) if self.running else (40, 110, 160)),
            Button(pygame.Rect(50 + (button_width + 20) * 3, button_y, button_width, 50),
                "Next", self.next_step,
                BLUE, (100, 150, 200), (40, 110, 160)),
            Button(pygame.Rect(50 + (button_width + 20) * 4, button_y, button_width, 50),
                "Last", self.go_to_last_step,
                BLUE, (100, 150, 200), (40, 110, 160)),
            Button(pygame.Rect(50 + (button_width + 20) * 5, button_y, button_width, 50),
                "Reset", self.reset_simulation,
                BLUE, (100, 150, 200), (40, 110, 160))
        ]

    def update_slider_position(self):
        self.animation_speed = (60 * FPS) // self.slider.val
        
    def precompute_simulation_steps(self):
        simulator_copy = copy.deepcopy(self.original_simulator)
        self.simulation_steps = []
        
        self.simulation_steps.append({
            "tapes": copy.deepcopy(simulator_copy.tapes),
            "state": simulator_copy.current_state,
            "transition": None
        })
        
        step = 0
        while step < 1000:  
            transition = simulator_copy.step()

            if transition is None:
                break

            step += 1
            
            self.simulation_steps.append({
                "tapes": copy.deepcopy(simulator_copy.tapes),
                "state": simulator_copy.current_state,
                "transition": transition
            })
    
    def reset_simulation(self):
        self.current_step = 0
        self.animation_frame = 0
        self.running = False
        
    def go_to_first_step(self):
        self.current_step = 0
        self.animation_frame = 0
        self.running = False
        
    def go_to_last_step(self):
        self.current_step = len(self.simulation_steps) - 1
        self.animation_frame = 0
        self.running = False
        
    def next_step(self):
        if self.current_step < len(self.simulation_steps) - 1:
            self.current_step += 1
            self.animation_frame = self.animation_speed
            
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.animation_frame = self.animation_speed
            
    def toggle_play(self):
        self.running = not self.running
        
    def update_tapes(self):
        current_tapes = self.simulation_steps[self.current_step]["tapes"]
        for tape_gui, tape in zip(self.tape_guis, current_tapes):
            tape_gui.tape = tape

    def draw_tapes(self):
        for tape_gui in self.tape_guis:
            tape_gui.draw(
                screen=self.screen,
                title_font=self.title_font,
                regular_font=self.font,
                small_font=self.small_font
            )
            
    def draw_transition_info(self):
        if self.current_step == 0:
            transition_text = "Initial state"
        else:
            transition = self.simulation_steps[self.current_step]["transition"]
            transition_text = str(transition) if transition else "No transition"
        
        state_text = f"Current State: {self.simulation_steps[self.current_step]['state']}"
        step_text = f"Step {self.current_step}/{len(self.simulation_steps)-1}"
        
        info_rect = pygame.Rect(50, 30, WINDOW_WIDTH - 100, 80)
        pygame.draw.rect(self.screen, LIGHT_BLUE, info_rect)
        pygame.draw.rect(self.screen, BLACK, info_rect, 2)
        
        transition_surface = self.font.render(transition_text, True, BLACK)
        state_surface = self.font.render(state_text, True, BLACK)
        step_surface = self.title_font.render(step_text, True, BLACK)
        
        self.screen.blit(transition_surface, (60, 50))
        self.screen.blit(state_surface, (60, 80))
        self.screen.blit(step_surface, (WINDOW_WIDTH - 250, 60))
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for button in self.buttons:
                if button.handle_event(event):
                    break
    
            self.slider.handle_event(event)
        
        for button in self.buttons:
            if button.check_hover(mouse_pos):
                self.hovered_button = button
        self.update_slider_position()

    def animate_transition(self):
        if self.animation_frame > 0:
            self.animation_frame -= 1
            return
            
        if self.running and self.current_step < len(self.simulation_steps) - 1:
            self.next_step()

    def draw_buttons(self):
        for button in self.buttons:
            if button.get_text() in ["Play", "Pause"]: 
                button.colors['normal'] = DARK_BLUE if self.running else BLUE
                button.colors['hover'] = (0, 0, 130) if self.running else (100, 150, 200)
                button.colors['click'] = BLUE if self.running else (40, 110, 160)
                
                button.text = lambda: "Pause" if self.running else "Play"
                
            button.draw(self.screen, self.font)

    def draw_slider(self):
        self.slider.draw(self.screen, self.font)
        label = self.font.render("instructions/min:", True, BLACK)
        self.screen.blit(label, (self.slider.rect.left, self.slider.rect.top - 30))

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.animate_transition()
            self.update_tapes()
            
            self.screen.fill(WHITE)
            
            self.draw_tapes()
            
            self.draw_transition_info()
            
            self.draw_buttons()
            self.draw_slider()
            
            pygame.display.flip()


