from networkx import DiGraph
import networkx as nx
from vrpy import VehicleRoutingProblem
import matplotlib.pyplot as plt

G = DiGraph()

# G.add_edge("Source", 1, cost=1)
# G.add_edge("Source", 2, cost=2)
# G.add_edge(1, "Sink", cost=0)
# G.add_edge(2, "Sink", cost=2)
# G.add_edge(1, 2, cost=1)

#mixed fleet
G.add_edge("Source", 1, cost=[1, 2])
G.add_edge("Source", 2, cost=[2, 4])
G.add_edge(1, "Sink", cost=[0, 0])
G.add_edge(2, "Sink", cost=[2, 4])
G.add_edge(1, 2, cost=[1, 2])
prob = VehicleRoutingProblem(G, mixed_fleet=True, load_capacity=[10, 15])

#customer demand
# G.nodes[1]["demand"] = 2
# G.nodes[2]["demand"] = 3

#vrp time constraint (time for each edges)
# G.edges["Source",1]["time"] = 5
# G.edges["Source",2]["time"] = 4
# G.edges[1,2]["time"] = 2
# G.edges[1,"Sink"]["time"] = 2
# G.edges[2,"Sink"]["time"] = 1

#time window
# G.nodes[1]["lower"] = 0
# G.nodes[1]["upper"] = 10
# G.nodes[2]["lower"] = 5
# G.nodes[2]["upper"] = 9
# G.nodes[1]["service_time"] = 1
# G.nodes[2]["service_time"] = 2

#Simultaneous Distribution and Collection
# G.nodes[1]["collect"] = 2           #set amount to picked
# G.nodes[2]["collect"] = 1    

#pickup and delivery (pickup +,delivery -)
# G.nodes[1]["request"] = 2
# G.nodes[1]["demand"] = 3
# G.nodes[2]["demand"] = -3

#periodic
# G.nodes[1]["frequency"] = 2


# prob = VehicleRoutingProblem(G, load_capacity=10) #main
# prob.duration = 9      # set maximun time per vehicle
# prob.num_stops = 1     # set maximum number of customers per trip
# prob.time_windows = True 
# prob.load_capacity = 10
# prob.distribution_collection = True
# prob.pickup_delivery = True
# prob.periodic = 2
# prob.solve(cspy=False)
prob.solve()



print("prob.best_value : ", prob.best_value)                   # best overall cost solution
print("prob.best_routes : ",prob.best_routes)                  # best path
print("prob.best_routes_load : ",prob.best_routes_load)        # sum of customer demand
nx.draw(G,with_labels=1)
plt.show()
