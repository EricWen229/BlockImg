from PIL import Image, ImageDraw, ImageFilter
from random import randint, random, uniform

import numpy as np

'''class GaussianBlur(ImageFilter.Filter):

	name = "GaussianBlur"

	def __init__(self, radius=2):
		self.radius = radius

	def filter(self, image):
		return image.gaussian_blur(self.radius)'''

###

class Block:

	def __init__(self, pos, size):
		self.pos = pos
		self.size = size

###

class Individual:

	def __init__(self, size, blockNum=512, minBlockSize=1, maxBlockSize=1, blocks=None):
		self.size = size
		if blocks == None:
			self.blocks = []
			for i in range(blockNum):
				randX = randint(0, size[0] - 1)
				randY = randint(0, size[1] - 1)
				randBlockSize = uniform(minBlockSize, maxBlockSize)
				self.blocks.append(Block(pos=(randX, randY), size=randBlockSize))
		else:
			self.blocks = blocks

	def generateImg(self):
		newImg = Image.new(mode='L', size=self.size, color=255)
		newDraw = ImageDraw.Draw(newImg)
		for block in self.blocks:
			posX, posY = block.pos
			x0 = posX - block.size
			y0 = posY - block.size
			x1 = posX + block.size
			y1 = posY + block.size
			newDraw.rectangle(xy=[x0, y0, x1, y1], outline=0, fill=0)
		return newImg

###

class BlockImgGenerate:

	# default parameters
	d_imgFilePath = 'img.png'
	d_maxGeneration = 256
	d_possiCrossover = 0.25
	d_possiVariation = 0.125
	d_blockNum = 512
	d_minBlockSize = 0.5
	d_maxBlockSize = 2
	#d_blurRadius = 1

	# internal parameters
	i_populationSize = 16
	i_zoomRatio = 2

	def __init__(self):
		pass

	def calFitness(self, master, pop):
		fitness = []
		masterArray = np.asarray(master)
		for i in pop:
			iPic = i.generateImg()
			#iPic = iPic.filter(GaussianBlur(radius=self.d_blurRadius))
			iArray = np.asarray(iPic.resize((int(iPic.size[0]/self.i_zoomRatio), int(iPic.size[1]/self.i_zoomRatio))))
			diffArray = masterArray - iArray
			diffArraySq = diffArray ** 2
			diff = np.sum(diffArraySq)
			fitness.append(diff)
		minDiff = min(fitness)
		fitness = list(map(lambda x:x-minDiff, fitness))
		maxDiff = max(fitness)
		fitness = list(map(lambda x:maxDiff-x, fitness))
		sumDiff = sum(fitness)
		if sumDiff > 0:
			fitness = list(map(lambda x:float(x)/sumDiff, fitness))
		accFitness = []
		acc = 0.0
		for f in fitness:
			acc += f
			accFitness.append(acc)
		accFitness[-1] = 1.0
		return (fitness, accFitness)

	def selectRandom(self, pop, accFitness):
		rand = random()
		selected = None
		for i in range(0, len(pop)):
			if rand < accFitness[i]:
				selected = pop[i]
				break
		return selected

	def crossOver(self, a, b, possiCrossover):
		aBlocks = a.blocks
		bBlocks = b.blocks
		cBlocks = []
		dBlocks = []
		for i in range(len(aBlocks)):
			rand = random()
			if rand < possiCrossover:
				# exchange
				cBlocks.append(bBlocks[i])
				dBlocks.append(aBlocks[i])
			else:
				# inherit
				cBlocks.append(aBlocks[i])
				dBlocks.append(bBlocks[i])
		return (Individual(size=a.size, blocks=cBlocks), Individual(size=b.size, blocks=dBlocks))

	def variation(self, i, possiVariation, size, minBlockSize, maxBlockSize):
		for k in range(len(i.blocks)):
			rand = random()
			if rand < possiVariation:
				randX = randint(0, size[0] - 1)
				randY = randint(0, size[1] - 1)
				randBlockSize = uniform(minBlockSize, maxBlockSize)
				i.blocks[k] = Block(pos=(randX, randY), size=randBlockSize)
		return i

	def generate(self, picFilePath=d_imgFilePath, maxGeneration=d_maxGeneration, possiCrossover=d_possiCrossover, possiVariation=d_possiVariation, blockNum=d_blockNum, minBlockSize=d_minBlockSize, maxBlockSize=d_maxBlockSize):
		# read picture
		master = Image.open(picFilePath)

		# preprocess
		master = master.convert('L')
		size = master.size
		master = master.resize((int(size[0]/self.i_zoomRatio), int(size[1]/self.i_zoomRatio)))
		#master = master.filter(GaussianBlur(radius=self.d_blurRadius))

		# initialize population
		currGeneration = 0
		pop = []
		for i in range(self.i_populationSize):
			pop.append(Individual(size=size, blockNum=blockNum, minBlockSize=minBlockSize, maxBlockSize=maxBlockSize))

		# generation loop
		while currGeneration < maxGeneration:
			currGeneration += 1
			print('current generation: ' + str(currGeneration))
			fitness, accFitness = self.calFitness(master, pop)
			maxFitness = 0
			index = 0
			for i in range(len(fitness)):
				if fitness[i] > maxFitness:
					maxFitness = fitness[i]
					index = i

			#if currGeneration % 512 == 0:
				#pop[index].generateImg().show()

			newPop = []
			newPop.append(pop[index]) # elite strategy: keep the best individual
			currPopulationSize = 1

			# population loop
			while currPopulationSize < self.i_populationSize:
				a = self.selectRandom(pop, accFitness)
				b = self.selectRandom(pop, accFitness)
				c, d = self.crossOver(a, b, possiCrossover)
				c = self.variation(c, possiVariation, size, minBlockSize, maxBlockSize)
				d = self.variation(d, possiVariation, size, minBlockSize, maxBlockSize)
				newPop.append(c)
				newPop.append(d)
				currPopulationSize += 2

			'''pop.extend(newPop)
			totalFitness, totalAccFitness = self.calFitness(master, pop)
			fitnessTuples = list(zip(totalFitness, pop))
			fitnessTuples = sorted(fitnessTuples, key=lambda x:x[0], reverse=True)
			fitnessTuples = fitnessTuples[0:self.i_populationSize]
			fitnessTuples = list(zip(*fitnessTuples))
			pop = list(fitnessTuples[1])'''

			pop = newPop

		maxFitness = 0
		index = 0
		for i in range(len(fitness)):
			if fitness[i] > maxFitness:
				maxFitness = fitness[i]
				index = i
		return pop[index].generateImg()

if __name__ == '__main__':
	g = BlockImgGenerate()
	im = g.generate(picFilePath='demo.png', maxGeneration=4096, possiCrossover=0.05, possiVariation=0.01, blockNum=512, minBlockSize=1, maxBlockSize=5)
	im.save('blockImg.png')
	print('image saved to \'blockImg.png\'')
