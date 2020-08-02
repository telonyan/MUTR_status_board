# MUTR_status_board
A status board for the Maryland University Training Reactor

## Getting Started
You will need to be able to run conda and git.

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html). For my setup, I used miniconda3 version 4.6 which can be found [here](https://repo.anaconda.com/miniconda/) in the installer archives. This was chosen due to compatibility issues with [pyfirmata](https://pypi.org/project/pyFirmata/), but may be resolve in the future.
2. Clone this repo into a directory ([instructions](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository))
3. Open a terminal where conda is enabled (e.g. Anaconda Prompt, Terminal, WSL)
4. Navigate to the folder you cloned the repo in
5. In your terminal, run `$ conda env create`
6. On Windows, run `$ conda activate reactor_status_board_test`. On MacOS/Linux, run `$ conda source activate reactor_status_board_test`. If you're using Anaconda Prompt, you don't need `conda` at the start

## Running the Status Board
The reactor_status_board_test environment contains packages necessary to run the program, as well packages necessary to run autopep8 and spyder IDE. The environment must be active for the program to run. You can set up [autoenv](https://github.com/inishchith/autoenv) for this or run `$ conda activate reactor_status_board_test` each time you re-open a terminal. While this environment is activated, you can run the __main__.py file to run the status board (double clicking, terminal command, or through IDEs are all fine). Alternatively, you can also run

`$ python /path/foldername`

where `foldername` is this repo's directory (this repo should be treatable as a package). Many other IDEs also support conda but were not included in the environment.
