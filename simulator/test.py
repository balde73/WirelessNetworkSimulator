POINTS_1_2_3_CLOSE = [
  (0.340, 0.500),
  (0.380, 0.500),
  (0.420, 0.500)
]

DEBUG_COUNT = [
  0,
  0,
  0
]

# (start_time (s), size (bytes)) #
DEBUG_TRANSMISSION_0 = [
  [
    (0.20, 100000),
    (0.25, 100000),
    (0.28, 100000)
  ],
  [
    (0.25, 100000),
    (0.70, 100000),
    (0.90, 100000)
  ],
  [
    (0.22, 100000),
    (0.40, 100000),
    (0.90, 100000)
  ]
]


# test: all node talk at the same time
# all transmission collide
DEBUG_TRANSMISSION_1 = [
  [
    (0.20, 100),
    (0.25, 100)
  ],
  [
    (0.20, 100),
    (0.25, 100)
  ],
  [
    (0.20, 100),
    (0.25, 100),
    (0.98, 1000000)
  ]
]

# debugging node1 is already trasmitting.
# node 1 try to talk again but cannot because is trasmitting. Delay transmission

DEBUG_TRANSMISSION_2 = [
  [
    (0.20, 100000),
    (0.21, 1000)
  ],
  [],
  []
]

# debugging node1 is already trasmitting. Delay transmission for node1 and node2. They will collide!
# EXPECTED BEHAVIOUR
# Node_1 transmits from 0,2 to 0,3
# Node_1 try to transmit but is already transmitting. So put in the queue and delays
# Node_2 try to transmit but is already receiving. So put in the queue and delays
# Node_1 and Node_2 transmit at the same time 0,3 and collide

DEBUG_TRANSMISSION_3 = [
  [
    (0.20, 100000),
    (0.21, 100) #this will be delayed and will collide
  ],
  [
    (0.22, 100), #this will be delayed and will collide
  ],
  []
]
 
# debugging if queue is working as expected
# EXPECTED BEHAVIOUR:
# node 1 trasmitting first trasmission
# node 1 try to trasmit at 0.221s but is already transmitting. Add to queue
# node 1 try to trasmit at 0.222s but is already transmitting. Add to queue
# node 1 try .........
# node 1 wakes up at time 0.3s since his status changed from transmitting to waiting
# node 1 has transmission in his queue, it's waiting so it's transmits
# node 1 wakes up again since his status changed from transmitting to waiting
# node 1 has ....
# NODE 1 SHOULD BE ABLE TO TRANSMIT EVERY PACKET THANKS TO HIS QUEUE

DEBUG_TRANSMISSION_4 = [
  [
    (0.20, 100000), #occupy the network for some time (from 0.2s to 0.3s)
    (0.221, 1),
    (0.222, 1),
    (0.223, 1),
    (0.224, 1),
    (0.225, 1),
    (0.226, 1),
    (0.227, 1),
    (0.228, 1),
    (0.229, 1),
    (0.230, 1),
    (0.231, 1),
    (0.232, 1),
    (0.233, 1),
    (0.234, 1),
    (0.235, 1),
    (0.236, 1),
    (0.237, 1),
    (0.238, 1),
    (0.239, 1),
    (0.240, 1)
  ],
  [], #node2 does nothing
  []  #node3 does nothing
]

# debugging queue is full and network is occupy! losing packets
# EXPECTED BEHAVIOUR: node1 trasmits first packet. Then try to trasmits other packets but cannot because is already trasmitting so put the packet in the queue.
# Continue to put packets in queue since queue is full, then lose packets.
# After, transmit every packet in the queue

DEBUG_TRANSMISSION_5 = [
  [
    (0.20, 500000), #occupy the network for a long time
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1),
    (0.22, 1)
  ],
  [],
  []
]


# Use this in combination with NODE_3_NEAR_1_2 meaning node 3 is near node 1 and 2 but 1 and 2 are far away
# Example   1 ------ 3 ------- 2
# Node1 transmits (from 0.2s to 0.3s)
# Node3 cannot transmit (is receaving) so delays his transmission
# Node2 transmits (from 0.25s to 0.35s)
# Node3 should start transmitting at time 0.35s

# in our implementation node_1 should try to transmit at time 0.3 but then undestands it cannot and wakes up again at time 0.35 and transmit

NODE_3_NEAR_1_2 = [
  (0.401, 0.387),
  (0.801, 0.387),
  (0.601, 0.387)
]

DEBUG_TRANSMISSION_6 = [
  [
    (0.20, 100000)
  ],
  [
    (0.25, 100000),
  ],
  [
    (0.22, 100000),
  ]
]

# Use this in combination with NODE_3_NEAR_1_2 meaning node 3 is near node 1 and 2 but 1 and 2 are far away
# Example   1 ------ 3 ------- 2
# Node3 transmits (from 0.1s to 0.2s)
# Node1 cannot transmit (is receaving) so delays his transmission
# Node2 cannot transmit (is receaving) so delays his transmission
# Node1 should start transmitting at time 0.2s
# Node2 should start transmitting at time 0.2s

# Transmissions from Node1 and Node2 should result in a collision

DEBUG_TRANSMISSION_7 = [
  [
    (0.15, 100000)
  ],
  [
    (0.13, 100000),
  ],
  [
    (0.10, 100000),
  ]
]


