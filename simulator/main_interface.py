from classes import NodeController
from classes import TransmissionController
from classes import Simulator
from classes import Transmission
import sys
from init import Init as init

from flask import render_template, jsonify
from flask import Flask
import webbrowser

######### CONFIGURATION #########
# the gamma value to simulate
# (inter-arrival-time in seconds)
gamma = 0.005
###### END OF CONFIGURATION #####


syms = ['\\', '|', '/', '-']
bs = '\b'
file_name = 'stats'

number = 0

init.config()

node_ctrl = NodeController()
node_ctrl.create_nodes()
node_ctrl.find_all_neighbours()

print("> Inizio simulazione")

transmission_ctrl = TransmissionController( gamma )
simulation = Simulator( node_ctrl, transmission_ctrl, gamma )
simulation.initialize()

webbrowser.open('http://127.0.0.1:5000/', new=0)

app = Flask('testapp')

@app.route('/')
def hello():
  return render_template('index.html', data = number)

@app.route('/_init', methods= ['GET'])
def init():
  transmissions = transmission_ctrl.get_dict_transmission()
  nodes = node_ctrl.get_dict_nodes()
  return jsonify(node_ctrl = transmissions, nodes = nodes)

@app.route('/_stuff', methods= ['GET'])
def stuff():
  elem = ''
  if(not simulation.finish()):
    elem = simulation.step()
    nodes = node_ctrl.get_dict_nodes()
    transmissions = transmission_ctrl.get_dict_transmission()
    print(elem)
    return jsonify(data = elem[0], t = elem[1].as_dict(), node_ctrl = transmissions, nodes = nodes, end = 0)
  print("finish")
  return jsonify(data = {}, t = {}, node_ctrl = {}, nodes = {}, end = 1)


@app.route('/_reset', methods= ['GET'])
def reset():
  transmission_ctrl = TransmissionController( gamma )
  simulation = simulation_line( node_ctrl, transmission_ctrl )
  simulation.initialize()

if __name__ == "__main__":
  app.run(debug=True)
