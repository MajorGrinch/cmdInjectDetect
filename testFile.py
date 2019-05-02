
from joern.all import JoernSteps

j = JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data/')

# j.addStepsDir('Use this to inject utility traversals')

j.connectToDatabase()

# query = 'g.V().getCallsTo("*cpy*")'
# query = 'g.V().queryNodeIndex("type:ExpressionStatement")'
query = "len(g.V())"

# query = 'g.V().getCallsTo("exec")'

res =  j.runGremlinQuery(query)
print(res)
# for r in res: print r