from .player import Player


def calculate_fitness(score: int, age: int, longest_edge: int) -> float:
    """Return a value determining how 'good' a player is."""
    
    adjusted_age = age // (longest_edge / 10)

    fitness = adjusted_age + ((2**score) + (score**2.1)*500) - (((.25 * adjusted_age)**1.3) * (score**1.2))
    
    #blacklist any players doing too badly
    fitness = max(fitness, .0)
    
    return fitness


def simulate(player: Player) -> Player:
    """Assign the player its fitness.
    
    Run the player in its environment dependent on simulation_settings.
    Collect stats and then calculate the fitness of the player and assign it.
    """

    player.start_state()

    longest_edge = max(player.grid_size)
    time_since_eaten = 0
    current_score = 0
    age = 0

    while True:

        age += 1

        player.look()
        move = player.think()
        player.move(move)

        #increase time_since_eaten
        if player.score == current_score:
            time_since_eaten += 1
        else:
            time_since_eaten = 0
            current_score = player.score
        
        #restart if needed
        M = max(6, min(player.score + player.start_length, longest_edge))   #variable for determining progress     
        if player.is_dead or time_since_eaten == M * longest_edge:
            break
        
    player.best_score = player.score

    player.fitness = calculate_fitness(player.score, age, longest_edge)
    return player