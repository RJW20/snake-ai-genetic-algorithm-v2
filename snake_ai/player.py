import numpy as np

from snake_app import Snake
from genetic_algorithm import BasePlayer
from snake_app.cartesian import Vector, Direction


class Player(Snake, BasePlayer):
    """Player existing in the game with a Genome to control its movements."""

    def __init__(self, **kwargs) -> None:
        super(Player, self).__init__(**kwargs)
        self.score = 0
        self.fitness = 0
        self.best_score = 0
        self.vision: np.ndarray = np.full((3, 8), np.inf)
        self.tail_direction: Direction

    def look_in_direction(self, search_vector: Vector, food_found: bool) -> tuple[bool, float, float, float]:
        """Return the distance to walls, food and (first occurence of, if applicable) own body in the given
        slope direction.
        
        Also return a boolean indicating if food is in that direction so we know to stop searching for it, 
        and recieve the same boolean so we know whether to search for it in this direction.
        """

        dist_to_wall = None
        dist_to_food = np.inf       #sight will be infinite if snake can't see it
        dist_to_body = np.inf       #" "
        wall_found = False
        body_found = False

        search_position = self.body[0] + search_vector     #can't start by looking at the head
        distance = 1

        #if we are looking on a diagonal we also observe food in the space next to the food in the direction the snake is
        #heading - this allows the snake to track down food on the diagonals.
        ordinal = False
        if abs(search_vector.run) + abs(search_vector.rise) == 2:
            ordinal = True
            phantom_food_position = self.target.position + self.direction.value

        #look until at the wall
        while not wall_found:

            if search_position.x < 0 or search_position.y < 0 or \
               search_position.x >= self.grid_size[0] or search_position.y >= self.grid_size[1]:
                dist_to_wall = distance
                wall_found = True
                break

            if not food_found:
                if search_position == self.target.position or (ordinal and search_position == phantom_food_position):  
                    dist_to_food = distance
                    food_found = True

            if not body_found and search_position in self.body:
                dist_to_body = distance
                body_found = True

            search_position = search_position + search_vector
            distance += 1

        return food_found, tuple(dist_to_wall, dist_to_food, dist_to_body)

    def look(self) -> None:
        """Set the snakes vision and tail direction.
        
        Can see in 8 directions around the snake (cardinal and ordinal compass points).
        """

        food_found = False
        search_directions = ((0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1))
        for i, slope in enumerate(search_directions):
            food_found, vision = self.look_in_direction(slope, food_found)
            self.vision[:, i] = np.array(vision)

        self.tail_direction = Direction(self.body[-2] - self.body[-1])

    @property
    def directions_array(self) -> np.ndarray:
        """Return an 8 entry int ndarray representing the direction of the player's head and tail.
    
        Returned array indicates whether head(tail) direction is [up, right, down, left, (...)].
        """

        values = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        output = np.zeros(8)
        output[values[self.direction.name]] = 1
        output[values[self.tail_direction.name]] = 1

        return output

    def think(self) -> str:
        """Feed the input into the Genome and turn the output into a valid move."""

        vision_input = np.reshape(np.reciprocal(self.vision), 24)    #use 1/sight as normalisation
        one_hot_directions_input = self.directions_array
        genome_input = np.concatenate((vision_input, one_hot_directions_input))
        genome_output = self.genome.propagate(genome_input)

        #turn output into move
        match(np.argmax(genome_output)):
            case 0:
                move = 'up'
            case 1:
                move = 'right'
            case 2:
                move = 'down'
            case 3:
                move = 'left'
        
        return move