# DEBUG API
# A debug module with some useful features.

# Import some time modules.
from time import strftime, localtime

# LOG function:
def log(arg):
	print('* {} * {};'.format(strftime("%m/%d/%Y, %H:%M:%S", localtime()), arg))