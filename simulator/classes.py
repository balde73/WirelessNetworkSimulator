# ----------------------------- #
# ---------- CLASSES ---------- #
# ----------------------------- #

from __future__ import division

# libs #
import queue
import math
import heapq
from numpy.random import randint
from numpy.random import exponential
from numpy.random import binomial

# print formatting #
from tabulate import tabulate

# my libs #
from init import Init as init

class Node(object):

	def __init__( self, x, y, node_id ):
		self.node_id 	= node_id
		self.x 			= x
		self.y 			= y
		self.neighbours = []
		self.queue 		= queue.Queue( init.QUEUE_SIZE )
		self.status 	= 'idle'

		# collision handling
		self.occupied_until 			= -1
		self.occupied_transmitting_until = -1
		self.last_idle_transmission 	= None

		# distribution inter arrival time
		self.last_prepare_transmission = 0

		# stats
		self.colliding 				= 0
		self.send_collision 		= [ 0, 0 ]
		self.receive_collision = [ 0, 0 ]
		self.send_general 			= [ 0, 0 ]
		self.receive_general  	= [ 0, 0 ]
		self.losses 					= [ 0, 0 ]
		self.load          		= [ 0, 0 ]

	def __str__(self):
		return 	"NODE id:%s occupied_until:%s neighbour:%s" % (self.node_id, self.occupied_until, self.stamp_neighbours())

	def __addNeighbour( self, neighbour ):
		self.neighbours.append( neighbour )

	def __isNeighbour( self, neighbour ):
		distance = math.hypot(self.x-neighbour.x, self.y-neighbour.y)
		if (distance <= init.BOUNDS):
			return 1
		return 0

	def get_id( self ):
		return self.node_id

	def __isMe( self, node_id ):
		return self.node_id == node_id

	def find_neighbours( self, nodes ):
		for node in nodes:
			if self.__isNeighbour( node ) and not self.__isMe( node.get_id() ):
				self.__addNeighbour( node )

	def stamp_neighbours( self ):
		str_neighbours = ""
		for n in self.neighbours:
			str_neighbours += str(n.node_id)+" "
		return str_neighbours

	def update_load( self, transmission ):
		self.load[0] += 1
		self.load[1] += transmission.size

	# metodi di transmissione
	def update_last_prepare_transmission( self, time ):
		self.last_prepare_transmission = time

	def is_idle_at_time( self, time ):
		return self.occupied_until < time

	def can_transmit( self, time ):
		
		if( self.is_idle_at_time( time ) ):
			return 1
		else :
			# allow transmission happening at the same point in time
			# receiving from another node and transmitting at the same time
			t_last = self.last_idle_transmission
			if( self.get_status()!="transmitting" and t_last and t_last.start_time == time and not self.__isMe( t_last.node_id ) ):
				# collision!! I'm receiving and transmitting at the same point in time. Cannot prevent it :(
				return 1
			return 0

	def add_to_queue( self, transmission ):
		if( not self.__queueIsFull() ):
			self.queue.put_nowait( transmission )
		else:
			self.losses[0] += 1
			self.losses[1] += transmission.size

	def get_from_queue( self, wake_up ):
		transmission = self.queue.get_nowait()
		transmission.reset_time( wake_up.start_time )
		return transmission

	def queue_is_empty( self ):
		return self.queue.empty()

	def __queueIsFull( self ):
		return self.queue.full()

	# status
	def set_status( self, status ):
		self.status = status

	def get_status( self ):
		return self.status

	def remove_sended_transmission(self, t):
		if( init.VERBOSE ):
			print("update send stats of node: ", self.get_id(), " removing ", t.size, "bytes")
		self.send_collision[0] += 1
		self.send_collision[1] += t.size

	def remove_received_transmission( self, t ):
		if( init.VERBOSE ):
			print("update received stats of node: ", self.get_id(), " removing ", t.size, "bytes from node ", t.node_id)
		self.receive_collision[0] += 1
		self.receive_collision[1] += t.size

	def is_colliding( self ):
		return self.colliding

	def get_last_idle_transmission( self ):
		return self.last_idle_transmission

	def transmit( self, t ):
		if( not self.is_idle_at_time( t.start_time ) ):
			# collision. Transmitting and receiving at the same time
			self.colliding = 1
		else:
			self.colliding = 0
			self.last_idle_transmission = t
		self.status = "transmitting"
		self.occupied_transmitting_until = t.end_time

		self.send_general[0] += len(self.neighbours)
		self.send_general[1] += t.size * len(self.neighbours)
		self.set_occupied_time( t.end_time )

	def receive( self, t ):
		self.receive_general[0] += 1
		self.receive_general[1] += t.size

		if(self.status == "idle"):
			self.status = "receiving"

		if( not self.is_idle_at_time( t.start_time ) ):
			self.colliding = 1
		else:
			self.colliding = 0
			self.last_idle_transmission = t

		self.set_occupied_time( t.end_time )

	def set_occupied_time( self, end ):
		if( end > self.occupied_until ):
			self.occupied_until = end

	def update_state_at_time( self, time ):
		if( self.is_idle_at_time(time) ):
			self.status = "idle"
			self.colliding = 0
		elif( self.occupied_transmitting_until < time ):
			# if not transmitting then i'm busy receiving
			self.status = "receiving"

	# clear
	def clear( self ):
		self.queue = queue.Queue( init.QUEUE_SIZE )
		self.status = 'idle'

		# collision handling
		self.occupied_until = -1
		self.last_idle_transmission = None

		# distribution inter arrival time
		self.last_prepare_transmission = 0

		# stats
		self.colliding 				= 0
		self.send_collision 		= [ 0, 0 ]
		self.receive_collision = [ 0, 0 ]
		self.send_general 			= [ 0, 0 ]
		self.receive_general 	= [ 0, 0 ]
		self.losses 					= [ 0, 0 ]
		self.load          = [ 0, 0 ]

	def as_dict( self ):
		return {
			"node_id": self.node_id,
			"x": self.x,
			"y": self.y,
			"occupied_until": self.occupied_until,
			"is_colliding": self.colliding,
			"send_general": self.send_general[1],
			"send_collision": self.send_collision[1],
			"queue_size": self.queue.qsize(),
			"neighbours": [node.get_id() for node in self.neighbours],
			"status": self.status
		}


class NodeController(object):
	def __init__( self ):
		self.points = init.DEBUG_POINTS if init.DEBUG else init.POINTS
		self.nodes 	= []

	def __str__(self):
		header = ['Id', 'state', 'send_col', 'rec_col', 'send_gen', 'rec_gen', 'losses']
		infos = []
		for node in self.nodes :
			send_real = node.send_general[1] - node.send_collision[1]
			info = [ node.node_id, node.status, node.send_collision, node.receive_collision, node.send_general, node.receive_general, node.losses ]
			infos.append( info )

		if( init.VERBOSE ):
			print(tabulate( infos, headers=header, tablefmt='orgtbl' ))
		return "-----------"

	def create_nodes( self ):
		for node_id, point in enumerate(self.points):
			node = Node( point[0], point[1], node_id )
			self.nodes.append( node )

	def find_all_neighbours( self ):
		for node in self.nodes:
			node.find_neighbours( self.nodes )

		if( init.VERBOSE ):
			for node in self.nodes:
				print( node )
				node.stamp_neighbours( )

	def get_nodes( self ):
		return self.nodes

	def get_node( self, node_id ):
		return self.nodes[node_id]

	def get_dict_nodes( self ):
		return [node.as_dict() for node in self.nodes]

	def clear( self ):
		for node in self.nodes:
			node.clear()


class Transmission(object):
	def __init__( self, node, gamma, last_prepare_transmission ):
		self.size = self.__calculateSize()
		self.duration = self.__getDuration()
		self.start_time = last_prepare_transmission + self.__getStart( gamma )
		self.end_time = self.start_time + self.duration
		self.node = node
		self.node_id = node.node_id
		self.type = "standard"

	def __str__(self):
		return 	"<TRANSMISSION node:%s start:%s end:%s d:%s>" % (self.node_id, self.start_time, self.end_time, self.size)

	def __calculateSize( self ):
		size = binomial(init.N, init.P) + init.MIN_SIZE
		return size if size <= init.MAX_SIZE else init.MAX_SIZE

	def __getDuration( self ):
		return self.size / init.SPEED

	def __getStart( self, gamma ):
		return exponential( gamma )

	def reset_time( self, time ):
		self.start_time = time
		self.end_time = self.start_time + self.duration

	def __lt__(self, other):
		return self.start_time < other.start_time

	def as_dict(self):
		return {
			"size": self.size,
			"duration": self.duration,
			"start_time": self.start_time,
			"end_time": self.end_time,
			"node_id": self.node_id,
			"type": self.type
		}

class FakeTransmission( Transmission ):
	def __init__( self, node, start_time ):
		self.size = 1
		self.duration = 1
		self.start_time = start_time + self.get_random_delay()
		self.end_time = self.start_time + 0.01
		self.node = node
		self.node_id = node.node_id
		self.type = "wake_up"

	def __lt__(self, other):
		return self.start_time < other.start_time

	def __str__(self):
		return 	"<WAKEUP_EVENT node:%s start:%s>" % (self.node_id, self.start_time)

	def get_random_delay(self):
		#i = randint(10000) / 1000000
		#i += 0.001
		#return i

		# not random for our implementation!
		return 0.00000000001

	def as_dict(self):
		return {
			"size": self.size,
			"duration": self.duration,
			"start_time": self.start_time,
			"end_time": self.end_time,
			"node_id": self.node_id,
			"type": self.type
		}

class DebugTransmission( Transmission ):

	def __init__( self, node ):
		conta = init.DEBUG_COUNT[node.node_id]
		if conta < len(init.DEBUG_TRANSMISSION[node.node_id]):
			data = init.DEBUG_TRANSMISSION[node.node_id][conta]

			self.size = data[1]
			self.duration = self.__getDuration()
			self.start_time = data[0]
			self.end_time = self.start_time + self.duration
			self.node = node
			self.node_id = node.node_id
			self.type = "debug"

			# update debug counter
			init.DEBUG_COUNT[node.node_id] += 1
		else:
			# out of MAX_TIME: will be ignored
			self.start_time = init.MAX_TIME + 10
			self.end_time = init.MAX_TIME + 100

	def __str__(self):
		return 	"<TRANSMISSION node:%s start:%s end:%s size:%s>" % (self.node_id, self.start_time, self.end_time, self.size)

	def __getDuration( self ):
		return self.size / init.SPEED

	def reset_time( self, time ):
		self.start_time = time
		self.end_time = self.start_time + self.duration

	def as_dict(self):
		return {
			"size": self.size,
			"duration": self.duration,
			"start_time": self.start_time,
			"end_time": self.end_time,
			"node_id": self.node_id,
			"type": self.type
		}

class TransmissionController(object):
	def __init__( self, gamma ):
		self.gamma = gamma
		self.transmission_list = []
		return

	def prepare_transmission( self, node ):
		if( not init.DEBUG ):
			t = Transmission( node, self.gamma, node.last_prepare_transmission )
		else:
			t = DebugTransmission( node )

		if(t.end_time < init.max_time(self.gamma)):
			node.update_load( t )
			node.update_last_prepare_transmission( t.start_time )

			# la aggiungo alla coda
			self.add_transmission( t )

	def prepare_wake_up( self, node ):
		if( init.VERBOSE ):
			print("node to wakeup: %s" % node)
		t = FakeTransmission( node, node.occupied_until )
		
		# la aggiungo alla coda
		self.add_transmission( t )

	def get_all_transmission( self ):
		return self.transmission_list

	def add_transmission( self, transmission ):
		heapq.heappush( self.transmission_list, ( transmission.start_time, transmission ) )

	def pop_transmission( self ):
		obj = heapq.heappop( self.transmission_list )
		return obj[1]

	def is_empty( self ):
		return self.transmission_list == []

	def get_dict_transmission( self ):
		return [task[1].as_dict() for task in self.transmission_list]


class Simulator(object):
	def __init__( self, node_ctrl, transmission_ctrl, gamma ):
		self.node_ctrl = node_ctrl
		self.transmission_ctrl = transmission_ctrl
		self.timer = 0
		self.gamma = gamma

	def initialize( self ):
		for node in self.node_ctrl.nodes:
			self.transmission_ctrl.prepare_transmission( node )

	def update_nodes_status(self, time):
		for node in self.node_ctrl.nodes:
			node.update_state_at_time( time )

	def step( self ):

		status = ''

		t = self.transmission_ctrl.pop_transmission()
		node = t.node
		connection_type = t.type

		self.update_nodes_status(t.start_time)

		if( node.can_transmit( t.start_time ) ):
			status = "transmitting"

			if( connection_type == "wake_up" ):
				# override with transmission in the queue
				status = "wakeup - "+status
				t = node.get_from_queue( t )

			if( not node.is_idle_at_time(t.start_time) ):
				# transmitting while receiving
				if( not node.is_colliding() ):
					# invalidate previous transmission
					t_last = node.get_last_idle_transmission()
					t_last.node.remove_sended_transmission( t_last )
					node.remove_received_transmission( t_last )
			node.transmit( t )

			if( connection_type == "wake_up" and not node.queue_is_empty() ):
					self.transmission_ctrl.prepare_wake_up( node )

			neighbours = node.neighbours
			for neighbour in neighbours:
				if( not neighbour.is_idle_at_time( t.start_time ) ):
					node.remove_sended_transmission( t )
					neighbour.remove_received_transmission( t )
					if( not neighbour.is_colliding() and neighbour.get_status()=="receiving"):
						t_last = neighbour.get_last_idle_transmission()
						t_last.node.remove_sended_transmission( t_last )
						neighbour.remove_received_transmission( t_last )
				neighbour.receive(t)
		else:
			status = "cannot transmit: delay"
			if( node.queue_is_empty() or (connection_type == "wake_up" and not node.queue_is_empty()) ):
				# add a fake transmission to retry later
				self.transmission_ctrl.prepare_wake_up( node )

			if( connection_type != "wake_up" ): # if not already in the queue
				node.add_to_queue( t )

		if( init.VERBOSE ):
			print(status)
			print(t)
			print( self.node_ctrl )

		# add next transmission for node: <node> if it was not a wakeup event
		if( connection_type != "wake_up" ):
			self.transmission_ctrl.prepare_transmission( node )

		return (status, t)

	def finish( self ):
		# check if simulation is finished
		if(self.transmission_ctrl.is_empty()):
			return 1
		t = self.transmission_ctrl.transmission_list[0][1]
		# if next transmission is out of MAX_TIME then stop simulation
		return t.end_time > init.max_time(self.gamma)

class StatsController(object):

	def __init__( self, file ):
		# open file to save statistics
		self.file_node = open( file+"_nodes.csv", "w" )

		# headers
		self.file_node.write( 'gamma,repetition,node,sim_time,num_nodes,offered,sent,load,losses,perc_success\n' )

	def process( self, node_ctrl, gamma, repetition ):
		stats_node = []
		for node in node_ctrl.nodes:

			perc = node.send_general[1] - node.send_collision[1]
			if( perc > 0 ):
				perc = perc / node.send_general[1]
			else:
				perc = 0

			send_real = node.send_general[1] / len(node.neighbours)
			send_correct = send_real * perc
			time = init.max_time(gamma)

			stats_node = [
				gamma,
				repetition,
				node.node_id,
				time,
				len(init.POINTS),
				send_real,
				send_correct,
				node.load[1],
				node.losses[1],
				perc
			]

			self.file_node.write( ",".join(str(x) for x in stats_node) )
			self.file_node.write( '\n' )

	def close( self ):
		self.file_node.close()
