import pygame

from snake_app import Grid
from genetic_algorithm import Population
from .player import Player
from .settings import player_args
from .settings import genetic_algorithm_settings
from .settings import playback_settings


##bind settings to variables
population_size = genetic_algorithm_settings['population_size']
total_generations = genetic_algorithm_settings['total_generations']
history_folder = genetic_algorithm_settings['history_folder']
history_type = genetic_algorithm_settings['history_type']
history_value = genetic_algorithm_settings['history_value']
block_width = playback_settings['block_width']
block_padding = playback_settings['block_padding']


def playback() -> None:
    """Show playback of the result of running the genetic algorithm on snake.
    
    Do not alter settings.py between running the genetic algorithm and running this.
    Switch between generations with the left and right arrow keys.
    Slow down up or speed up the playback with the j and k keys.
    """

    #initialize the grid the game will be modelled from
    grid = Grid(player_args['grid_size'], block_width, block_padding)

    #pygame setup
    game_offset = (250, 0)
    screen = pygame.display.set_mode((grid.screen_size[0] + game_offset[0],
                                     grid.screen_size[1] + game_offset[1]))
    pygame.display.set_caption("Snake: Genetic Algorithm Playback")
    clock = pygame.time.Clock()
    running = True

    #create a surface for the game
    game = pygame.Surface((grid.screen_size))

    #initialize text for the stats
    text_size = max(grid.screen_size[1] // 35, 17)
    text_colour = (190, 190, 190)
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), text_size)

    #intialize the playback population
    playback_pop = PlaybackPopulation(history_folder=history_folder, 
                                      history_type=history_type,
                                      history_value=history_value, 
                                      og_pop_size=population_size,
                                      total_generations=total_generations,
                                      player_args=player_args)
    
    #get and start the first snakes
    snakes = playback_pop.current_players
    for snake in snakes:
        snake.start_state()

    base_speed = 5
    speed_multiplier = 1

    #the score text depends on whether we are just showing a champ or multiple
    score_text = 'Score'
    if len(snakes) != 1:    #if not showing just champ or history type and value result in just saving 1 per gen
        score_text = 'Champ\'s ' + score_text

    while running:
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            #handle key presses
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    playback_pop.current_generation = playback_pop.current_generation % total_generations + 1
                    if not playback_pop.is_champs:
                        playback_pop.new_gen(playback_pop.current_generation)
                    snakes = playback_pop.current_players
                    for snake in snakes:
                        snake.start_state()
                    
                elif event.key == pygame.K_LEFT:
                    playback_pop.current_generation = (playback_pop.current_generation - 2) % total_generations + 1
                    if not playback_pop.is_champs:
                        playback_pop.new_gen(playback_pop.current_generation)
                    snakes = playback_pop.current_players
                    for snake in snakes:
                        snake.start_state()

                elif event.key == pygame.K_j:
                    speed_multiplier = max(1, speed_multiplier // 2)
                elif event.key == pygame.K_k:
                    speed_multiplier *= 2

        #move all snakes
        for snake in snakes:
            snake.look()
            move = snake.think()
            snake.move(move)

            #remove any that have died
            if snake.is_dead:
                snakes.remove(snake)

        #restart them if all are dead
        if len(snakes) == 0:
            snakes = playback_pop.current_players
            for snake in snakes:
                snake.start_state()

        #fill the screen to wipe last frame
        screen.fill((40,40,40))
        game.fill((40,40,40))

        #line separating game from stats
        width = 1
        pygame.draw.line(screen, 'white', (game_offset[0] - width, game_offset[1]), (game_offset[0] - width, game_offset[1] + grid.screen_size[1]), width = width)

        #draw the snakes and their foods on the game
        for snake in snakes:
            pygame.draw.rect(game, 'red', pygame.Rect(grid.gridpoint_to_coordinates(snake.target.position), (grid.block_width, grid.block_width)))
            for pos in snake.body:
                pygame.draw.rect(game, 'green', pygame.Rect(grid.gridpoint_to_coordinates(pos), (grid.block_width, grid.block_width)))
                    
        #generate the stats
        gen = font.render(f'Generation: {playback_pop.current_generation}', True, text_colour)
        gen_position = (15, 15)
        score = font.render(f'{score_text}: {max([snake.score for snake in snakes])}', True, text_colour)
        score_position = (15, 15 + 1.6*text_size)
        speed = font.render(f'Speed: {speed_multiplier}x', True, text_colour)
        speed_position = (15, 15 + 2*1.6*text_size)

        #display the changes
        screen.blit(game, game_offset)
        screen.blit(gen, gen_position)
        screen.blit(score, score_position)
        screen.blit(speed, speed_position)
        pygame.display.flip()
        
        #advance to next frame at chosen speed
        clock.tick(base_speed * speed_multiplier) / 1000

    pygame.quit()


class PlaybackPopulation(Population):
    """Extension of Population class with methods allowing us to manipulate
    which genomes are loaded.

    Will determine its own size and automatically load the first genomes.
    """

    def __init__(self, 
                 history_folder: str,
                 history_type: str, 
                 history_value: int, 
                 og_pop_size: int, 
                 total_generations: int,
                 player_args: dict
                 ) -> None:
        
        self.folder = history_folder
        self.current_generation = 1

        self.is_champs = False
        match(history_type):
            case('none'):
                raise Exception('No history was saved during evolution. If you would like ' + \
                                'to view playback, please adjust history settings and run again.')
            case('champ'):
                pop_size = total_generations
                self.is_champs = True
            case('absolute'):
                pop_size = history_value
            case('percentage'):
                pop_size = int(og_pop_size * history_value)
            case('entire'):
                pop_size = og_pop_size
            case _:
                raise Exception(f'Invalid history type {history_type}')
        self.size = pop_size
        self.players = [Player(**player_args) for _ in range(pop_size)]

        if self.is_champs:
            self.load(history_folder)   #load all champs
        else:
            self.new_gen()              #load just the first gen

    def new_gen(self, gen_id: int = 1) -> None:
        """Load generation {gen_id}.
        
        Sets self.current_generation to gen_id.
        """

        self.load(f'{history_folder}/{gen_id}')
        self.current_generation = gen_id

    @property
    def current_players(self) -> list[Player]:
        """Return the players we're currently playing back."""

        if self.is_champs:
            return self.players[self.current_generation - 1:self.current_generation]
        else:
            return self.players[:]