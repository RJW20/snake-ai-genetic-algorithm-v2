# Snake AI: Genetic Algorithm
Application of the Genetic Algorithm to the game Snake.

## Configuration

### What the Snake can see:
- The distance to the walls, and food or its own body if applicable in 8 directions around the head (cardinal and oridinal directions) - normalised values used in the neural network are actually 1 over these distances.
- The direction its head and tail are moving in, represented by 4 one-hot values each (1 for each cardinal direction).

### What the Snake can do:
Every frame the Snake can turn in any of the cardinal directions North, East, South or West.

### Neural Network Structure:
There are 32 input nodes (24 for sight, 8 for own direction), 4 output nodes (1 for each direction it could move in) with softmax activation and 2 hidden layers with 16 and 8 sigmoid nodes respectively.

### Fitness Function:
The fitness of the Snake is a function of how long it has survived (adjusted for the size of the game grid) and how many apples it has eaten. We want it to be able to avoid walls, but also not spin endlessly and instead try to hunt down the apples. See the `calculate_fitness` function in `snake_ai/simulator.py` for the full details.

### Results:
Snake is not a trivial game, but not too difficult that the Genetic Algorithm can't beat it. The first win came at generation 488, and after many more generations the Snake can beat the game with pretty much perfect consistency. Here is one such run:

![Snake completing the game](https://i.imgur.com/Pn685qp.gif)

However increasing the size of the grid beyond the 10x10 this Snake was trained on renders it completely unable to hunt down the apples, and the Snake just circles the edge (within 5 squares, where it knows in 10x10 is safe). One could potentially remedy this by using a more binary type of vision, that hence would work identically for all grid sizes.

## If you want to run it yourself

### Basic Requirements:
1. [Python](https://www.python.org/downloads/).
2. [Poetry](https://python-poetry.org/docs/) for ease of installing the dependencies.

### Getting Started:
1. Clone or download the repo `git clone https://github.com/RJW20/snake_ai_genetic_algorithm_v2.git`.
2. Download the submodules `git submodule update --init`.
3. Set up the virtual environment `poetry install`.
4. Enter the virtual environment `poetry shell`.

### Running the Algorithm:
1. Change any settings you want in `snake_ai/settings.py`. For more information on what they control see [here](https://github.com/RJW20/genetic_algorithm_template/blob/main/README.md). 
2. Run the algorithm `poetry run main`.
3. View the playback of saved history with `poetry run playback`. You can change the generation shown with the left/right arrow keys and increase or slow-down the playback speed with the k/j keys respectively.
