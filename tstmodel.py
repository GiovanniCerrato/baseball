from model.model import Model

mymodel = Model()

mymodel.getSquadreAnno(2012)
mymodel.buildGraph()

v0 = mymodel.getRandomNode()
path, score = mymodel.getPathV2(v0)
print(*(f"\n{n}" for n in path))
print(score)