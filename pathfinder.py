import time
found_path = False
diagonal = False
on_checking_event = []
on_finished_event = []
def Dijkstra(node_list, start_node, end_node):
	start_node.distance_from_start = 0
	current_node = start_node   # this list keeps track of the nodes we should check in order (lower distance from start to the higher)
	to_check = []
	while True:
		for surrounding_node in GetSurroundingNodes(node_list, current_node):
			if surrounding_node == end_node:
				return TrackBack(current_node, start_node)
			measured_distance = current_node.distance_from_start + surrounding_node.cost
			if surrounding_node != start_node and not surrounding_node.is_obstacle and surrounding_node.distance_from_start > measured_distance: 
				surrounding_node.distance_from_start = measured_distance
				surrounding_node.previous_node = current_node
				for i in range(len(to_check)):
					if to_check[i].distance_from_start > surrounding_node.distance_from_start:
						to_check.insert(i, surrounding_node)
						break
				if surrounding_node not in to_check:
					to_check.append(surrounding_node)
				CallEvent(on_checking_event, surrounding_node)
		CallEvent(on_finished_event, current_node)
		if to_check == []:
			return
		current_node = to_check.pop(0)

def AStar(node_list, start_node, end_node):
	start_node.distance_from_start = 0
	current_node = start_node
	to_check = []   # this list keeps track of the nodes we should check in order (lower total distance to the higher)
	finished_nodes = set()
	while True:
		# time.sleep(delay_time)
		for surrounding_node in GetSurroundingNodes(node_list, current_node):
			if surrounding_node == end_node:
				end_node.previous_node = current_node
				return TrackBack(end_node, start_node)
			if (not surrounding_node.is_obstacle) and surrounding_node.distance_from_start > (current_node.distance_from_start + surrounding_node.cost):
				surrounding_node.distance_from_start = current_node.distance_from_start +surrounding_node.cost
				surrounding_node.total_distance = surrounding_node.distance_from_start + GetNodeDistance(surrounding_node, end_node)
				surrounding_node.previous_node = current_node
				if surrounding_node not in to_check and surrounding_node not in finished_nodes:
					#Here we are inserting the node to out list (to_check) in the right place by doing this we won't need to sort the list
					# Beacuse our insertation isn't random
					for i in range(len(to_check)):
						if to_check[i].total_distance >= surrounding_node.total_distance :
							to_check.insert(i, surrounding_node)
							break
					if surrounding_node not in to_check:
						to_check.append(surrounding_node)
					CallEvent(on_checking_event, surrounding_node)
					
		CallEvent(on_finished_event, current_node)
		finished_nodes.add(current_node)
		if to_check == []:
			return
		current_node = to_check.pop(0)

def GreedyBFS(node_list, start_node, end_node):
	start_node.distance_from_start =  0
	current_node = start_node
	to_check = []  # this list keeps track of the nodes we should check in order (lower distance from end to the higher)
	while True:
		for surrounding_node in GetSurroundingNodes(node_list, current_node):
			if surrounding_node == end_node:
				return TrackBack(current_node, start_node)
			if not surrounding_node.is_obstacle and surrounding_node.distance_from_end == float("inf"):
				surrounding_node.distance_from_end = GetNodeDistance(surrounding_node, end_node)
				surrounding_node.previous_node = current_node
				CallEvent(on_checking_event, surrounding_node)
				for i in range(len(to_check)):
					if to_check[i].distance_from_end > surrounding_node.distance_from_end:
						to_check.insert(i, surrounding_node)
						break
				if surrounding_node not in to_check:
					to_check.append(surrounding_node)
		CallEvent(on_finished_event, current_node)
		if to_check == []:
			return
		current_node = to_check.pop(0)

def TrackBack(node, start_node):
	"""
		Goes all the way back from a certain node to the start node and return the path
		*previous_node should be implemented for each node
	"""
	track_list = [node]
	last_node = node
	if node == start_node:
		return start_node
	while True:
		last_node = last_node.previous_node
		if start_node == last_node:
			return track_list[::-1]
		else:
			track_list.append(last_node)
def GetSurroundingNodes(node_list, node):
	"""
		Returns all surrounding nodes without going out of node_list range
	"""
	surroundings = [(node.column, node.row-1), (node.column+1, node.row),(node.column, node.row+1), (node.column-1, node.row)]
	if diagonal:
		surroundings += [(node.column+1, node.row+1), (node.column+1, node.row-1), (node.column-1, node.row-1), (node.column-1, node.row+1)]
	
	#Here we filter the surroundings to make sure that we don't go out of the list range
	return list(map(lambda x: node_list[x[0]][x[1]],
                        filter(lambda x: x[0] >= 0 and x[0] < len(node_list) and x[1] >= 0 and x[1] < len(node_list[0]), surroundings)))
def GetNodeDistance(node, target):
	"""
		Returns the distance from the given node the the given target
	"""
	return abs(node.column - target.column) + abs(node.row - target.row)
def CallEvent(event, parameter = None):
	"""
		Call all the given event subscribers and pass the given parameter to them
			parameter: None = no parameters (Default = None)
	"""
	for function in event:
		if parameter == None:
			function()
		else:
			function(parameter)
def GetIsWeighted(algorithm):
	"""
		Returns whether the algorithm is Weighted or not
	"""
	if algorithm in [Dijkstra, AStar]:
		return True
	else:
		return False