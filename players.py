import copy, random

class Player:
    #Abstract player class
    def __init__(self, game):
        self.game = game
        
    def select_piece(self):
        return 0
    
    def select_position(self, piece):
        return [0,0]

class RandomPlayer(Player):
    #Plays randomly all the way!
    #Humpty Dumpty sat on a wall!
    def __init__(self, game):
        self.game = game

    def select_piece(self):
        index = random.randrange(0, len(self.game.remaining_pieces))
        return self.game.remaining_pieces[index]

    def select_position(self, piece):
        index = random.randrange(0,len(self.game.remaining_positions))
        return self.game.remaining_positions[index]

class NovicePlayer(RandomPlayer):
    #Plays randomly
    #Avoids selecting pieces which will give a win to opponent
    #Puts a piece if winning position if possible
    def __init__(self, game):
        self.game = game
        
    def __str__(self):
        return "Novice"
    
    def select_piece(self):
        piece_list = self.check_1_piece_ply()
        
        if len(piece_list) > 0:
            index = random.randrange(0,len(piece_list))
            return piece_list[index]
            
        index = random.randrange(0,len(self.game.pieces))
        return self.game.pieces[index]
    
    def select_position(self, piece):
        position = self.check_1_position_ply(piece)
        if position == False:
            return self.game.remaining_positions[random.randrange(0,len(self.game.remaining_positions))]
        return position
    
    #method that simulates 1 ply down the game for each piece possible to pick
    #returns the list of remaining pieces, with pieces giving the opponent winning favor removed
    def check_1_piece_ply(self):
        piece_list = []
        for piece in self.game.remaining_pieces:
            for pos in self.game.remaining_positions:
                sim_game = copy.deepcopy(self.game)
                sim_game.place_piece(piece, pos=pos)
                if not sim_game.is_terminal_state():
                    piece_list.append(piece)
                    break
        
        return piece_list
    
    #simulates the game 1 ply down for each possible position to pick for the given piece
    #return the position of a winning position if there exists one
    def check_1_position_ply(self, piece):
        for pos in self.game.remaining_positions:
            sim_game = copy.deepcopy(self.game)
            sim_game.place_piece(piece, pos=pos)
            if sim_game.is_terminal_state():
                return pos
        return False


class MinimaxPlayer(Player):
    
    def __init__(self, game):
        Player.__init__(self, game)
    
    def __str__(self):
        return "Minimax"
    
    def select_piece(self):
        if len(self.game.remaining_pieces) < 9:
            max_piece = None
            max_piece_value = -1001
            for piece in self.game.remaining_pieces:
                max_pos = self.max_position(piece)
                if max_pos > max_piece_value:
                    max_piece = piece
                    max_piece_value = max_pos
        
            return piece
        else:
            novice_player = NovicePlayer(self.game)
            return novice_player.select_piece()
    
    def select_position(self, piece):
        if len(self.game.remaining_pieces) < 9:
            max_position = None
            max_position_value = -1001
            for position in self.game.remaining_positions:
                sim_game = copy.deepcopy(self.game)
                sim_game.place_piece(piece, pos=position)
            
                value = self.max_piece(game=sim_game)
                if value > max_position_value:
                    max_position = position
                    max_position_value = value
        
            return max_position
        else:
            novice_player = NovicePlayer(self.game)
            return novice_player.select_position(piece)
    
    def position_value(self, position, game):
        """Returns a number based on non-recursing heuristics."""
        
        # Terminal game state (victory) yields 1000
        if game.terminal_state():
            return 1000
        
        # Count number of empty slots on each row/col
        n = 0
        n_row = 0
        n_col = 0
        for i in range(3):
            row_index = i if i < position[0] else i + 1
            col_index = i if i < position[1] else i + 1
            if game.board[row_index][position[1]] == 0:
                n += 1
                n_row += 1
            if game.board[position[0]][col_index] == 0:
                n += 1
                n_col += 1
            
            # Check if we're placed on the diagonal
            if position[0] == position[1]:
                if game.board[row_index][row_index] == 0:
                    n += 1
        
        # For now, just return the number of free positions on row/col as a positive thing
        return n
    
    def piece_value(self, piece):
        """Returns value of piece given the current game."""
        return 0
    
    def max_piece(self, minimize=True, game=None, levels=3):
        """Returns a number indicating the strength of the given position."""
        game = game if game else self.game
        
        # Collect values from potential piece selections
        values = []
        for piece in game.remaining_pieces:
            
            # Deep copy a game to simulate the piece selection on
            sim_game = copy.deepcopy(game)
            
            # Recurse!
            values.append(self.max_position(piece, minimize=(not minimize), game=sim_game, levels=levels))
        
        if len(values) == 0:
            return 0
        
        # Lastly, invert values propagated upwards if we're minimizing this tree level
        if minimize:
            return -max(values)
        else:
            return max(values)
    
    def max_position(self, piece, minimize=True, game=None, levels=3):
        """Returns the optimal position."""
        game = game if game else self.game
        
        values = []
        
        for position in game.remaining_positions:
        
            # Use a deep copy of the game
            sim_game = copy.deepcopy(game)
        
            # After simulating placing of the piece, apply heuristics
            sim_game.place_piece(piece, pos=position)
        
            # If at leaf node, use some heuristic to propagate a score back upwards
            if levels == 0:
                value = self.position_value(position, sim_game)
                values.append(value)
            
            # Ready to continue recursing
            else:
            
                if sim_game.terminal_state():
                    values.append(self.position_value(position, sim_game))
        
                else:
                    # If not terminal state, recurse
                    value = self.max_piece(minimize=(not minimize), game=sim_game, levels=levels-1)
                    values.append(value)

        if len(values) == 0:
            return 0

        # Lastly, invert values propagated upwards if we're minimizing this tree level
        if minimize:
            return -max(values)
        else:
            return max(values)

