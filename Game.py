
class Game:
    
    #represents the quqarto board?
    #represents the boardstate using bitstrings
    
    def __init__(self, board=[]):
        #Initiate the board with empty spaces
        self.board = board
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        
        self.remaining_pieces = PIECES.keys()
        
        self.horizontal_win = False
        self.vertical_win = False
        self.diagonal_win = False
        
        self.current_player = 1
        
        
    def print_board(self):
        print "  1   2   3   4" #x pos
        y_pos = 0
        for i in self.board:
            y_pos += 1
            print str(y_pos) + PIECES[i[0]] + PIECES[i[1]] + PIECES[i[2]] + PIECES[i[3]]
        
    #winning checker, returns true if this state is a terminal state
    def terminal_state(self):
        for i in range(0,4):
            line = self.board[i]
            #check horizontal
            if (line[0] & line[1] & line[2] & line[3]) != 0:
                self.horizontal_win = True
                return self.board.index(line)+1
            #check vertical
            if (self.board[0][i] & self.board[1][i] & self.board[2][i] & self.board[3][i]) != 0:
                self.vertical_win = True
                return i+1
        #check diagonal lines!
        if (self.board[0][0] & self.board[1][1] & self.board[2][2] & self.board[3][3]) != 0:
            self.diagonal_win = True
            return 1
        elif (self.board[0][3] & self.board[1][2] & self.board[2][1] & self.board[3][0]) != 0:
            self.diagonal_win = True
            return 4
        return False
            
    #takes in a position and a piece, as a bitstring, and places it on the board
    def place_piece(self, x, y, piece):
        if self.board[y-1][x-1] == 0b00000000:
            self.board[y-1][x-1] = piece
            return True
        return False
            
            
import random

class Player:
    #Abstract player class
    def __init__(self, game):
        self.game = game
        
    def select_piece(self):
        return 0
    
    def select_position(self):
        return [0,0]

class HumanPlayer(Player):
    #Plays based on input through console
    def __init__(self, game):
        self.game = game
        
    def select_piece(self):
        return 0

class RandomPlayer(Player):
    #Plays randomly all the way!
    #Humpty Dumpty sat on a wall!
    def __init__(self, game):
        self.game = game
        
    def select_piece(self):
        pieces = PIECES.keys()
        return pieces[random.randrange(0, pieces)]
        
    def select_position(self):
        

class NovicePlayer(Player):
    #Plays randomly
    #Avoids selecting pieces which will give a win to opponent
    #Puts a piece if winning position if possible
    
class Minimax3Player(Player):
    #Searches through the tree of game states with a depth of 3
    #chooses winning move if possible
    
class Minimax4Player(Player):
    #Searches through the tree of game states with a depth of 4
    #chooses winning move if possible
    
class MonteCarloPlayer(Player):
    #for each possible piece selection/placing given a game state:
    #simulates 1000k rounds of game
    #chooses the move which statistically has highest probability of winning
    
    

#pieces unstarred.starred unbracketed.bracketed small.big red.blue
PIECES = {
          0b00000000: '    ',
          0b10101010: ' r  ',
          0b10101001: ' b  ',
          0b10100110: ' R  ',
          0b10100101: ' B  ',
          0b10011010: ' (r)',
          0b10011001: ' (b)',
          0b10010110: ' (R)',
          0b10010101: ' (B)',
          0b01101010: ' r* ',
          0b01101001: ' b* ',
          0b01100110: ' R* ',
          0b01100101: ' B* ',
          0b01011010: '(r*)',
          0b01011001: '(b*)',
          0b01010110: '(R*)',
          0b01010101: '(B*)',
          }
                 
if __name__ == "__main__":
    game = Game()
    
    game.place_piece(1, 4, 0b10101001)   
    game.place_piece(2, 3, 0b10100101)  
    game.place_piece(3, 2, 0b10010101)   
    game.place_piece(4, 1, 0b01101001)
    game.print_board()
    
    print game.terminal_state()
    
