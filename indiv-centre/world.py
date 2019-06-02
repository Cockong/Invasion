import random

class World(object):
	
	def __init__(self, w = 100, h = 100, nP = 200, nR = 200, nV = 200):
		self.w = w
		self.h = h
		self.pop = [[ Case(i,j,0,0,0) for j in range(self.w)] for i in range(self.h)]
		self.nP = nP
		self.nR = nR
		self.nV = nV
		
		self.pop[0][0].nP = nP
		
		self.pop[1][self.w -1].nR = nR
		
		self.pop[self.h -1][0].nV = nV
		
		
	def aleatoire(self,i,j):
		if i==0:
			if j==0:
				liste = [0,1,4]
			elif j==self.w -1:
				liste = [0,3,7]
			else:
				liste = [0,1,3,4,7]
		
		elif i==self.h -1:
			if j==0:
				liste = [1,2,5]
			elif j==self.w -1:
				liste = [2,3,6]
			else:
				liste = [1,2,3,5,6]
			
		elif j==0:
			liste = [0,1,2,4,5]
		
		elif j==self.w -1:
			liste = [0,2,3,6,7]
		
		else:
			liste = [0,1,2,3,4,5,6,7]
				
		return random.choice(liste)	
		
	def move_indiv(self, temp, species,  i, j):
		alea = self.aleatoire(i,j)
		if alea == 0:
			# move south
			if species == 0:
				temp[i+1][j].nP +=1
			elif species == 1:
				temp[i+1][j].nR +=1
			else:
				temp[i+1][j].nV +=1
				
		elif alea == 1:
			# move east
			if species == 0:
				temp[i][j+1].nP +=1
			elif species == 1:
				temp[i][j+1].nR +=1
			else:
				temp[i][j+1].nV +=1
				
		elif alea == 2:
			# move north
			if species == 0:
				temp[i-1][j].nP +=1
			elif species == 1:
				temp[i-1][j].nR +=1
			else:
				temp[i-1][j].nV +=1
		
		elif alea == 3:
			# move west
			if species == 0:
				temp[i][j-1].nP +=1
			elif species == 1:
				temp[i][j-1].nR +=1
			else:
				temp[i][j-1].nV +=1
		
		elif alea == 4: #south east
			if species == 0:
				temp[i+1][j+1].nP +=1
			elif species == 1:
				temp[i+1][j+1].nR +=1
			else:
				temp[i+1][j+1].nV +=1
		
		elif alea == 5: #north east
			if species == 0:
				temp[i-1][j+1].nP +=1
			elif species == 1:
				temp[i-1][j+1].nR +=1
			else:
				temp[i-1][j+1].nV +=1
		
		elif alea == 6: #north west
			if species == 0:
				temp[i-1][j-1].nP +=1
			elif species == 1:
				temp[i-1][j-1].nR +=1
			else:
				temp[i-1][j-1].nV +=1
					
		else: # (alea == 7)
			if species == 0:
				temp[i+1][j-1].nP +=1
			elif species == 1:
				temp[i+1][j-1].nR +=1
			else:
				temp[i+1][j-1].nV +=1

	
	def move(self):
		temp = [[ Case(i,j,0,0,0) for j in range(self.w)] for i in range(self.h)]
	
		for i in range(self.h):
			for j in range(self.w):
				#if !self.pop[i][j].empty:
				for n in range(self.pop[i][j].nP):
					self.move_indiv(temp,0, i, j)
				for n in range(self.pop[i][j].nR):
					self.move_indiv(temp,1, i, j)
				for n in range(self.pop[i][j].nV):
					self.move_indiv(temp,2, i, j)
		
		
		self.pop = temp
		self.count()
				
	def eat(self):
		for i in range(self.h):
			for j in range(self.w):
				self.pop[i][j].eat()
				
		self.count()
				
	def count(self):
		P =0
		R =0
		V =0
		for i in range(self.h):
			for j in range(self.w):
				P += self.pop[i][j].nP
				R += self.pop[i][j].nR
				V += self.pop[i][j].nV
				
		self.nP =P
		self.nR =R
		self.nV =V
					
class Case(object):
	
	def __init__(self, x, y, nP, nR, nV):
		self.x = x
		self.y = y
		self.nP = nP
		self.nR = nR
		self.nV = nV
		#self.empty = empty
	
		
	def eat(self):
		tempP = 0
		tempR = 0
		tempV = 0
		
		if (self.nP != 0):
			if (self.nP < self.nV):
				tempP = self.nP
			else:
				tempP = self.nV
		
		if (self.nR != 0):
			if (self.nR < self.nP):
				tempR = self.nR
			else:
				tempR = self.nP
		
		if (self.nV != 0):
			if (self.nV < self.nR):
				tempV = self.nV
			else:
				tempV = self.nR
		
		self.nP = self.nP + tempP - tempR
		self.nR = self.nR + tempR - tempV
		self.nV = self.nV + tempV - tempP
		
if __name__ == "__main__":
	myworld = World(3,3,2,2,2)
	
	print(myworld)
	myworld.move()
	myworld.eat()