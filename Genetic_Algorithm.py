import random
import numpy as np
import copy
import tetris_original as game
import tetris_ai as ai


class Chromosome():
    def __init__(self, weights):
        self.weights = weights
        self.score = 0
        self.used_pieces = 0
    def calculate_fitness(self, game_state):
        self.score = game_state[2]
        self.used_pieces = game_state[0]
    def best_move(self, board, piece,show_board = True):

        best_x_axis = 0
        best_rotation = 0
        best_y_axis = 0
        best_score = -1e5

        # Calculate the total the holes and blocks above holes before play
        num_holes_bef, num_blocking_blocks_bef = game.calc_initial_move_info(board)
        for rotation in range(len(game.PIECES[piece['shape']])):
            # Iterate through every possible rotation
            for x_axis in range(-2, game.BOARDWIDTH - 2):
                # Iterate through every possible position
                movement_info = game.calc_move_info(board, piece, x_axis, rotation,num_holes_bef,num_blocking_blocks_bef)

                # Check if it's a valid movement
                if (movement_info[0]):
                    movement_score = 0
                    for i in range(1, len(movement_info)):
                        movement_score += self.weights[i - 1] * movement_info[i]

                    # Update best movement
                    if (movement_score > best_score):
                        best_score = movement_score
                        best_x_axis = x_axis
                        best_rotation = rotation
                        best_y_axis = piece['y']



        piece['y'] = best_y_axis
        piece['x'] = best_x_axis
        piece['rotation'] = best_rotation

        return best_x_axis, best_rotation


class Algorithm:
    def __init__(self, num_pop, max_score,num_weights=7,show = False):
        self.chromosomes = []

        for i in range(num_pop):
            weights = np.random.uniform(-1, 1, size=(num_weights))
            chrom = Chromosome(weights)
            self.chromosomes.append(chrom)

            # Evaluate fitness
            game_state = ai.run_game(self.chromosomes[i], 1000,max_score, show,'','',)
            self.chromosomes[i].calculate_fitness(game_state)

    # selection using roulette wheel
    def selection(self, population, num_selection):
        fitness = np.array([chrom.score for chrom in population])

        # Normalized fitness
        norm_fitness = fitness / fitness.sum()

        # roulette probability
        roulette_prob = np.cumsum(norm_fitness)

        selected = []
        while len(selected) < num_selection:
            pick = random.random()
            for index, individual in enumerate(self.chromosomes):
                if pick < roulette_prob[index]:
                    selected.append(individual)
                    break

        return selected

    # arithmetic crossover
    def crossover(self, selected, cross_rate):

        genes = len(selected[0].weights)  # Chromosome size
        offspring = [copy.deepcopy(c) for c in selected]

        for i in range(0, len(selected), 2):
            a = random.random()


            parent1 = random.randint(0, 100)
            parent2 = random.randint(0, 100)
            if (parent1 < cross_rate*100 and parent2 < cross_rate*100):

                for j in range(0, genes):
                    offspring[i].weights[j] = a * offspring[i].weights[j] + (1 - a) * offspring[i + 1].weights[j]
                    offspring[i + 1].weights[j] = a * offspring[i + 1].weights[j] + (1 - a) * offspring[i].weights[j]



        return offspring

    def mutation(self, chromosomes, mutation_rate):
        for chromo in chromosomes:
            for i, point in enumerate(chromo.weights):
                if random.random() < mutation_rate:
                    chromo.weights[i] = random.uniform(-1.0, 1.0)
        return chromosomes

    def replace(self, mutated):

        new_pop = sorted(self.chromosomes, key = lambda x: x.score, reverse=True)
        new_pop[-(len(mutated)):] = mutated
        random.shuffle(new_pop)

        self.chromosomes = new_pop