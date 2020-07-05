Path Finding Visualizer Project
====================
About the project
-----------------
This project is all about implementing the popular path finding algorithms

In this project I wanted to write the code by my own so I have not looked at any online implementation  
I have just looked at the theory of the path finding algorithms

**Note**: My code isn't the most efficient, if you want to use a proper path finding algorithm look it up online

Requirements
------------
All you need to run this code on you're device is:
1. python
2. pygame library (for the graphics)

About The App
-------------
After you run the code a pygme window will pop up, which will have a basic grid (I drew squares in a for loop)  
you will also find start(blue) and end(red) nodes. In addition to an info panel in the left-down side of the window

### Nodes  
The app contains 5 main node types to use:
* Normal node   (white)
* Start node    (blue)
* End node      (red)
* Obstacle node (black)
* Weight node   (Weight icon)

###Algorithms  
I currently have 3 algorithms:
* Dijkstra
* A*
* Greedy

![Algorithms](https://user-images.githubusercontent.com/60931606/85296377-f7e9f880-b4a9-11ea-9d40-f13fa6a0744c.gif)


Controls
--------
### Drawing nodes  
After choosing the a node type to place, hold the left mouse button and hover over the nodes you want to change  
Use Right mouse button to remove Obstacle and Weight nodes

|Node type|Keyboard key|
|---------|------------|
|  Start  |     S      |
|   End   |     E      |
|Obstacle |     O      |
| Weight  |     W      |

![Obstacle](https://user-images.githubusercontent.com/60931606/85296162-a2155080-b4a9-11ea-995f-2a32abc0a84e.gif)
![Drawing](https://user-images.githubusercontent.com/60931606/85296277-d0932b80-b4a9-11ea-9281-da5740aa237f.gif)


### Running the algorithm  
Choose the algorithm you want to user then press Enter

|Algorithm|Keyboard key|
|---------|------------|
|Dijkstra |     1      |
|   A*    |     2      |
| Greedy  |     3      |

### Other Controls
|  Function  |    Key     |
|------------|------------|
| Reset      |     R      |
|Zoom in/out |Mouse scroll|

Features
--------
1. The ability to Draw nodes
2. The ability to switch beteen the algorithm
3. Obstacle and Weight nodes
4. Control the delay time/speed of the visualization
5. Diagonal move