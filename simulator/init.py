import argparse
import test
from font import colors
import numpy

# PLEASE NOTE:
# UNITS:
# time: seconds
# information: bytes
# speed: bytes/seconds

class Init(object):

	POINTS = [
		(0.714, 0.341),
		(0.941, 0.266),
		(0.211, 0.351),
		(0.654, 0.153),
		(0.203, 0.145),
		(0.45, 0.117),
		(0.935, 0.524),
		(0.394, 0.239),
		(0.786, 0.361),
		(0.024, 0.146)
	]

	BOUNDS = 0.25

	QUEUE_SIZE = 40

	SIMULATION_REPETITION = 10

	MAX_TIME = 30

	# dinamic time is an experimental feature that change the MAX_TIME considering the inter-arrival time.
	# Different max_time for every gamma. Set DYNAMIC_TIME = 1000 means int(gamma * 1000)
	DYNAMIC_TIME = 0

	# Transmission dimension
	P = 0.843
	N = 7111

	# BYTES UNITS
	MIN_SIZE = 32
	MAX_SIZE = 7143

	#MIN_SIZE = 6026
	#MAX_SIZE = 6026

	# Inter arrival time distribution
	a = numpy.arange(0.003, 0.01, 0.001)
	b = numpy.arange(0.01, 0.04, 0.0025)
	c = [0.04, 0.05, 0.07, 0.2, 0.5, 2, 100]
	GAMMA = sorted(list(set().union(a,b,c)))

	# GAMMA = [ 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.0125, 0.015, 0.02, 0.025, 0.0275, 0.03, 0.04, 0.05, 
	# 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.5, 1, 2, 100]

	# SPEED (bytes / seconds)
	SPEED = 1000000

	# -------------------------------------------- #
	# ---------------- DEBUG MODE ---------------- #
	# -------------------------------------------- #
	# set DEBUG = 1 to enter debug mode
	# explore test.py file to find some usefull tests or create new ones.

	DEBUG = 0
	VERBOSE = 0

	MAX_DEBUG_COUNT = 2

	DEBUG_POINTS = test.NODE_3_NEAR_1_2

	DEBUG_COUNT = [
	  0,
	  0,
	  0
	]

	DEBUG_TRANSMISSION = test.DEBUG_TRANSMISSION_7

	@classmethod
	def max_time( self, gamma ):
		if self.DYNAMIC_TIME:
			return int(gamma * self.DYNAMIC_TIME)
		else:
			return self.MAX_TIME

	@classmethod
	def config( self ):

		parser = argparse.ArgumentParser(description='Process some integers.')
		parser.add_argument('-g', '--gammas',
							nargs='+',
							type=float,
							help="Array of gamma values")
		parser.add_argument('-rg', '--repeat',
							nargs=1,
							type=int,
							help="Number of repetition for every gamma value")
		parser.add_argument('-vb', '--verbose',
							action='store_true',
							help="Print the output in console for every step")
		parser.add_argument('-t', '--time',
							nargs=1,
							type=int,
							help="Time (in seconds) at which stop the simulation")
		parser.add_argument('-dt', '--dynamictime',
							nargs=1,
							type=int,
							help="Dynamic time (in repetition) at which stop the simulation")
		parser.add_argument('-nodb', '--nodebug',
							action='store_true',
							help="Ignore the debug flag")
		parser.add_argument('-db', '--debug',
							action='store_true',
							help="Start a default debug test")

		config = parser.parse_args()

		if( config.gammas ):
			self.GAMMA = config.gammas
		if( config.repeat ):
			self.SIMULATION_REPETITION = config.repeat[0]
		if( config.time ):
			self.MAX_TIME = config.time[0]
		if( config.dynamictime ):
			self.DYNAMIC_TIME = config.dynamictime[0]
		if( config.verbose ):
			self.VERBOSE = config.verbose
		if( config.debug ):
			self.DEBUG = 1
			self.MAX_DEBUG_COUNT = 2
			self.DEBUG_POINTS = test.NODE_3_NEAR_1_2
			self.DEBUG_TRANSMISSION = test.DEBUG_TRANSMISSION_7
		if( config.nodebug ):
			self.DEBUG = not config.nodebug

		if(self.DEBUG):
			self.DYNAMIC_TIME = 0
			self.MAX_TIME = 1000
			self.GAMMA = [1]

		# cleaning GAMMAS
		self.GAMMA = [round(gamma, 3) for gamma in self.GAMMA]

		if(not self.DEBUG):
			print(colors.WARNING + "[-] Gamma: " +(' '.join(str(e) for e in self.GAMMA)) + colors.ENDC)
			print(colors.WARNING + "[-] Repetition for every gamma: " +str(self.SIMULATION_REPETITION) + colors.ENDC)
			if(not self.DYNAMIC_TIME):
				print(colors.WARNING + "[-] Time for every repetition: " +str(self.MAX_TIME) + "s" + colors.ENDC)
			else:
				print(colors.WARNING + "[-] Time dynamic enabled: " +str(self.MAX_TIME)+colors.ENDC)
		else:
			print(colors.WARNING + "[-] DEBUG MODE ENABLED! Disable it in the init.py file or using -nodb flag"+colors.ENDC)
