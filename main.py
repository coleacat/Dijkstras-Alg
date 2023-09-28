from queue import Queue
n = 194         #size for adjacency matrix
INF = 1000      #infinity

# Flight object
class Flight:
    # Initialize the Flight object with the given attributes
    def __init__(self, start, sink, depart, arrival, capacity):
        self.start = start
        self.sink = sink
        self.depart = depart
        self.arrival = arrival
        self.capacity = capacity

    def getString(self):
        print(f"{self.start} {self.sink} {self.depart} {self.arrival} {self.capacity}")

    def getStart(self):
        return self.start

    def getSink(self):
        return self.sink

    def getDepart(self):
        return self.depart

    def getArrival(self):
        return self.arrival

    def getCapacity(self):
        return self.capacity


# Open input and parse the data in flight objects
def parseFile(name, arr):
    with open(name, 'r') as file:
        for line in file:
            # Split the line into tokens
            tokens = line.split()

            # Extract the values of the tokens
            start = tokens[0]
            sink = tokens[1]
            depart = int(tokens[2])
            arrival = int(tokens[3])
            capacity = int(tokens[4])

            # Create Flight object with the extracted values
            flight = Flight(start, sink, depart, arrival, capacity)

            # Add the Flight object to the flight list
            arr.append(flight)
    file.close() # Close the file like a good little programmer

# Hash the airport name and time into a number to create vertices that account for time
def hash(name, t):
    if name == "LAX":
        return 0
    elif name == "SFO":
        return 1 + t
    elif name == "PHX":
        return 25 + t
    elif name == "SEA":
        return 49 + t
    elif name == "DEN":
        return 73 + t
    elif name == "ATL":
        return 97 + t
    elif name == "ORD":
        return 121 + t
    elif name == "BOS":
        return 145 + t
    elif name == "IAD":
        return 169 + t
    else:   #JFK
        return 193

# Ford-Fulkerson algorithm with BFS
def FordFulkerson(flow, start, sink):
    result = 0
    while True:
        # Queue of vertices to evaluate
        q = Queue()
        q.put(start)
        # Initialize list of visited vertices in current augmenting path
        visited = [-1] * n 
        # Initialize list of parent nodes in current augmenting path
        parent = [-1] * n
        while not q.empty():
            x = q.get()
            for i in range(n):
                # If the from x to i is greater than zero and i has not been visited yet
                if flow[x][i] > 0 and visited[i] == -1:
                    q.put(i)        # Queue vertex i
                    parent[i] = x   # Set x as vertex i's parent
                    visited[i] = x  # Add i to list of visited nodes
        if visited[sink] == -1: # Break the loop if we visit JFK
            break
        # Set pathFlow to 1000 to find the min flow in the augmenting path
        pathFlow = INF
        y = sink
        # Find the min flow of the path
        while y != start:
            x = parent[y]
            pathFlow = min(pathFlow, flow[x][y])
            y = visited[y]
        y = sink
        # Subtract the bottle neck from forward edges and add it to back edges
        while y != start:
            x = parent[y]
            flow[x][y] -= pathFlow
            flow[y][x] += pathFlow
            y = visited[y]
        result += pathFlow
    # Return the max flow
    return result
    

def main():
    # Array to store flights
    flight = []
    name = "flights.txt"
    # Extract data
    parseFile(name, flight)

    # Variable for direct flight capacity and array size [n][n] for adjacency matrix initialized at 0
    direct = 0
    adjacencyMatrix = [[0 for i in range(n)] for j in range(n)]

    # Loop through all flights
    for i in range(len(flight)):
        # Hash the starting city and departure time to x
        x = hash(flight[i].getStart(), flight[i].getDepart())
        # Hash the destination city and arrival time to y
        y = hash(flight[i].getSink(), flight[i].getArrival())

        # If the flight is from LAX to JFK add its capacity to direct
        if x == 0 and y == n - 1:
            direct = direct + flight[i].getCapacity()
        else:
            # If the flight is a multi-hop flight add its capacity to the flow matrix
            adjacencyMatrix[x][y] = adjacencyMatrix[x][y] + flight[i].getCapacity()

    # Loop through the flow matrix and set the flow between airports that are in the same city to infinity to avoid travel to the same city
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if i < j:
                if (((i > 0 and j > 0) and (i < 25 and j < 25)) or ((i > 24 and j > 24) and (i < 49 and j < 49))
                        or ((i > 48 and j > 48) and (i < 73 and j < 73)) or (
                                (i > 72 and j > 72) and (i < 97 and j < 97))
                        or ((i > 96 and j > 96) and (i < 121 and j < 121)) or (
                                (i > 120 and j > 120) and (i < 145 and j < 145))
                        or ((i > 144 and j > 144) and (i < 169 and j < 169)) or (i > 168 and j > 168)):
                    adjacencyMatrix[i][j] = INF

    # Compute max flow + direct flow
    result = FordFulkerson(adjacencyMatrix, 0, n - 1) + direct

    # Print the maximum flow
    print(result)

if __name__ == "__main__":
    main()