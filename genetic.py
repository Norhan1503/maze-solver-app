import random


class Individual:
    def __init__(self, path):
        self.path = path  
        self.fitness = 0

    def crossover(self, parent2):
        split = random.randint(0, len(self.path))
        child = self.path[:split] + parent2.path[split:]
        return Individual(child)

    

class GeneticAlgorithm:
    def __init__(self, original_maze):
        self.maze = original_maze.walls
        self.start = original_maze.start
        self.goal = original_maze.goal
        self.moves = ['U', 'D', 'L', 'R']

    
    @classmethod
    def create_individual(cls, size):
        path = [random.randint(0, 3) for _ in range(size)]
        return Individual(path)
        
    def evaluate_fitness(self, individual):
        current_position = list(self.start)
        path_to_goal = []
        for move in individual.path:
            next_position =  current_position.copy()
            if self.moves[move] == 'U':
                next_position[0] -= 1
            elif self.moves[move] == 'D':
                next_position[0] += 1
            elif self.moves[move] == 'L':
                next_position[1] -= 1
            elif self.moves[move] == 'R':
                next_position[1] += 1

            if (0 <= next_position[0] < len(self.maze)) and (0 <= next_position[1] < len(self.maze[0])) and self.maze[next_position[0]][next_position[1]] != True:
                current_position = next_position
                path_to_goal.append(move)

            if tuple(current_position) == self.goal:
                break
        
        distance_to_goal = abs(current_position[0] - self.goal[0]) + abs(current_position[1] - self.goal[1])
        
        if distance_to_goal == 0:
            optimal_path_length = abs(self.goal[0] - self.start[0]) + abs(self.goal[1] - self.start[1])
            actual_path_length = len(path_to_goal)
            fitness = 100000 * (optimal_path_length / actual_path_length)        
        else:
            fitness = 1000 / (distance_to_goal + 1)

        #fitness -= (len(individual.path) - len(path_to_goal)) * 10
        fitness -= len(path_to_goal)*0.1
        individual.fitness = max(0, fitness)
        individual.path = path_to_goal

    def mutate(self, individual, mutation_rate):
        for i in range(len(individual.path)):
            if random.random() < mutation_rate:
                individual.path[i] = random.randint(0, 3)
        return individual
    
    def elitism(self, population, elitism_size):
        return sorted(population, key=lambda x: x.fitness, reverse=True)[:elitism_size]

          
    def tournament_selection(self, population, tournament_size):
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)
    
def solve_genetic(maze):
    MAX_ATTEMPTS = 10
    for attempt in range(MAX_ATTEMPTS):
        POPULATION_SIZE = 100
        MAX_GENERATIONS = 10000
        ELITISM_SIZE = 2
        TOURNAMENT_SIZE = 5
        INITIAL_MUTATION_RATE = 0.1

        best_fitness = 0
        generations_without_improvement = 0

        ga = GeneticAlgorithm(maze)
        population = [GeneticAlgorithm.create_individual(maze.height * maze.width) for _ in range(POPULATION_SIZE)]

        for generation in range(MAX_GENERATIONS):
            for ind in population:
                ga.evaluate_fitness(ind)

            population = sorted(population, key=lambda x: x.fitness, reverse=True)

            if population[0].fitness > best_fitness:
                best_fitness = population[0].fitness
                best_individual = population[0]
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1

            if generations_without_improvement >= 200:
                break

            mutation_rate = INITIAL_MUTATION_RATE * (1 - generation / MAX_GENERATIONS)
            
            new_generation = ga.elitism(population, ELITISM_SIZE)

            while len(new_generation) < POPULATION_SIZE:
                parent1 = ga.tournament_selection(population, TOURNAMENT_SIZE)
                parent2 = ga.tournament_selection(population, TOURNAMENT_SIZE)
                child = parent1.crossover(parent2)
                child = ga.mutate(child, mutation_rate)
                new_generation.append(child)
                
            population = new_generation

        best_individual = population[0]
        cells = convert_path_to_cells(maze, best_individual.path)

        # Check if the last cell in the path is the goal
        if cells[-1] == maze.goal:
            return cells  # Return the successful path

    # If no successful path is found after MAX_ATTEMPTS
    return cells

def convert_path_to_cells(maze, path):
    current_position = list(maze.start)
    cells = [tuple(current_position)]
    moves = ['U', 'D', 'L', 'R']
    
    for move in path:
        if moves[move] == 'U':
            current_position[0] -= 1
        elif moves[move] == 'D':
            current_position[0] += 1
        elif moves[move] == 'L':
            current_position[1] -= 1
        elif moves[move] == 'R':
            current_position[1] += 1
        
        if (0 <= current_position[0] < maze.height) and (0 <= current_position[1] < maze.width) and not maze.walls[current_position[0]][current_position[1]]:
            cells.append(tuple(current_position))
        
        if tuple(current_position) == maze.goal:
            break
    return cells

# This function will be called by searchAlgorithms.py
def main(maze):
    return solve_genetic(maze)
