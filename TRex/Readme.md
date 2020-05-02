# T-Rex game with NEAT solver

In this project i recreated the famous Chrome T-Rex game using pygame, and solved it using NEAT (the genetic algorithm). After a few tries, it takes 9 inputs:
- The four main distances between dino and first obstable (front, back, up, down)
- Same for second obstacle
- Speed

A few funny things were to notice:
- Having the four inputs for the second obstacle made it really more confusing for the first generations and made them much less efficient, even if in the end it seemed to improve their reaction with multiple obstacles coming in a row
- The way they deal with birds really seems conditionned to the altitude of the birds they meet in the first generations. 
- The scoring system can have side effects if not thought thouroughly. For example i tried to penalize the fact that T-Rexs jump too much. This seems  to work well but at first the malus for that was too high and dinosaurs preferred to crash into cactus instead of risking disappointing me :(

Anyway it was a fun project. A video of the result can be found here:
https://www.youtube.com/watch?v=0EJp1UplOqM
