import random
import pygame
import sys
import math
import time


class Constants:
    SIZE = 600
    BOARD = (230, 184, 135)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255) 


def switch_player(jogador):
    if jogador == 1:
        return 2
    else:
        return 1


class PahTum:
    def __init__(self):
        self.board_width = 7 
        self.board_height = 7
        self.board = [[' ' for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.black_holes = [] 
        self.current_player = 1
        self.pieces = ['X', 'O']
        self.place_black_holes()
        self.x_seen=[]
        self.y_seen=[]


    #buracos negros
    def place_black_holes(self):
        self.black_holes = []
        while len(self.black_holes) < 5:
            row = random.randint(0, self.board_height - 1)
            col = random.randint(0, self.board_width - 1)
            if (row, col) not in self.black_holes:
                self.black_holes.append((row, col))
                self.board[row][col] = 'B'



    def empty_space(self, row, col):
        for hole_row, hole_col in self.black_holes:
            if row == hole_row and col == hole_col:
                return False
        return self.board[row][col] == " "


    def switch_turns(self):
        self.current_player = switch_player(self.current_player)


    def piece_place(self, row, col, piece, change_player=True):
        if self.empty_space(row, col):
            self.board[row][col] = piece
            if change_player:
                self.current_player = switch_player(self.current_player)



    def game_is_over(self):

        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.empty_space(row, col):
                    return False
        return True
    


#X conta quantas peças estão conectadas horizontalmente a partir de uma determinada posição (x,y) do tabuleiro
#Y conta as peças que estão conectadas verticalmente 

    def count_pieces_X_black(self,x,y):
        if x<0 or x>=7 or y<0 or y>=7 or self.board[y][x]=='B' or self.board[y][x]=='O' or (x,y) in self.x_seen:
            return 0
        self.x_seen.append((x,y)) #evita repetições
        return 1+self.count_pieces_X_black(x+1, y) #conta com a peça da posição atual

    def count_pieces_Y_black(self,x,y):
        if x < 0 or x >= 7 or y < 0 or y >= 7 or self.board[y][x] == 'B' or self.board[y][x] == 'O' or (x, y) in self.y_seen:
            return 0
        self.y_seen.append((x, y))
        return 1 + self.count_pieces_Y_black(x, y+1)
    
    def count_pieces_X_white(self, x, y):
        if x < 0 or x >= 7 or y < 0 or y >= 7 or self.board[y][x] == 'B' or self.board[y][x] == 'X' or (x, y) in self.x_seen:
            return 0
        self.x_seen.append((x, y))
        return 1 + self.count_pieces_X_white(x+1, y)

    def count_pieces_Y_white(self, x, y):
        if x < 0 or x >= 7 or y < 0 or y >= 7 or self.board[y][x] == 'B' or self.board[y][x] == 'X' or (x, y) in self.y_seen:
            return 0
        self.y_seen.append((x, y))
        return 1 + self.count_pieces_Y_white(x, y+1)
    
    
    
    def calculate_points(self,player):
        total_points=0
        self.x_seen=[]
        self.y_seen=[]
        for i in range(7):
            for j in range(7):
                if self.board[i][j]==player:
                    total_points += self.converter(self.count_pieces_X_black(j,i)) if player== 'X' else self.converter(self.count_pieces_X_white(j,i))
                    total_points += self.converter(self.count_pieces_Y_black(j,i)) if player== 'X' else self.converter(self.count_pieces_Y_white(j,i))

        return total_points
            


    def converter(self,pont):
        match pont:
            case 0:
                return 0
            case 1:
                return 0
            case 2:
                return 0
            case 3:
                return 3
            case 4:
                return 10
            case 5:
                return 25
            case 6:
                return 56
            case 7: 
                return 119


    def evaluate_board(self, player):
        opponent = 'O' if player == 'X' else 'X'
        player_score = self.calculate_points(player)
        opponent_score = self.calculate_points(opponent)
        return player_score - opponent_score



    def minimax(self, depth, alpha, beta, maximizing_player):

        current_piece = self.pieces[0] if maximizing_player else self.pieces[1]

        if depth == 0 or self.game_is_over():
            return self.evaluate_board(current_piece)

        if maximizing_player:
            max_eval = -math.inf
            for i in range(self.board_height):
                for j in range(self.board_width):
                    if self.empty_space(i, j):
                        self.piece_place(i, j, self.pieces[0], change_player=False)
                        eval = self.minimax(depth - 1, alpha, beta, False)
                        self.board[i][j] = ' '
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = math.inf
            for i in range(self.board_height):
                for j in range(self.board_width):
                    if self.empty_space(i, j):
                        self.piece_place(i, j, self.pieces[1], change_player=False)
                        eval = self.minimax(depth - 1, alpha, beta, True)
                        self.board[i][j] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return min_eval


    def computer_move(self):
        best_score = -math.inf
        best_move = (-1, -1)
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.empty_space(i, j):
                    self.piece_place(i, j, self.pieces[0])
                    score = self.minimax(3, -math.inf, math.inf, False)
                    self.piece_place(i, j, ' ')
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        self.piece_place(*best_move, self.pieces[0])






class MainMenu:
    def __init__(self):
        self.window_width = 600
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('PahTum - Menu')
        self.start_button_rect = pygame.Rect(190, 150, 200, 100)
        self.rules_button_rect = pygame.Rect(210,330,150,75)
        self.quit_button_rect = pygame.Rect(210,450,150,75)
        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load("wallpaper.png").convert()

    def run_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button_rect.collidepoint(event.pos):
                        second_menu= SecondMenu()
                        mode = second_menu.run_menu()
                        return mode
                    elif self.rules_button_rect.collidepoint(event.pos):
                        rules_menu= RulesMenu()
                        rules_menu.run_menu()
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.draw_menu()
            pygame.display.flip()

    def draw_menu(self):

        self.window.fill(Constants.WHITE)
        self.window.blit(self.background_image, (0, 40))

        pygame.draw.rect(self.window, Constants.WHITE, self.start_button_rect)
        pygame.draw.rect(self.window, Constants.WHITE, self.rules_button_rect)
        pygame.draw.rect(self.window, Constants.WHITE, self.quit_button_rect)


        pygame.draw.rect(self.window, Constants.BLACK, self.start_button_rect, 2)
        pygame.draw.rect(self.window, Constants.BLACK, self.rules_button_rect, 2)
        pygame.draw.rect(self.window, Constants.BLACK, self.quit_button_rect, 2)


        start_text = self.font.render('Start', True, Constants.BLACK)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.window.blit(start_text, start_text_rect)

        rules_text = self.font.render('Rules', True, Constants.BLACK)
        rules_text_rect = rules_text.get_rect(center=self.rules_button_rect.center)
        self.window.blit(rules_text, rules_text_rect)

        quit_text = self.font.render('Quit', True, Constants.BLACK)
        quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
        self.window.blit(quit_text, quit_text_rect)


class RulesMenu:
    
    def __init__(self):
        self.window_width=600
        self.window_height=600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("PahTum - Rules")
        self.back_button_rect= pygame.Rect(250,480,100,50)
        self.font= pygame.font.Font(None,36)
        self.background_image = pygame.image.load("wallpaper.png").convert()
        self.background_image.set_alpha(140)

    def run_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button_rect.collidepoint(event.pos):
                        main_menu = MainMenu()
                        main_menu.run_menu()
                        return
                    
            self.draw_menu()
            pygame.display.flip()

    def draw_menu(self):
        self.window.fill(Constants.WHITE)
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render('PAHTUM RULES', True, Constants.BLACK)
        title_text_rect = title_text.get_rect(center=(self.window_width / 2, 50))
        self.window.blit(title_text, title_text_rect)
        self.window.blit(self.background_image, (0, 50))

        rules_font = pygame.font.Font(None, 20)
        rules_text_lines = [
    '-> 7x7 board with 5 black holes positioned randomly at the beginning of each game.',
    '',
    '-> The black holes are locations on the board where pieces cannot be placed.',
    '',
    '-> Each player alternately places a piece in an empty space on the board',
    '   with the aim of getting the maximum number of pieces in a line (vertical or horizontal).',
    '',
    '-> Pieces that have already been played on the board cannot be moved.',
    '',
    '-> The game ends when all spaces are occupied.',
    '',
    '-> Scoring works as follows:',
    '   3 in a row: 3 points',
    '   4 in a row: 10 points',
    '   5 in a row: 25 points',
    '   6 in a row: 56 points',
    '   7 in a row: 119 points',
    '',
    'The player with the most points wins the game.'
]

        y_offset = 100 
        for line in rules_text_lines:
            text_surface = rules_font.render(line, True, Constants.BLACK)
            text_rect = text_surface.get_rect(center=(self.window_width / 2, y_offset))
            self.window.blit(text_surface, text_rect)
            y_offset += text_rect.height + 5 

        pygame.draw.rect(self.window, Constants.BLACK, self.back_button_rect, 2)
        text = self.font.render('Back', True, Constants.BLACK)
        text_rect = text.get_rect(center=self.back_button_rect.center)
        self.window.blit(text, text_rect)
    

class SecondMenu:
    def __init__(self):
        self.window_width = 600
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('PahTum - Second Menu')
        self.player_vs_player_button_rect = pygame.Rect(200, 60, 200, 100)
        self.computer_vs_computer_button_rect = pygame.Rect(200, 200, 200, 100)
        self.computer_vs_player_button_rect = pygame.Rect(200, 350, 200, 100)
        self.back_button_rect = pygame.Rect(250,480,100,50)
        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load("wallpaper.png").convert()

    def run_menu(self):
        running = True
        difficulty_selection=None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.player_vs_player_button_rect.collidepoint(event.pos):
                        game_gui = PahTumGUI()
                        game_gui.run_game()
                        return 
                    elif self.computer_vs_computer_button_rect.collidepoint(event.pos):
                        difficulty_menu=DifficultyMenu()
                        difficulty_selection=difficulty_menu.run_difficulty_menu()
                        if difficulty_selection:
                            self.start_computer_vs_computer_game(difficulty_selection)
                        return
                    elif self.computer_vs_player_button_rect.collidepoint(event.pos):
                        difficulty_menu=DifficultyMenu()
                        difficulty_selection=difficulty_menu.run_difficulty_menu()
                        if difficulty_selection:
                            self.start_computer_vs_player_game(difficulty_selection)
                        return 
                        

                    elif self.back_button_rect.collidepoint(event.pos):
                        main_menu = MainMenu()
                        main_menu.run_menu()
                        return

            self.draw_menu()
            pygame.display.flip()

    def start_computer_vs_computer_game(self, difficulty_selection):
        pygame.init()
        game_gui = PahTumGUI()
        game_gui.run_computer_vs_computer_game(difficulty_selection)
        pygame.quit()

    def start_computer_vs_player_game(self, difficulty_selection):
        pygame.init()
        game_gui = PahTumGUI() 
        game_gui.run_computer_vs_player_game(difficulty_selection)
        pygame.quit()

    def draw_menu(self):
        self.window.fill(Constants.WHITE)
        self.window.blit(self.background_image, (0, 40))
        
        
        pygame.draw.rect(self.window, Constants.WHITE, self.player_vs_player_button_rect)  
        pygame.draw.rect(self.window, Constants.WHITE, self.computer_vs_computer_button_rect) 
        pygame.draw.rect(self.window, Constants.WHITE, self.computer_vs_player_button_rect)  

        # Desenhar as bordas pretas dos botões
        pygame.draw.rect(self.window, Constants.BLACK, self.player_vs_player_button_rect, 2)
        pygame.draw.rect(self.window, Constants.BLACK, self.computer_vs_computer_button_rect, 2)
        pygame.draw.rect(self.window, Constants.BLACK, self.computer_vs_player_button_rect, 2)

        # Renderizar e centralizar o texto nos botões
        pygame.draw.rect(self.window, Constants.WHITE, self.player_vs_player_button_rect)  
        pygame.draw.rect(self.window, Constants.BLACK, self.player_vs_player_button_rect, 2) 
        text1_line1 = self.font.render('Player', True, Constants.BLACK)
        text1_line2 = self.font.render('vs', True, Constants.BLACK)
        text1_line3 = self.font.render('Player', True, Constants.BLACK)
        line_spacing = 10
        text1_rect1 = text1_line1.get_rect(midtop=(self.player_vs_player_button_rect.centerx, self.player_vs_player_button_rect.centery - 30 - line_spacing))
        text1_rect2 = text1_line2.get_rect(midtop=(self.player_vs_player_button_rect.centerx, self.player_vs_player_button_rect.centery - 10))
        text1_rect3 = text1_line3.get_rect(midtop=(self.player_vs_player_button_rect.centerx, self.player_vs_player_button_rect.centery + 10 + line_spacing))
        self.window.blit(text1_line1, text1_rect1)
        self.window.blit(text1_line2, text1_rect2)
        self.window.blit(text1_line3, text1_rect3)

        # Botão "Computer vs Computer"
        pygame.draw.rect(self.window, Constants.WHITE, self.computer_vs_computer_button_rect)  # Preencher com branco
        pygame.draw.rect(self.window, Constants.BLACK, self.computer_vs_computer_button_rect, 2)  # Desenhar a borda preta
        text2_line1 = self.font.render('Computer', True, Constants.BLACK)
        text2_line2 = self.font.render('vs', True, Constants.BLACK)
        text2_line3 = self.font.render('Computer', True, Constants.BLACK)
        line_spacing = 10  # Espaço entre as linhas
        text2_rect1 = text2_line1.get_rect(midtop=(self.computer_vs_computer_button_rect.centerx, self.computer_vs_computer_button_rect.centery - 30 - line_spacing))
        text2_rect2 = text2_line2.get_rect(midtop=(self.computer_vs_computer_button_rect.centerx, self.computer_vs_computer_button_rect.centery - 10))
        text2_rect3 = text2_line3.get_rect(midtop=(self.computer_vs_computer_button_rect.centerx, self.computer_vs_computer_button_rect.centery + 10 + line_spacing))
        self.window.blit(text2_line1, text2_rect1)
        self.window.blit(text2_line2, text2_rect2)
        self.window.blit(text2_line3, text2_rect3)

        # Botão "Computer vs Player"
        pygame.draw.rect(self.window, Constants.WHITE, self.computer_vs_player_button_rect)
        pygame.draw.rect(self.window, Constants.BLACK, self.computer_vs_player_button_rect, 2)
        text3_line1 = self.font.render('Computer', True, Constants.BLACK)
        text3_line2 = self.font.render('vs', True, Constants.BLACK)
        text3_line3 = self.font.render('Player', True, Constants.BLACK)
        line_spacing = 10
        text3_rect1 = text3_line1.get_rect(midtop=(self.computer_vs_player_button_rect.centerx, self.computer_vs_player_button_rect.centery - 30 - line_spacing))
        text3_rect2 = text3_line2.get_rect(midtop=(self.computer_vs_player_button_rect.centerx, self.computer_vs_player_button_rect.centery - 10))
        text3_rect3 = text3_line3.get_rect(midtop=(self.computer_vs_player_button_rect.centerx, self.computer_vs_player_button_rect.centery + 10 + line_spacing))
        self.window.blit(text3_line1, text3_rect1)
        self.window.blit(text3_line2, text3_rect2)
        self.window.blit(text3_line3, text3_rect3)

        pygame.draw.rect(self.window, Constants.BLACK, self.back_button_rect, 2) # Draw back button border
        text4 = self.font.render('Back', True, Constants.BLACK)
        text_rect4 = text4.get_rect(center=self.back_button_rect.center)
        self.window.blit(text4, text_rect4)
        

class DifficultyMenu:
    def __init__(self):
        self.window_width = 600
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('PahTum - Difficulty Menu')
        self.easy_button_rect = pygame.Rect(200, 70, 200, 100)
        self.medium_button_rect = pygame.Rect(200, 195, 200, 100)
        self.hard_button_rect = pygame.Rect(200, 320, 200, 100)
        self.back_button_rect = pygame.Rect(250,480,100,50)
        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load("wallpaper.png").convert()


    def run_difficulty_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.easy_button_rect.collidepoint(event.pos):
                        difficulty = "EASY"
                        return {"player1": difficulty, "player2": difficulty}
                    elif self.medium_button_rect.collidepoint(event.pos):
                        difficulty = "MEDIUM"
                        return {"player1": difficulty, "player2": difficulty}
                    elif self.hard_button_rect.collidepoint(event.pos):
                        difficulty = "HARD"
                        return {"player1": difficulty, "player2": difficulty}
                    elif self.back_button_rect.collidepoint(event.pos):
                        second_menu = SecondMenu()  
                        return second_menu.run_difficulty_menu() 

    

            self.draw_menu()
            pygame.display.flip()
        

    
    def draw_menu(self):
        self.window.fill(Constants.WHITE)
        self.window.blit(self.background_image, (0, 40))

        pygame.draw.rect(self.window, Constants.WHITE, self.easy_button_rect)
        pygame.draw.rect(self.window, Constants.WHITE, self.medium_button_rect)
        pygame.draw.rect(self.window, Constants.WHITE, self.hard_button_rect)


        pygame.draw.rect(self.window, Constants.BLACK, self.easy_button_rect, 2)
        pygame.draw.rect(self.window, Constants.BLACK, self.medium_button_rect, 2)
        pygame.draw.rect(self.window, Constants.BLACK, self.hard_button_rect, 2)


        text1 = self.font.render('EASY', True, Constants.BLACK)
        text_rect1 = text1.get_rect(center=self.easy_button_rect.center)
        self.window.blit(text1, text_rect1)

        text2 = self.font.render('MEDIUM', True, Constants.BLACK)
        text_rect2 = text2.get_rect(center=self.medium_button_rect.center)
        self.window.blit(text2, text_rect2)

        text3 = self.font.render('HARD', True, Constants.BLACK)
        text_rect3 = text3.get_rect(center=self.hard_button_rect.center)
        self.window.blit(text3, text_rect3)

        pygame.draw.rect(self.window, Constants.BLACK, self.back_button_rect, 2)
        text4 = self.font.render('Back', True, Constants.BLACK)
        text_rect4 = text4.get_rect(center=self.back_button_rect.center)
        self.window.blit(text4, text_rect4)
        



class Player:
    def __init__(self, piece, skill_level):
        self.piece = piece
        self.skill_level= skill_level

    def make_move(self, game):
        if self.skill_level == "EASY":
            self.make_easy_move(game)
        elif self.skill_level == "MEDIUM":
            self.make_medium_move(game)
        elif self.skill_level == "HARD":
            self.make_hard_move(game)

    def make_easy_move(self, game):
        best_move = self.alpha_beta_search(game, 2)
        if best_move:
            game.piece_place(best_move[0], best_move[1], self.piece)


    def make_medium_move(self, game):
        best_move = self.alpha_beta_search(game, 3)
        if best_move:
            game.piece_place(best_move[0], best_move[1], self.piece)


    def make_hard_move(self, game):
        best_move = self.alpha_beta_search(game, 4)
        if best_move:
            game.piece_place(best_move[0], best_move[1], self.piece)



    def alpha_beta_search(self, game, depth):
        alpha = float('-inf')
        beta = float('inf')
        best_move = None

        for row in range(game.board_height):
            for col in range(game.board_width):
                if game.empty_space(row, col):
                    game.piece_place(row, col, self.piece)
                    score = self.min_value(game, alpha, beta, depth - 1)
                    game.board[row][col] = ' '
                    if score > alpha:
                        alpha = score
                        best_move = (row, col)

        return best_move

    def max_value(self, game, alpha, beta, depth):
        if depth == 0 or game.game_is_over():
            return self.evaluate(game)

        value = float('-inf')
        for row in range(game.board_height):
            for col in range(game.board_width):
                if game.empty_space(row, col):
                    game.piece_place(row, col, self.piece)
                    value = max(value, self.min_value(game, alpha, beta, depth - 1))
                    game.board[row][col] = ' '  
                    if value >= beta:
                        return value
                    alpha = max(alpha, value)

        return value

    def min_value(self, game, alpha, beta, depth):
        if depth == 0 or game.game_is_over():
            return self.evaluate(game)

        value = float('inf')
        for row in range(game.board_height):
            for col in range(game.board_width):
                if game.empty_space(row, col):
                    game.piece_place(row, col, 'O' if self.piece == 'X' else 'X')
                    value = min(value, self.max_value(game, alpha, beta, depth - 1))
                    game.board[row][col] = ' '
                    if value <= alpha:
                        return value
                    beta = min(beta, value)

        return value

    def evaluate(self, game):
        player_piece = self.piece
        opponent_piece = 'O' if player_piece == 'X' else 'X'

        player_score = game.calculate_points(player_piece)
        opponent_score = game.calculate_points(opponent_piece)

        return player_score - opponent_score

    def minimax(self, game, depth, maximizing_player):
        if depth == 0 or game.game_is_over():
            return game.calculate_points(self.piece), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for row in range(game.board_height):
                for col in range(game.board_width):
                    if game.empty_space(row, col):
                        game.piece_place(row, col, self.piece)
                        eval, _ = self.minimax(game, depth - 1, False)
                        game.board[row][col] = ' '  
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (row, col)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for row in range(game.board_height):
                for col in range(game.board_width):
                    if game.empty_space(row, col):
                        game.piece_place(row, col, 'O' if self.piece == 'X' else 'X')
                        eval, _ = self.minimax(game, depth - 1, True)
                        game.board[row][col] = ' '  
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (row, col)
            return min_eval, best_move

    def evaluate_move(self, game):
        player_piece = self.piece
        opponent_piece = 'O' if player_piece == 'X' else 'X'
    
        player_score = game.calculate_points(player_piece)
        opponent_score = game.calculate_points(opponent_piece)
    
        return player_score - opponent_score 


        
class PahTumGUI: 


    def __init__(self):
        self.game = PahTum()
        self.square_size = 85
        #definir comprimentos da GUI
        self.window_width = self.game.board_width * self.square_size
        self.window_height = self.game.board_height * self.square_size
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('PahTum')
        self.player1_turn = True
        
    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                

            self.draw_board()

            if not self.game.game_is_over():

                if pygame.mouse.get_pressed()[0]:
                    self.mouse_click()

            else:
                self.handle_game_end()

           
            pygame.display.flip()

        pygame.quit()

    def start_computer_vs_computer_game(self, difficulty_selection):
        pygame.init()
        game_gui = PahTumGUI()
        game_gui.run_computer_vs_computer_game(difficulty_selection)
        game_gui.handle_game_end()
        pygame.quit()

    def start_computer_vs_player_game(self, difficulty_selection):
        pygame.init()
        game_gui = PahTumGUI()
        game_gui.run_computer_vs_player_game(difficulty_selection)
        game_gui.handle_game_end()
        pygame.quit()

    def run_computer_vs_computer_game(self, difficulty_selection):
        running = True
        player1_difficulty=difficulty_selection["player1"]
        player2_difficulty=difficulty_selection["player2"]
        player1=Player('X' if self.game.current_player==1 else 'O', player1_difficulty)
        player2=Player('O' if self.game.current_player==1 else 'X', player2_difficulty)
            
        while running:
            print("starting new round")
            if not self.game.game_is_over():
                print("player 1 turn")
                player1.make_move(self.game)
                self.draw_board()
                pygame.display.flip()
                time.sleep(0.5)

                if self.game.game_is_over():
                    print("game is over")
                    self.handle_game_end()
                    break
                
                print("player 2 turn")
                player2.make_move(self.game)
                self.draw_board()
                pygame.display.flip()
                time.sleep(0.5)

                if self.game.game_is_over():
                    print("game over")
                    self.handle_game_end()
                    break

            else:
                print("game over")
                self.handle_game_end()
                time.sleep(0.5)
                break
        pygame.display.flip()
        time.sleep(2)

    def run_computer_vs_player_game(self, difficulty_selection):
        running = True 
        player1_difficulty = difficulty_selection["player1"]
        player2_difficulty = difficulty_selection["player2"]
        player1=Player('X', None)
        player2=Player('O', player2_difficulty)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
            

            self.draw_board()

            if not self.game.game_is_over():
                if self.player1_turn:
                    if pygame.mouse.get_pressed()[0]:
                        self.mouse_click()
                else:
                    player2.make_move(self.game)
                    self.player1_turn = True

            else:
                self.handle_game_end()

           
            pygame.display.flip()

        pygame.quit()

    

    def draw_message_winner(self, winner, black_points, white_points):
        font = pygame.font.Font(None, 45)
        if winner == "Tie":
            message = "IT'S A TIE"
        else:
            message = f"PLAYER {winner} WINS"
        text = font.render(message, True, Constants.RED)
        text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))


        pygame.draw.rect(self.window, Constants.WHITE, (text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, text_rect.height + 10))
        pygame.draw.rect(self.window, Constants.BLACK, (text_rect.left - 10, text_rect.top - 5, text_rect.width + 20, text_rect.height + 10), 2)


        self.window.blit(text, text_rect)


        font = pygame.font.Font(None, 32)
        

        text1 = font.render(f"Black Player (X): {black_points}", True, Constants.GREEN)
        text_rect1 = text1.get_rect(center=(self.window_width // 2, self.window_height // 2 + 50))
        pygame.draw.rect(self.window, Constants.WHITE, (text_rect1.left - 10, text_rect1.top - 5, text_rect1.width + 20, text_rect1.height + 10))
        pygame.draw.rect(self.window, Constants.BLACK, (text_rect1.left - 10, text_rect1.top - 5, text_rect1.width + 20, text_rect1.height + 10), 2)
        self.window.blit(text1, text_rect1)


        text2 = font.render(f"White Player (O): {white_points}", True, Constants.GREEN)
        text_rect2 = text2.get_rect(center=(self.window_width // 2, self.window_height // 2 + 80))
        pygame.draw.rect(self.window, Constants.WHITE, (text_rect2.left - 10, text_rect2.top - 5, text_rect2.width + 20, text_rect2.height + 10))
        pygame.draw.rect(self.window, Constants.BLACK, (text_rect2.left - 10, text_rect2.top - 5, text_rect2.width + 20, text_rect2.height + 10), 2)
        self.window.blit(text2, text_rect2)




    def draw_board(self):
        self.window.fill(Constants.WHITE)  #Fundo branco
        for row in range(self.game.board_height):
            for col in range(self.game.board_width):
                x= col * self.square_size
                y= row * self.square_size

                if self.game.board[row][col] == 'B':
                    color = Constants.BLACK
                else:
                    color= Constants.BOARD
                pygame.draw.rect(self.window, color, (x,y,self.square_size, self.square_size))

                if self.game.board[row][col]== 'X':
                    pygame.draw.circle(self.window, Constants.BLACK, (x+self.square_size//2, y+self.square_size//2), self.square_size//2)
                elif self.game.board[row][col] == 'O':
                    pygame.draw.circle(self.window, Constants.WHITE, (x+self.square_size//2, y+self.square_size//2), self.square_size//2)
                
                pygame.draw.rect(self.window, (Constants.BLACK), (x,y, self.square_size, self.square_size), 1)

    

   

     

    def mouse_click(self):
        if not self.game.game_is_over():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // self.square_size
            row = mouse_y // self.square_size
            if 0 <= row < self.game.board_height and 0 <= col < self.game.board_width:

                if self.game.empty_space(row,col):
                    self.game.piece_place(row, col, 'X' if self.player1_turn else 'O')
                    self.player1_turn = not self.player1_turn
        
                
    def handle_game_end(self):
        black_points = self.game.calculate_points('X')
        white_points = self.game.calculate_points('O')
        if black_points > white_points:
            winner = 'Black (X)'
        elif white_points > black_points:
            winner = 'White (O)'
        else:
            winner = 'Tie'
        self.draw_message_winner(winner, black_points, white_points)

            

if __name__ == '__main__':
    pygame.init()
    main_menu=MainMenu()
    main_menu.run_menu()
    pygame.quit()

    
    