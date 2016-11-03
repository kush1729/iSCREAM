# iSCREAM
A pacman style arcade game about ice creams

DESCRIPTION OF GAME:
It is an arcade game played in a 17x17 grid, tho the outer perimeter is nonreachable (actual play space is 15x15, and the outer 1st and 17th row and column is just for decoration)
User moves the player (in the form of an ugly mutant ice cream) by the arrow keys.
Basic aim of the game is to collect all fruits in a level and complete all levels to win the game.
There are monsters of varying types (chasing, patrolling, etc) that are out to kill the player. The player should avoid them at all costs. 

Each playing level compulsorily has 2 types of walls: 
1) Normal walls: These are indestructible blocks blue in colour.
2) Ice walls: These are blocks that the player can make or break.
There can be more types of blocks.

PS: Harder to play than it sounds

ABOUT THE CODE:

Uses pygame module of python extensively and also uses the time module mainly to time the levels.

Mostly hardcoding has been avoided but as each level has been designed with a 15x15 playing space it is better that none of the constants/values be messed around with.

All images are either stock images from the net or done in paint. Some have a transparent background and some don't, though it is better that all of them should have a transparent background.
Images should be in the same folder for the program to function properly (throws an error otherwise)
For the blocks, no images have been used, rather it has been drawn using pygame.draw.rect() function.

About The Levels:
Each new level should be of increasing difficulty. If it doesn't feel so then the names of the classes can be changed to swap the levels without throwing an error.
There is a particular format to creating a new class for a new level, which is given as a multiline comment in the code itself.
Creating a new level does not take much time (half hour max) unless a new type of monster or fruit is being created.

For creating a new monster a new class for the monster has to be created. Like creation of new levels, there is again a particular format to doing this.

TO DOs:
 CREATE MORE LEVELS. Current goal is to create at least 15 levels. This is the topmost priority, and there is actually nothing much else to do.

Optional- 
Improve logic of the monsters to make them more effecient. (especially monsters whose movement depends on the location of the player, like chasing monsters etc)
Create interesting new monsters.
Create new fruits that have interesting properties (maybe move around a fixed path etc)
Create new types of blocks, for example a lava block that kills the player but not the monsters.
Maybe create stuff like buttons etc that do certain things to the play area
Improve UI. Decorate the different screens
Also, as of now the game itself doesn't feel ice cream based which ruins the pun-ny title. Possible create a story board that shows the pun in the title.
Improve the instructions page by giving more info related to monsters (though this is not necessary as ignorance of type of monster increases difficulty). Change of controls option could be added.
Improve picture quality (all pictures currently look extremely ugly)





