import Genetic_Algorithm as ga
import tetris_original as game
import tetris_ai as ai
import copy
import matplotlib.pyplot as plt
def train(GAME_SPEED,Generations,Population,Iterations ,Gap ,MutRate,CrossRate,MaxScore):

    NUM_CHILD = round(Population * Gap)

    best_chromos = []
    init_pop = ga.Algorithm(Population,MaxScore)

    file = open('train.txt', 'w')
    for iteration in range(Iterations):

        pop = copy.deepcopy(init_pop)

        # Initialize generation list
        generations = []

        for generation in range(Generations):
            print(' \n')
            print(f'*- - - ->Iteration: {iteration+1} , Generation: {generation+1} <- - - -*')
            print(' \n')
            temp = copy.deepcopy(pop)
            generations.append(temp)

            selected_pop = pop.selection(pop.chromosomes, NUM_CHILD)
            crossover = pop.crossover(selected_pop, CrossRate)
            new_chromo = pop.mutation(crossover, MutRate)

            for i in range(Population):
                game_state = ai.run_game(pop.chromosomes[i], GAME_SPEED, MaxScore, False,"Train",iteration+1,generation+1)
                pop.chromosomes[i].calculate_fitness(game_state)


            temp = sorted(temp.chromosomes, key=lambda x: x.score, reverse=True)
            file.writelines(str(temp[0].weights) + " Score = " + str(temp[0].score))
            file.writelines(str(temp[1].weights) + " Score = " + str(temp[1].score))

            best_chromos.append(temp[0])
            best_chromos.append(temp[1])


            pop.replace(new_chromo)

            fitness = [chrom.score for chrom in pop.chromosomes]
            print(fitness)
    file.close()





    return best_chromos











def test():
    GAME_SPEED = 500000000
    Generations = 10
    Population = 15
    Iterations = 30
    Gap = 0.3
    MutRate= 0.2
    CrossRate = 0.75
    MaxScore = 15000

    best_chromos = train(GAME_SPEED,Generations,Population,Iterations,Gap,MutRate,CrossRate,MaxScore)
    best_chromos = sorted(best_chromos, key=lambda x: x.score, reverse=True)
    print("----------------------------------------------------------------------")
    game.show_text_screen(f"Train Finished, Best Score = {best_chromos[0].score}")

    file = open('test.txt','w')
    for i in range(600):
        game_state = ai.run_game(best_chromos[i],GAME_SPEED,MaxScore,True,"Test",i+1)
        best_chromos[i].calculate_fitness(game_state)
        if best_chromos[i].score >= MaxScore:
            file.writelines("weights = "+str(best_chromos[i].weights)+", Score = "+str(best_chromos[i].score)+"\n")
    file.close()


def main():
    test()


main()