# DijkstrasAlg
## Program Report

For this assignment, I was tasked with computing the max capacity of a simplified NAS
model. The max amount of people who travel from LAX to JFK either by a direct flight or
multiple flight hopping was to be calculated and maximized. This is extremely similar to the
max flow problem but has a temporal aspect where the time of flights’ departure and arrival
matter. This added a restriction where the arrival time of a passenger must be less than the
departure time of the desired departure for them to board the flight.
In the program, a flight object is created to store the flight information such as: start city,
destination city, departure time, arrival time, and passenger capacity. The main of the program
first calls parseFile() which extracts tokens of information and creates a flight object for each
line in the text file. This function also adds all flights to a flight array initialized and passed by
main.

Next in main, an adjacency matrix is initialized, and each flight is analyzed. Every flight
is hashed into an integer based on departure city and departure time into variable x and arrival
city and arrival time into variable y. This incorporates the temporal and spatial aspects into a
single integer that can be easily analyzed. Variables x and y are compared and if they are a flight
from LAX to JFK, their capacity is automatically added to the total as it is a direct flight.
Otherwise, the flight [x][y] is added to the adjacency matrix with its capacity as its value. After
all flights have been evaluated and the adjacency matrix has been completed, the matrix is then
traversed to ensure that travel to the same city does not occur. This is done by comparing the
hash values of x and y and if the conditions are met, their value in the matrix is set to infinity.

Finally, the function FordFulkerson() is called to compute the maximum flow of
multiflight paths. The algorithm uses firstly a queue to store adjacent cities to be evaluated,
starting with LAX. Lists of visited and parent nodes are initialized as well. While the sink has
not been visited, the algorithm evaluates nodes in the queue. It then loops through the graph to
find adjacent nodes via breadth first search and mark them as visited as well as maintain which
node is their parent. After a path is found, the minimum flow or bottleneck of the path is
calculated. After the minimum is found the flow of the path and the capacity are updated and the
algorithm repeats. Once all augmenting paths are found, the max flow of the multi-hop flights
are returned to main, added to the max flow of direct flights, and printed to the user.
The max flow that I found using my algorithm is 8727. This was using a Python program
using version 3.10.2.
