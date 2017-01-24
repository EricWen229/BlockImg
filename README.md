#BlockImg

![image](https://github.com/EricWen229/BlockImg/raw/master/demo.png)

![image](https://github.com/EricWen229/BlockImg/raw/master/blockImg.png)

---

A tiny python program that uses genetic algorithm to create image consisting of blocks

##Dependencies

* PIL (Pillow for Python 3.x)
* numpy

##Usage

    g = BlockImgGenerate()
    im = g.generate(picFilePath='demo.png', maxGeneration=4096, possiCrossover=0.05, possiVariation=0.01, blockNum=512, minBlockSize=1, maxBlockSize=5)

Parameters (all with default values):

* picFilePath: file path of input image
* maxGeneration: maximum generation before program quits
* possiCrossover: possibility of crossover
* possiVariation: possibility of variation
* blockNum: number of blocks
* minBlockSize: minimum size of blocks
* maxBlockSize: maximum size of blocks

The method returns a `PIL.Image` object for future use.

##TODO

* more colors
* more shapes

