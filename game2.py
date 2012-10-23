from players import *

class Game:
    
    def __init__(self, player1_cls, player2_cls):
        self.players = (player1_cls(self), player2_cls(self))
        self.reset()
    
    def reset(self):
        self.board = [[None] * 4 for i in range(4)]
        self.pieces = range(16)
        self.player_turn = 0
    
    def is_full(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] is None:
                    return False
        return True
    
    def next_player(self):
        self.player_turn = (self.player_turn + 1) % 2
    
    def terminal_state(self):
        return self.is_terminal_state()
    
    def clear_position(self):
        """docstring for clear_position"""
        pass
    
    def is_terminal_state(self):
        
        # Check rows and cols
        for i in range(4):
            row = [self.board[i][j] for j in range(4)]
            col = [self.board[j][i] for j in range(4)]
            if self.is_quarto(row) or self.is_quarto(col):
                return True
        
        # Check diagonals
        diag1 = [self.board[i][i] for i in range(4)]    
        diag2 = [self.board[i][3-i] for i in range(4)]
        if self.is_quarto(diag1) or self.is_quarto(diag2):
            return True
        
        # No match? No terminal state.
        return False
    
    def is_quarto(self, pieces, invert=True):
        if len(pieces) != 4: raise Exception("NOOOOOOOOOOOOOOOOOOOOO!")
        
        for piece in pieces:
            if piece is None:
                return False
        
        # First, bitwise AND pieces as they are
        result = reduce(lambda x, y: x & y, pieces)
        if result > 0:
            return True
        
        # If inverting as well, call self with inverted pieces
        if invert:
            return self.is_quarto([~x for x in pieces], invert=False)
        
        # No hit :-(
        return False
    
    def current_player(self):
        return self.players[self.player_turn]
    
    @property
    def remaining_pieces(self):
        return self.pieces
    
    @property
    def remaining_positions(self):
        positions = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] is None:
                    positions.append((i, j))
        return positions
    
    def select_piece(self):
        player = self.current_player()
        return player.select_piece()
    
    def place_piece(self, piece, pos=None):
        player = self.current_player()
        if pos is None:
            pos = player.select_position(piece)
        
        self.pieces.remove(piece)
        
        self.board[pos[0]][pos[1]] = piece
    
    def play(self):
        while not self.is_full() and not self.is_terminal_state():
            piece = self.select_piece()
            
            self.next_player()
            self.place_piece(piece)
            
            self.print_board()
        
        return self.result()
    
    def print_board(self):
        print "  1   2   3   4" #x pos
        y_pos = 0
        for i in self.board:
            y_pos += 1
            print str(y_pos) + PIECES[i[0]] + PIECES[i[1]] + PIECES[i[2]] + PIECES[i[3]]
        print " "

    
    def result(self):
        winner = self.current_player()
        print "%s won." % winner
        return self.player_turn

PIECES = {
    None:   '    ',
    0:      ' r  ',
    1:      ' b  ',
    2:      ' R  ',
    3:      ' B  ',
    4:      ' (r)',
    5:      ' (b)',
    6:      ' (R)',
    7:      ' (B)',
    8:      ' r* ',
    9:      ' b* ',
    10:     ' R* ',
    11:     ' B* ',
    12:     '(r*)',
    13:     '(b*)',
    14:     '(R*)',
    15:     '(B*)',
}

if __name__ == '__main__':
    wins = {0: 0, 1: 0}
    for i in range(100):
        game = Game(NovicePlayer, MinimaxPlayer)
        winner = game.play()
        wins[winner] += 1
    
    for i in range(2):
        print "Player %d: %d (%s)" % (i + 1, wins[i], game.players[i])
