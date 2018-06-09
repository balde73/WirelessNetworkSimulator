ANALYSIS OF A SIMPLE WIRELESS COMMUNICATION NETWORK
---------------------------------------------------

Visit https://github.com/balde73/SPE-assignment-2 to read the markdown version of this file and the full repository.



PREREQUISITES
-------------

This project requires `python3`, `python3-pip` and `python3-tk`. So if they are already installed simply skip this part (Tkinter and pip should be shipped with Python out of box). Otherwise use the command:

```
make prepare
```

Or as alternative install the missing one using:

```
sudo apt-get install python3
sudo apt-get install python3-tk
sudo apt-get install python3-pip
```

If you use python v3.x as default python instead of python3 this should be handled. The default pip command will be `pip` instead of `pip3` and `python` instead of `python3`.

If you  feel **really lucky** you could skip this part and simply run the project using one rule of makefile. A subroutine will check the python version installed and will perform `make prepare` and `make install` for you if no `python3` is found.



INSTALLING
----------

Now you need to install the python library using pip

```shell
make install
```

That simply performs `pip3 install -r requirements.txt`



HOW TO RUN
----------

Many option are available to run the project. Type `make` or `make help` for a complete list

```
> make help

\\ will output

make prepare
    prepare development environment, use only once
make install
    install all python requirements, use only once
make start
    start the simulation as in init.py
make start-fast
    start a fast simulation (results will be less accurate)
make start-normal
    start a default simulation (results can be considerate good)
make start-slow
    this is the best simulation (but it is really slow)
make start-verbose
    start the simulation with verbose flag
make start-debug
    start the simulation using a default test
make start-beautiful
    start the simulation in the browser with a user interface
make start-beautiful-debug
    start the simulation in the browser with a user interface and a default test
make model
    start the model
make analysis
    start the analysis of data
make start-all-in-one
    start a fast simulation then the model and at the end the analysis of data
```

### A fast simulation

The fastest way to test the full project is by simply run `make start-all-in-one`

This will perform:
```
make check_version
make start-normal
make model
make analysis
```

That will be translated as:
#### make start-normal
```
python3 simulator -dt 1000 -r 10 -nodb
```
-**dt 1000**: Run a simulation using dynamic time flag on. This means that for every gamma the network will be simulated for `avg_inter_arrival_time * 1000` seconds.

-**-r 10**: Means 10 repetition for every gamma

-**-nodb**: Ignore debug flag. We are not debugging

The gammas will be the one in the `./simulator/init.py` file.

At the end a new file `stats_nodes.csv` will be created.
For a full list of options see: `simulator init` or run `python simulator --help`.

#### make model
```
python3 model
```
Will run the mathematical model in order to compute the steady state of every quantization matrix. At the end will create a `model.csv` file.

#### make analysis
```
python3 analysis
```
Will plot all the graph to analyze the simulation and the model using the file created. 


### Running out of time

Another way to test the project is by copying the `stats-nodes.csv` and `model.csv` in the csv folder and put it in the root folder. This file are already the outputs of the simulator and the model.

Now it is possible to plot the graph using
```
make analysis
```
or
```
python3 analysis
```



ADVANCED CONFIGURATION
----------------------
It is possible to modify the `./simulator/init.py` file in order to change the parameters of the network such as: speed, nodes position, queue size, gamma values ... Please remember that this modification could be rewritten by some script such as `make start-fast` so please use it in combination with: `make start` or `python3 simulator`.



TESTING
-------

Also in the `./simulator/init.py` it is possible to test the network using the tests defined in `./simulator/test.py`. To test the network enable test flag!

Example of `init.py`:
```
import test

[...]

DEBUG = 1
VERBOSE = 1

DEBUG_POINTS = test.NODE_3_NEAR_1_2

DEBUG_COUNT = [
  0,
  0,
  0
]

DEBUG_TRANSMISSION = test.DEBUG_TRANSMISSION_7
```

The file `test.py` will have:
```
# Position (x,y) for every node
NODE_3_NEAR_1_2 = [
  (0.401, 0.387),
  (0.801, 0.387),
  (0.601, 0.387)
]

# Use this in combination with NODE_3_NEAR_1_2 meaning node 3 is near node 1 and 2 but 1 and 2 are far away
# Example   1 ------ 3 ------- 2
# Node3 transmits (from 0.1s to 0.2s)
# Node2 cannot transmit at time 0.13s (is receaving) so delays his transmission
# Node1 cannot transmit at time 0.15s (is receaving) so delays his transmission
# Node2 should start transmitting at time 0.2s
# Node1 should start transmitting at time 0.2s

# Transmission from Node3 should be ok (no collision)
# Transmissions from Node1 and Node2 should result in a collision

DEBUG_TRANSMISSION_7 = [
  [
    (0.15, 100000)
  ],
  [
    (0.13, 100000),
  ],
  [
    (0.10, 100000),
  ]
]
```
Many tests are already available, of course it is possible to create new ones defining the position of nodes and for every node the transmissions they will try to perform specifying `(<start_time>, <packet_size>)`. A default test could be load using `make start-debug`



USER INTERFACE
--------------

A convenient user interface is provided in order to better understand the network behaviour. This provides an overview about:

- all the nodes (what are the nodes transmitting, receiving, colliding at every step)

- all the tranmisssion (how transmissions are distributed in time)

- the simulator (how the decision to delay transmission, collisions and more are made)

To start the simulation using the user interface run:
```
make start-beautiful

or

python3 ./simulator/main_interface.py
```
This will run the simulation as described in the `./simulator/init.py` file for a single value of gamma that is possible to change inside `./simulator/main_interface.py`.

`./simulator/main_interface.py` works exaclty as `./simulator/__main__.py` so it is possible to start a test, or personalize the value of the network as described before.

A new tab will be open in the default browser at `http://127.0.0.1:5000/` thanks to *Flask*. Use the three button to:

- next: perform only one step in the simulator

- start: start the simulator (same as continuously pressing next)

- stop: pause the simulator. (Use start to continue the simulator from this point)
