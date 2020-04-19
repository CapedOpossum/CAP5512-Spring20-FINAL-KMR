import sys
import configparser
import importlib
from . import SimpleGa

import matplotlib.pyplot as plt


def resolve_symbol(fq_symbol_name):
  symbol_comps = fq_symbol_name.split('.')
  symbol_name = symbol_comps[-1]
  is_local = len(symbol_comps) == 1
  source_module = importlib.import_module('gabasic')
  if not is_local:
    mod_name = '.'.join(symbol_comps[:-1])
    source_module = importlib.import_module(mod_name)
  return getattr(source_module, symbol_name)

def create_component(ini_config, ini_key, *args, **kwargs):
  comp_name = ini_config['GA'][ini_key]
  comp_cls = resolve_symbol(comp_name)
  comp_config = {} if not parser.has_section(comp_name) else dict(ini_config[comp_name].items())
  comp_config.update(kwargs)
  return comp_cls(*args, **comp_config)
    
if len(sys.argv) < 2:
  print('Usage: gabasic <configuration INI>')
  sys.exit(1)

print('Executing GA using INI: {}'.format(sys.argv[1]))
parser = configparser.ConfigParser()
parser.read(sys.argv[1])
ga_config = dict(parser['GA'].items())
fitness_type = create_component(parser, 'fitness_type')
individual = create_component(parser, 'individual', ga_config['fitness_type'])
fitness_eval = create_component(parser, 'fitness_eval')
selection = create_component(parser, 'selection')
crossover_type = create_component(parser, 'crossover_type')
mutation_type = create_component(parser, 'mutation_type')
toolbox_mods = [fitness_eval, individual, selection, crossover_type, mutation_type]

if 'algorithm' in parser['GA']:
  ga = create_component(parser, 'algorithm', toolbox_mods, **ga_config)
else:
  ga = SimpleGa(toolbox_mods, **ga_config)

pop, log = ga.run()

# Plot the fitness results of the run
gen = log.select("gen")
avg_fit = log.chapters['fitness'].select("avg")
best_fit = log.chapters['fitness'].select("max")

line1 = plt.plot(gen, avg_fit, "b-", label="Average Fitness")
line2 = plt.plot(gen, best_fit, "r-", label="Best Fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness", color="b")

lns = line1 + line2
labels = [l.get_label() for l in lns]
plt.legend(lns, labels, loc="center right")

plt.show()

# Plot the length results of the run
avg_len = log.chapters['length'].select('avg')
max_len = log.chapters['length'].select('max')

plt.plot(gen, avg_len, 'b-')
plt.plot(gen, max_len, 'r-')
plt.xlabel('Generation')
plt.ylabel('Chromo Len')
plt.legend(['Average Chromo Len', 'Max Chromo Len'])
plt.show()


# vim: set ts=2 sw=2 expandtab:
