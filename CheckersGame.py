from copy import deepcopy
import pygame

#------------------------CONSTANSTS----------------------------------
ROWS, COLUMNS = 8,8
PIECE_SIZE = 100
RED = (255,0,0)
WHITE = (251,252,252)
BLACK = (27,27,26)
GRAY = (128,128,128)
BROWN = (230,126,34)
BLUE = (52,152,219)
CROWN_IMG = pygame.transform.scale(pygame.image.load("crown.png"),(44,25))
#---------------------------------------------------------------------
 




class Piece:
    def __init__(self,row,col,color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = col*PIECE_SIZE + 50
        self.y = row*PIECE_SIZE + 50
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),30)
        if self.king:
            screen.blit(CROWN_IMG, (self.x - CROWN_IMG.get_width()//2, self.y - CROWN_IMG.get_height()//2))
    def move(self,col,row):
        self.col = col
        self.row = row
        self.x = col*PIECE_SIZE + 50
        self.y = row*PIECE_SIZE + 50
    def get_x_y(self):
        return self.x, self.y
    def make_king(self):
        self.king = True
    def check_king(self):
        return self.king 

class BoardGame:
    def __init__(self,first_color_turn):
        self.board = [[0,Piece(0,1,RED),0,Piece(0,3,RED),0,Piece(0,5,RED),0,Piece(0,7,RED)],
                      [Piece(1,0,RED),0,Piece(1,2,RED),0,Piece(1,4,RED),0,Piece(1,6,RED),0],
                      [0,Piece(2,1,RED),0,Piece(2,3,RED),0,Piece(2,5,RED),0,Piece(2,7,RED)],
                      [0,0,0,0,0,0,0,0],                                                    
                      [0,0,0,0,0,0,0,0],
                      [Piece(5,0,BROWN),0,Piece(5,2,BROWN),0,Piece(5,4,BROWN),0,Piece(5,6,BROWN),0],
                      [0,Piece(6,1,BROWN),0,Piece(6,3,BROWN),0,Piece(6,5,BROWN),0,Piece(6,7,BROWN)],
                      [Piece(7,0,BROWN),0,Piece(7,2,BROWN),0,Piece(7,4,BROWN),0,Piece(7,6,BROWN),0]]
        self.red_piece = 12
        self.brown_piece = 12
        self.red_king =0
        self.brown_king = 0
        self.first_turn = first_color_turn
    def draw_board(self,screen,color):
        for i in range(0,ROWS,2):
            for j in range(1,COLUMNS,2):
                pygame.draw.rect(screen,color,(i*PIECE_SIZE,j*PIECE_SIZE,PIECE_SIZE,PIECE_SIZE))
        for i in range(1,ROWS,2):
            for j in range(0,COLUMNS,2):
                pygame.draw.rect(screen,color,(i*PIECE_SIZE,j*PIECE_SIZE,PIECE_SIZE,PIECE_SIZE))
        for i in range(ROWS):
            for j in range(COLUMNS):
                p = self.board[i][j]
                if p != 0:
                    p.draw(screen)
    
    def move_piece(self,p,col,row):
        self.board[row][col] = self.board[p.row][p.col]
        self.board[p.row][p.col] = 0
        if row == 0:
            if not p.check_king():
                self.brown_king +=1
            p.make_king()
        elif row == ROWS -1:
            if not p.check_king():
                self.red_king +=1
            p.make_king()
        p.move(col,row)
    def remove_piece(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    if piece.check_king():
                        self.red_king -=1
                    self.red_piece -= 1
                else:
                    if piece.check_king():
                        self.brown_king -=1
                    self.brown_piece -= 1
    def get_piece(self,col,row):
        return self.board[row][col]
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.king:
            moves.update(self.traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
            moves.update(self.traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self.traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
        if piece.color == BROWN:
            moves.update(self.traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == RED:
            moves.update(self.traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self.traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves
    def traverse_left(self,start,stop,step,color,left,skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.traverse_left(r+step, row, step, color, left-1,skipped=skipped +last))
                    moves.update(self.traverse_right(r+step, row, step, color, left+1,skipped=skipped +last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves
    def traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLUMNS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.traverse_left(r+step, row, step, color, right-1,skipped=skipped +last))
                    moves.update(self.traverse_right(r+step, row, step, color, right+1,skipped=skipped + last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    def no_valid_moves(self):
        #print("Checking")
        valid_moves1 = []
        valid_moves2 = []
        for piece in self.all_pieces(RED):
            valid_moves1 += self.get_valid_moves(piece)
        for piece in self.all_pieces(BROWN):
            valid_moves2 += self.get_valid_moves(piece)
        if valid_moves1 and valid_moves2:
            return None
        else:
            if valid_moves1:
                return RED
            else:
                return BROWN
    def winner(self):
        if self.red_piece ==0:
            return BROWN
        elif self.brown_piece == 0:
            return RED
        else:
            return self.no_valid_moves()
    def score(self):
        return self.brown_piece + 0.5*self.brown_king - self.red_piece - 0.5*self.red_king
    def all_pieces(self,color):
        all_pieces = []
        for r in self.board:
            for piece in r:
                if piece == 0:
                    continue
                if piece.color == color:
                    all_pieces += [piece]      
        return all_pieces
        
class Checkers:
    def __init__(self,screen,first_color_turn,level):
        self.board = BoardGame(first_color_turn)
        self.turn = first_color_turn
        self.screen = screen
        self.piece_selected = None
        self.valid_move = {}
        self.level = level
    def update(self):
        self.board.draw_board(self.screen,BLACK)
        if self.piece_selected:
            if self.board.get_piece(self.piece_selected.col,self.piece_selected.row) !=0:
                self.draw_piece_selected(self.piece_selected)
        self.draw_valid_moves(self.valid_move)
        #print("Red_king:",self.board.red_king)
        #print("Brown_king:",self.board.brown_king)
        #print("==========================")
        pygame.display.update()
    
    def select_square_or_piece(self,col,row):
        if self.piece_selected:
            res = self.move_piece(col,row)
            if not res:
                self.valid_move = {}
                self.piece_selected = None
                self.select_square_or_piece(col,row)
        else:
            piece = self.board.get_piece(col,row)
            if piece !=0 and piece.color == self.turn:
                self.piece_selected = piece
                self.valid_move = self.board.get_valid_moves(piece)
                return True
        return False    
    def move_piece(self,col,row):
        piece = self.board.get_piece(col,row)
        if self.piece_selected and piece == 0 and (row,col) in self.valid_move:
            self.board.move_piece(self.piece_selected,col,row)
            skipped = self.valid_move[(row,col)]
            if skipped:
                self.board.remove_piece(skipped)
            self.change_turn()
            self.valid_move= {}
        else:
            return False
        return True
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLUE, (col * PIECE_SIZE + 50, row *PIECE_SIZE + 50), 15)
    def draw_piece_selected(self,piece):
        x,y = piece.get_x_y()
        pygame.draw.circle(self.screen, BLUE, (x,y), 40)
        if piece.color == RED:
            pygame.draw.circle(self.screen,RED,(x,y),30)
        else:
            pygame.draw.circle(self.screen,BROWN,(x,y),30)
        if piece.king:
                self.screen.blit(CROWN_IMG, (x - CROWN_IMG.get_width()//2, y - CROWN_IMG.get_height()//2))

    def change_turn(self):
        if self.turn == RED:
            self.turn = BROWN
        else:
            self.turn = RED
    def winner(self):
        return self.board.winner()
    def ai_move(self,board):
        self.board = board
        self.change_turn()

def get_new_board(piece,board, move,skipped):
    row = move[0]
    col = move[1]
    board.move_piece(piece,col,row)
    if skipped:
        board.remove_piece(skipped)
    return board
def get_all_board(board,color):
    boards = []
    for piece in board.all_pieces(color):
        valid_moves = board.get_valid_moves(piece)  #{move: [skipped]}
        for move, skipped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.col,piece.row)
            new_board = get_new_board(temp_piece,temp_board,move,skipped)
            boards += [new_board]
    return boards
def minimaxAlgorithm(currBoard, level,color):
    best_score = -999
    best_board = None
    if level ==0 or currBoard.winner() != None:
        if color == BROWN:
            return currBoard.score(), currBoard
        else:
            return - currBoard.score(), currBoard
    for board in get_all_board(currBoard,color):
        if color == RED:
            change_color = BROWN
        else:
            change_color = RED
        new_value = - minimaxAlgorithm(board,level - 1,change_color)[0]
        if new_value > best_score:
            best_score = new_value
            best_board = board
    return best_score, best_board


def get_piece_from_mouse(pos):
        x , y = pos
        row = y // PIECE_SIZE
        col = x // PIECE_SIZE
        return col,row
def show_choice():
    while True:
        print("Chọn nước đi trước hay sau:")
        print("1. Nâu (đi trước)")
        print("2. Đỏ (đi sau)")
        print("3. Thoát")
        first_color = int(input("Chọn số: "))
        if first_color == 3:
            exit()
        if first_color == 1:
            first_color = BROWN
            break
        if first_color == 2:
            first_color = RED
            break   
    print("=================================")
    while True:
        print("Chọn độ khó trò chơi:")
        print("1. Dễ")
        print("2. Trung bình")
        print("3. Khó")
        print("4. Thoát")
        level = int(input("Chọn số: "))
        if level == 4:
            exit()
        if level == 1 or level == 2 or level == 3:
            break
    return first_color,level
def main():
    choose_color, level=show_choice()
    screen = pygame.display.set_mode((800,800))
    screen.fill(WHITE)
    pygame.display.set_caption("Checkers")
    game = Checkers(screen,BROWN,level)
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        if choose_color == BROWN:
            if game.turn == RED:
                new_board = minimaxAlgorithm(game.board,level,RED)[1]
                game.ai_move(new_board)                    
        else:
            if game.turn == BROWN:
                new_board = minimaxAlgorithm(game.board,level,BROWN)[1]
                game.ai_move(new_board)

        if game.winner() != None:
            if game.winner() == RED:
                print("RED WINNER")
            else:
                print("BROWN WINNER")
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col,row = get_piece_from_mouse(pos)
                game.select_square_or_piece(col,row)
        #print(str(game.board.brown_piece) + "-BROWN- " +str(game.board.brown_king))
        #print(str(game.board.red_piece) + "-RED- " +str(game.board.red_king))
        #print("=====================================================")
        game.update()
    pygame.quit()
main()
