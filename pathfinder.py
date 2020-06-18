import time
found_path = False
diagonal = False
on_checking_event = []
on_visited_event = []
on_surrounding_check_event = []
def UpdateSurrounding(node_list, start_node, end_node, delay_time, nodes_to_scan = None):
	"""
		Takes a list of nodes and update the surrounding nodes values\n
		Get Surrounding nodes, update them, store them an a list, call the function again for the list
	"""
	start_node.distance_from_start = 0
	global found_path
	if nodes_to_scan == None:
		found_path = False
		nodes_to_scan = [start_node]

	total_surroundings = set()
	time.sleep(delay_time)
	for current_node in nodes_to_scan:
		surroundings = GetSurroundingNodes(node_list, current_node)
		to_remove = set()  # Stores the nodes that shouldn't get updated and delete them after the loop (like obstacles, already updated nodes, etc..)
		for surrounding_node in surroundings:
			if surrounding_node == start_node or surrounding_node.is_obstacle:
				to_remove.add(surrounding_node)
				continue
			elif surrounding_node == end_node:
				found_path = True
				return TrackBack(current_node, start_node)
			elif current_node.distance_from_start + surrounding_node.cost < surrounding_node.distance_from_start:
				surrounding_node.distance_from_start = current_node.distance_from_start+surrounding_node.cost
				CallEvent(on_checking_event, surrounding_node)
				surrounding_node.previous_node = current_node
			else:
				to_remove.add(surrounding_node)
		surroundings.difference_update(to_remove)
		total_surroundings.update(surroundings)
	for node in nodes_to_scan:
		if node != start_node:
			CallEvent(on_visited_event, node)
	CallEvent(on_surrounding_check_event, None)
	if not total_surroundings == set():
		return UpdateSurrounding(node_list, start_node, end_node, delay_time, total_surroundings)
	elif not found_path:
		print("couldn't find a path")


def AStar(node_list, start_node, end_node, delay_time):
	start_node.distance_from_start = 0
	start_node.total_distance = GetDistanceFormEnd(start_node, end_node)
	current_node = start_node
	checked_nodes = []
	finished_nodes = set()
	while True:
		time.sleep(delay_time)
		for surrounding_node in GetSurroundingNodes(node_list, current_node):
			if surrounding_node == end_node:
				end_node.previous_node = current_node
				return TrackBack(end_node, start_node)
			if (not surrounding_node.is_obstacle) and surrounding_node.distance_from_start > (current_node.distance_from_start + surrounding_node.cost):
				surrounding_node.distance_from_start = current_node.distance_from_start +surrounding_node.cost
				surrounding_node.total_distance = surrounding_node.distance_from_start + GetDistanceFormEnd(surrounding_node, end_node)
				surrounding_node.previous_node = current_node
				inserted = False
				# print(surrounding_node.distance_from_start)
				if surrounding_node not in checked_nodes and surrounding_node not in finished_nodes:
					for i in range(len(checked_nodes)):
						if checked_nodes[i].total_distance >= surrounding_node.total_distance :
							checked_nodes.insert(i, surrounding_node)
							inserted = True
							break
					if not inserted:
						checked_nodes.insert(len(checked_nodes), surrounding_node)
					CallEvent(on_checking_event, surrounding_node)
		CallEvent(on_visited_event, current_node)

		finished_nodes.add(current_node)
		if len(checked_nodes) == 0:
			return
		current_node = checked_nodes.pop(0)
		CallEvent(on_surrounding_check_event, None)


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
	surroundings = {(node.column+1, node.row), (node.column-1, node.row),(node.column, node.row+1), (node.column, node.row-1)}
	if diagonal:
		surroundings.update({(node.column+1, node.row+1), (node.column+1, node.row-1), (node.column-1, node.row-1), (node.column-1, node.row+1)})
	
	#Here we filter the surroundings to make sure that we don't go out of the list range
	return set(map(lambda x: node_list[x[0]][x[1]],
                        filter(lambda x: x[0] >= 0 and x[0] < len(node_list) and x[1] >= 0 and x[1] < len(node_list[0]), surroundings)))
def GetDistanceFormEnd(node, end_node):
	return abs(node.column - end_node.column) + abs(node.row - end_node.row)
def CallEvent(event, paramater):
	for function in event:
		if paramater == None:
			function()
		else:
			function(paramater)
