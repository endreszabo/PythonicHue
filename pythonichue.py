#!/usr/bin/env python
from bridge import Bridge

from config import bridges

if __name__ == '__main__':
	for bridge in bridges:
		bridge = Bridge(**bridge) #feels so perl :3
		with open(bridge.name+'.py','w') as out:
			print('#!/usr/bin/env python',file=out)
			print('from hue import *',file=out)
			print('from bridge import Bridge',file=out)
			print('import pythonichue',file=out)
			print(bridge.to_python(), file=out)
			print('bridge.commit()',file=out)
			#print(bridge.to_python())
else:
    print(1)
    pass


