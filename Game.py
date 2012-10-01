
class Game:
    
    #represents the quqarto board?
    #represents the boardstate using bitstrings
    
    def __init__(self, board=[]):
        self.board = board
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.horizontal_win = False
        self.vertical_win = False
        self.diagonal_win = False
        
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
            diagonal_win = True
            return 1
        elif (self.board[0][3] & self.board[1][2] & self.board[2][1] & self.board[3][0]) != 0:
            diagonal_win = True
            return 4
        return False
            
    #takes in a position and a piece, as a bitstring, and places it on the board
    def place_piece(self, x, y, piece):
        if self.board[y-1][x-1] == 0b00000000:
            self.board[y-1][x-1] = piece
            return True
        return False
            
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
    
