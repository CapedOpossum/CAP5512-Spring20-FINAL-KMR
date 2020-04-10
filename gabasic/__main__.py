import sys
import configparser
import importlib
from . import SimpleGa


def resolve_symbol(fq_symbol_name):
  symbol_comps = fq_symbol_name.split('.')
  symbol_name = symbol_comps[-1]
  is_local = len(symbol_comps) == 1
  source_module = importlib.import_module('gabasic')
  if not is_local:
    mod_name = '.'.join(symbol_comps[:-1])
    source_module = importlib.import_module(mod_name)
  return getattr(source_module, symbol_name)

def create_component(ini_config, ini_key, *args):
  comp_name = ini_config['GA'][ini_key]
  comp_cls = resolve_symbol(comp_name)
  comp_config = {} if not parser.has_section(comp_name) else dict(ini_config[comp_name].items())
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
ga = SimpleGa(toolbox_mods, **ga_config)
ga.run()

# vim: set ts=2 sw=2 expandtab:
