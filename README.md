# MUTR_status_board
A status board for the Maryland University Training Reactor.

## Getting Started
You will need to be able to run conda and git.

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html). For my setup, I used miniconda3 version 4.6 (not the latest version due to compatibility issues) which can be found [here](https://repo.anaconda.com/miniconda/)
2. Clone this repo into a folder of your choice ([instructions](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository))
3. Open a terminal where conda is enabled (e.g. Anaconda Prompt on Windows, Temrinal on MacOS/Linux)
4. Navigate to the folder you cloned the repo in
5. In your terminal, run `$ conda env create`
6. On Windows, run `$ activate reactor_status_board_test`. On MacOS/Linux, run `$ source activate reactor_status_board_test`

## Running the Status Board
The reactor_status_board_test environment contains the spyder package. While this environment is activated, you can run 

`$ spyder` 

to open a spyder window. Open `status_board.py` from there. Alternatively, you can also run

`$ python status_board.py` directly from the terminal.
