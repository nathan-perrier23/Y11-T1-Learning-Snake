# imports all required libaries
import pygame
import sys
import os
from pygame.image import load
from pygame.draw import rect
from pygame.font import Font
from pygame.math import Vector2
from pygame import Rect
from random import randint
from segments import SEGMENTS
from data import DATA
from sqlite3 import Error
import socket
import cProfile

# sets the starting colours for the difficulty buttons
BLACK = (0,0,0)
EASY = (27, 206, 25)
MED = (27, 30, 25)
HARD = (254, 6, 0)
BOUND = (0,0,155)
BOUND_TEXT = "BOUNDARIES OFF" # sets the boundries text to OFF

class SNAKE:  # creates a class called 'SNAKE'
	def __init__(self): 
		self.reset()
		self.adding_segments = False
  
	def set_img(self):
     
		# set's the different orientations for the head as variables
  
		self.head_up = load('Graphics/head_up.png').convert_alpha()
		self.head_down = load('Graphics/head_down.png').convert_alpha()
		self.head_right = load('Graphics/head_right.png').convert_alpha()
		self.head_left = load('Graphics/head_left.png').convert_alpha()
  
		# set's the different orientations for the head as variables
		
		self.tail_up = load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = load('Graphics/tail_left.png').convert_alpha()

		# set's the different orientations for body as variables

		self.body_vertical = load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = load('Graphics/body_horizontal.png').convert_alpha()

		# set's the different corners for the body as variables 

		self.body_tr = load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = load('Graphics/body_tl.png').convert_alpha()
		self.body_br = load('Graphics/body_br.png').convert_alpha()
		self.body_bl = load('Graphics/body_bl.png').convert_alpha()

		# put's the snakes segemnt images into a list 
  
		self.segments = [self.head_up, self.head_down, self.head_right, self.head_left,self.tail_up ,self.tail_down,self.tail_right,self.tail_left ,self.body_vertical ,self.body_horizontal ,self.body_tr ,self.body_tl ,self.body_br,self.body_bl]
		
	def colour(self):
		if self.celebrate == True: # if celebrate is True
			for index,segment in enumerate(self.segments):	# for every segment in the segments list enumerate two variables, index and the segment
				self.coloured_segment = SEGMENTS.colorize(segment, self.colours) # colour the segment to the new dedicated colour
				self.segments[index] = self.coloured_segment # replace the old segment with the coloured one
			self.celebrate = False # set celebrate to false

	def draw_snake(self):
     
		self.update_head_graphics(),self.update_tail_graphics() # get the direction of the head and tail
		
		for index,block in enumerate(self.body):  # for every element in self.body (snake's body) enumerate the elements (segments) in  the list with a corresponding index
			x_pos = int(block.x * cell_size) #  set's the x position of the snake to the integer of the multiplication of the x value of block and the cell_size
			y_pos = int(block.y * cell_size) #  set's the y position of the snake to the integer of the multiplication of the y value of block and the cell_size
			block_rect = Rect(x_pos,y_pos,cell_size,cell_size) # creats a rectangle with the parameters of the x,y values and the dimensions of each cell (block)

			if index == 0: screen.blit(self.head,block_rect) # finds the head of the snake and draws the head of the snake
			elif index == len(self.body) - 1: screen.blit(self.tail,block_rect) #  finds the tail of the snake (the last part/segment) and draws the tail of the snake
			else: # for every other body part 
				previous_block = self.body[index + 1] - block #  set's a previous block by adding to the current index in the loop and subtracting the block to get the last block
				next_block = self.body[index - 1] - block #  set's the previous block by subtracting 1 from the current index and subracting the block
				if previous_block.x == next_block.x: screen.blit(self.segments[8],block_rect)#  if thev x value of the previous block is equal to the x value next block then if the snake is moving up or down as the x value is the same so display a vertical body part/segment
				elif previous_block.y == next_block.y: screen.blit(self.segments[9],block_rect) # if thev y value of the previous block is equal to the y value next block then if the snake is moving left or right as the y value is remaining the same so display a horizontal body part/segment
				else: # else if the snake is not moving up,down,left or right it must have turned (as the x and y values are not consistant) so display a corner / turning body part/segment
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1: screen.blit(self.segments[11],block_rect) #  if the snake is going right and turns left/up or if the snake is going down and turns right (in proportion to snakes direction (left if looking at screen)), display the corner segment that relates to the turn (also refered to as a top left turn as reference in a vector dimentions graph)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1: screen.blit(self.segments[13],block_rect) # if the snake is going right and turns right/down or if the snake is going up and turns left, display the corner segment that relates to the turn (also refered to as a bottom left turn as reference in a vector dimentions graph)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1: screen.blit(self.segments[10],block_rect) # if the snake is going in the left direction and turns right/up or if the snake is going down and turns left (in proportion to snakes direction (right if looking at screen)), display the corner segment that relates to the turn (also refered to as a top right turn as reference in a vector dimentions graph)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1: screen.blit(self.segments[12],block_rect) # if the snake is going left and turns left/down or if the snake is going up and turns right, displat the corner segment that relates to the turn (also refered to as a bottom right turn as reference in a vector dimentions graph)
			pygame.display.update

	def update_head_graphics(self): # will have to change and put into draw_snake()
		head_relation = self.body[1] - self.body[0] # set the variable head_relation to the second element in the array - the first elemnt 
		if head_relation == Vector2(1,0):self.head = self.segments[3] # if head realtion is equal to vector(1,0) or moving left in accordance to typical vector dimentions hen set the head to head_left
		elif head_relation == Vector2(-1,0):self.head = self.segments[2] # if the head relation is equal to vector(-1,0) or moving right then set the head to head_right
		elif head_relation == Vector2(0,1):self.head = self.segments[0] # if the head relation is equal to vector(0,1) or moving up then set the head to head_up
		elif head_relation == Vector2(0,-1):self.head = self.segments[1] # if the head relation is equal to vector(0,1) or moving down then set the head to head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1] # set the variable tail_relation to the second last element in the array - the last elemnt 
		if tail_relation == Vector2(1,0):self.tail = self.segments[7] # if the tails relation is equal to vector(1,0) or moving left in accordance to vector dimentions then set the tail to tail_left
		elif tail_relation == Vector2(-1,0):self.tail = self.segments[6] # if the tails relation is equal to vector(-1,0) or moving right then set the tail to tail_right
		elif tail_relation == Vector2(0,1):self.tail = self.segments[4] # if the tails relation is equal to vector(0,1) or moving up then set the tail to tail_up
		elif tail_relation == Vector2(0,-1):self.tail = self.segments[5] # if the tails relation is equal to vector(0,1) or moving down then set the tail to tail_down
			  
	def move_snake(self):
		if self.new_block == True and self.i < self.amount: # if new_block is True and i is less than the amount that needs to be added or subracted
			self.adding_segments = True
			if self.operator == "+": # if the snake's operator is +
				body_copy = self.body[:] # create a copy of the list of snake segments
				if main_game.machine == True: main_game.ai_snake.append(main_game.ai_grid[main_game.ai_current.x][main_game.ai_current.y])
				body_copy.insert(0,body_copy[0] + self.direction) # insert a segment in the same directionas the other parts
				self.body = body_copy[:] # set the snakes body to the edited copy
			else: # if the snake's operator is -
				try: # if there is enough segments to subtract
					if main_game.machine == True: main_game.ai_snake.pop(0)
					self.adding_segments = True
					body_copy = self.body[:-2] # make a copy of the snakes segments, subtracting the last two segments
					body_copy.insert(0,body_copy[0] + self.direction) # add a segment
					self.body = body_copy[:] # set the snakes body to the edited copy
				except: main_game.game_over() # if there is not enough segments left, end the game
			self.i=self.i+1 # add 1 to i
   
		elif self.new_block == True and self.i >= self.amount: # if new_block is true but i is more or equal to the amount
			self.adding_segments = False
			self.i=0 # set i to 0
			self.amount = 0 # set amount to 0
			self.new_block = False # set new_block to false
		else: # if new_block if false 
			self.adding_segments = False
			body_copy = self.body[:-1] # creates a copy of self.body but subracts the last element in the array
			body_copy.insert(0,body_copy[0] + self.direction) # inserts a body segment with the x pos of 0 and the y pos of the position of the snakes head (the very first array in body_copy (body_copy[0])) plus (+) the direction
			self.body = body_copy[:] # sets self.body to the copy of the array 


	def add_block(self, amount):
		self.new_block = True  # if the snake gets an apple then new_block is set to True 
		self.amount = self.amount + amount # add the amount to the existing amount that needs to be added or subracted
  
	def reset(self):
		self.operator = '+'  # set's the snakes operation to +
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]  # Array of snakes body parts
		self.direction = Vector2(0,0) # set's the direction of the snake
		self.set_img() # declaire the images of the snakes segments
		self.new_block = False # set's new_block to False
		self.amount = 0 # set's amount to 0
		self.i = 0 # sets i to 0
		self.celebrate = False # set's celebrate t false
		try: main_game.score = 0 #  try to reset the score
		except: pass


class OPERATIONS:
	def __init__(self):
		try: self.numbers = NUMBERS()
		except: pass
		self.plus = ['+',load('Graphics/plus.png').convert_alpha()] # declairs the variable plus as the symbol and image
		self.minus = ['-',load('Graphics/minus.png').convert_alpha()] # declairs the variable minus as the symbol and image
		self.operators = [(self.plus,(self.randomise())), (self.minus,(self.randomise())), (self.plus,(self.randomise())), (self.minus,(self.randomise()))] # creates a list of all the operators and their locations, symbol and image
		self.check_doubles() # check if the locations have doubled up
  
	def draw_operations(self):
		for index, operation in enumerate(self.operators):	# for every operation in operators 
			operation_rect = Rect(int(operation[1].x * cell_size),int(operation[1].y * cell_size),cell_size,cell_size)  # operators demensions 
			screen.blit(operation[0][1],operation_rect) # visually inputs the operators on the sceen
			
	def randomise(self):
		self.x = randint(0, cell_number - 1) # get the new x position by picking a random number between 0 and 15 (the max width)
		self.y = randint(1, cell_number - 1) # get the new y position by picking a random number between 0 and 15 (the max width)
		self.pos= Vector2(self.x,self.y) # uses vector2 to creat a 2 demensional vector using the two new positions and set's it as the new position of the operator
		try:
			for j in range(0,len(self.numbers.numbers)): # for every number between 1 and the amount of operators plus 1
				if self.pos.x == self.numbers.numbers[j][1][0] and self.pos.y == self.numbers.numbers[j][1][1]: # if the position of the number equals the position of a operator
					print(self.pos, '==', self.numbers.numbers[j][1])
					self.randomise() # get a new position
					break # break the loop
				else: pass
			return self.pos # return the position
		except: return self.pos # return the position

	def check_doubles(self):
		for i in range(1,len(self.operators)+1): # for every number from 1 to the number of operators + 1
			for j in range(i+1,len(self.operators)+1): # for every number from i+1 to the number of operators + 1
				if self.operators[i-1][1] == self.operators[j-1][1]: # if any two operators' positions are equal
					pos = self.randomise() # get a new position
					self.operators[i-1][1][0] = pos.x # set the new x position of the operator
					self.operators[i-1][1][1] = pos.y #  set the new y position of the operator
					self.check_doubles() #maybe
				else: pass# if they don't match pass
					
    

  
class NUMBERS:
    def __init__(self):
        self.operations = OPERATIONS() # set operations as the class, OPERATIONS()
        self.snake = SNAKE() # set snake as the class SNAKE
        self.numbers = [] # create an empty list called numbers
        for i in range(0,10): self.numbers.append([randint(1,9),self.randomise()]) # for numbers 0 to 10 (amount of numbers wanted), append a random number between 1,9 and a random position to the list
        self.check_doubles() # check if the locations double up


    def draw_numbers(self):
        i=0 # set i to 0
        while i < len(self.numbers): # while i is less than the amount of elements in the lsit
            number_surface = game_font.render(str(self.numbers[i][0]),True,BLACK) # render the value of the element
            number_rect = number_surface.get_rect(center = (int(cell_size * self.numbers[i][1][0])+20,int(cell_size * self.numbers[i][1][1])+20)) # create dimentions of the rectangle that change with the size of the number
            screen.blit(number_surface,number_rect) # show the number on the screen
            number_rect = Rect(int(self.numbers[i][1][0] * cell_size+5),int(self.numbers[i][1][1] * cell_size+5),cell_size-10,cell_size-10)  # create a surrounding rectange 
            rect(screen,(27, 30, 25),number_rect,3) # draw the surrounding rectangle
            i=i+1 # plus 1 to i
            
    
    def randomise(self):
        self.x = randint(0, cell_number - 1) # get the new x position by picking a random number between 0 and 15 (the max width)
        self.y = randint(1, cell_number - 1) # get the new y position by picking a random number between 0 and 15 (the max width)
        self.pos= Vector2(self.x,self.y) # uses vector2 to creat a 2 demensional vector using the two new positions and set's it as the new position of the number
        for j in range(0,len(self.operations.operators)): # for every number between 1 and the amount of operators plus 1
            if self.pos.x == self.operations.operators[j][1][0] and self.pos.y == self.operations.operators[j][1][1]: # if the position of the number equals the position of a operator
                print(self.pos, '==', self.operations.operators[j][1])
                self.randomise() # get a new position
                break # break the loop
            else: pass
        return self.pos # return the position
			
        
    
    def check_doubles(self):
        for i in range(1,len(self.numbers)+1): # for every number between 1 and the amount of numbers in the list + 1
             for j in range(i+1,len(self.numbers)+1): #  for every number between i + 1 and the amount of numbers in the list + 1
                if self.numbers[i-1][1] == self.numbers[j-1][1]: # if two numbers have the same location
                    pos = self.randomise() # get a new postion
                    self.numbers[i-1][1][0] = pos.x # set the new x position of the number
                    self.numbers[i-1][1][1] = pos.y # set the new y position of the number
                    self.check_doubles() #check
                else: pass
    
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.obstacle = False
        self.camefrom = []
        
        
    def add_neighbours(self, grid): 
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.x < cell_number - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y < cell_number - 1:
            self.neighbours.append(grid[self.x][self.y + 1])
        if bound == False:
            if self.x == 0:
                self.neighbours.append(grid[cell_number-1][self.y]) 
            if self.y == 0:
                self.neighbours.append(grid[self.x][cell_number-1])	
            if self.x == cell_number - 1:
                self.neighbours.append(grid[0][self.y])
            if self.y == cell_number - 1:
                self.neighbours.append(grid[self.x][0])
            if self.x == 0 and self.y == cell_number - 1:
                self.neighbours.append(grid[cell_number-1][self.y])
                self.neighbours.append(grid[self.x][0])
            if self.x == cell_number - 1 and self.y == cell_number - 1:
                self.neighbours.append(grid[0][self.y])
                self.neighbours.append(grid[self.x][0])
            if self.x == cell_number - 1 and self.y == 0:
                self.neighbours.append(grid[0][self.y])
                self.neighbours.append(grid[self.x][cell_number-1])	     
            if self.x == 0 and self.y == 0:
                 self.neighbours.append(grid[cell_number-1][self.y])
                 self.neighbours.append(grid[self.x][cell_number-1])	
                
		 
               
        
                
                    

class MAIN:
	def __init__(self):
		self.snake = SNAKE()  # set's snake to the class SNAKE
		self.operations = OPERATIONS() # set's operations to class OPERATION
		self.numbers = NUMBERS() # set's numbers to class NUMBERS
		self.title_font = Font('Font/PoetsenOne-Regular.ttf', 70) # declairs the font used for the titles
		self.score = 0 # set's the players score to 0
		self.target = randint(2,20) #  sets a random target for the player to achieve
		if self.target == 3: self.target = randint(2,20)
		self.data = DATA()
		self.db_updated = False
		self.begin = False
		self.done = False
		self.reset_password = False
		self.leaderboard = False
		self.username = 'username'
		self.password = 'password'
		self.confirm_password = 'password'
		self.hostname = ''
		self.ip_address = ''
		self.problem = ''
		self.goal_array = []
		self.machine = False
		self.reset_ai()

		# self.c = self.leaderboard_db.conn_db.cursor()
		
	def get_ip(self):
    	# getting the hostname by socket.gethostname() method
		hostname = socket.gethostname()
		# getting the IP address using socket.gethostbyname() method
		ip_address = socket.gethostbyname(hostname)
		# printing the hostname and ip_address
		print(f"Hostname: {hostname}")
		print(f"IP Address: {ip_address}")
		return hostname, ip_address

	def check_user_ip(self, conn_db):
		hostname, ip_address = self.get_ip()
		cursor = conn_db.execute('''select * from sqlite_master''')
		usernames = [username[0] for username in cursor.execute("SELECT username FROM users")]
		passwords = [password[0] for password in cursor.execute("SELECT user_password FROM users")]
		users_hostname = [device_name[0] for device_name in cursor.execute("SELECT user_device_name FROM users")]
		users_ip = [ip[0] for ip in cursor.execute("SELECT ip FROM users")]
		for i in range(0,len(users_ip)): users_ip[i] = users_ip[i].split()
		print(users_ip)
		new_user = True
		for i in range(0,len(users_hostname)):
			if users_hostname[i] == hostname:
				for j in range(0,len(users_ip[i])):
					if users_ip[i][j] == ip_address:
						self.username = usernames[i]
						self.password = passwords[i]
						new_user = False
						self.done = True
						conn_db.close()
						break
						
				if self.done == False:
					users_ip[i].append(ip_address)
					user_ip_adress = ''
					for x in range(0,len(users_ip[i])): user_ip_adress = user_ip_adress + ' ' + str(users_ip[i][x])
					conn_db.execute("UPDATE users SET ip = (?) where user_device_name = (?)", (user_ip_adress, hostname))
					conn_db.commit()
					self.problem = 'ip could not be identified'
					self.done = False
					new_user = False
					break
			else: pass
		return hostname, ip_address, new_user
	
	def check_user(self, conn_db, new_user):
		print('check password')
		cursor = conn_db.execute('''select * from sqlite_master''')
		usernames = [username[0] for username in cursor.execute("SELECT username FROM users")]
		passwords = [password[0] for password in cursor.execute("SELECT user_password FROM users")]
		invalid = [',','_', '-', '\'', ']','[','(',')','*','&','^','#', ' ','@','!','$','/','.','|','+','=']
		if new_user == True:
			for i in range(0,len(usernames)):
				if self.username == usernames[i]: return 'username already in use'
				else: pass
			if self.username == 'username': return "Invalid Username"
			elif self.password == 'password': return "Invalid Password"
			else:
				if len(self.username) <= 3: return "Username entered is too short"
				elif len(self.password) <= 3: return "Password entered is too short"
				else:
					if len(self.username) > 15: return "Username entered is too long"
					elif len(self.password) > 15: return "password entered is too long"
					else:
						for i in range(0,len(self.username)):
							if self.username[i] in invalid: return 'invalid character in username'
						for i in range(0,len(self.password)):
							if self.password[i] in invalid: return 'invalid character in password'
						if self.username == self.password: return 'username and password are the same'
						else:
							conn_db.execute("INSERT INTO users  VALUES (?,?,?,?)", (self.username, self.password, self.hostname, self.ip_address))  
							conn_db.commit()
							self.done = True
							conn_db.close()
							return None
		else:
			for i in range(0,len(usernames)):
				if self.username == usernames[i]:
					if self.password == passwords[i]:
						self.done = True
						conn_db.close()
						return None
					else: return 'password is incorrect' 
			return 'username not found'
    
	def reset_password_check(self, conn_db):
		print('reset password')
		cursor = conn_db.execute('''select * from sqlite_master''')
		usernames = [username[0] for username in cursor.execute("SELECT username FROM users")]
		passwords = [password[0] for password in cursor.execute("SELECT user_password FROM users")]
		invalid = [',','_', '-', '\'', ']','[','(',')','*','&','^','#', ' ','@','!','$','/','.','|','+','=']
		if self.username not in usernames: return 'username not found'
		elif self.password != self.confirm_password: return 'passwords do not match'
		else:
			for i in range(0,len(usernames)):
				if self.username == usernames[i]:
					if self.password == passwords[i]: return 'password already in use'
			if self.password == 'password': return "Invalid Password"
			else:
				if len(self.password) <= 3: return "Password entered is too short"
				elif len(self.password) > 15: return "password entered is too long"
				else:
					for i in range(0,len(self.password)):
						if self.password[i] in invalid: return 'invalid character in password'
					if self.username == self.password: return 'username and password are the same'
					else:
						conn_db.execute("UPDATE users SET user_password = (?) where username = (?)", (self.password, self.username))  
						conn_db.commit()
						self.reset_password = False
						conn_db.close()
						return None
	
	def forgot_screen_display(self): 
     
		screen.fill((58, 133, 33))
  
		title_surface = self.title_font.render("RESET PASSWORD",True,(27, 30, 25))

		username_surface = game_font.render("USERNAME",True,(27, 30, 25))
		new_password_surface = game_font.render("NEW PASSWORD",True,(27, 30, 25))
		confirm_surface = game_font.render("CONFIRM PASSWORD",True,(27, 30, 25))
  
		reset_surface = game_font.render("RESET",True,(27, 30, 25))
		quit_surface = game_font.render("QUIT",True,(27, 30, 25))
  
		first_x = int(cell_size * cell_number/2) 
		title_y = int(cell_size * cell_number - (cell_size * cell_number - 70)) 
		username_y = int(cell_size * cell_number - (cell_size * cell_number - 175)) 
		new_passowrd_y = int(cell_size * cell_number - (cell_size * cell_number - 300))
		confirm_y = int(cell_size * cell_number - (cell_size * cell_number - 425)) 
		reset_x = int(cell_size * cell_number/3)
		quit_x = int(cell_size * cell_number/3 + cell_size * cell_number/3)
		third_y = int(cell_size * cell_number - (cell_size * cell_number - 575))

		title_rect = title_surface.get_rect(center = (first_x,title_y))
		username_rect = username_surface.get_rect(center = (first_x,username_y))
		new_password_rect = new_password_surface.get_rect(center = (first_x,new_passowrd_y))
		confirm_rect = confirm_surface.get_rect(center = (first_x,confirm_y))
		reset_rect = reset_surface.get_rect(center = (reset_x,third_y))
		quit_rect = quit_surface.get_rect(center = (quit_x,third_y))
		
		screen.blit(title_surface,title_rect)
		screen.blit(username_surface,username_rect)
		screen.blit(new_password_surface,new_password_rect)
		screen.blit(confirm_surface,confirm_rect)
		screen.blit(reset_surface, reset_rect)
		screen.blit(quit_surface, quit_rect)
  
		reset_rect = reset_surface.get_rect(size=(100,50), center=(reset_x,third_y))
		quit_rect = quit_surface.get_rect(size=(100,50), center=(quit_x,third_y))
  
		# draws the rectangles
		rect(screen,(27, 30, 25),reset_rect,3)
		rect(screen,(27, 30, 25),quit_rect,3)

		return first_x, quit_rect, reset_rect, confirm_rect
        
	def forgot_password_func(self):
     
		problem = None
     
		conn_db = self.data.create_db_connection(self.data.database)
  
		first_x, quit_rect, reset_rect, confirm_rect = self.forgot_screen_display()

		username_active = True
		new_password_active = False
		confirm_active = False
  
		font = Font(None, 40)
		font_username = Font(None, 25)

		while self.reset_password: 
      
			first_x, quit_rect, reset_rect, confirm_rect = self.forgot_screen_display()
			
			if problem is not None: #check if works after getting password wrong on login page
				first_x, quit_rect, reset_rect, confirm_rect = self.forgot_screen_display()
				problem_surface = font.render(problem, True, (155,0,0))
				problem_y = int(cell_size * cell_number - (cell_size * cell_number - 125)) 
				problem_rect = problem_surface.get_rect(center = (first_x,problem_y))
				screen.blit(problem_surface,problem_rect)

			username_surface = font_username.render(self.username[:15] if len(self.username) <= 15 else self.username[:15] + '...', True, (255,255,255))
			username_rect = username_surface.get_rect(topleft = (320,225))
			username_rect = username_surface.get_rect(size=(username_rect.width + 10, username_rect.height+20),topleft = (310 - username_rect.width/2,215))
			rect(screen, (0,0,0), username_rect)
			screen.blit(username_surface, (320 - username_rect.width/2, 225))
			
			password_surface = font.render('*'*len(self.password[:15]), True, (255,255,255))
			new_password_rect = password_surface.get_rect(topleft = (320,360))
			new_password_rect = password_surface.get_rect(size=(new_password_rect.width + 10, new_password_rect.height+10),topleft = (310 - new_password_rect.width/2,347))
			rect(screen, (0,0,0), new_password_rect)
			screen.blit(password_surface, (320 - new_password_rect.width/2, 360))
	
			confirm_password_surface = font.render('*'*len(self.confirm_password[:15]), True, (255,255,255))
			confirm_password_rect = confirm_password_surface.get_rect(topleft = (320,485))
			confirm_password_rect = confirm_password_surface.get_rect(size=(confirm_password_rect.width + 10, confirm_password_rect.height+10),topleft = (310 - confirm_password_rect.width/2,472))
			rect(screen, (0,0,0), confirm_password_rect)
			screen.blit(confirm_password_surface, (320 - confirm_password_rect.width/2, 485))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos() 
					if username_rect.collidepoint(pos):
						new_password_active = False
						confirm_active = False
						username_active = True
					elif new_password_rect.collidepoint(pos):
						username_active = False
						confirm_active = False
						new_password_active = True
					elif confirm_rect.collidepoint(pos):
						username_active = False
						new_password_active = False
						confirm_active = True
					elif reset_rect.collidepoint(pos): 
						problem = self.reset_password_check(conn_db)
					elif quit_rect.collidepoint(pos): 
						pygame.quit()
						sys.exit()
					else:
						confirm_active = True
						new_password_active = False
						username_active = False
						
				elif event.type == pygame.KEYDOWN and new_password_active == True:						
					if event.key == pygame.K_BACKSPACE:
						self.password=self.password[:-1]
					else:  
						self.password += event.unicode
				elif event.type == pygame.KEYDOWN and confirm_active == True:
					if event.key == pygame.K_RETURN:
						print(self.username, ' -- ', self.password)  
						problem = self.reset_password_check(conn_db)

						
					elif event.key == pygame.K_BACKSPACE:
						self.confirm_password=self.confirm_password[:-1]
					else:  
						self.confirm_password += event.unicode
				elif event.type == pygame.KEYDOWN and username_active == True:
					if event.key == pygame.K_BACKSPACE:
						self.username=self.username[:-1]
					else:  
						self.username += event.unicode
	
			pygame.display.update()
			clock.tick(30)


	def log_in_display(self):
     
		screen.fill((58, 133, 33))

		forgot_font = Font('Font/PoetsenOne-Regular.ttf', 20)
		seccond_title_font = Font('Font/PoetsenOne-Regular.ttf', 50)

		welcome_surface = seccond_title_font.render("WELCOME TO",True,(27, 30, 25))
		title_surface = self.title_font.render("SNAKEY MATH",True,(27, 30, 25))

		username_surface = game_font.render("USERNAME",True,(27, 30, 25))
		password_surface = game_font.render("PASSWORD",True,(27, 30, 25))
  
		forgot_password_surface = forgot_font.render("FORGOT PASSWORD?",True,(155,0,0))
  
		enter_surface = game_font.render("ENTER",True,(27, 30, 25))
		quit_surface = game_font.render("QUIT",True,(27, 30, 25))
  
		first_x = int(cell_size * cell_number/2) 
		welcome_y = int(cell_size * cell_number - (cell_size * cell_number - 75)) 
		title_y = int(cell_size * cell_number - (cell_size * cell_number - 130)) 
		seccond_x = int(3*(cell_size * cell_number/4))
		username_y = int(cell_size * cell_number - (cell_size * cell_number - 275)) 
		passowrd_y = int(cell_size * cell_number - (cell_size * cell_number - 400)) 
		forgot_y = int(cell_size * cell_number - (cell_size * cell_number - 500))
		enter_x = int(cell_size * cell_number/3)
		quit_x = int(cell_size * cell_number/3 + cell_size * cell_number/3)
		third_y = int(cell_size * cell_number - (cell_size * cell_number - 575))

		welcome_rect = welcome_surface.get_rect(center = (first_x,welcome_y))
		title_rect = title_surface.get_rect(center = (first_x,title_y))
		username_rect = title_surface.get_rect(center = (seccond_x,username_y))
		password_rect = title_surface.get_rect(center = (seccond_x,passowrd_y))
		forgot_rect = forgot_password_surface.get_rect(center = (first_x,forgot_y))
		enter_rect = enter_surface.get_rect(center = (enter_x,third_y))
		quit_rect = quit_surface.get_rect(center = (quit_x,third_y))
		
		screen.blit(welcome_surface,welcome_rect)
		screen.blit(title_surface,title_rect)
		screen.blit(username_surface,username_rect)
		screen.blit(password_surface,password_rect)
		screen.blit(forgot_password_surface,forgot_rect)
		screen.blit(enter_surface, enter_rect)
		screen.blit(quit_surface, quit_rect)

		forgot_rect = forgot_password_surface.get_rect(size=(220,50), center=(first_x,forgot_y))
  
		enter_rect = enter_surface.get_rect(size=(100,50), center=(enter_x,third_y))
		quit_rect = quit_surface.get_rect(size=(100,50), center=(quit_x,third_y))
  
		# draws the rectangles
		rect(screen,(27, 30, 25),forgot_rect,3)
		rect(screen,(27, 30, 25),enter_rect,3)
		rect(screen,(27, 30, 25),quit_rect,3)

		return first_x, enter_rect, quit_rect, forgot_rect
  
	def log_in_screen(self): 
		
		self.problem = 'Please enter a username and password'
     
		conn_db = self.data.create_db_connection(self.data.database)
     
		first_x, enter_rect, quit_rect, forgot_rect = self.log_in_display()
		
		self.hostname, self.ip_address, new_user = self.check_user_ip(conn_db)
  
		first_x, enter_rect, quit_rect, forgot_rect = self.log_in_display()
		problem_y = int(cell_size * cell_number - (cell_size * cell_number - 200)) 
  
		username_active = True
		password_active = False
  
		font = Font(None, 40)
		font_username = Font(None, 25)
  
		while not self.done:
      
			first_x, enter_rect, quit_rect, forgot_rect = self.log_in_display()
   
			if self.problem != 'Please enter a username and password':
				problem_surface = font.render('', True, (155,0,0))
				problem_surface = font.render(self.problem, True, (155,0,0))
				problem_rect = problem_surface.get_rect(center = (first_x,problem_y))
				screen.blit(problem_surface,problem_rect)
				
			else:
				problem_surface = font.render(self.problem, True, (27, 30, 25))
				problem_rect = problem_surface.get_rect(center = (first_x,problem_y))
				screen.blit(problem_surface,problem_rect)
    
			username_surface = font_username.render(self.username[:15] if len(self.username) <= 15 else self.username[:15] + '...', True, (255,255,255))
			username_rect = username_surface.get_rect(topleft = (320,295))
			username_rect = username_surface.get_rect(size=(username_rect.width + 10, username_rect.height+20),topleft = (310 - username_rect.width/2,285))
			rect(screen, (0,0,0), username_rect)
			screen.blit(username_surface, (320 - username_rect.width/2, 295))
			
			password_surface = font.render('*'*len(self.password[:15]), True, (255,255,255))
			password_rect = password_surface.get_rect(topleft = (320,420))
			password_rect = password_surface.get_rect(size=(password_rect.width + 10, password_rect.height+10),topleft = (310 - password_rect.width/2,408))
			rect(screen, (0,0,0), password_rect)
			screen.blit(password_surface, (320 - password_rect.width/2, 420))
   
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos() 
					if username_rect.collidepoint(pos):
						password_active = False
						username_active = True
					elif password_rect.collidepoint(pos):
						username_active = False
						password_active = True
					elif enter_rect.collidepoint(pos): 
						self.problem = self.check_user(conn_db, new_user)
					elif quit_rect.collidepoint(pos): 
						pygame.quit()
						sys.exit()
					elif forgot_rect.collidepoint(pos):
						conn_db.close()
						self.done = True
						self.reset_password = True
					else:
						password_active = False
						username_active = False
						
				elif event.type == pygame.KEYDOWN and password_active == True:
					if event.key == pygame.K_RETURN:
						print(self.username, ' -- ', self.password)  
						self.problem = self.check_user(conn_db, new_user)
						
					elif event.key == pygame.K_BACKSPACE:
						self.password=self.password[:-1]
					else:  
						self.password += event.unicode
				elif event.type == pygame.KEYDOWN and username_active == True:
					if event.key == pygame.K_BACKSPACE:
						self.username=self.username[:-1]
					else:  
						self.username += event.unicode
			
			pygame.display.update()
			clock.tick(30)
  
  
	def leaderboard_screen(self):
     
		conn_db = self.data.create_db_connection(self.data.database)
		
		screen.fill((58, 133, 33)) # fills the screen with a green colour
  
		title_surface = self.title_font.render("LEADERBOARD",True,(27, 30, 25)) # renders the title
  
		first_x = int(cell_size * cell_number/2) 
		title_y = int(cell_size * cell_number - (cell_size * cell_number - 75)) 
  
		title_rect = title_surface.get_rect(center = (first_x,title_y))
  
		screen.blit(title_surface,title_rect)
  
		place_surface = game_font.render("Placement",True,(27, 30, 25))
		usern_surface = game_font.render("Username",True,(27, 30, 25))
		scor_surface = game_font.render("Score",True,(27, 30, 25))
  
		place_x = int(cell_size * cell_number/4) 
		username_x = int(cell_size * cell_number/2)
		score_x = int(cell_size * cell_number / 4 *3)

		seccond_y = int(cell_size * cell_number - (cell_size * cell_number - 160)) 
  
		place_rect = place_surface.get_rect(center = (place_x,seccond_y))
		usern_rect = usern_surface.get_rect(center = (username_x,seccond_y))
		scor_rect = scor_surface.get_rect(center = (score_x,seccond_y))
  
  
		cursor = conn_db.execute('''select * from sqlite_master''')
		usernames = [username[0] for username in cursor.execute("SELECT username FROM high_scores")]
		placements = [placement[0] for placement in cursor.execute("SELECT placement FROM high_scores")]
		scores = [score[0] for score in cursor.execute("SELECT score FROM high_scores")]

		ten_users = []
		not_top_ten = True
  
		for i in range(0, len(placements)): 
			if int(placements[i]) <= 10 and len(ten_users) < 12: ten_users.append([placements[i], usernames[i], scores[i]])
		for i in ten_users: 
			if self.username in i and len(ten_users) > 0: not_top_ten = False
		
		
		bg_rect = Rect(place_rect.left-9,place_rect.top-3,(place_rect.width+6 + usern_rect.width + 12 + scor_rect.width + 6)*1.33,(scor_rect.height+3) * (12 if not_top_ten == True or len(ten_users) > 10 else 10.5)) 
 
		rect(screen,(0,155,0),bg_rect)
	
		bg_rect = Rect(place_rect.left-12,place_rect.top-6,(place_rect.width+9 + usern_rect.width + 11 + scor_rect.width + 9)*1.33,(scor_rect.height+3 + (1/3 if not_top_ten == True or len(ten_users) > 10 else 1/1.5)) * (12 if not_top_ten == True or len(ten_users) > 10 else 10.5)) 
 
		rect(screen,(27, 30, 25),bg_rect, 3)
  
		screen.blit(place_surface,place_rect)
		screen.blit(usern_surface,usern_rect)
		screen.blit(scor_surface,scor_rect)
		
		height = 170 #150
  
		for i in range(0, len(ten_users)):
      
			height = height + 30
			
			if ten_users[i][1] == self.username: colour = (0,0,0) 
			else: colour = (27, 30, 25)
      
			placement_surface = game_font.render(str(ten_users[i][0]),True,colour) # renders the title
			user_surface = game_font.render(str(ten_users[i][1]),True,colour)
			score_surface = game_font.render(str(ten_users[i][2]),True,colour)
  
			temp_y = int(cell_size * cell_number - (cell_size * cell_number - height))
   
			placement_rect = placement_surface.get_rect(center = (place_x,temp_y))
			user_rect = user_surface.get_rect(center = (username_x,temp_y))
			score_rect = score_surface.get_rect(center = (score_x,temp_y))	
 
			screen.blit(placement_surface,placement_rect)
			screen.blit(user_surface,user_rect)
			screen.blit(score_surface,score_rect)
	
			
		if i == 0 and not_top_ten == False and len(ten_users) == 0: #issue
			
			colour = (0,0,0)
			placement_surface = game_font.render("1",True,colour) 
			user_surface = game_font.render(str(self.username),True,colour)
			score_surface = game_font.render(str(self.score),True,colour)
  
			temp_y = int(cell_size * cell_number - (cell_size * cell_number - height))
   
			placement_rect = placement_surface.get_rect(center = (place_x,temp_y))
			user_rect = user_surface.get_rect(center = (username_x,temp_y))
			score_rect = score_surface.get_rect(center = (score_x,temp_y))	
 
			screen.blit(placement_surface,placement_rect)
			screen.blit(user_surface,user_rect)
			screen.blit(score_surface,score_rect)
			i = 1
		i = i + 1 #test
		if i < 9:
			colour = (27, 30, 25)
			for j in range(i, 10): #test
       
				i=i+1
    
				height = height + 30
    
				placement_surface = game_font.render(str(i),True,colour) 

				temp_y = int(cell_size * cell_number - (cell_size * cell_number - height))
	
				placement_rect = placement_surface.get_rect(center = (place_x,temp_y))

				screen.blit(placement_surface,placement_rect)
    
		
   
		if not_top_ten == True and len(usernames) > 1:
			
			height = height + 30
			
			colour = (0,0,0) 

			for i in range(0, len(usernames)):
				if self.username == usernames[i]:
					temp_score = scores[i]
					temp_place = placements[i]
			try:
				print(temp_score)
			except:
				temp_score = 0
				temp_place = '--'
     
			placement_surface = game_font.render(str(temp_place),True,colour) # renders the title
			user_surface = game_font.render(str(self.username),True,colour)
			score_surface = game_font.render(str(temp_score),True,colour)
  
			temp_y = int(cell_size * cell_number - (cell_size * cell_number - height))
   
			placement_rect = placement_surface.get_rect(center = (place_x,temp_y))
			user_rect = user_surface.get_rect(center = (username_x,temp_y))
			score_rect = score_surface.get_rect(center = (score_x,temp_y))	

			bg_rect = Rect(placement_rect.left-9,placement_rect.top,(placement_rect.width+6 + user_rect.width + 6 + score_rect.width)*2,score_rect.height+3) 
 
			rect(screen,(167,209,61),bg_rect)
   
			screen.blit(placement_surface,placement_rect)
			screen.blit(user_surface,user_rect)
			screen.blit(score_surface,score_rect)
   
		return_surface = game_font.render("RETURN",True,MED)

		return_x = int(cell_size * cell_number/2)
		third_y = int(cell_size * cell_number - (cell_size * cell_number - 590)) 
			
		return_rect = return_surface.get_rect(center = (return_x,third_y))

		screen.blit(return_surface, return_rect)
  
		return_rect = return_surface.get_rect(size =(100,50), center=(return_x,third_y))
  
		rect(screen,(27, 30, 25),return_rect,3)
	
 
	def start_screen(self):
		conn_db = self.data.create_db_connection(self.data.database)
		cursor = conn_db.execute('''select * from sqlite_master''')
		usernames = [username[0] for username in cursor.execute("SELECT username FROM high_scores")]
		placements = [placement[0] for placement in cursor.execute("SELECT placement FROM high_scores")]
		scores = [score[0] for score in cursor.execute("SELECT score FROM high_scores")]

		for i in range(0, len(usernames)):
			if self.username == usernames[i]:
				temp_h_score = scores[i]
				temp_place = placements[i]
		try:
			temp_h_score = temp_h_score
		except:
			temp_h_score = 0
			temp_place = '--'
        
		screen.fill((58, 133, 33)) # fills the screen with a green colour

		seccond_title_font = Font('Font/PoetsenOne-Regular.ttf', 50)

		welcome_surface = seccond_title_font.render("WELCOME TO",True,(27, 30, 25))
		title_surface = self.title_font.render("SNAKEY MATH",True,(27, 30, 25)) # renders the title
  
		# renders the text for each button
		leader_surface = game_font.render("LEADERBOARD",True,(155,155,0))
		easy_surface = game_font.render("EASY",True,EASY)
		med_surface = game_font.render("MED",True,MED)
		hard_surface = game_font.render("HARD",True,HARD)
		play_surface = game_font.render("PLAY",True,(27, 30, 25))
		quit_surface = game_font.render("QUIT",True,(27, 30, 25))
		demo_surface = game_font.render("PLAY DEMO",True,(30,60,155))
		bound_surface = game_font.render(BOUND_TEXT,True,BOUND)
  
		# set's the position for each button and for the title
		first_x = int(cell_size * cell_number/2) 
		welcome_y = int(cell_size * cell_number - (cell_size * cell_number - 75)) 
		title_y = int(cell_size * cell_number - (cell_size * cell_number - 130)) 
		leader_x = int(cell_size * cell_number/3) - 10
		leader_y = int(cell_size * cell_number - (cell_size * cell_number - 215)) 
		easy_x = int(cell_size * cell_number/5)
		med_x = int(cell_size * cell_number/2)
		hard_x = int((cell_size * cell_number/5)*4)
		second_y = int(cell_size * cell_number - (cell_size * cell_number - 300))
		play_x = int(cell_size * cell_number/3)
		quit_x = int(cell_size * cell_number/3 + cell_size * cell_number/3)
		third_y = int(cell_size * cell_number - (cell_size * cell_number - 520))
		fourth_y = int(cell_size * cell_number - (cell_size * cell_number - 595))
		bound_x = int((cell_size * cell_number/3) + (cell_size * cell_number/3)) + 10
  

  
		# creates a rectangle for each button and for the title
		welcome_rect = welcome_surface.get_rect(center = (first_x,welcome_y))
		title_rect = title_surface.get_rect(center = (first_x,title_y))
		leader_rect = leader_surface.get_rect(center = (leader_x,leader_y))
		easy_rect = play_surface.get_rect(center = (easy_x,second_y))
		med_rect = play_surface.get_rect(center = (med_x,second_y))
		hard_rect = play_surface.get_rect(center = (hard_x,second_y))
		play_rect = play_surface.get_rect(center = (play_x,third_y))
		quit_rect = quit_surface.get_rect(center = (quit_x,third_y))
		demo_rect = demo_surface.get_rect(center = (med_x,fourth_y))
		# checks if boundries are on or off
		if bound == False:
			bound_rect = quit_surface.get_rect(center = (bound_x-69,leader_y))
		else:
			bound_rect = quit_surface.get_rect(center = (bound_x-67,leader_y))

		# displays both the text using the rectange for positioning
		screen.blit(welcome_surface,welcome_rect)
		screen.blit(title_surface,title_rect)
		screen.blit(leader_surface, leader_rect)
		screen.blit(easy_surface, easy_rect)
		screen.blit(med_surface, med_rect)
		screen.blit(hard_surface, hard_rect)
		screen.blit(play_surface, play_rect)
		screen.blit(quit_surface, quit_rect)
		screen.blit(bound_surface, bound_rect)
		screen.blit(demo_surface, demo_rect)

		# creates a rectangle to surround the text to create the button
		leader_rect = play_surface.get_rect(size =(220,50), center=(leader_x,leader_y))
		easy_rect = play_surface.get_rect(size =(100,50), center=(easy_x,second_y))
		med_rect = play_surface.get_rect(size =(100,50), center=(med_x,second_y))
		hard_rect = play_surface.get_rect(size =(100,50), center=(hard_x,second_y))
		play_rect = play_surface.get_rect(size =(100,50), center=(play_x,third_y))
		quit_rect = quit_surface.get_rect(size =(100,50), center=(quit_x,third_y))
		bound_rect = quit_surface.get_rect(size =(220,50), center=(bound_x,leader_y))
		demo_rect = demo_surface.get_rect(size =(150,50), center=(med_x,fourth_y))		
  
		# draws the rectangles
		rect(screen,(27, 30, 25),leader_rect,3)
		rect(screen,(27, 30, 25),easy_rect,3)
		rect(screen,(27, 30, 25),med_rect,3)
		rect(screen,(27, 30, 25),hard_rect,3)
		rect(screen,(27, 30, 25),play_rect,3)
		rect(screen,(27, 30, 25),quit_rect,3)
		rect(screen,(27, 30, 25),bound_rect,3)
		rect(screen,(27, 30, 25),demo_rect,3)

		place_surface = game_font.render("Placement",True,(27, 30, 25))
		usern_surface = game_font.render("Username",True,(27, 30, 25))
		scor_surface = game_font.render("Score",True,(27, 30, 25))
		
		place_x = int(cell_size * cell_number/4) 
		username_x = int(cell_size * cell_number/2)
		score_x = int(cell_size * cell_number / 4 *3)

		leaderboard_y = int(cell_size * cell_number - (cell_size * cell_number - 380))
  
		place_rect = place_surface.get_rect(center = (place_x,leaderboard_y))
		usern_rect = usern_surface.get_rect(center = (username_x,leaderboard_y))
		scor_rect = scor_surface.get_rect(center = (score_x,leaderboard_y))
  
		placement_surface = game_font.render(str(temp_place),True,(0,0,0)) # renders the title
		user_surface = game_font.render(str(self.username),True,(0,0,0))
		score_surface = game_font.render(str(temp_h_score),True,(0,0,0))

		temp_y = int(cell_size * cell_number - (cell_size * cell_number - 430))
  
		placement_rect = placement_surface.get_rect(center = (place_x,temp_y))
		user_rect = user_surface.get_rect(center = (username_x,temp_y))
		score_rect = score_surface.get_rect(center = (score_x,temp_y))	

		bg_rect = Rect(place_rect.left-9,place_rect.top-3,(place_rect.width+6 + usern_rect.width + 12 + scor_rect.width + 6)*1.33,((scor_rect.height+3)*3)-3) 
 
		rect(screen,(0,155,0),bg_rect)
	
		bg_rect = Rect(place_rect.left-12,place_rect.top-6,(place_rect.width+9 + usern_rect.width + 11 + scor_rect.width + 9)*1.33,(scor_rect.height+3)*3) 
 
		rect(screen,(27, 30, 25),bg_rect, 3)
  
		screen.blit(place_surface,place_rect)
		screen.blit(usern_surface,usern_rect)
		screen.blit(scor_surface,scor_rect)
  
		screen.blit(placement_surface,placement_rect)
		screen.blit(user_surface,user_rect)
		screen.blit(score_surface,score_rect)
   
  
		#draws a blue diagonal line
  
		pygame.draw.line(screen,(0,0,155), (((cell_number*cell_size)+20), ((cell_number*cell_size) - (cell_number*cell_size)/3)), (((cell_number*cell_size) - (cell_number*cell_size)/3), (cell_number*cell_size)+15), 40)
		
		#display atc logo
  
		logo = load('Graphics/logo.png').convert_alpha()
		logo_x = int((cell_size * cell_number) - ((cell_size * cell_number)/13))
		logo_y = int((cell_size * cell_number) - ((cell_size * cell_number)/13))
		logo_rect = logo.get_rect(center = (logo_x,logo_y))

		screen.blit(logo, logo_rect)
  
	def end_screen(self):
		screen.fill((27, 30, 25)) # fills the screen with a grey colour

		title_surface = self.title_font.render("YOU DIED!",True,(155,0,0)) # renders the text for the title of the page
		# renders the text for the buttons
		play_surface = game_font.render("PLAY",True,(155,0,0))
		quit_surface = game_font.render("QUIT",True,(155,0,0))
  
		# sets the position of each item
		title_x = int(cell_size * cell_number/2) 
		title_y = int(cell_size * cell_number - (cell_size * cell_number - 200)) 
		play_x = int(cell_size * cell_number/3)
		quit_x = int(cell_size * cell_number/3 + cell_size * cell_number/3)
		third_y = int(cell_size * cell_number - (cell_size * cell_number - 450))

		# creates rectangles for each item
		title_rect = title_surface.get_rect(center = (title_x,title_y))
		play_rect = play_surface.get_rect(center = (play_x,third_y))
		quit_rect = quit_surface.get_rect(center = (quit_x,third_y))
  
		# displays the text
		screen.blit(title_surface,title_rect)
		screen.blit(play_surface, play_rect)
		screen.blit(quit_surface, quit_rect)

		# creates a surrounding rectange for the buttons
		play_rect = play_surface.get_rect(size=(100,50), center=(play_x,third_y))
		quit_rect = quit_surface.get_rect(size=(100,50), center=(quit_x,third_y))
  
		# draws the rectangles
		rect(screen,(155,0,0),play_rect,3)
		rect(screen,(155,0,0),quit_rect,3)


	def pause(self): # check
		loop = 1 # if the pause function is called upon set lopp to 1 (True)
  
		screen.fill((27, 30, 25)) # set;s the background to a grey coour
  
		# renders the text for each element
		pause_surface = self.title_font.render('PAUSED', True, (65, 65, 255))
		play_surface = game_font.render("PLAY",True,(65, 65, 255))
		quit_surface = game_font.render("QUIT",True,(65, 65, 255))

		# sets the position for each element
		pause_x = int(cell_size * cell_number/2) 
		pause_y = int(cell_size * cell_number - (cell_size * cell_number - 200)) 
		play_x = int(cell_size * cell_number/3)
		quit_x = int(cell_size * cell_number/3 + cell_size * cell_number/3)
		third_y = int(cell_size * cell_number - (cell_size * cell_number - 450))

		# creates a rectangle for each element
		pause_rect = pause_surface.get_rect(center = (pause_x,pause_y))
		play_rect = play_surface.get_rect(center = (play_x,third_y))
		quit_rect = quit_surface.get_rect(center = (quit_x,third_y))
  
		# displays each element
		screen.blit(pause_surface, pause_rect)
		screen.blit(play_surface, play_rect)
		screen.blit(quit_surface, quit_rect)
  
		# creates a surrounding rectangle for the buttons
		play_rect = play_surface.get_rect(size=(100,50), center=(play_x,third_y))
		quit_rect = quit_surface.get_rect(size=(100,50), center=(quit_x,third_y))
  
		# displays the surrounding rectangle
		rect(screen,(65, 65, 255),play_rect,3)
		rect(screen,(65, 65, 255),quit_rect,3)
  
		while loop: # while loop == 1 (while loop is True)
			for event in pygame.event.get(): # for each pygame event
				if event.type == pygame.QUIT: pygame.quit(), sys.exit()# is the user quits, quit the game
				if event.type == pygame.KEYDOWN: # if the user presses a key
					if event.key == pygame.K_ESCAPE: loop = 0 # if the user presses the escape key, end the loop
					if event.key == pygame.K_SPACE: loop = 0 # if the user presses the space button, end the loop
				if event.type == pygame.MOUSEBUTTONUP: # if the user clicks on the screen
					pos = pygame.mouse.get_pos() # get the position where the user pressed
					if (abs(pos[0] - 214) <= 50) and (abs(pos[1] - 450) <= 25): loop = 0 # if the user presses the same location as the play button, end the loop
					elif (abs(pos[0] - 426) <= 50) and (abs(pos[1] - 450) <= 25): pygame.quit(),sys.exit() # if the user presses the exit button, quit the game
					
      
			pygame.display.update() # update the display
			clock.tick(100) # set the clocks tick to 100 frames per second
        
    
	def get_amount_needed(self):
		return self.target - len(self.snake.body)
        
	def get_goal(self):
		self.goal_array = []
		amount_needed = self.get_amount_needed()
		print(amount_needed)
		if self.snake.adding_segments == False:
			if amount_needed > 0:
				for i in range(len(self.numbers.numbers)):
					if self.numbers.numbers[i][0] == amount_needed:
						if ['+',self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)]] not in self.goal_array and len(self.goal_array) == 0:
							print('+', self.numbers.numbers[i][0])
							self.goal_array.append(['+',self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)]]) # and self.get_plus_operator()
							break
					else:
						for j in range(i+1,len(self.numbers.numbers)+1):
							if (self.numbers.numbers[i-1][0] + self.numbers.numbers[j-1][0]) == amount_needed and len(self.goal_array) == 0:
								if ['+',self.ai_grid[int(self.numbers.numbers[i-1][1].x)][int(self.numbers.numbers[i-1][1].y)]] not in self.goal_array and ['+',self.ai_grid[int(self.numbers.numbers[j-1][1].x)][int(self.numbers.numbers[j-1][1].y)]] not in self.goal_array:
									print('+', self.numbers.numbers[i-1][0])
									print('+', self.numbers.numbers[j-1][0])
									self.goal_array.append(['+',self.ai_grid[int(self.numbers.numbers[i-1][1].x)][int(self.numbers.numbers[i-1][1].y)]])
									self.goal_array.append(['+',self.ai_grid[int(self.numbers.numbers[j-1][1].x)][int(self.numbers.numbers[j-1][1].y)]]) #change to [i][1]
									#self.get_plus_operator() #make function that checks the operator of the next 
				if len(self.goal_array) == 0: 
					for i in range(len(self.numbers.numbers)):
						print('+', self.numbers.numbers[i][0])
						self.goal_array.append(['+',self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)]])
						break
	
			else:
				for i in range(len(self.numbers.numbers)):
					if -(self.numbers.numbers[i][0]) == amount_needed:
						if ['-',self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)]] not in self.goal_array and len(self.goal_array) == 0:
							print('-', self.numbers.numbers[i][0])
							self.goal_array.append(['-',self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)]]) # and self.get_minus_operator()
							break
					else:
						for j in range(i+1,len(self.numbers.numbers)+1):
							if -(self.numbers.numbers[i-1][0] + self.numbers.numbers[j-1][0]) == amount_needed  and len(self.goal_array) == 0:
								if ['-',self.ai_grid[int(self.numbers.numbers[i-1][1].x)][int(self.numbers.numbers[i-1][1].y)]] not in self.goal_array and ['-',self.ai_grid[int(self.numbers.numbers[j-1][1].x)][int(self.numbers.numbers[j-1][1].y)]] not in self.goal_array:
									print('-', self.numbers.numbers[i-1][0])
									print('-', self.numbers.numbers[j-1][0])
									self.goal_array.append(['-',self.ai_grid[int(self.numbers.numbers[i-1][1].x)][int(self.numbers.numbers[i-1][1].y)]])
									self.goal_array.append(['-',self.ai_grid[int(self.numbers.numbers[j-1][1].x)][int(self.numbers.numbers[j-1][1].y)]]) #change to [i][1]
				
				if len(self.goal_array) == 0:
					for i in range(len(self.numbers.numbers)):
						if (len(self.snake.body) - self.numbers.numbers[i][0]) >= 2: 
							print('-', self.numbers.numbers[i][0])
							self.goal_array.append(['-',self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)]])
							break
						else: continue
					if len(self.goal_array) == 0:
						temp = self.ai_grid[randint(2,(cell_number-3))][randint(2,(cell_number-3))]
						self.goal_array.append(['+',(temp if temp not in self.ai_snake else self.ai_grid[randint(1,(cell_number-2))][randint(1,(cell_number-2))])])
		else:
			print('adding blocks')
			temp = self.ai_grid[randint(2,(cell_number-3))][randint(2,(cell_number-3))]
			self.goal_array.append(['+',(temp if temp not in self.ai_snake else self.ai_grid[randint(1,(cell_number-2))][randint(1,(cell_number-2))])])

	def check_operator(self):
		try:	
			if self.snake.operator == self.goal_array[-1][0]: pass
			else:
				for i in range(len(self.operations.operators)):
					if self.operations.operators[i][0][0] == self.goal_array[-1][0]:
						self.goal_array.append([self.goal_array[-1][0], self.ai_grid[int(self.operations.operators[i][1].x)][int(self.operations.operators[i][1].y)]])
						break
		except: print('ERROR')
	
	def get_obsticles(self): #issue
		for i in range(0,len(self.numbers.numbers)):
			for j in self.goal_array:
				if int(self.numbers.numbers[i][1].x) != int(j[1].x) and int(self.numbers.numbers[i][1].y) != int(j[1].y):
					self.ai_grid[int(self.numbers.numbers[i][1].x)][int(self.numbers.numbers[i][1].y)].obstacle = True
		for i in range(0,len(self.operations.operators)):
			for j in self.goal_array:
				if int(self.operations.operators[i][1].x) != int(j[1].x) and int(self.operations.operators[i][1].y) != int(j[1].y):
					self.ai_grid[int(self.operations.operators[i][1].x)][int(self.operations.operators[i][1].y)].obstacle = True
		
 
	#The function reset_ai is used to reset the AI grid, snake, and direction.
	def reset_ai(self):
		# The AI grid is a 2D list of Spot objects with dimensions cell_number x cell_number
		self.ai_grid = [[Spot(i, j) for j in range(0, cell_number)] for i in range(0,cell_number)]
		# The initial AI snake is a list of three Spot objects, starting from (3,10), (4,10), and (5,10).
		self.ai_snake = [self.ai_grid[3][10], self.ai_grid[4][10], self.ai_grid[5][10]]
		# The initial AI direction is a Vector2 object with values (1,0).
		self.ai_direction = Vector2(1,0)
		# The current AI position is set to the last element of the AI snake.
		self.ai_current = self.ai_snake[-1]		
   
   		
	def update(self):
		if self.died:
			# print('SCORE:', self.score)
			self.reset_ai()
		else:
			self.snake.move_snake()  # update snakes movement
			self.check_collision()  # checks for collision
			self.check_fail()	# checks if snake runs into wall or itself
			self.get_goal() 
			self.check_operator()
			self.get_obsticles()
			# If the machine is turned on and the AI has not died, the following code runs:
			if self.machine == True and self.died == False:
				# The current food is set to a `Spot`  object.
				# print(self.goal_array[-1][1], self.goal_array[-1][1].x)
				food = self.goal_array[-1][1] # self.ai_grid[int(self.goal_array[-1][1].x)][int(self.goal_array[-1][1].y)]
				# except: food = self.ai_grid[int(self.goal_array[-1][1][0])][int(self.goal_array[-1][1][1])]
				print('food:', food.x, food.y)
				[[self.ai_grid[i][j].add_neighbours(self.ai_grid) for j in range(cell_number)] for i in range(cell_number)] # For every cell in the grid Add the neighboring cells to the current cell
						
				# The function `getpath` is called to get the AI snake's path to the food.
				try: 
					dir_array, food = self.getpath(food, self.ai_snake)
					# The last element of the path is set as the AI direction.
					self.ai_direction = dir_array.pop(-1) 
					print('food:', food.x, food.y)

				# If there is an exception
				except: 
					# Select a random cell in the grid that is not part of the snake 
					temp = self.ai_grid[randint(2,(cell_number-3))][randint(2,(cell_number-3))]
					self.goal_array.append(['+',(temp if temp not in self.ai_snake else self.ai_grid[randint(1,(cell_number-2))][randint(1,(cell_number-2))])])
					# Set the AI direction to be the same as the direction of the snake 
					self.ai_direction = self.snake.direction
					print('FORCED MOVEMENT')	
     		
				food_array = [food] 
				if self.ai_direction.y == 1:   
					self.ai_snake.append(self.ai_grid[self.ai_current.x][((self.ai_current.y + 1) if self.ai_current.y < (cell_number - 1) else 0)]) # if bound == False else self.ai_current.y + 1
					self.snake.direction = Vector2(0,1)
					print('---------------- down --------------------')
				if self.ai_direction.x == 1: 
					self.ai_snake.append(self.ai_grid[(((self.ai_current.x + 1) if self.ai_current.x < (cell_number - 1) else 0))][self.ai_current.y])
					self.snake.direction = Vector2(1,0)
					print('---------------- right --------------------')
				if self.ai_direction.y == -1: 
					self.ai_snake.append(self.ai_grid[self.ai_current.x][((self.ai_current.y - 1) if self.ai_current.y > 0 else (cell_number - 1))])
					self.snake.direction = Vector2(0,-1)
					print('---------------- up --------------------')
				if self.ai_direction.x == -1: 
					self.ai_snake.append(self.ai_grid[((self.ai_current.x - 1) if self.ai_current.x > 0 else (cell_number - 1))][self.ai_current.y])
					self.snake.direction = Vector2(-1,0)
					print('---------------- left --------------------')
				self.ai_current = self.ai_snake[-1] 
				if self.ai_current == food:
					food_array.append(food)
				self.ai_snake.pop(0)
					
			

	def heuristic(self, current1, food1, neighbour):
		#set's abs as a localised function
		_abs = abs
		#calculates the current point to goal vector
		dx1 = current1.x - food1.x
		dy1 = current1.y - food1.y
		#calculates the start to goal vector
		dx2 = self.ai_current.x - food1.x
		dy2 = self.ai_current.y - food1.y
		#calculates the cross product
		cross = _abs(dx1*dy2 - dx2*dy1)
		#calculates the heuristic without considering the cross product
		h = _abs(neighbour.x - food1.x) + _abs(neighbour.y - food1.y)
		#returns the heuristics that considers the cross product 
		return h + cross*0.001

	def new_food(self, blocked, snake1, attempts):
		temp_food = self.ai_grid[randint(2,(cell_number-3))][randint(2,(cell_number-3))]
		if temp_food in blocked or temp_food in snake1: 
			if attempts >= 3: return self.ai_grid[randint(1,(cell_number-2))][randint(1,(cell_number-2))]
			else:
				attempts += 1
				return self.new_food(blocked, snake1, attempts)		
		else: return temp_food
 

	def getpath(self,food1, snake1): 
		openset = [snake1[-1]] # sets openset to the node of the snake's head
		closedset = [] # creates a list to store closed nodes (explored nodes) called closedset 
		blocked = [] # creates a list to store nodes in or near the snake called blocked
		for segments in snake1: # for every segment of the snake
			if segments == snake1[-1]: continue # check if it's the snakes head and if so continue
			else: # if the segment is not the snakes head
				[blocked.append(neighbour) for neighbour in segments.neighbours if neighbour != snake1[-1]] #for every neighbour of that segment check if the neighbour is not in the snake then add it to the blocked list
    
		if food1 in blocked or food1 in closedset: #check if the food (goal) is too hard to get to (near snake) or in a closed node
			attempts = 0 #set a variable to track how many attempts the function takes to return a new position 
			food1 = self.new_food(blocked, snake1, attempts) # finds a new position for the food (goal) that is not blocked
   
		print('============================================================')
		for y in range(cell_number):
			for x in range(cell_number):
				print(('O' if self.ai_grid[x][y] == food1 else ('8' if self.ai_grid[x][y] in self.ai_snake else (('X' if (self.ai_grid[x][y].obstacle or (self.ai_grid[x][y] in blocked and self.ai_grid[x][y] not in self.ai_snake) or self.ai_grid[x][y] in closedset) else ' ')))), end= ("" if x < 15 else "."))
			print()
		print('============================================================')
		# 	while true check every node and determine the best / quickest path by using the f value or cost of the path
		while 1:
			current1 = min(openset, key=lambda x: x.f) # set the current node to the node with the lowest distance to the goal
			openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1] #for every node in openset check if the node in openset is not the current node then set openset to that node
			closedset.append(current1) #add current node to the list of closed node
			for neighbour in current1.neighbours: #for every neighbour of the current nodes
				if neighbour not in closedset and neighbour not in self.ai_snake and not neighbour.obstacle: # check to see if the neighbour is not blocked by the snake or surrounding nodes and check to see if it's not already explored or is a obstacle
					tempg = neighbour.g + 1 #set a temporary g value for the neighbour  
					if neighbour in openset: #if neighbour in the list of nodes
						if tempg < neighbour.g:#if the temporary g value is less than the neighbouring g value
							neighbour.g = tempg #/set the neighbouring g value to the temporary g value
					else: #if the neighbour is not in the list of nodes
						neighbour.g = tempg #set the neighbouring g value to the temporary g value
						openset.append(neighbour) #append neighbour to the list of nodes
					neighbour.h = self.heuristic(current1, food1, neighbour) #calculates the heuristic
					neighbour.f = neighbour.g + neighbour.h #calculate the f value (total)
					neighbour.camefrom = current1 #sets neighbour.camefrom to the current1 node
				else: continue
			if current1 == food1: break # if the algorithm finds the food (goal) break the loop
		blocked = [] # empty the blocked list
		return self.retrace_path(current1, food1, snake1) # get the list of directions to the goal

	def retrace_path(self, current1, food1, snake1):
		dir_array1 = []
		while current1.camefrom: 
			current1_next = self.ai_grid[(int(current1.x + self.snake.direction.x) if 0 <= int(current1.x + self.snake.direction.x) <= cell_number - 1 else (cell_number - 1 if int(current1.x + self.snake.direction.x) == 16 else (0))) if bound == True else (int(current1.x + self.snake.direction.x) if 0 <= int(current1.x + self.snake.direction.x) <= (cell_number - 1) else (cell_number - 1 if int(current1.x + self.snake.direction.x) < 0 else (cell_number - 1)))][(int(current1.y + self.snake.direction.y) if 0 <= int(current1.y + self.snake.direction.y) <= (cell_number - 1) else ((cell_number - 1) if int(current1.y + self.snake.direction.y) == 16 else (0))) if bound == True else (int(current1.y + self.snake.direction.y) if 0 <= int(current1.y + self.snake.direction.y) <= cell_number -1 else (cell_number - 1 if int(current1.y + self.snake.direction.y) < 0 else (cell_number -1)))]
			for neighbour in current1_next.neighbours: continue
			if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
				dir_array1.append(Vector2(0,-1) if int(self.snake.direction.y) != 1 else (self.snake.direction if (current1_next not in snake1) else (Vector2((current1_next.x - neighbour.x), (current1_next.y - neighbour.y)) if (neighbour not in snake1 for neighbour in current1_next.neighbours) else (Vector2(0, 1))))) # test
			elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
				dir_array1.append(Vector2(0,1) if int(self.snake.direction.y) != -1 else (self.snake.direction if (current1_next not in snake1) else (Vector2((current1_next.x - neighbour.x), (current1_next.y - neighbour.y)) if (neighbour not in snake1 for neighbour in current1_next.neighbours) else (Vector2(0, -1))))) 
			elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y: 
				dir_array1.append(Vector2(-1,0) if int(self.snake.direction.x) != 1 else (self.snake.direction if (current1_next not in snake1) else (Vector2((current1_next.x - neighbour.x), (current1_next.y - neighbour.y)) if (neighbour not in snake1 for neighbour in current1_next.neighbours) else (Vector2(1, 0))))) 
			elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
				dir_array1.append(Vector2(1,0) if int(self.snake.direction.x) != -1 else (self.snake.direction if (current1_next not in snake1) else (Vector2((current1_next.x - neighbour.x), (current1_next.y - neighbour.y)) if (neighbour not in snake1 for neighbour in current1_next.neighbours) else (Vector2(-1, 0))))) 
			current1 = current1.camefrom
   
		for i in range(cell_number):
			for j in range(cell_number):
				self.ai_grid[i][j].camefrom = []
				self.ai_grid[i][j].obstacle = False
				self.ai_grid[i][j].f = 0
				self.ai_grid[i][j].h = 0
				self.ai_grid[i][j].g = 0
		return dir_array1, food1

	def draw_elements(self):
		self.draw_grass() # draw the grass by calling upon the function
		self.operations.draw_operations() # call upon the function that draws the operations
		self.numbers.draw_numbers()
		self.snake.draw_snake()
		self.draw_score() # show the score
		self.draw_tally()
		self.draw_target()
		self.draw_operator()
		
	
  
	def check_collision(self): # temp
		i = 0
		while i < len(self.operations.operators):
			if self.operations.operators[i][1] == self.snake.body[0]: # if the apples position is equal to the first element in the snakes body (the head)  
				pos = self.operations.randomise() # call upon the randomise function to get a new position
				self.operations.operators[i][1][0] = pos.x  # sets the new x positio of the operator
				self.operations.operators[i][1][1] = pos.y # sets the new y positio of the operator
				self.snake.operator = self.operations.operators[i][0][0] # set's the snake opporator to + or -
				self.operations.check_doubles() # checks if the new location matchs another one in use
			i+=1
   
		i = 0
		while i < len(self.numbers.numbers):
			if self.numbers.numbers[i][1] == self.snake.body[0]: # checks if snake head touches a number
				self.snake.add_block(self.numbers.numbers[i][0]) # calls upon the add block function, passing through the value of the number
				self.numbers.numbers[i][0] = randint(1,9) # nets the new value of the number
				pos = self.numbers.randomise() # call upon the randomise function to get a new position
				self.numbers.numbers[i][1][0] = pos.x # sets the new x positio of the number
				self.numbers.numbers[i][1][1] = pos.y # sets the new y positio of the number
				self.numbers.check_doubles() # checks if the new location matchs another one in use

			i+=1

		if len(self.snake.body) == self.target and self.snake.new_block == False: # if the length of the snake matches the target and there are no new blocks be added or subtracted 
			self.score += 1 # add to the score
			self.target = randint(2,20) if self.machine == False else randint(2,10) # set a new target
			self.snake.colours = SEGMENTS.random_color() # change the colour of the snake
			self.snake.celebrate = True # set celebrate to True
			self.snake.colour() # call upon the colour function to colour the segments

	def check_fail(self):
		i=0 # set i to 0
		if bound == False: # if boundries are off
			while i < len(self.snake.body):  # while i is less than the number of elements in snake.body
				if not 0 <= self.snake.body[i].x < cell_number: # if snake.body.x is less than 0 or more than the number of cels
					if not 0 <= self.snake.body[i].x: self.snake.body[i].x = self.snake.body[i].x + cell_number #  if snake.body.x is less than 0 (width) add the max width to the snake.body.x to translate the snake to the opposit side
					if not self.snake.body[i].x < cell_number: self.snake.body[i].x = self.snake.body[i].x - cell_number# is snake.body.x is more thn the number of cells(width), subtract the maxwidth from snake.body.x to translate the snake to the opposit side
		
				if not 0 <= self.snake.body[i].y < cell_number: # if snake.body.x is less than 0 or more than the number of cels
					if not 0 <= self.snake.body[i].y: self.snake.body[i].y = self.snake.body[i].y + cell_number #  if snake.body.x is less than 0 (width) add the max width to the snake.body.x to translate the snake to the opposit side
					if not self.snake.body[i].y < cell_number: self.snake.body[i].y = self.snake.body[i].y - cell_number # is snake.body.x is more thn the number of cells(width) subtract the maxwidth from snake.body.x to translate the snake to the opposit side
				i=i+1 # increse i by 1
		else: # if boundries are on
			if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: self.game_over() # if the snakes head touches the walls/boundries end the game/display the you died screen
   			
		[(self.game_over(), print('head:', self.snake.body[0], 'touched',block)) for block in self.snake.body[1:] if self.snake.body[0] == block and len(self.snake.body) > 3] #for blocks in elements after the first element (for every other element other than the first) if the blocks position is equal to the head of the snake's position or the first element in the array end the game as the player has collided with themselves 
	
	def game_over(self):
		conn_db = self.data.create_db_connection(self.data.database)
		if self.db_updated == False:
			if self.machine == False: self.check_placment(conn_db,self.username)
			self.db_updated = True
		else: pass
		conn_db.close()
		self.died = True # set died to true
	
	def check_existing_player(self, conn_db):
		#check if exists, then check if score is larger then old score
		cursor = conn_db.execute('''select * from sqlite_master''')
		users = [user[0] for user in cursor.execute("SELECT username FROM high_scores")]
		scores = [score[0] for score in cursor.execute("SELECT score FROM high_scores")]
		cursor.close()
		existing_user = False
		update_score = False
		for i in range(0,len(users)): 
			if self.username == users[i]:
				existing_user = True
				user_score = scores[i]
				print(self.username, user_score)
				if user_score < self.score:
					update_score = True

		print(existing_user, update_score)
		return existing_user, update_score

            
     
	def check_placment(self, conn_db, username):
		existing_user, update_score = self.check_existing_player(conn_db) # returns true or false depending if the user exists and if so if they got a higher score
		list_scores_users = [] #creates a list that will hold users scores and usernames
		list_placement_user_score = [] #creates a list that will hold users placement, username, and score
		cursor = conn_db.execute('''select * from sqlite_master''') #creates a connection that can execute data or commands to the database 
		scores = [score[0] for score in cursor.execute("SELECT score FROM high_scores")] #cycles through everything in the scores column and adds every users score to a list
		users = [user[0] for user in cursor.execute("SELECT username FROM high_scores")] #cycles through everything in the username column and adds every users username to a list 
		cursor.close() #closes database connection
		if len(users) == 0: #if there are no users
			user_placement = 1 #set the user's placement to 1
			conn_db.execute("INSERT INTO high_scores  VALUES (?,?,?)", (user_placement, username, self.score)) #inserts the user's data into the database
		else: #if there is more than 1 user in the database		
			#append the users score to the list, list_scores_users if the user does not exist or the user exists and got a better score
			if (existing_user == False and update_score == False) or (existing_user == True and update_score == True): list_scores_users.append([self.score,username])  
			for i in range(0,len(users)): #for every user in the database
				if existing_user == True and update_score == True: # if the user exists and their new score is higher
					if users[i] != username: list_scores_users.append([scores[i], users[i]]) #if the current user in the database does not match the user then add the database user to the list, list_scores_user
					else: pass
				#if the user does not exist or does exist but their score is lower than their best then append every user to the list, list_scores_users
				if (existing_user == False and update_score == False) or (existing_user == True and update_score == False): list_scores_users.append([scores[i], users[i]])
			
     
			list_scores_users.sort(key=lambda a: a[0], reverse=True) #sort the list by using the scores
			placement = 1 #sets the placement to 1
			for i in range(0,len(list_scores_users)): # for every user in the list, list_scores_users
				try:
					if list_scores_users[:][i][0] == list_scores_users[::-1][len(list_scores_users) - (i)][0]: #compares elements in opposite positions of the list and checks if their equal
						placement = placement - 1 #subtracts 1 from placement
						list_placement_user_score.append([placement,list_scores_users[:][i][1],list_scores_users[:][i][0]]) # add the users placement, username and score to the list, list_placement_user_score
					else: list_placement_user_score.append([placement,list_scores_users[:][i][1],list_scores_users[:][i][0]]) # if they're not equal then add the users placement, username and score to the list, list_placement_user_score
				except:
					list_placement_user_score.append([placement,list_scores_users[:][i][1],(scores[i] if (scores[i] > self.score) else self.score)]) # if a users score is higher than the users score then add the placement, username and score of that user to the list, list_placement_user_score else if the user has a higher score  add the users placement, username and score to the list, list_placement_user_score
					print('error - line 1494')
				placement = placement + 1 #plus 1 to placement
			print(list_placement_user_score)
			conn_db.close() #close databse connection
			conn_db = self.data.create_db_connection(self.data.database) # connect to the database
			conn_db.execute("DROP TABLE high_scores") #delete everything in the table, high_scores
			self.data.create_table(self.data.sql_create_player_table,conn_db) #recreate the database table
			for i in range(0,len(list_placement_user_score)): #for everything in list_placement_user_score
				try:
					conn_db.execute("INSERT INTO high_scores  VALUES (?,?,?)", (list_placement_user_score[i][0], list_placement_user_score[i][1], list_placement_user_score[i][2]))  # insert each users details into the database
				except Error as e: #if an error occurs
					print(e) #print error
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print(exc_type, fname, exc_tb.tb_lineno)
		conn_db.commit() #  provides the database confirmation regarding the changes made by a user or an application in the database
		
			
		
     
	def draw_grass(self):
		grass_color = (167,209,61)  # set's the colour of the grass 
		for row in range(cell_number): # for every row in cell_number
			if row % 2 == 0:  # checks for even rows (if row is even)
				for col in range(cell_number): # for every column in cell_number
					if col % 2 == 0: # checks for even columns (if column is even)
						grass_rect = Rect(col * cell_size,row * cell_size,cell_size,cell_size) # grass demensions 
						rect(screen,grass_color,grass_rect) # draw grass
			else: # if row is not even
				for col in range(cell_number): # for every column in cell_number
					if col % 2 != 0: # if col is not even
						grass_rect = Rect(col * cell_size,row * cell_size,cell_size,cell_size) # grass demensions
						rect(screen,grass_color,grass_rect)	# draw grass		

	def draw_score(self):
		score_text = str(self.score) # set's the score to the legth of the snakes body minus (-) the starting values (3)
		score_surface = game_font.render(score_text,True,(56,74,12)) # renders the score using the specific game font declaired in a varibale and set it to grey
		name_surface = game_font.render("SCORE: ",True,(56,74,12)) # set's the title
		score_x = int((cell_size * cell_number/5)*2.75) # sets the x position of the scoring
		score_y = int(cell_size * cell_number - (cell_size * cell_number - 20)) # sets the y position of the scoring
		score_rect = score_surface.get_rect(center = (score_x,score_y)) #  creates a rectangle using the previous x and y cordinates as the center and is used to display the score
		name_rect = name_surface.get_rect(midright = (score_rect.left,score_rect.centery))	# creates a rectange for the title/name to sit left of the score rectangle while being centered vertically
		bg_rect = Rect(name_rect.left-6,name_rect.top,name_rect.width+6 + score_rect.width + 6,score_rect.height) # creates a big rectangle to include both elements
		screen.blit(score_surface,score_rect) # displays the score
		screen.blit(name_surface,name_rect) # displays the name
		rect(screen,(56,74,12),bg_rect,2) # draws the rectange with a grey colour with a width of 2px
  
	def draw_tally(self):
		tally_text = str(len(self.snake.body)) # set's the score to the legth of the snakes body minus (-) the starting values (3)
		tally_surface = game_font.render(tally_text,True,(56,74,12)) # renders the tally using the specific game font declaired in a varibale and set it to grey
		name_surface = game_font.render("TALLY: ",True,(56,74,12)) # renders the name/title using the specific game font declaired in a varibale and set it to grey
		tally_x = int(cell_size * cell_number/5) # sets the x position of the tally
		tally_y = int(cell_size * cell_number - (cell_size * cell_number - 20)) # sets the y position of the tally
		tally_rect = tally_surface.get_rect(center = (tally_x,tally_y)) #  creates a rectangle using the previous x and y cordinates as the center and is used to display the tally
		name_rect = name_surface.get_rect(midright = (tally_rect.left,tally_rect.centery)) # creates a rectange for the title/name to sit left of the score rectangle while being centered vertically
		bg_rect = Rect(name_rect.left-6,name_rect.top,name_rect.width+6 + tally_rect.width + 6,tally_rect.height) # creates a big rectangle that holds both elements
		screen.blit(tally_surface,tally_rect) # displays the tally
		screen.blit(name_surface,name_rect) # display the title
		rect(screen,(56,74,12),bg_rect,2) # draw the big ractangle
  
	def draw_target(self):
		target_text = str(self.target) # set's the score to the legth of the snakes body minus (-) the starting values (3)
		target_surface = game_font.render(target_text,True,(56,74,12)) # renders the score using the specific game font declaired in a varibale and set it to grey
		name_surface = game_font.render("TARGET: ",True,(56,74,12)) # renders the score using the specific game font declaired in a varibale and set it to grey
		target_x = int((cell_size * cell_number/5)*4.5) # sets the x position of the tally
		target_y = int(cell_size * cell_number - (cell_size * cell_number - 20)) # sets the y position of the target
		target_rect = target_surface.get_rect(center = (target_x,target_y)) #  creates a rectangle using the previous x and y cordinates as the center and is used to display the target
		name_rect = name_surface.get_rect(midright = (target_rect.left,target_rect.centery)) #  creates a rectangle using the previous x and y cordinates as the center and is used to display the title
		bg_rect = Rect(name_rect.left-6,name_rect.top,name_rect.width+6 + target_rect.width + 6,target_rect.height) # creates a big rectangle that holds both elements
		screen.blit(target_surface,target_rect) # displays the target
		screen.blit(name_surface,name_rect) # display the title
		rect(screen,(56,74,12),bg_rect,2) # draw the big rectangle
  
	def draw_operator(self):
		operator_text = self.snake.operator # set's the operator to the text to be displayed
		operator_surface = game_font.render(operator_text,True,(56,74,12)) # renders the operator using the specific game font declaired in a varibale and set it to grey
		operator_x = int(cell_size * cell_number - 20) # set's the x position
		operator_y = int(cell_size * cell_number - 20) # set's the y position
		operator_rect = operator_surface.get_rect(center = (operator_x,operator_y-2)) #  creates a rectangle using the previous x and y cordinates as the center and is used to display the operator
		screen.blit(operator_surface,operator_rect) # displays the operator
		operator_rect = operator_surface.get_rect(size=(operator_rect.width+12, operator_rect.height),center = (operator_x,operator_y)) # creates a surrounding rectangle
		rect(screen,(56,74,12),operator_rect,3) # draws the surrounding rectangle
	

pygame.mixer.pre_init(44100,-16,2,512) # presets the default mixer init arguments
pygame.init() # initialises all imported pygame modules
cell_size = 40 # sets the size of each cell to 40px
cell_number = 16 # sets the number of cells to 16
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size)) # uses the cell_size and cell_number to determine the width and height of the display
clock = pygame.time.Clock() # initialises the clock as a variable
game_font = Font('Font/PoetsenOne-Regular.ttf', 25) # declairs the font used in the game
difficulty = 120  # the difficulty of the game (the delay in screen input (lower = faster (harder)))

SCREEN_UPDATE = pygame.USEREVENT 
pygame.time.set_timer(SCREEN_UPDATE,difficulty) # updates the screen using the delay

main_game = MAIN() # set main_game to inherit Main()

wr = (cell_number*cell_size)/cell_number 
hr = (cell_number*cell_size)/cell_number

main_game.begin = False # set's begin to false
main_game.died = False # set died to false
bound = False # set bound to false
main_game.score = 0 # set's the players score to 0
db = DATA()

if __name__ == '__main__':
    db.main_db()

while True: 
	for event in pygame.event.get():	#  for event in user input
		if event.type == pygame.QUIT:   # if the exit button is presssed then quit
			pygame.quit()
			sys.exit()
   
		if event.type == SCREEN_UPDATE and main_game.begin == True:	main_game.update() # cProfile.run('main_game.update()') #	if Screen_update is called upon after the delay above then update the game update the snake and game
   
		if event.type == pygame.MOUSEBUTTONUP and main_game.begin == False: # if the users clicks on the screen and the start screen is active
			pos = pygame.mouse.get_pos() # get the position the mouse clicked
			print(pos)
			if (abs(pos[0] - 214) <= 50) and (abs(pos[1] - 520) <= 25) and main_game.done == True: main_game.begin = True # if the user clicks the play button then begin the game
    
			elif (abs(pos[0] - 426) <= 50) and (abs(pos[1] - 520) <= 25) and main_game.done == True: pygame.quit(), sys.exit()# if the user presses the quit button then quit the game
    
			elif (abs(pos[0] - 204) <= 110) and (abs(pos[1] - 215) <= 25): main_game.leaderboard = True # if the user presses the EASY button then set difficulty to easy

			elif (abs(pos[0] - 320) <= 75) and (abs(pos[1] - 595) <= 25) and main_game.leaderboard == False:
				difficulty = difficulty + 150
				main_game.target = randint(2,10)
				main_game.reset_ai()
				main_game.machine = True
				main_game.begin = True

			elif (abs(pos[0] - 130) <= 50) and (abs(pos[1] - 300) <= 25): # if the user presses the EASY button then set difficulty to easy
				difficulty = 150 # change dificulty/delay
				EASY = (27, 30, 25) # change colours
				MED = (254, 6, 255)
				HARD = (254, 6, 0)
				SCREEN_UPDATE = pygame.USEREVENT  # upadate the games delay
				pygame.time.set_timer(SCREEN_UPDATE,difficulty) 
    
			elif (abs(pos[0] - 320) <= 50) and (abs(pos[1] - 300) <= 25): # if the user presses the Medium button then set difficulty to medium
				difficulty = 120 # change difficulty/delay
				EASY = (27, 206, 25) # change colours
				MED = (27, 30, 25)
				HARD = (254, 6, 0)
				SCREEN_UPDATE = pygame.USEREVENT # upadate the games delay
				pygame.time.set_timer(SCREEN_UPDATE,difficulty) 
    
			elif (abs(pos[0] - 515) <= 50) and (abs(pos[1] - 300) <= 25): # if the user presses the HARD button then set difficulty to hard
				difficulty = 90 # change the difficulty/delay
				EASY = (27, 206, 25) # change the colours
				MED = (254, 6, 255)
				HARD = (27, 30, 25)
				SCREEN_UPDATE = pygame.USEREVENT # upadate the games delay
				pygame.time.set_timer(SCREEN_UPDATE,difficulty) 
    
			elif (abs(pos[0] - 428) <= 110) and (abs(pos[1] - 215) <= 25): # if the user presses on the boundries button then change the boundries
				if bound == False: # check if the boundries are off 
					bound = True # turn on boundries
					BOUND_TEXT = "BOUNDARIES ON" # change the text to symbolise that the boundries are turned on
					BOUND = (155,0,0) # change the texts colour
				else: # if boundries are on
					bound = False # turn the boundries off
					BOUND_TEXT = "BOUNDARIES OFF" # change the text
					BOUND = (0,0,155) # change the colour
    
		if event.type == pygame.MOUSEBUTTONUP and main_game.leaderboard == True:
			pos = pygame.mouse.get_pos() # gets the position of the click
			if (abs(pos[0] - 320) <= 50) and (abs(pos[1] - 590) <= 25): main_game.leaderboard = False
				

		if event.type == pygame.MOUSEBUTTONUP and main_game.died == True: # if the user clicks on the screen and the 'you died' screen is active
			pos = pygame.mouse.get_pos() # gets the position of the click
			if (abs(pos[0] - 214) <= 50) and (abs(pos[1] - 450) <= 25): # if the user presses the play button
				main_game.target = randint(2,20)  #reset target
				main_game.snake.reset() # reset the snake 
				main_game.reset_ai()
				main_game.machine = False
				main_game.begin = False
				main_game.died = False # set died to false to stop displaying the 'you died' screen
				main_game.db_updated = False
			elif (abs(pos[0] - 426) <= 50) and (abs(pos[1] - 450) <= 25): pygame.quit(), sys.exit()# if the user presses the quit button, quit the game
				
    
		if event.type == pygame.KEYDOWN: # if a key is pressed
			if event.key == pygame.K_ESCAPE and main_game.begin == True and main_game.died == False: main_game.pause() # if the user presses the escape button while playing the game then call upon the pause screen, pause the game
			if event.key == pygame.K_UP or event.key == pygame.K_w: # if user press' the up arrow 
				if main_game.snake.direction.y != 1: main_game.snake.direction = Vector2(0,-1)	# if snake vector is not (0,1) (snake going down) then change the snakes vector to (0,-1) (moving up) (to prevent snake from killing itself with backwards movement) 
	
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # if user press' the right arrow
				if main_game.snake.direction.x != -1: main_game.snake.direction = Vector2(1,0) # if snake vector is not (-1,0) (snake going left (user's view)) then change the snakes vector to (1,0) (moving right (user's view))
					
			if event.key == pygame.K_DOWN or event.key == pygame.K_s: # if user press' the down arrow
				if main_game.snake.direction.y != -1: main_game.snake.direction = Vector2(0,1)# if snake vector is not (0,-1) (snake going up) then change the snakes vector to (0,1) (moving down)
					
			if event.key == pygame.K_LEFT or event.key == pygame.K_a: # if user press' the left arrow
				if main_game.snake.direction.x != 1: main_game.snake.direction = Vector2(-1,0) # if snake vector is not (1,0) (snake going right (user's view)) then change the snakes vector to (-1,0) (moving left (user's view))
					
			for key, direction in (pygame.K_UP, Vector2(0,-1)), (pygame.K_RIGHT, Vector2(1,0)), (pygame.K_DOWN, Vector2(0,1)), (pygame.K_LEFT, Vector2(-1,0)): # for every key event
				if event.key == key and main_game.snake.direction == direction: main_game.snake.direction = direction # if the key the user pressed matches one of the keys and the snakes current direction is equal to on of the directions, set the snakes current direction to the direction
    
	screen.fill((175,215,70)) # fill the screen with a light green colour that if different to the one used for the grass
	if main_game.reset_password == False:
		if main_game.died == False: 
			if main_game.begin == True and main_game.done == True: 
				main_game.draw_elements() 
			else: 
				if main_game.done == False:
					main_game.log_in_screen()  
				else:
					main_game.start_screen() if main_game.leaderboard == False else main_game.leaderboard_screen()  #change to log in screen
		else: main_game.end_screen() # if they are dead display the end screen
	else: main_game.forgot_password_func()
	pygame.display.update() # update display
	clock.tick(60) # set fps to 60


