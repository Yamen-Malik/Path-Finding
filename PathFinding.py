import pygame, sys, time, node, pathfinder, colors

algorithm = pathfinder.UpdateSurrounding	#The algorithm that we are going to user
default_screen_size = (750, 700)
rect_size = [25, 25]  			# The rectangle size *In pixels
margin = 1						# Margin between each node in Pixels
columns, rows = 0, 0  # Number of columns & rows you want to generate * it will be calculated later
node_list = []  					# List to contain the all the generated nodes
weighted_node_cost = 4
weight_image_path = r"D:\Yamen\Programming folder\Python\Path-Finding\weight.png"
default_start_grid_pos, default_end_grid_pos = (5,5), (15,5)	# X and Y value to the start & end nodes (relitive to the grid not thee screen)
start_node, end_node = None, None
delay_time = 0			# The time you want to delay between each node update *In Seconds (in other words: speed)
info_panel_size = (500, 180)
info_text = " Keyboard bindings: \n Place node mode: \n Start-node: s \t End-node: e \t Obstacle-node: o \n Remove obstacle-node: u \n Reset: r \t Run: return/enter \t Zoom in\\out : mouse scroll\n\n*Click left\\right mouse button on a node after choosing \n a place node to change it"

#Colors
background_color = pygame.Color("gray")
# ?Should I set them here and assign them to the colors calss?
# text_color = pygame.Color("black")
# normal_color = pygame.Color("white")
# path_color = pygame.Color("magenta")
# start_color = pygame.Color("blue")
# end_color = pygame.Color("red")
# obstacle_color = pygame.Color("black")
# visited_color = pygame.Color("purple")
# cheking_color = pygame.Color("cyan")

#Moved
	# cslass Node:
		# def __init__(self, screen, column, row, color = normal_color):
		# 	self.screen = screen
		# 	self.grid_position = self.column, self.row = column, row
		# 	# self.position = self.CalculatePosition()								# Position in pixels
		# 	self.distance_from_start = float("inf")		# If this value = infinity that means it hasn't been updated yet
		# 	self.previous_node = None					# The node that updated this node (this help us to track back our path)
		# 	self.is_obstacle = False					# Defines whether the node blocks the path or not (True = blocks the path)
		# 	self.color = color

		# def CalculatePosition(self):
		# 	"""
		# 		Calculates the node position in pixels
		# 	"""
		# 	self.position = self.column*(rect_size[0] + margin), self.row*(rect_size[1] + margin)
			
		# def Draw(self, color = None):
		# 	if color == None:
		# 		color = self.color
		# 	self.CalculatePosition()
		# 	pygame.draw.rect(self.screen, color, pygame.Rect(self.position[0], self.position[1], rect_size[0], rect_size[1]))
		# 	self.DrawNumber()
			
		# def ChangeColor(self, new_color):
		# 	self.color = new_color
		# 	self.Draw(new_color)

		# def SetDistance(self, distance):
		# 	"""
		# 	Sets the distance from the start node to this node
		# 	"""
		# 	self.distance_from_start = distance
		# 	# self.ChangeColor(visited_color)
		# 	self.DrawNumber()
		# 	pygame.display.flip()
		# def DrawNumber(self):
		# 	if self.distance_from_start not in (float("inf"), 0) and rect_size[0] >= 25:
		# 		self.screen.blit(font.render(str(self.distance_from_start), True, text_color), (self.position[0]+(rect_size[0]/2), self.position[1]+(rect_size[1]/2 -5)))
			

	# def UpdateSurrounding(nodes):
	# 	"""
	# 		Takes a list of nodes and update the surrounding nodes values\n
	# 		Get Surrounding nodes, update them, store them an a list, call the function again for the list
	# 	"""
	# 	total_surroundings = set()
	# 	for current_node in nodes:
	# 		# surroundings = [nodes[node.column+1][node.row], nodes[node.column-1][node.row], nodes[node.column][node.row+1], nodes[node.column][node.row-1]]
	# 		surroundings = set(map(lambda x: node_list[x[0]][x[1]], 
	# 							filter(lambda x: x[0] >=0 and x[0] < columns and x[1] >=0 and x[1] < rows, 
	# 									set(((current_node.column+1, current_node.row), (current_node.column-1, current_node.row), (current_node.column, current_node.row+1), (current_node.column, current_node.row-1))))))
	# 		to_remove = set()		#Stores that shouldn't get updated and delete them after the loop (like obstacles, already updated nodes, etc..) 
	# 		for surrounding_node in surroundings:
	# 			time.sleep(delay_time)
	# 			if surrounding_node.grid_position == start_grid_pos or surrounding_node.is_obstacle:
	# 				to_remove.add(surrounding_node)
	# 				continue
	# 			elif surrounding_node.grid_position == end_grid_pos:
	# 				global found_path
	# 				found_path = True
	# 				TrackBack(current_node)
	# 				return
	# 			elif surrounding_node.distance_from_start == float("inf"):
	# 				surrounding_node.SetDistance(current_node.distance_from_start+1)
	# 				surrounding_node.ChangeColor(cheking_color)
	# 				surrounding_node.previous_node = current_node
	# 			else:
	# 				to_remove.add(surrounding_node)
	# 		surroundings.difference_update(to_remove)
	# 		total_surroundings.update(surroundings)
	# 	for node in nodes:
	# 		if node != start_node:
	# 			node.ChangeColor(visited_color)
	# 	if not total_surroundings == set():
	# 		UpdateSurrounding(total_surroundings)
	# 	elif not found_path:
	# 		print("couldn't find a path")
	# def TrackBack(node):
	# 	track_list = [node]
	# 	last_node = node
	# 	while True:
	# 		last_node = last_node.previous_node
	# 		if start_grid_pos == last_node.grid_position:
	# 			for i in track_list:
	# 				i.ChangeColor(path_color)
	# 			return
	# 		else:
	# 			track_list.append(last_node)

def CreateNode(column, row):
	return node_generator.Node(screen, CalculateNodePosition(column, row), column, row)
def CalculateNodePosition(column, row):
	"""
		Calculates the node position in pixels using it's column, row and size
	"""
	return column*(rect_size[0] + margin), row*(rect_size[1] + margin)
def CalculateRows():
	"""
		Calculates the amount of rows that can fit in the screen
	"""
	return round(screen.get_height() / (rect_size[1] + margin))
def CalculateColumns():
	"""
		Calculates the amount of rows that can fit in the screen
	"""
	return round(screen.get_width() / (rect_size[0] + margin))
def SetStart(node):
	"""
		Sets the start node the given node
	"""
	global start_node
	if start_node != None:
		start_node.Reset()
	node.ChangeColor(colors.NodeColors.start.value)
	start_node = node
def SetEnd(node):
	"""
		Sets the end node the given node
	"""
	global end_node
	if end_node != None:
		end_node.Reset()
	node.ChangeColor(colors.NodeColors.end.value)
	end_node = node
def SetObstacle(node):
	"""
		Set the given node to an obstacle
	"""
	node.ChangeColor(colors.NodeColors.obstacle.value)
	node.is_obstacle = True
def ModifyNode(position, type):
	"""
		Takes a position on the screen and find the node in that position then updates the node to match the type value
	"""
	x = int(position[0]/(rect_size[0]+margin))
	y = int(position[1]/(rect_size[1]+margin))
	if x >= columns or y >= rows:
		return
	node = node_list[x][y]
	if node in (start_node, end_node):
		return
	if set_mode == "start":
		SetStart(node)
	elif set_mode == "end":
		SetEnd(node)
	elif set_mode == "obstacle":
		SetObstacle(node)
	elif set_mode == "weighted":
		node.is_obstacle = False
		node.SetToWeighted(weighted_node_cost)
	elif set_mode == "remove":
		node.Reset()
def Reset(remove_obstacles = False):
	"""
		Rsets all the nodes to normal nodes except the start and end nodes
	"""
	screen.fill(background_color)
	for x in node_list:
		for node in x:
			if node.is_obstacle or node.is_weighted:
				if remove_obstacles:
					node.Reset()
				elif node.is_weighted:
					node.distance_from_start = float("inf")
					node.total_distance = float("inf")
				node.Draw()
				continue
			elif not node in [start_node, end_node]:
				node.Reset()
			else:
				node.Draw()
def FillEmptyScreen():
	"""
		Fils the emty part of the screen with more nodes
	"""
	global columns, rows, node_list
	needed_columns = CalculateColumns() - columns
	needed_rows = CalculateRows() - rows
	if needed_columns < 0 :
		needed_columns = 0
	if needed_rows < 0:
		needed_rows = 0
	# AddNewNodes(needed_columns, needed_rows)
	for x in range(needed_columns):
		node_list.append([CreateNode(columns + x, y) for y in range(rows)])
	columns += needed_columns
	for column in node_list:
		for y in range(needed_rows):
			column.append(CreateNode(node_list.index(column), rows + y))
	rows += needed_rows
def OnCheking(node):
	if node in (start_node, end_node):
		return
	node.ChangeColor(colors.NodeColors.cheking.value)
def OnVisited(node):
	if node in (start_node, end_node):
		return
	node.ChangeColor(colors.NodeColors.visited.value)
def Flip():
	pygame.display.flip()
#? Sould I use this func?
def AddNewNodes(new_columns, new_rows):
	global columns, rows
	for x in range(new_columns):
		node_list.append([CreateNode(columns + x, y) for y in range(rows)])
	columns += new_columns
	for column in node_list:
		for y in range(new_rows):
			column.append(CreateNode(node_list.index(column), rows + y))
	rows += new_rows


def DrawNodes():
	"""
		Draws all the nodes
	"""
	screen.fill(background_color)
	for x in node_list:
		for node in x:
			node.position = CalculateNodePosition(node.column, node.row)
			node.Draw()
def DrawInfoPanel():
	# info_panel = pygame.Surface(info_panel_size)
	# info_panel.set_alpha(100)
	# info_panel.fill((64,64,64))
	i= 0
	font = pygame.font.SysFont("arial", 20)
	for line in info_text.split("\n"):
		t = font.render(line.replace("\t", "    ").replace("\n", ""), True, pygame.Color("green"))
		# info_panel.blit(t, (0, 20 * i))
		screen.blit(t, (0, screen.get_height() - info_panel_size[1] + 20 *i))
		i += 1 
	#// text = pygame.font.SysFont("arial", 20).render(, True, colors.NodeColors.text.value)
	#// info_panel.blit(font.render("keyboard bindings:\n set start-node: s \t set end-node: e \t set obstacle-node: o \n remove obstacle-node: u \t reset: r \t run: return/enter", True, colors.NodeColors.text), (0, 0))
	#// info_panel.blit(text, (0,0))
	# screen.blit(info_panel, (0, screen.get_height()- info_panel_size[1]))
def FindPath():
	# path = pathfinder.UpdateSurrounding(node_list, start_node, end_node, delay_time)
	path = algorithm(node_list, start_node, end_node, delay_time)
	if path == None:
		return
	for node in path:
		if node in (start_node, end_node):
			continue
		node.ChangeColor(colors.NodeColors.path.value)
def Zoom(multiplier):
	"""
		Changes the rect size by 1/10, creates new nodes if needed
			multiplier: 1 = bigger/zoom in, -1 = smaller, zoom out 
	"""
	global rect_size
	rect_size[0] += multiplier
	rect_size[1] += multiplier
	FillEmptyScreen()
	DrawNodes()
def ZoomIn():
	if rect_size[0] < 396 and rect_size[1] < 296:
		Zoom(1)
def ZoomOut():
	if rect_size[0] > 10 and rect_size[1] > 10:
		Zoom(-1)

pygame.init()
font = pygame.font.SysFont("arial", 12)
node_generator = node.NodeGenerator(rect_size, font, weight_image_path)
screen = pygame.display.set_mode(default_screen_size, pygame.RESIZABLE)

FillEmptyScreen()
DrawNodes()
pathfinder.on_checking_event.append(OnCheking)
pathfinder.on_visited_event.append(OnVisited)

pathfinder.on_surrounding_check_event.append(Flip)

SetStart(node_list[default_start_grid_pos[0]][default_start_grid_pos[1]])
SetEnd(node_list[default_end_grid_pos[0]][default_end_grid_pos[1]])

mouse_down = False
set_mode = "start"
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.VIDEORESIZE:
			if event.size == screen.get_size():
				break
			screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
			FillEmptyScreen()
			DrawNodes()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 5:
				ZoomOut()
			elif event.button == 4:
				ZoomIn()
			else:
				mouse_down = True
				ModifyNode(pygame.mouse.get_pos(), set_mode)
		elif event.type == pygame.MOUSEBUTTONUP: 
			mouse_down = False
		#Keyboard input
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				set_mode = "start"
			elif event.key == pygame.K_e:
				set_mode = "end"
			elif event.key == pygame.K_o:
				set_mode = "obstacle"
			elif event.key == pygame.K_w:
				set_mode = "weighted"
			elif event.key == pygame.K_u:
				set_mode = "remove"
			elif event.key == pygame.K_r:
				Reset(True)
			elif event.key == pygame.K_RETURN:
				Reset()
				FindPath()
		#Mofify nodes
		elif (mouse_down and event.type == pygame.MOUSEMOTION):
			ModifyNode(pygame.mouse.get_pos(), set_mode)
	node_generator.UpdateRectSize(rect_size)
	DrawInfoPanel()
	pygame.display.flip()
