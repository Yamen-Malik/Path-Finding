import time
found_path = False
on_checking_event = []
on_visited_event = []
on_surrounding_check_event = []
def UpdateSurrounding(node_list, start_node, end_node, delay_time, nodes_to_scan = None):
	"""
		Takes a list of nodes and update the surrounding nodes values\n
		Get Surrounding nodes, update them, store them an a list, call the function again for the list
	"""
	global found_path
	if nodes_to_scan == None:
		found_path = False
		nodes_to_scan = [start_node]

	total_surroundings = set()
	time.sleep(delay_time)
	for current_node in nodes_to_scan:
		# surroundings = [nodes_to_scan[node.column+1][node.row], nodes_to_scan[node.column-1][node.row], nodes_to_scan[node.column][node.row+1], nodes_to_scan[node.column][node.row-1]]
		surroundings = set(map(lambda x: node_list[x[0]][x[1]],
							filter(lambda x: x[0] >= 0 and x[0] < len(node_list) and x[1] >= 0 and x[1] < len(node_list[0]),
									set(((current_node.column+1, current_node.row), (current_node.column-1, current_node.row), (current_node.column, current_node.row+1), (current_node.column, current_node.row-1))))))
		to_remove = set()  # Stores the nodes that shouldn't get updated and delete them after the loop (like obstacles, already updated nodes, etc..)
		for surrounding_node in surroundings:
			if surrounding_node == start_node or surrounding_node.is_obstacle:
				to_remove.add(surrounding_node)
				continue
			elif surrounding_node == end_node:
				found_path = True
				return TrackBack(current_node, start_node)
				return
			elif surrounding_node.distance_from_start == float("inf"):
				surrounding_node.SetDistance(current_node.distance_from_start+1)
				CallEvent(on_checking_event, surrounding_node)
				#// surrounding_node.ChangeColor(colors.NodeColors.cheking.value)
				surrounding_node.previous_node = current_node
			else:
				to_remove.add(surrounding_node)
		surroundings.difference_update(to_remove)
		total_surroundings.update(surroundings)
	for node in nodes_to_scan:
		if node != start_node:
			CallEvent(on_visited_event, node)
			#// node.ChangeColor(colors.NodeColors.visited.value)
	CallEvent(on_surrounding_check_event, None)
	if not total_surroundings == set():
		return UpdateSurrounding(node_list, start_node, end_node, delay_time, total_surroundings)
	elif not found_path:
		print("couldn't find a path")


def TrackBack(node, start_node):
	track_list = [node]
	last_node = node
	while True:
		last_node = last_node.previous_node
		if start_node == last_node:
			# for i in track_list:
				# i.ChangeColor(colors.NodeColors.path.value)
			return track_list[::-1]
		else:
			track_list.append(last_node)

def CallEvent(event, paramater):
	for function in event:
		if paramater == None:
			function()
		else:
			function(paramater)