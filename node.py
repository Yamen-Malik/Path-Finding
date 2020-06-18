import pygame, colors

rect_size = None
font = None
weight_image = None
class NodeGenerator():
	def __init__(self, rect_size_, font_, weight_image_):
		global rect_size, font, weight_image
		rect_size = rect_size_
		font = font_
		weight_image = weight_image_
	def UpdateRectSize(self, new_size):
		global rect_size
		rect_size = new_size
	class Node:
		def __init__(self, screen, position, column, row, cost = 1, color = colors.NodeColors.normal.value):
			self.screen = screen
			self.grid_position = self.column, self.row = column, row
			self.position = position								# Position in pixels
			self.distance_from_start = float("inf")		# If this value = infinity that means it hasn't been updated yet
			self.total_distance = float("inf")
			self.previous_node = None					# The node that updated this node (this help us to track back our path)
			self.is_obstacle = False					# Defines whether the node blocks the path or not (True = blocks the path)
			self.is_weighted = False
			self.color = color
			self.cost = cost
		
		def Draw(self, color = None):
			if color == None:
				color = self.color
			if self.position[0] > self.screen.get_width() or self.position[1] > self.screen.get_height():
				return
			pygame.draw.rect(self.screen, color, pygame.Rect(self.position[0], self.position[1], rect_size[0], rect_size[1]))
			if self.is_weighted:
				image = pygame.image.load(weight_image)
				image = pygame.transform.scale(image, (int(image.get_width() * (rect_size[0]/100)), int(image.get_height() *(rect_size[1]/100))))
				self.screen.blit(image, (self.position[0] + (rect_size[0] - image.get_width())/2, (self.position[1] + (rect_size[1] - image.get_height())/2)))
			
			if self.distance_from_start != 0:
				if self.distance_from_start not in (float("inf"), 0) and rect_size[0] >= 25:
					if self.total_distance == float("inf"):
						self.screen.blit(font.render(str(self.distance_from_start), True, colors.NodeColors.text.value), (self.position[0]+(rect_size[0]/3), self.position[1]+(rect_size[1]/3)))
					else:
						self.screen.blit(pygame.font.SysFont("arial", 9).render(str(self.distance_from_start), True, colors.NodeColors.text.value), (self.position[0], self.position[1]+(rect_size[1]) - 10))
						self.screen.blit(font.render(str(self.total_distance), True, colors.NodeColors.text.value), (self.position[0]+(rect_size[0]/3), self.position[1]+(rect_size[1]/3)))

		def ChangeColor(self, new_color):
			self.color = new_color
			self.Draw(new_color)
		def SetToWeighted(self, cost):
			self.is_weighted = True
			self.cost = cost
			self.Draw()
		def Reset(self):
			self.distance_from_start = float("inf")
			self.total_distance = float("inf")
			self.is_obstacle = False
			self.is_weighted = False
			self.cost = 1
			self.ChangeColor(colors.NodeColors.normal.value)
