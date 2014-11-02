from src import parse

__author__ = 'deepak'

f = "/home/deepak/workspace/slob/WebContent/SecOntV2.owl"

subc, superc, eqc = parse(f)


print subc['Threat']
print superc['Threat']
print eqc['Threat']