# Playing with QAOA

<p align="left">
  <a href="https://azure.microsoft.com/en-us/solutions/quantum-computing/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488491-609828a4-cd1f-4076-b5b2-a8d9fc2d0fa4.png" width="30%"/> </a>
  <a href="https://ionq.com/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488159-da95eb05-9277-4abe-b1ba-b49871d563ed.svg" width="20%" style="padding: 1%;padding-left: 5%"/></a>
  <a href="https://iquhack.mit.edu/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151647370-d161d5b5-119c-4db9-898e-cfb1745a8310.png" width="8%" style="padding-left: 5%"/> </a>
</p>

This repo contains our solutions to IonQ + Microsoft Joint Challenge @ MIT iQuHACK 2022.

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

... Interested? Read more [here](paper.pdf).

## Submitting your projects
To submit your solutions:
1. Fork this repository to your GitHub account.
2. Commit your project to your forked repository.  
Include any files you consider relevant: the project itself, README including the description of the project and instructions on running the project, screenshots of results, any visualizations you've done, your project presentation, etc.
3. To submit your project, submit the link to your repository as detailed on https://iquhack.mit.edu/.
Your repository has to be made public at the time of the Hackathon end for us to be able to judge your solutions. We don't recommend making your work public early during the Hackathon, so as not to tempt other teams to borrow from your work. Let everybody enjoy their exploration!
*Note that GitHub doesn't allow to change visibility of the forks. You can either fork the repository, keep it public, and push your changes at the last possible moment, or you can duplicate the repository, make it private to work on it during the Hackathon, and make it public at the end of the Hackathon.*
4. If you want to write a blog post about your project, publish it shortly after the Hackathon ends and add a link to it to your GitHub repository.

## Judging

We'll be evaluating the projects based on several criteria, as detailed in this **rubric:** 

https://docs.google.com/document/u/1/d/e/2PACX-1vR5PVoInN_Fi42lIOchhblgGBPblgNyouj1XHukonZ4sdqY-p5ulS9TxdzvddEcDNFc5k_6teFyKzXv/pub

## Eligibility and prizes
The (1) highest team score will receive a **$500 Visa Gift Card** (physical or virtual) for the team. The next (4) highest team scores will receive a **$250 Visa Gift Card** (physical or virtual) for the team. The (5) winning teams will have an opportunity to present their projects to the Microsoft Quantum Team at a later date and time (to be scheduled after the results announcement).

Government officials and Microsoft employees are not eligible to participate in this challenge.

For the general rules on eligibility and hackathon participation, please refer to the [official rules](http://iquhack.mit.edu/).

## Resources

### Microsoft Quantum Development Kit installation

For this Hackathon, you have several options of setting up the QDK:

* local setup: you'll need the [standalone QDK](https://docs.microsoft.com/en-us/azure/quantum/install-command-line-qdk), and possibly (depending on what kind of project you decide to do) integration with [Q# Jupyter Notebooks](https://docs.microsoft.com/en-us/azure/quantum/install-jupyter-qkd) and/or with [Python](https://docs.microsoft.com/en-us/azure/quantum/install-python-qdk).
* qBraid: you can use qBraid virtual environment to develop your project. Here are the tutorials on how to [use Q# with qBraid](https://www.youtube.com/watch?v=E5JH1YfqSos) and [submit Azure Quantum jobs with qBraid](https://www.youtube.com/watch?v=WLAAqsqlYb8).
* Azure Portal: you can use the hosted notebooks experience to run code directly from Azure Portal.

### Documentation and tutorials

* [Azure Quantum and QDK documentation](https://docs.microsoft.com/quantum).
* [The Quantum Katas](https://github.com/Microsoft/QuantumKatas/) - a collection of tutorials and practice problems.
* Microsoft Learn learing path ["Quantum computing foundations"](https://docs.microsoft.com/learn/paths/quantum-computing-fundamentals/).
* [Q# developer blog](https://devblogs.microsoft.com/qsharp/).
* Azure Fridays episode [Quantum programming with Q# and running on hardware with Azure Quantum](https://www.youtube.com/watch?v=c9Df90CVHkc) shows the end-to-end quantum software development process with the QDK tools.

## Our experience at QuHack 2022

The QuHACK 2022 was an amazing experience for the team. It allowed us to learn
more about quantum computing, how to work as a team, and tackle a fast-paced
project.  We were a team of 5 people that didn’t know each other beforehand, but
by a complete coincidence it turned out that most of us were actually working in
the same town! For us the most exciting part was getting our game to work and
then successfully running it on an actual quantum device. This event ended up
being a perfect way to learn more about quantum computing, meet motivated,
like-minded people that we could collaborate with in the future.

