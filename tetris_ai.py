import time,pygame
import tetris_original as tetris_game

size = [640, 480]
screen = pygame.display.set_mode((size[0], size[1]))

def run_game(chromosome, speed, max_score, show_game,type = '', exp = '', gene = ''):

    tetris_game.FPS = int(speed)
    tetris_game.main()

    board = tetris_game.get_blank_board()
    last_fall_time = time.time()
    score = 0
    level, fall_freq = tetris_game.calc_level_and_fall_freq(score)
    falling_piece = tetris_game.get_new_piece()
    next_piece = tetris_game.get_new_piece()

    # Calculate best move
    chromosome.best_move(board, falling_piece)

    num_used_pieces = 0
    removed_lines = [0,0,0,0]


    Continue = True
    win = False


    while Continue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit")
                exit()

        if falling_piece == None:
            falling_piece = next_piece
            next_piece = tetris_game.get_new_piece()

            chromosome.best_move(board, falling_piece)

            num_used_pieces += 1
            score += 1

            last_fall_time = time.time()

            #stoping condition
            if (not tetris_game.is_valid_position(board, falling_piece)):
                Continue = False

        if not show_game or time.time() - last_fall_time > fall_freq:
            if (not tetris_game.is_valid_position(board, falling_piece, adj_Y=1)):
                tetris_game.add_to_board(board, falling_piece)


                num_removed_lines = tetris_game.remove_complete_lines(board)

                if(num_removed_lines == 1):
                    score += 40
                    removed_lines[0] += 1

                elif (num_removed_lines == 2):
                    score += 120
                    removed_lines[1] += 1

                elif (num_removed_lines == 3):
                    score += 300
                    removed_lines[2] += 1

                elif (num_removed_lines == 4):
                    score += 1200
                    removed_lines[3] += 1

                falling_piece = None

            else:
                # Piece did not land, just move the piece down
                falling_piece['y'] += 1
                last_fall_time = time.time()

        if (show_game):

            tetris_game.DISPLAYSURF.fill(tetris_game.BGCOLOR)
            tetris_game.draw_board(board)
            tetris_game.draw_status(score,type,exp,gene,num_used_pieces)
            tetris_game.draw_next_piece(next_piece)

            if falling_piece != None:
                tetris_game.draw_piece(falling_piece)

            pygame.display.update()
            tetris_game.FPSCLOCK.tick(tetris_game.FPS)

        # Stop condition
        if (score > max_score):
            Continue = False
            win = True

    # Save the game state
    game_state = [num_used_pieces, removed_lines, score, win]

    return game_state
