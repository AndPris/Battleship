import pygame

# buttons = []


class Button:
    def __init__(self, screen, x, y, width, height, font_size, text='Button', onclick_function=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.text = text
        self.onclick_function = onclick_function
        self.already_pressed = False

        self.font = pygame.font.SysFont('Arial', self.font_size)

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.button_label = self.font.render(self.text, True, (20, 20, 20))

        # buttons.append(self)

    def process(self):
        mouse_position = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])

        if self.button_rect.collidepoint(mouse_position):
            self.button_surface.fill(self.fill_colors['hover'])

            if pygame.mouse.get_pressed(3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])

                if not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_label, [
            self.button_rect.width / 2 - self.button_label.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_label.get_rect().height / 2
        ])
        self.screen.blit(self.button_surface, self.button_rect)
