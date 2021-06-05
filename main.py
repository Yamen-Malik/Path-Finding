import pygame, sys, time, node, pathfinder, colors, os, time
from node import NodeTypes

#Grid
rect_size = [25, 25]  			# The rectangle size *In pixels
columns, rows = 0, 0  # Number of columns & rows you want to generate * it will be calculated later
margin = 1						# Margin between each node in Pixels
node_list = []  					# List to contain the all the generated nodes

#Defaults
default_screen_size = (750, 700)
background_color = pygame.Color("gray")
default_start_grid_pos, default_end_grid_pos = (5,5), (15,5)	# X and Y value to the start & end nodes (relitive to the grid not to the screen)
weight_image_path = os.path.abspath("weight.png")
weighted_node_cost = 4
info_panel_size = (500, 130)
minimum_delay = 0.001
maximum_delay = 0.5

#Other
algorithm = pathfinder.Dijkstra	#The algorithm that we are going to use (Default : Dijkstra)
start_node, end_node = None, None
delay_time = minimum_delay			# The time you want to delay between each node update *In Seconds (in other words: speed)
info_text = ""
#This will load the info text from a .txt file
try:
	f = open(os.path.abspath("info.txt"), "r")
	info_text = f.read()
except:
	print("\"info.txt\" is unreachable")


def CreateNode(column, row):
	"""
		Returns a new grid node with the given column and row
	"""
	return node_generator.Node(CalculateNodePosition(column, row), column, row)
def CalculateNodePosition(column, row):
	"""
		Calculates the node position in pixels using it's column, row and the global/public size variable
	"""
	return column*(rect_size[0] + margin), row*(rect_size[1] + margin)
def CalculateRows():
	"""
		Returns the amount of rows that can fit in the screen using the public node	size
	"""
	return round(screen.get_height() / (rect_size[1] + margin))
def CalculateColumns():
	"""
		Returns the amount of rows that can fit in the screen using the public node	size
	"""
	return round(screen.get_width() / (rect_size[0] + margin))
def SetStart(node):
	"""
		Sets the given node as Start Node and resets the last start node to normal (if there is any)
	"""
	global start_node
	if start_node != None:
		start_node.Reset()
	node.Reset()
	node.ChangeColor(colors.NodeColors.start.value)
	start_node = node
def SetEnd(node):
	"""
		Sets the given node as End Node and resets the last end node to normal (if there is any)
	"""
	global end_node
	if end_node != None:
		end_node.Reset()
	node.Reset()
	node.ChangeColor(colors.NodeColors.end.value)
	end_node = node
def ModifyNode(position, new_type):
	"""
		Takes a position on the screen and find the node in that position then updates the node to match the given type
	"""
	x = int(position[0]/(rect_size[0]+margin))
	y = int(position[1]/(rect_size[1]+margin))
	if x >= columns or y >= rows:
		return
	if is_info_panel_drawn:
		DrawNodes()
	node = node_list[x][y]
	if node in (start_node, end_node):
		return
	if new_type == NodeTypes.Start:
		SetStart(node)
	elif new_type == NodeTypes.End:
		SetEnd(node)
	elif new_type == NodeTypes.Obstacle:
		node.SetToObstacle()
	elif new_type == NodeTypes.Weight and not node.is_obstacle:
		node.SetToWeighted(weighted_node_cost)
	elif new_type == NodeTypes.Normal:
		node.Reset()
def Reset(remove_obstacles = False, remove_weight = False):
	"""
		Rsets all the nodes to normal nodes except the start and end nodes
	"""
	global remaining_nodes_to_flip
	remaining_nodes_to_flip = 0
	screen.fill(background_color)
	for column in node_list:
		for node in column:
			if node.is_obstacle:
				if remove_obstacles:
					node.Reset()
				node.Draw()
			elif node.is_weight:
				if remove_weight:
					node.Reset()
				else:
					node.ResetDistances()
					node.ChangeColor(colors.NodeColors.normal.value)
			elif node not in [start_node, end_node]:
				node.Reset()
			else:
				node.ResetDistances()
				node.Draw()
def FillEmptyScreen():
	"""
		Fils the empty part of the screen with more nodes and add them to the public node list
	"""
	global columns, rows, node_list
	needed_columns = CalculateColumns() - columns
	needed_rows = CalculateRows() - rows
	if needed_columns < 0 :
		needed_columns = 0
	if needed_rows < 0:
		needed_rows = 0
	for x in range(needed_columns):
		node_list.append([CreateNode(columns + x, y) for y in range(rows)])
	columns += needed_columns
	for column in node_list:
		for y in range(needed_rows):
			column.append(CreateNode(node_list.index(column), rows + y))
	rows += needed_rows

#This function triggers when the algorithm is checking on certain nodes values
def OnCheking(node):
	"""
		Changes the given node color to the "cheking color" unless it is the start or end node
	"""
	if node in (start_node, end_node):
		return
	node.ChangeColor(colors.NodeColors.cheking.value)

#This function triggers when the algorithm is visiting certain node to check on its neighbor
def OnVisited(node):
	if node in (start_node, end_node):
		return
	node.ChangeColor(colors.NodeColors.visited.value)

	#We don't want to flip too fast because the visualization will be slow
	call_time = time.time()
	while True:			#I didn't use time.sleep here beause it will set pygame as not responding
		if time.time() - call_time >= delay_time:
			pygame.display.flip()
			return
def DrawNodes():
	"""
		Draws all the nodes (that in the public node list) on the main screen
	"""
	screen.fill(background_color)
	for x in node_list:
		for node in x:
			node.position = CalculateNodePosition(node.column, node.row)
			node.Draw()
	global is_info_panel_drawn
	is_info_panel_drawn = False
def DrawInfoPanel():
	"""
		Draws the info panel on the left-down part of the screen using the public info_text and info_panel_size
	"""
	global is_info_panel_drawn
	is_info_panel_drawn = True
	i= 0
	for line in info_text.split("\n"):
		text = font.render(line.replace("\t", "    ").replace("\n", ""), True, colors.General.info_text.value)
		screen.blit(text, (0, screen.get_height() - info_panel_size[1] + 20*i))
		i += 1 
def DrawDelayTime():
	"""
		Draws the delay time text on the left-up part of the screen using the public font
	"""
	text = font.render("delay: " + str(delay_time)[:4] + "s", True, colors.General.info_text.value, colors.General.text.value)
	screen.blit(text, (0,0))
def DrawDuringTime(totalseconds):
	text = font.render("DuringTime: " + str(totalseconds)[:4] + "s", True, colors.General.info_text.value, colors.General.text.value)
	screen.blit(text, (0,23))
def FindPath():
	"""
		Start the algorithm then draw the path
	"""
	if not pathfinder.GetIsWeighted(algorithm):
		Reset(False, True)
	else:
		Reset(False, False)
	path = algorithm(node_list, start_node, end_node)
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
pygame.display.set_caption("Path finding Visualizer")
screen = pygame.display.set_mode(default_screen_size, pygame.RESIZABLE)
node_generator = node.NodeGenerator(screen, rect_size, weight_image_path)
font = pygame.font.SysFont("arial", 20)
pathfinder.on_checking_event.append(OnCheking)
pathfinder.on_finished_event.append(OnVisited)

FillEmptyScreen()
DrawNodes()
DrawInfoPanel()

#Set default start and end nodes
SetStart(node_list[default_start_grid_pos[0]][default_start_grid_pos[1]])
SetEnd(node_list[default_end_grid_pos[0]][default_end_grid_pos[1]])

mouse_down = False
remove_mode = False
draw_mode = NodeTypes.Start
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
			DrawInfoPanel()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 5:
				ZoomOut()
			elif event.button == 4:
				ZoomIn()
			elif event.button == 1:
				mouse_down = True
				ModifyNode(pygame.mouse.get_pos(), draw_mode)
			elif event.button == 3:
				remove_mode = True
				ModifyNode(pygame.mouse.get_pos(), NodeTypes.Normal)
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1: 
				mouse_down = False
			elif event.button == 3:
				remove_mode = False
		#Keyboard input
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				draw_mode = NodeTypes.Start
			elif event.key == pygame.K_e:
				draw_mode = NodeTypes.End
			elif event.key == pygame.K_o:
				draw_mode = NodeTypes.Obstacle
			elif event.key == pygame.K_w:
				draw_mode = NodeTypes.Weight
			elif event.key == pygame.K_r:
				Reset(True, True)
			elif event.key == pygame.K_PERIOD:
				if delay_time < maximum_delay:
					delay_time += 0.01
					print(delay_time)
			elif event.key == pygame.K_COMMA:
				if delay_time > minimum_delay:
					delay_time -= 0.01
					print(delay_time)
			elif event.key == pygame.K_F1:
				DrawInfoPanel()
			elif event.key == pygame.K_1:
				algorithm = pathfinder.Dijkstra
			elif event.key == pygame.K_2:
				algorithm = pathfinder.AStar
			elif event.key == pygame.K_3:
				algorithm = pathfinder.GreedyBFS
			elif event.key == pygame.K_RETURN:
				currentTime=time.time()
				FindPath()
				totalseconds=time.time()-currentTime
				DrawDuringTime(totalseconds)
		#Modify nodes
		elif event.type == pygame.MOUSEMOTION:
			if remove_mode:
				ModifyNode(pygame.mouse.get_pos(), NodeTypes.Normal)
			elif mouse_down:
				ModifyNode(pygame.mouse.get_pos(), draw_mode)
	node_generator.UpdateRectSize(rect_size)
	DrawDelayTime()
	pygame.display.flip()
