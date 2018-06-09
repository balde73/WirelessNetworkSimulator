from classes import NodeController
from classes import TransmissionController
from classes import StatsController
from classes import Simulator
import sys
from init import Init as init
from font import colors

syms = ['\\', '|', '/', '-']
bs = '\b'
file_name = 'stats'

def main():

	init.config()
	stats_ctrl = StatsController( file_name )

	node_ctrl = NodeController()
	node_ctrl.create_nodes()
	node_ctrl.find_all_neighbours()

	print("> Inizio simulazione ")

	for i, gamma in enumerate(init.GAMMA):
		perc_done = int((i+1)/len(init.GAMMA)*100)
		print("\b> "+str(gamma)+" \t\t "+str(perc_done)+"%")
		for a in range(0, init.SIMULATION_REPETITION):

			transmission_ctrl = TransmissionController( gamma )

			simulation = Simulator( node_ctrl, transmission_ctrl, gamma )
			simulation.initialize()

			while( not simulation.finish() ):
				simulation.step()

			stats_ctrl.process( node_ctrl, gamma, a )
			node_ctrl.clear();

			sys.stdout.write("\b%s" % syms[ a % len(syms) ])
			sys.stdout.flush()

	print("\b" + colors.OKGREEN + " Simulazione conclusa" + colors.ENDC)
	print("Ho creato il file: " + colors.OKGREEN + file_name + ".svg" + colors.ENDC)
	print("Ho creato il file: " + colors.OKGREEN + file_name + "-nodes.svg" + colors.ENDC)

if __name__ == "__main__":
	main()
