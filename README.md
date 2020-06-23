# MUTR_status_board
A status board for the Maryland University Training Reactor

## Getting Started
You will need to be able to run conda and git.

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html). For my setup, I used miniconda3 version 4.6 (not the latest version due to compatibility issues) which can be found [here](https://repo.anaconda.com/miniconda/)
2. Clone this repo into a direcotry ([instructions](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository))
3. Open a terminal where conda is enabled (e.g. Anaconda Prompt on Windows, Temrinal on MacOS/Linux)
4. Navigate to the folder you cloned the repo in
5. In your terminal, run `$ conda env create`
6. On Windows, run `$ activate reactor_status_board_test`. On MacOS/Linux, run `$ source activate reactor_status_board_test`

## Running the Status Board
The reactor_status_board_test environment contains packages necessary for the program, as well the spyder package. As a result, the environment must be activated for the program to run. You can use [autoenv](https://github.com/inishchith/autoenv) for this or run `$ activate reactor_status_board_test` each time you re-open a terminal. While this environment is activated, you can run 

`$ spyder` 

to open a spyder window where you can open and run `status_board.py`. Alternatively, while in the directory you cloned into, you can also run

`$ python status_board.py` directly from the terminal. Other IDEs that support conda can also be used but were not included in the environment.
