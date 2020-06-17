import pygame, colors

rect_size = None
font = None
class NodeGenerator():
	def __init__(self, rect_size_, font_):
		global rect_size, font
		rect_size = rect_size_
		font = font_
	def UpdateRectSize(self, new_size):
		global rect_size
		rect_size = new_size
	def get_rect_size(self):
		return rect_size
	class Node:
		def __init__(self, screen, position, column, row, color = colors.NodeColors.normal.value):
			self.screen = screen
			self.grid_position = self.column, self.row = column, row
			self.position = position								# Position in pixels
			self.distance_from_start = float("inf")		# If this value = infinity that means it hasn't been updated yet
			self.previous_node = None					# The node that updated this node (this help us to track back our path)
			self.is_obstacle = False					# Defines whether the node blocks the path or not (True = blocks the path)
			self.color = color
		
		def Draw(self, color = None):
			if color == None:
				color = self.color
			if self.position[0] > self.screen.get_width() or self.position[1] > self.screen.get_height():
				return
			pygame.draw.rect(self.screen, color, pygame.Rect(self.position[0], self.position[1], rect_size[0], rect_size[1]))
			if self.distance_from_start not in (float("inf"), 0) and rect_size[0] >= 25:
				self.screen.blit(font.render(str(self.distance_from_start), True, colors.NodeColors.text.value), (self.position[0]+(rect_size[0]/2), self.position[1]+(rect_size[1]/2 -5)))
			
		def ChangeColor(self, new_color):
			self.color = new_color
			self.Draw(new_color)

		def SetDistance(self, distance):
			"""
				Sets the distance from the start node to this node
			"""
			self.distance_from_start = distance
			self.ChangeColor(colors.NodeColors.visited.value)
