
import random
import copy
import TCP
from test.test_wait3 import Wait3Test

class Game:
    
    #represents the quqarto board?
    #represents the boardstate using bitstrings
    
    def __init__(self):
        #Initiate the board with empty spaces
        self.board = []
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.board.append([0b00000000, 0b00000000, 0b00000000, 0b00000000])
        
        self.remaining_pieces = PIECES.keys()
        self.remaining_pieces.pop(0)
        
        #instanciate the lists of pssible positions
        self.remaining_positions = []
        for i in range(0,4):
            for j in range(0,4):
                self.remaining_positions.append([i,j])
                      
        self.horizontal_win = False
        self.vertical_win = False
        self.diagonal_win = False
        
        self.players = [RandomPlayer(self), RandomPlayer(self)]
        self.player_to_pick = 0
        self.player_to_place = 1
        
    def set_player_one(self, player):
        self.players[0] = player
        
    def set_player_two(self, player):
        self.players[1] = player
        
    def print_board(self):
        print "  1   2   3   4" #x pos
        y_pos = 0
        for i in self.board:
            y_pos += 1
            print str(y_pos) + PIECES[i[0]] + PIECES[i[1]] + PIECES[i[2]] + PIECES[i[3]]
        print " "
        
    def print_pieces(self):
        print "Remaining Pieces"
        a_string = ""
        for n in range(1,len(self.remaining_pieces)+1):
            a_string += repr(n).rjust(5)
        print a_string
        remaining_pieces_string = "  "
        for i in self.remaining_pieces:
            remaining_pieces_string += str(PIECES[i]).rjust(5)
        print remaining_pieces_string
        
    #winning checker, returns the index of winning line if this state is a terminal state
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
        if self.board[y][x] == 0b00000000:
            self.board[y][x] = piece
            return True
        return False
    
    def clear_position(self, x, y):
        self.board[y][x] = 0b00000000
    
    def take_piece(self, piece_index):
        if self.remaining_pieces[piece_index]:
            self.remaining_pieces.pop(piece_index)
            return True
        return False

    def play(self):
#        self.player_selection()
        self.print_board()
        while(len(self.remaining_pieces)>0):
            #Player 1 selects piece from the pool
            self.print_pieces()
            piece_index = self.players[self.player_to_pick].select_piece()
            print piece_index
            piece = self.remaining_pieces[piece_index]
            while not self.take_piece(piece_index):
                print "Error: Player is an idiot: Piece does not exist!"
                piece_index = self.players[self.player_to_pick].select_piece()
                piece = self.remaining_pieces[piece_index]
            print "Player " +str(self.player_to_pick+1)+ " selects the piece " +PIECES[piece]
            
            self.print_board()
            #Player 2 selects where to put the piece
            position_index = self.players[self.player_to_place].select_position(piece)
            position = self.remaining_positions[position_index]
            while not self.place_piece(position[0], position[1], piece):
                print "Error: Player is an idiot: The position is taken!"
                position_index = self.players[self.player_to_place].select_position(piece)
                position = self.remaining_positions[position_index]
                print str(position)
            print "Player " +str(self.player_to_place+1)+ " places it in position " +str(position[0]+1)+ "," +str(position[1]+1)
            self.remaining_positions.pop(position_index)
            self.print_board()
            
            #Check for a winner
            winning_position = self.terminal_state()
            if winning_position != False:
                break
            #Swap the player indexes
            temp = self.player_to_pick
            self.player_to_pick = self.player_to_place
            self.player_to_place = temp
        
        #End of game
        if len(self.remaining_pieces)==0 and winning_position==False:
            print "GAME OVER"
            print "Draw"
        else:
            print "GAME OVER"
            print "Winner: Player "+str(self.player_to_place+1)
            print "Horizontal="+str(self.horizontal_win)+" Vertical="+str(self.vertical_win)+" Diagonal="+str(self.diagonal_win)
            print "Line "+str(winning_position)
        return self.player_to_place+1
               
        
    #prompts input from console to select level of players
    def player_selection(self):
        print "Select level of player 1:"
        print "1: Randomizing Player. 2: Novice Player. 3: Minmax3 Player. 4: Minimax4 Player. 5: Human Player."
        level = int(raw_input("-->"))
        player1 = {
                  1: RandomPlayer(self),
                  2: NovicePlayer(self),
                  3: Minimax3Player(self),
                  4: Minimax4Player(self),
                  5: HumanPlayer(self)
                  }[level]
        self.set_player_one(player1)
        
        print "Select level of player 2:"
        print "1: Randomizing Player. 2: Novice Player. 3: Minmax3 Player. 4: Minimax4 Player. 5: Human Player."
        level = int(raw_input("-->"))
        player2 = {
                  1: RandomPlayer(self),
                  2: NovicePlayer(self),
                  3: Minimax3Player(self),
                  4: Minimax4Player(self),
                  5: HumanPlayer(self)
                  }[level]
        self.set_player_two(player2)
        
        
            


class HumanPlayer(Player):
    #Plays based on input through console
    def __init__(self, game):
        self.game = game
        
    def select_piece(self):
        print "Select piece nr.:"
        console_in = raw_input("-->")
        return int(console_in)-1
            
    
    def select_position(self, piece):
        print "Select x position for piece:"
        console_in1 = raw_input("-->")
    
        print "Select y position for piece:"
        console_in2 = raw_input("-->")
        return self.game.remaining_positions.index([int(console_in1)-1, int(console_in2)-1])
    

    
    
class Minimax3Player(Player):
    #Searches through the tree of game states with a depth of 3
    #chooses winning move if possible
    def __init__(self, game):
        Player.__init__(self, game)
       
    #return the piece index of the piece to be placed as it is in the game.remaining_pieces list 
    def select_piece(self):
        return Player.select_piece(self)
    
    #return the position index of the position to be placed in as it is in the game.remaining_positions list
    def select_position(self, piece):
        return Player.select_position(self)
    
 
   
class Minimax4Player(Player):
    #Searches through the tree of game states with a depth of 4
    #chooses winning move if possible
    def __init__(self, game):
        Player.__init__(self, game)
        
    def select_piece(self):
        #TODO
        #find the piece we wantz to uze
        piece = 0b00000000
        if(self.is_connected):  #send the piece through TCP if the other agent is a remote agent
            self.tcp.send_piece(piece)
            
        return piece
    
    def select_position(self, piece):
        #TODO
        #find position we want!
        position = [0,0]
        if(self.is_connected):
            self.tcp.send_position(position)
            
        return position
    
    def set_connection(self, tcp):
        self.tcp = tcp
        self.is_connected = True
        
    

class MonteCarloPlayer(NovicePlayer):
    #IMPLEMENT IF WE WANT TO, not necessary/mandatory/obligatory/mandatory
    #for each possible piece selection/placing given a game state:
    #simulates 1000k rounds of game
    #chooses the move which statistically has highest probability of winning
    
    def __init__(self, game):
        self.game = game
     
    def select_piece(self):
        return self.simulate_piece_selection()
    
    def select_position(self, piece):
        if len(self.game.remaining_positions) > 12:
            return super(MonteCarloPlayer, self).select_position(piece)
        return self.simulate_position_selection(piece)

   
class MonteCarloMinimaxPlayer(Player):
    #IF WE WANT TO IMPLEMENT IT, we don't need to, not compulsory/mandatory/obligatory
    #combines the techniques of montecarlo playing and minimax analasysis
    def __init__(self, game):
        Player.__init__(self, game)
        
    def select_piece(self):
        return Player.select_piece(self)
    
    def select_position(self, piece):
        return Player.select_position(self)
    
    
class RemotePlayer(Player):
    #gets information on moves from a remote player using a TCP socket server and stuff
    #needs to be player 2 in the game
    
    def __init__(self, game):
        self.tcp = TCP("127.0.0.1", "5005")
        self.game.players[0].set_connection(self.tcp)
        
    def select_piece(self):
        data = self.tcp.receive_piece()
        while data == None:
            print "No data received"
        return int(data)
    
    def select_position(self, piece):
        data = self.tcp.receive_position()
        while data == None:
            print "No data received"
        return int(data)
    
    

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
#
#    player = NovicePlayer()
#    player.check_1_piece_ply()
    winning_stats = [0, 0]
    for i in range(0, 100):
        game = Game()
        game.set_player_two(NovicePlayer(game))
        game.set_player_one(MinimaxPlayer(game))
        winner = game.play()
        print "Winner: Player "+str(winner)
        winning_stats[winner-1] += 1
    print winning_stats
        
    
#    while(True):
#        print " "
#        print "NEW GAME? (y/n)"
#        if raw_input("-->") == 'y':
#            game = Game()
#            game.play()
#        else:
#            break
