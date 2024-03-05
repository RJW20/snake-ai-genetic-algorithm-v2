player_args = {

    #grid properties
    'grid_size': (10, 10),  #(width, height)

    #snake properties
    'start_length': 3     #note will be set to min(grid_size)//2 if larger than that to prevent some of the body starting outside the grid

}


genetic_algorithm_settings = {

    #population properties
    'population_size': 1500,                    #number of players in the population
    'creation_type': 'new',                     #options are ['new', 'load']
    'load_folder': 'latest_genomes',                          #folder to load from if applicable
    'parents_folder': 'latest_genomes',            #folder to save parents of each generation to (for use with repopulation, will be overwritten each time)
    'total_generations': 1000,                   #number of generations to run for

    #history properties
    'history_folder': 'history',            #folder to permanently save the best of each generation too
    'history_type': 'champ',                #options are ['none', 'champ', 'absolute', 'percentage', 'entire']
    'history_value': 0,                     #dependent on history_type: 'absolute' -> int: number to save, 'percentage' -> float: percentage to save 

    #genome properties
    'structure': ((32, ), (16, 'relu'), (8, 'relu'), (4, 'softmax')),    #options for activation are ['sigmoid', 'relu', 'softmax', 'linear']

    #evolution properties
    'parent_percentage': 0.2,       #percentage of parents to repopulate the next generation from
    'crossover_type': 'one-point',  #options are ['one-point', 'uniform']
    'mutation_type': 'gaussian',    #options are ['gaussian', 'uniform']
    'mutation_rate': 0.05,          #probability a gene will mutate

}


playback_settings = {

    #grid properties
    'block_width': 20,
    'block_padding': 2,

}