# Opti-maze: playing with QAOA

[![Extended description](https://img.shields.io/badge/-Description-Blue)](assets/iQuHack.pdf)
[![Slides](https://img.shields.io/badge/-Slides-Blue)](assets/hackathon_mega_presentation.pdf)

<p align="left">
  <a href="https://azure.microsoft.com/en-us/solutions/quantum-computing/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488491-609828a4-cd1f-4076-b5b2-a8d9fc2d0fa4.png" width="30%"/> </a>
  <a href="https://ionq.com/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488159-da95eb05-9277-4abe-b1ba-b49871d563ed.svg" width="20%" style="padding: 1%;padding-left: 5%"/></a>
  <a href="https://iquhack.mit.edu/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151647370-d161d5b5-119c-4db9-898e-cfb1745a8310.png" width="8%" style="padding-left: 5%"/> </a>
</p>

This repo contains our solutions to IonQ + Microsoft Joint Challenge @ MIT iQuHACK 2022.

High-dimensional optimization problems with exponentially large search space lie
in the foundation of many yet unresolved scientific problems or pressing issues
that the world society is currently facing. During the MIT iQuHACK 2022
hackathon, we developed the *Opti-maze* game aimed at increasing awareness of
complexity of such problems. In this game, a player either competes with or is
being assisted by the Quantum Approximate Optimization Algorithm which can run
on a near-term noisy quantum device. The game showcases (1) how quantum
advantage can be beneficial to researchers and the general public and (2) how
even a near-term noisy quantum device can be used to tackle large-scale
optimization problems.

## Opti-Maze game

Quantum computers promise to deliver an exponential speed up to various problems
that are hard on the classical counterpart. One such class of problems is
combinatorial optimization. To solve this type of problems classically, one is
generally required to explore all possible configurations, which is in general
exponentially hard in the number of degrees of freedom. On a quantum computer,
the famous Quantum Approximate Optimization Algorithm (QAOA) promises possible
ease of this complexity. During this hackathon, we have created a game that is
aimed at helping to understand the challenges of the optimization problems and
the benefits that quantum computing can offer. Many popular computer games, from
the historical Monopoly to more advanced civilization games like Sid Mayer's
Civilization, are based on the difficulty in finding optimal solutions to a
resource allocation problem. Generally, the game is aimed to optimize a metric
on a graph and has two game regimes: *standard* and *cooperative*. In
the former, player is challenged by a *Quantum Artificial Player* which
uses the QAOA to tackle the resource allocation problem. In the latter, quantum
computer *helps* the player to solve an hard optimization problem. 

Many challenges that the humanity is currently facing can be formulated in terms
of a resource allocation problem. One of such challenges is the *fight against
the climate change*. Even though our game is ran on an arbitrary graph, we
specifically tailored one special case that illustrated applicability of QAOA to
tackling this pressing issue.

In part, the game would educate quantum novices on possible usages and
applications of *variational quantum algorithms*. At the same time, it
will make the users aware of non-triviality of resource allocation problems
including fighting the climate crisis.

... Interested? Read more [here](assets/iQuHack.pdf) or have a look at
[our slides](assets/hackathon_mega_presentation.pdf) .


### Starting the game

**Q:** I have qiskit & access to IonQ, how to I play your game on real
hardware?<br>
**A:** Unfortunately, due to time constraints and long queues for running code
with IonQ backend, we prototype the main core of our game using the Aer qiskit
simulator. IonQ backend has been used for training an instance of QAOA via
simulation and to run few instances of the final circuit with qpu. These test
have been performed in the “QAOA_Azure_part.ipynb” notebook, while the main game
is currently in “QAOA_part.ipynb”. Luckily, with some more qpu-time at disposal,
we would have set up the whole process on real quantum hardware from training to
evaluation.

**Q**: I have qiskit, but no access to IonQ, what do I do then?<br>
**A:** In this case you can run the simulator in the cells 1-2 of 
```
QAOA_part.ipynb
```

**Q**: I have neither qiskit nor access to IonQ... am I screwed?<br>
**A:** No, you are not. You can run the game locally by simply typing

```bash
python3 main_loop.py
```

**NOTE:** this mode is discouraged, because the QAOA is replaced by a
brute-force approach. Things will still work, but you won't get a feeling for
how good/bad QAOA is.

Then have a look at [our slides](assets/hackathon_mega_presentation.pdf)
which contain screencasts of us playing the game.


### Available commands in Standard mode

* Typing a number will select/deselect a component
* Typing `cheat` will show you the QAOA solution.

### Available commands in Cooperative mode

* Typing a number will select/deselect a component
* Typing `solve 0, 1, 3` will run QAOA on a sub-problem defined by regions 0, 1, and 3.

## Our experience at MIT iQuHack 2022

The iQuHACK 2022 was an amazing experience for the team. It allowed us to learn
more about quantum computing, how to work as a team, and tackle a fast-paced
project. We were a team of 5 people that didn’t know each other beforehand, but
by a complete coincidence it turned out that most of us were actually working in
the same town! For us the most exciting part was getting our game to work and
then successfully running it on an actual quantum device. Only slightly negative point of the experience has been on the long queuing times for accessing both the simulator and the real qpu of the ionq backend. However, this event ended up
being a perfect way to learn more about quantum computing, meet motivated,
like-minded people that we could collaborate with in the future.

