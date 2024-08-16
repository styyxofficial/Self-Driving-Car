## About
This project was an experiment to see if it was possible to train an artificial neural network to find the most optimal path around a race track. The idea came about from a friend who told me how F1 drivers follow "racing-lines" which are not the shortest path around the track, but rather the fastest. These lines share the trait that they try to preserve the maximum speed of the car, which I tried to replicate in this project.

## Prerequisites
1. Install Git on your machine. I used the [Windows 64-bit installer](https://github.com/git-for-windows/git/releases/download/v2.46.0.windows.1/Git-2.46.0-64-bit.exe) but use whatever installer best describes your machine.
2. Install miniconda on your machine. I used the [Windows 64-bit installer](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe). Use the default installation settings.


## How to Build
To set up the project, follow these steps:
```shell
# Open up Git Bash, which you installed in the previous section

# Navigate to where you want the project to be saved
cd "C:/some/random/directory"

# Clone the repository
git clone https://github.com/styyxofficial/Self-Driving-Car.git
```

Now you want to create an isolated environment for the project so that it does not interfere with anything on your machine:
```make
:: Open up the Anaconda Prompt, which should have been installed with miniconda

:: Navigate to the directory where the project was cloned
cd "C:/some/random/directory/Self-Driving-Car"

:: Use environment.yml file to create the environment with all the dependencies
conda env create -f environment.yml

:: Activate the environment you just created. From here, you are ready to run the project.
conda activate self-driving-car

:: Once you are DONE running the project, you can deactivate the conda env
conda deactivate
```

## How to Run
Follow these steps after setting up the dependencies to run the program:
```python
# Open up Git Bash again and make sure you are in the directory containing the project
cd "C:/some/random/directory/Self-Driving-Car"

# Run the python program
python Moving_Car.py
```

## Customization
This project allows you to change certain variables to run the experiments you want.\
\
First, you can see the [NEAT Config File documentation](https://neat-python.readthedocs.io/en/latest/config_file.html) which allows you to customize the behavior of the NEAT AI. Some basic knowledge of neural networks is required to understand NEAT's configuration options. You can modify the configuration options in `neat_config.txt`.\
\
Second, you can customize initialization settings in `initialization.txt`. Here you can change various parameters:
```python
[INITIALIZATION]
generations = 200           # Number of generations you want to train for
cpu_cores = 2               # Number of cpu cores you want to use for parallelization. More cpu cores allows you to increase the simulation size.
map_path = images/map2.png  # Path of the map that you want the car to race on. Must be 1920x1080 resolution
car_start_x = 881           # Starting X coordinate of the car
car_start_y = 800           # Starting Y coordinate of the car
```