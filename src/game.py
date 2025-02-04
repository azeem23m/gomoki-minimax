import pygame
import sys
from referee import game_referee
from ai import AI

class Game:
    """
        Game class

        Include GUI Implementation and main game loop
    
    """

    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 200
    BG_COLOR = (210, 180, 140)
    TEXT_COLOR = (0, 0, 0)
    BOARD_BG_COLOR = (210, 180, 140)
    LINE_COLOR = (0, 0, 0)
    cell_size = 40
    button_width = 120
    button_height = 40


    your_turn = True
    game_over = False
    winner = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.FONT = pygame.font.Font(None, 33)
    
    def start(self):
        self.grid_size = self.set_size()
        self.difficulty = self.set_game_difficulty()
        self.depth = game_referee.diffMap[self.difficulty] 
        self.board_size = self.grid_size * Game.cell_size
        self.replay_button_x = self.board_size // 4 - Game.button_width // 2
        self.quit_button_x = self.board_size * 3 // 4 - Game.button_width // 2
        self.button_y = self.board_size + 20
        self.screen = pygame.display.set_mode((self.board_size, self.board_size))
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        pygame.display.set_caption("Enjoy!")
        while True:
            self.screen.fill(Game.BOARD_BG_COLOR)
            self.draw_board(self.screen, self.grid_size, Game.cell_size)
            self.draw_stones(self.screen, self.grid, Game.cell_size)
            pygame.display.flip()

            winner = game_referee.check_game_over(self.grid, self.grid_size)
            if winner:
                self.display_game_over(winner)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.get_cell(event.pos, Game.cell_size)
                    if self.your_turn and game_referee.isValidMove(self.grid, self.grid_size, row, col):
                        self.grid[row][col] = 1
                        self.your_turn = False
                        continue
                    
                if not self.your_turn:
                    ai_move = AI.make_move(self.grid, self.grid_size, self.depth)
                    if ai_move is None:
                        continue
                    self.grid[ai_move[0]][ai_move[1]] = 2
                    self.your_turn = True


    def draw_text(self, screen, text, font, color, center):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, text_rect)

    def draw_board(self, screen, grid_size, cell_size):
        for i in range(grid_size + 1):
            pygame.draw.line(screen, Game.LINE_COLOR, (0, i * Game.cell_size), (grid_size * Game.cell_size, i * Game.cell_size))
            pygame.draw.line(screen, Game.LINE_COLOR, (i * Game.cell_size, 0), (i * Game.cell_size, grid_size * Game.cell_size))

    def draw_stones(self, screen, grid, cell_size):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1:
                    pygame.draw.circle(
                        screen, (0, 0, 0),
                        (col * Game.cell_size + Game.cell_size // 2, row * Game.cell_size + Game.cell_size // 2),
                        Game.cell_size // 3
                    )
                elif self.grid[row][col] == 2:
                    pygame.draw.circle(
                        screen, (255, 255, 255),
                        (col * Game.cell_size + Game.cell_size // 2, row * Game.cell_size + Game.cell_size // 2),
                        Game.cell_size // 3
                    )

    def draw_button(self, screen, text, x, y, width, height, color, text_color):
        pygame.draw.rect(screen, color, (x, y, width, height))  
        self.draw_text(screen, text, self.FONT, text_color, (x + width // 2, y + height // 2))

    def get_cell(self, pos, cell_size):
        x, y = pos
        return y // cell_size, x // cell_size

    def set_size(self):
        screen = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
        pygame.display.set_caption("Enter Game Size")
        input_box = pygame.Rect(100, 80, 200, 40)
        user_input = ""
        invalid_size = False

        while True:
            screen.fill(Game.BG_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if user_input.isdigit() and int(user_input) >= 5:
                            grid_size = int(user_input)
                            return grid_size
                        else:
                            print("invalid size")
                            invalid_size = True
                            user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

            if invalid_size:
                self.draw_text(screen, "Size can't be less than 5", self.FONT, Game.TEXT_COLOR, (Game.WINDOW_WIDTH // 2, 160))
            self.draw_text(screen, "Enter Grid Size:", self.FONT, Game.TEXT_COLOR, (Game.WINDOW_WIDTH // 2, 40))
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            self.draw_text(screen, user_input, self.FONT, Game.TEXT_COLOR, input_box.center)
            pygame.display.flip()

    def display_game_over(self, winner):
        winner_window = pygame.display.set_mode((self.board_size, self.board_size+100))
        pygame.display.set_caption("Game ended!")
        winner_bg_color = (210, 180, 140)
        winner_text_color = (0, 0, 0)
        winner_window.fill(winner_bg_color)
        Game.button_width = 80
        Game.button_height = 40
        replay_button_x = self.board_size // 4 - Game.button_width // 2
        quit_button_x = self.board_size * 3 // 4 - Game.button_width // 2
        button_y = self.board_size + 40

        winner_message = "You Win!" if winner==1 else ("AI Wins!" if winner==2 else "It's a Tie!") 

        self.draw_text(winner_window, winner_message, self.FONT, winner_text_color, (self.board_size // 2, self.board_size + 20))
        self.draw_button(winner_window, "Replay", replay_button_x, button_y, Game.button_width, Game.button_height, (242, 210, 189), winner_text_color)
        self.draw_button(winner_window, "Quit", quit_button_x, button_y, Game.button_width, Game.button_height, (242, 210, 189), winner_text_color)
        self.draw_board(self.screen, self.grid_size, Game.cell_size)
        self.draw_stones(self.screen, self.grid, Game.cell_size)


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.handle_button_click(event.pos, replay_button_x, button_y, Game.button_width, Game.button_height):
                        print("Replay the game")
                        return self.start()  
                    elif self.handle_button_click(event.pos, quit_button_x, button_y, Game.button_width, Game.button_height):
                        print("Quit the game")
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()

    def handle_button_click(self, pos, button_x, button_y, button_width, button_height):
        x, y = pos
        return button_x <= x <= button_x + Game.button_width and button_y <= y <= button_y + Game.button_height

    def set_game_difficulty(self):
        screen = pygame.display.set_mode((Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT))
        pygame.display.set_caption("Choose Difficulty")
        Game.button_width = 120
        Game.button_height = 40
        button_y = Game.WINDOW_HEIGHT // 2
        easy_button_x = Game.WINDOW_WIDTH // 4 - Game.button_width // 2
        medium_button_x = Game.WINDOW_WIDTH // 2 - Game.button_width // 2
        hard_button_x = Game.WINDOW_WIDTH * 3 // 4 - Game.button_width // 2

        while True:
            screen.fill(Game.BG_COLOR)
            self.draw_text(screen, "Choose Difficulty:", self.FONT, Game.TEXT_COLOR, (Game.WINDOW_WIDTH // 2, 40))
            self.draw_button(screen, "Easy", easy_button_x, button_y, Game.button_width, Game.button_height, (242, 210, 189), Game.TEXT_COLOR)
            self.draw_button(screen, "Medium", medium_button_x, button_y, Game.button_width, Game.button_height, (242, 210, 189), Game.TEXT_COLOR)
            self.draw_button(screen, "Hard", hard_button_x, button_y, Game.button_width, Game.button_height, (242, 210, 189), Game.TEXT_COLOR)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.handle_button_click(event.pos, easy_button_x, button_y, Game.button_width, Game.button_height):
                        return "easy"
                    elif self.handle_button_click(event.pos, medium_button_x, button_y, Game.button_width, Game.button_height):
                        return "medium"
                    elif self.handle_button_click(event.pos, hard_button_x, button_y, Game.button_width, Game.button_height):
                        return "hard"
                    