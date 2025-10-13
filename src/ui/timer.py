# ui/timer.py
import time
import pygame

class Timer:
    def __init__(self, font, x, y):
        self.font = font
        self.x = x
        self.y = y
        self.icon_size = 20
        
        #Timer State
        self.start_time = None
        self.paused = False
        self.pause_start = None
        self.total_paused = 0

        # Pause icon area
        self.pause_rect = pygame.Rect(self.x + 80, self.y + 5, self.icon_size, self.icon_size)
        self.resume_rect = None # Overlay button

    def start(self):
        #Start or restart the timer
        self.start_time = time.time()
        self.paused = False
        self.total_paused = 0

    def pause(self):
        #Pause the timer
        if not self.paused:
            self.paused = True
            self.pause_start = time.time()

    def resume(self):
        #Resume the timer after pausing
        if self.paused:
            self.total_paused += time.time() - self.pause_start
            self.paused = False

    def toggle(self):
        #Toggle pause/resume
        if self.paused:
            self.resume()
        else:
            self.pause()

    def get_elapsed(self):
        #Get elapsed time in seconds
        if not self.start_time:
            return 0
        if self.paused:
            elapsed = self.pause_start - self.start_time - self.total_paused
        else:
            elapsed = time.time() - self.start_time - self.total_paused
        return elapsed

    def draw(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT, FONT):
        # Draw timer
        elapsed = int(self.get_elapsed())
        minutes, seconds = divmod(elapsed, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        label = self.font.render(time_str, True, (0, 0, 0))
        screen.blit(label, (self.x, self.y))

        # Draw Overlay
        icon_color = (50, 50, 50)
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(255)  # not-transparent
            overlay.fill((50, 50, 50))  # dark grey overlay
            screen.blit(overlay, (0,0))

            paused_text = FONT.render("PAUSED", True, (255, 255, 255))
            screen.blit(paused_text, (SCREEN_WIDTH//2 - paused_text.get_width()//2,
                                    SCREEN_HEIGHT//2 - paused_text.get_height()//2))

            # Resume button
            resume_text = FONT.render("Resume", True, (0, 0, 0))
            self.resume_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50)
            pygame.draw.rect(screen, (255, 255, 255), self.resume_rect)  # button background
            screen.blit(resume_text, (SCREEN_WIDTH//2 - resume_text.get_width()//2,
                                    SCREEN_HEIGHT//2 + 60))

        else:
            # Draw pause bars
            bar_width = self.icon_size // 4
            gap = bar_width
            pygame.draw.rect(
                screen, icon_color,
                (self.pause_rect.left, self.pause_rect.top, bar_width, self.icon_size)
            )
            pygame.draw.rect(
                screen, icon_color,
                (self.pause_rect.left + bar_width + gap, self.pause_rect.top, bar_width, self.icon_size)
            )


    def handle_event(self, event):
        #Handle mouse clicks for pause icon
        if event.type == pygame.MOUSEBUTTONUP:
            # STATE 1) If overlay is showing (paused), check overlay resume button
            if self.paused and self.resume_rect and self.resume_rect.collidepoint(event.pos):
                self.toggle()
                return True  # handled event

            # STATE 2) If game is not paused, check play button in the main timer menu
            elif not self.paused and self.pause_rect and self.pause_rect.collidepoint(event.pos):
                self.toggle()
                return True  # handled event

        return False  # event not handled