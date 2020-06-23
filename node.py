import pygame, colors
pygame.init()
font = pygame.font.SysFont("arial", 10)
font_size = 10
class NodeGenerator():
	rect_size = None
	weight_image = None
	screen = None
	def __init__(self, screen_, rect_size_, weight_image_):
		global screen, rect_size, weight_image
		screen = screen_
		rect_size = rect_size_
		# font = font_
		weight_image = weight_image_
	def UpdateRectSize(self, new_size):
		global rect_size, font, font_size
		rect_size = new_size
		font_size = int(rect_size[0] / 2.5)
		font = pygame.font.SysFont("arial", font_size)

	class Node:
		def __init__(self, position, column, row, cost = 1, color = colors.NodeColors.normal.value):
			self.column, self.row = column, row
			self.position = position								# Position in pixels
			self.distance_from_start = float("inf")		# If this value = infinity that means it hasn't been updated yet
			self.distance_from_end = float("inf")
			self.total_distance = float("inf")
			self.previous_node = None					# The node that updated this node (this help us to track back our path)
			self.is_obstacle = False					# Defines whether the node blocks the path or not (True = blocks the path)
			self.is_weight = False
			self.color = color
			self.cost = cost
		
		def Draw(self, color = None):
			"""
				Draws the node with the given the color
				color: if the value us None then the node color will be used (Default = False)
			"""
			if color == None:
				color = self.color
			#If the node isn't in the screen don't draw it
			if self.position[0] > screen.get_width() or self.position[1] > screen.get_height():
				return
			pygame.draw.rect(screen, color, pygame.Rect(self.position[0], self.position[1], rect_size[0], rect_size[1]))
			if self.is_weight:
				image = pygame.image.load(weight_image)
				image = pygame.transform.scale(image, (int(image.get_width() * (rect_size[0]/100)), int(image.get_height() *(rect_size[1]/100))))
				screen.blit(image, (self.position[0] + (rect_size[0] - image.get_width())/2, (self.position[1] + (rect_size[1] - image.get_height())/2)))
			
			if rect_size[0] >= 25:
				if self.distance_from_start not in (0, float("inf")):
					# screen.blit(font1.render(str(self.distance_from_start), True, colors.General.text.value), (self.position[0], self.position[1]+(rect_size[1]) - 10))
					screen.blit(font.render(str(self.distance_from_start), True, colors.General.text.value), (self.position[0], self.position[1]+(rect_size[1]) - font_size))
				if self.distance_from_end not in (0, float("inf")):
					# screen.blit(font1.render(str(self.distance_from_end), True, colors.General.text.value), (self.position[0] + rect_size[0] - 10, self.position[1]+ rect_size[1]) - 10)
					screen.blit(font.render(str(self.distance_from_end), True, colors.General.text.value), (self.position[0] + rect_size[0] - font.size(str(self.distance_from_end))[0], self.position[1]))
					# screen.blit(font1.render(str(self.distance_from_end), True, colors.General.text.value), (self.position[0] + rect_size[0] - font1.size(self.distance_from_end), self.position[1] - font_size))
				if self.total_distance not in (0, float("inf")):
					# screen.blit(font.render(str(self.total_distance), True, colors.General.text.value), (self.position[0]+(rect_size[0]/3), self.position[1]+(rect_size[1]/3)))
					screen.blit(font.render(str(self.total_distance), True, colors.General.text.value), (self.position[0], self.position[1]))

			# if self.distance_from_start not in (0, float("inf")) and rect_size[0] >= 25:
			# 	if self.total_distance == float("inf"):
			# 		screen.blit(font.render(str(self.distance_from_start), True, colors.General.text.value), (self.position[0]+(rect_size[0]/3), self.position[1]+(rect_size[1]/3)))
			# 	else:
			# 		screen.blit(pygame.font.SysFont("arial", 9).render(str(self.distance_from_start), True, colors.General.text.value), (self.position[0], self.position[1]+(rect_size[1]) - 10))
			# 		screen.blit(font.render(str(self.total_distance), True, colors.General.text.value), (self.position[0]+(rect_size[0]/3), self.position[1]+(rect_size[1]/3)))

		def ChangeColor(self, new_color):
			"""
				Changes the node color to the given color and draw the node
			"""
			self.color = new_color
			self.Draw(new_color)
		def SetToWeighted(self, cost):
			"""
				Set the values that will make this node a weight node
			"""
			self.is_weight = True
			self.cost = cost
			self.Draw()
		def SetToObstacle(self):
			"""
				Set the values that will make this node a obstacle node
			"""
			self.Reset()
			self.is_obstacle = True
			self.ChangeColor(colors.NodeColors.obstacle.value)
		def ResetDistances(self):
			self.distance_from_start = float("inf")
			self.distance_from_end = float("inf")
			self.total_distance = float("inf")
		def Reset(self):
			"""
				Resets the node to the default values
			"""
			self.ResetDistances()
			self.is_obstacle = False
			self.is_weight = False
			self.cost = 1
			self.ChangeColor(colors.NodeColors.normal.value)
