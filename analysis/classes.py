import matplotlib
matplotlib.use('Agg')

from scipy.stats import binom
from scipy.stats import expon
import matplotlib.pyplot as plt
import matplotlib.markers as mmark
import numpy as np
import datetime, os

# setting network
mean_packet_size = binom.mean(n=7111, p=0.843, loc=0) + 32
convert_megabyte = 0.000001
N = 10
CAPACITY = 1000000
max_load = CAPACITY * N

# setting graphs
font = {'size'   : 14}
font_leg = {'fontsize': 11}

matplotlib.rc('font', **font)
matplotlib.rc('legend', **font_leg)

class StatsHandler(object):
  def __init__(self, data):
    self.subsets = data
    self.rate = []
    self.load = []
    self.computed_load = []
    self.offered = []
    self.throughput = []
    self.lost = []
    self.collided = []
    self.throughput_nodes = []
    self.nodes_stats = []
    self.perc = []

    self.nodes_collisions = []
    self.nodes_loss = []

  def get_rate(self):
    return self.rate

  def get_load(self): 
    return self.load

  def get_computed_load(self): 
    return self.computed_load

  def get_offered(self): 
    return self.offered

  def get_throughput(self): 
    return self.throughput

  def get_lost(self): 
    return self.lost

  def get_collided(self): 
    return self.collided

  def get_throughput_nodes(self): 
    return self.throughput_nodes

  def get_nodes_stats(self): 
    return self.nodes_stats

  def get_pers(self):
    return self.perc

  def compute_some_stats(self):
    for subset in self.subsets:
      rate = float(subset[0]["rate"])
      i_load = load_from_rate(rate)
      self.load.append(i_load*convert_megabyte)

      # compute packet lost
      # loosing = split_int(subset, "loosing")
      # loosing_rate = column(loosing[1], "prob")
      # print(loosing_rate)
      # loss = float(np.sum(loosing_rate))

      states = split(subset, "state")
      transmitting_rate = column_fusion(states[0], "prob", "transmitting")
      colliding_rate = column_fusion(states[1], "prob", "transmitting")
      offered_rate = column_fusion(subset, "prob", "transmitting")

      transmitting = float(np.sum(transmitting_rate))
      colliding = float(np.sum(colliding_rate))
      offered = float(np.sum(offered_rate))

      total = transmitting + colliding
      self.throughput.append(transmitting*CAPACITY*convert_megabyte)
      self.offered.append(offered*CAPACITY*convert_megabyte)
      self.collided.append(colliding*CAPACITY*convert_megabyte)
      #self.lost.append(loss)

  def print_nodes_stats(self):

    plot_multiple(self.computed_load, self.nodes_stats, "total load (MB/s)", "offered throughput (MB/s)", "nodes_offered")
    plot_multiple(self.computed_load, self.nodes_collisions, "total load (MB/s)", "collisions (MB/s)", "nodes_collisions")
    plot_multiple(self.computed_load, self.nodes_loss, "total load (MB/s)", "loss rate %", "nodes_losses")

  def compute_stats(self):
    for i,v in enumerate([0] * N):
      self.nodes_stats.append([])
      self.nodes_collisions.append([])
      self.nodes_loss.append([])

    for idx, subset in enumerate(self.subsets):

      # load esperimental parameters
      gamma   = float(subset[0]["gamma"])
      sim_time = float(subset[0]["sim_time"])
      num_nodes = int(subset[0]["num_nodes"])
      
      repetition = count_distinct(subset, "repetition")

      byte_offered = column(subset, "offered")
      byte_sent    = column(subset, "sent")
      byte_load    = column(subset, "load")
      perc_success = column(subset, "perc_success")
      byte_lost    = column(subset, "losses")
      
      i_load        = sum(byte_load)/sim_time/repetition*convert_megabyte
      i_throughput  = sum(byte_sent)/sim_time/repetition*convert_megabyte
      i_offered     = sum(byte_offered)/sim_time/repetition*convert_megabyte
      i_lost        = sum(byte_lost)/sim_time/repetition*convert_megabyte
      i_collided    = i_offered - i_throughput
      i_correct_p    = avg(perc_success)

      i_computed_load = mean_packet_size / expon.mean(loc=0, scale=gamma) * num_nodes * convert_megabyte

      self.rate.append(1/gamma)
      self.load.append(i_load)
      self.computed_load.append(i_computed_load)
      self.offered.append(i_offered)
      self.throughput.append(i_throughput)
      self.lost.append(i_lost)
      self.collided.append(i_collided)
      self.perc.append(i_correct_p)
      self.throughput_nodes.append([sent/sim_time for sent in byte_sent])

      #print(gamma, " - p:", mean_packet_size, " > ", i_load, " = ", i_computed_load)

      # add offered load statistic for every node to undestand network topology behaviour
      subset_nodes = split_int(subset, "node")
      for n, sub in enumerate(subset_nodes):
        byte_load = column(sub, "load")
        byte_offered = column(sub, "offered")
        byte_throughput = column(sub, "sent")
        byte_lost = column(sub, "losses")
        perc_success = column(sub, "perc_success")

        n_offered = avg(byte_offered)/sim_time*convert_megabyte
        n_throughput = avg(byte_throughput)/sim_time*convert_megabyte
        n_collision_rate = n_offered - n_throughput
        n_lost_rate = avg(byte_lost)/sim_time*convert_megabyte

        p = avg(perc_success)
        self.nodes_stats[n].append(n_offered)
        self.nodes_collisions[n].append(n_collision_rate)
        self.nodes_loss[n].append(n_lost_rate)


directory = '.'
def init_space():
  now = datetime.datetime.now()
  global directory
  directory = os.path.join(os.getcwd(), "images", datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

  try:
    os.makedirs(directory)
  except:
    print("impossible to create folder "+directory+" to store images. Using ./images")
    directory = './images'
  return directory

def split(data, index):
  subsets = []
  value = "*_"
  num = -1
  for row in data:
    if(value!=row[index]):
      value = row[index]
      num = num + 1
      subsets.append([])
    subsets[num].append(row);
  return subsets

def split_int(data, index):
  subsets = []
  c_max = -1
  for row in data:
    num = int(row[index])
    if(num > c_max):
      c_max = num
      subsets.append([])
    subsets[num].append(row);
  return subsets

def column_fusion(data, index, multiplier):
  d = column(data, index)
  m = column(data, multiplier)
  return [a*b for a,b in zip(d,m)]

def column(data, index):
  column_values = []
  for row in data:
    column_values.append(float(row[index]))
  return column_values

def count_distinct(data, index):
  column_values = []
  old_value = ""
  count = 0
  for row in data:
    value = float(row[index])
    if(value != old_value):
      count = count+1
      old_value = value
  return int(count)

def avg(data):
  return sum(data) / float(len(data))

def sum_avg(data):
  subdata = split_int(data, "repetition")
  return sum(data)/float(len(subdata))

def plot_multiple(x, data_y, x_label, y_label, title="Graph"):
  plt.figure()
  label = []
  markers = ["s", "|", "|", "*", "^", "o", "|", "x", "^", "|"]
  ls = ["--", "-", ":", ":", "--", "-", "--", "-", ":", "-"]
  sizes = [5, 7, 7, 7, 7, 5, 7, 7, 7, 7]
  plots = []
  for i,y in enumerate(data_y):
    label.append("node"+str(i))
    j = i%len(markers)
    p = plt.plot(x, y, marker=markers[j], markersize=sizes[j], ls=ls[j], label="node"+str(i))
    plots.append(p)
  plt.xlabel(x_label)
  plt.ylabel(y_label)

  plt.legend(loc='best')
  plt.savefig(directory+"/"+title+".pdf")
  plt.close()

def plot_compare(x1, y1, x2, y2, x_label, y_label, title="Graph"):
  plt.figure()
  plt.plot(x1, y1, marker="o", markersize=5, ls="-", color="black", label="model")
  plt.plot(x2, y2, marker="s", markersize=5, ls=":", color="gray", label="simulation")
  plt.xlabel(x_label)
  plt.ylabel(y_label)

  plt.legend(loc='best')
  plt.savefig(directory+"/"+title+".pdf")
  plt.close()

def plot_line(x, y, x_label, y_label, title="Graph"):
  plt.figure()
  plt.plot(x, y, marker='o', markersize=5, color="black")
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.savefig(directory+"/"+title+".pdf")
  plt.close()

def plot_four_line(x, y1, y2, y3, y4, x_label, y_label, title="Graph"):
  plt.figure()
  
  plt.plot([0, max(x)], [50, 50], color="gray", lw=.5)
  p1 = plt.plot(x, [x*100 for x in y1], marker='^', markersize=5, ls=':', color="black", label="sent")
  p2 = plt.plot(x, [x*100 for x in y2], marker='x', markersize=5, ls=':', color="red", label="lost")
  p3 = plt.plot(x, [x*100 for x in y3], marker='^', markersize=5, ls='-', color="green", label="correct / sent")
  p4 = plt.plot(x, [x*100 for x in y4], marker='x', markersize=5, ls='-', color="orange", label="collisions / sent")

  plt.xlabel(x_label)
  plt.ylabel(y_label)

  plt.legend(loc='best')
  plt.savefig(directory+"/"+title+".pdf")
  plt.close()

def plot_special(x_values, y_values, title="Graph"):
  fig, ax = plt.subplots()
  # i=0
  # for y in y_values:
  #   median = min(y)
  #   plt.plot(x_values[i], median, 'o')
  #   i=i+1

  #plt.boxplot(y_values, positions=x_values)
  x = [round(x/1000000,1) for x in x_values]
  ax.boxplot(y_values, positions=x)

  x_labels = []
  last_x = 0
  for x_i in x:
    if(x_i > (last_x + 5) or x_i < (last_x - 5)):
      x_labels.append(x_i)
      last_x = x_i
    else:
      x_labels.append("")


  ax.set_xticklabels(x_labels)
  plt.savefig(directory+"/"+title+".pdf")
  plt.close()

def load_from_rate(rate):
  arrival_time = 1/rate
  return 6026 / arrival_time * 10

def show():
  return plt.show()
