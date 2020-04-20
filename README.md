# CAP 5512: Evolutionary Computation Spring 2020 Final Project

## Team Members

* Kyle Benko
* Matthew Kurtz
* Rolando Nieves

## Development Environment

This software requires Python 3.7 or later be already installed.

Packages in addition to Python 3.7 are required. In order to simplify the inclusion of all pre-requisites, create a virtual Python 3 environment using the included `requirements.txt` file:

    $ python3 -m venv pyenv
    ...
    $ . pyenv/bin/activate
    (pyenv) $ pip3 install -r ./requirements.txt
    ...

## Run Tic-Tac-Toe

The repository contains a baseline configuration file that is able to use the
`gabasic` package to find an optimal Tic-Tac-Toe player policy. Prior to running the search, a proper runtime environment must be available. Refer to the *Development Environment* section for instructions on how to create this runtime environment. To execute the
search, run:

    (pyenv) $ python3 -m gabasic tic_tac_toe.ini

## GABASIC Framework

The `gabasic` package contains a framework of components meant to be used as
constituents in a Genetic Algorithm (GA) model. The package is based off of the
DEAP package, and extends it by introducing the concept of GA model construction
using configuration files.

The `gabasic` package can be ran on its own using the name of the GA model
configuration file as its only argument:

    (pyenv) $ python3 -m gabasic <model INI>

The model INI file format is basically a typical Microsoft INI text file with
a set of key-value pairs grouped in sections.

Every model INI file must contain a `GA` section where the configuration and
participating components of a GA model must be specified. The `GA` section must
contain the following key-value pairs:

| Key              | Class                 | Meaning                              |
| :---             | :---                  | :---                                 |
| `fitness_type`   | *Fitness Type*        | Fitness maximization or minimization |
| `individual`     | *Individual Type*     | GA population individual to use      |
| `fitness_eval`   | *Fitness Evaluation*  | Fitness evaluation logic             |
| `selection`      | *Selection Algorithm* | Type of population selection to use  |
| `crossover_type` | *Crossover Type*      | Type of crossover GA operator to use |
| `mutation_type`  | *Mutation Type*       | Type of mutation GA operator to use  |

Each one of the key-value pairs presented in the previous table identifies a
component for the resulting GA model. The collection of built-in components
available to model designers are:

| Component Name | Component Class | Description |
| :---           | :---            | :---        |
| `FitnessMax` | Fitness Type | Maximizes fitness values in the population. |
| `BitString`  | Individual Type | Individual containing an arbitrary number of binary digits. |
| `SumItems`   | Fitness Evaluation | Produces the overall sum of every element in an individual as its fitness. |
| `TournamentSelection` | Selection Algorithm | *n*-way tournament selection in a single generation. |
| `TwoPointCrossover`        | Crossover Type | Two-point crossover done during mating of sequence-type individuals. |
| `OnePointMappingCrossover` | Crossover Type | One-point crossover done during mating of mapping-type (i.e., `dict` individuals).
| `FlipBitMutation` | Mutation Type | Random binary digit flipping during mutation of individuals. |

In addition, the `GA` section may contain the following key-value pairs that
configure the overall behavior of the algorithm:

| Key  | Default Value | Meaning |
| :--- |          ---: | :---    |
| `population_size` | `100` | Population size of the GA model. |
| `max_generation_count` | `100` | Number of generations to run. |
| `crossover_probability` | `0.5` | Probability of selecting two individuals for mating. |
| `mutation_probability` | `0.1` | Probability of selection an individual for mutation. |

> **A note on DEAP fitness evaluations:** DEAP is able to handle GA models with
> simultaneous fitness goals. To do so, DEAP considers the single fitness goal
> mode (the most common in GA models) as a *special case* of the multiple
> simultaneous fitness goals. Thus, anytime DEAP manages fitness (either type or
> evaluations) it expects the values in the form of a tuple, with each element in
> the tuple aligned with the goal it represents. Single fitness goal models must
> manage their fitness weights and scores as a tuple with a single element.

### `FitnessMax` Configuration
When using the `FitnessMax` *Fitness Type*, it is possible to specify the
relative weights of all fitness evaluation results. By default, the relative
weights are all initialized to `1.0`. This can be changed by adding a section 
to the model INI file as follows:

```ini
[FitnessMax]
weights=<csv of weights>
```

Where the `weights` key-value pair specifies the relative weights as a single
line of comma-separated values.

### `BitString` Configuration
Although `gabasic` provides a default bit string length of `10`, more likely
than not this value will be inadequate for custom models. The length of bit
string individuals can be specified by adding a section to the INI file as
follows:

```ini
[BitString]
bitstring_size=<size in bits>
```

Where the `bitstring_size` key-value pair specifies the count of bits present in
every individual.

### `TournamentSelection` Configuration
The `TournamentSelection` component can be configured to perform a generic
*n*-way tournament. By default, the tournament is 2-way. Other modes can be
configured by adding a section to the INI file as follows:

```ini
[TournamentSelection]
tournament_size=<n value>
```

Where the `tournament_size` key contains the *n* value to use when executing the
selection tournament.

### `FlipBitMutation` Configuration
The overall GA model selects individuals for mutation via the `mutation_rate`
key-value pair in the `GA` section. However, the `FlipBitMutation` component
must decide the probability of each binary digit in a bit string mutating 
individually. By default, each binary digit in a bit string has a `0.05` chance
of being mutated. This can be customized by adding a section to the INI file as
follows:

```ini
[FlipBitMutation]
indv_bit_mut_prob=<probability>
```

Where the `indv_bit_mut_prob` key-value pair specifies the individual bit flip
probability.

## Extending `gabasic`

Given the limited set of components available in *stock* `gabasic`, it is almost
a given that GA model implementors will need to extend the component collection
in order to leverage `gabasic`. When extending `gabasic`, familiarity with DEAP,
especially with the `deap.creator` and `deap.base.Toolbox` facilities, is
**strongly** recommended. Each of the following model INI key-value pairs (with
their corresponding classes) identifies a component that can be integrated
from external code:

* `fitness_type` (*Fitness Type*)
* `individual` (*Individual Type*)
* `fitness_eval` (*Fitness Evaluation*)
* `selection` (*Selection Algorithm*)
* `crossover_type` (*Crossover Type*)
* `mutation_type` (*Mutation Type*)

For each of the aforementioned keys, the value represents a Python class name.
Whether the Python class name is fully-qualified (i.e., specified with its
containing package) or not determines whether `gabasic` sources the component
from either its internal collection or an external package. For example, 
specifying an *Individual Type* of `tictactoe.TicTacToeChromo` assumes that the
Python interpreter is able to import the `tictactoe` package and obtain a
reference to the `TicTacToeChromo` class within that package. On the other hand,
specifying an *Individual Type* of `BitString` assumes the identified class is
available within the `gabasic` package itself.

### New *Fitness Type*
A new *Fitness Type* component must be implemented as a Python class that adds
the fitness type implementation as a class to the `deap.creator` facility. The
implementation of `FitnessMax` is shown below providing a concise example:

```python
class FitnessMax(object):
  def __init__(self, **kwargs):
    super(FitnessMax, self).__init__()
    weights_str = kwargs.get('weights', '1.0')
    weights = [float(a_weight) for a_weight in weights_str.split(',')]
    creator.create('FitnessMax', base.Fitness, weights=weights)
```

The constructor for the new *Fitness Type* will be provided a mapping in the
`kwargs` argument which contains the set of key-value pairs found under the
eponymous section of the model INI file (if one was present). `gabasic` does
not pay heed to any of the arguments in the custom INI file section.

The actual behavior of the *Fitness Type* must conform to the
`deap.base.Fitness` base class provided in DEAP. More often than not, new
*Fitness Type* behaviors will just derive from the aforementioned base class.

### New *Individual Type*
Similar to *Fitness Type*, a new *Individual Type* must be implemented as a
Python class. There are additional requirements, however, levied on this
component. The Python *Individual Type* component is among a category that 
`gabasic` calls *Toolbox Contributors*. The name of this category reveals the
purpose of these components: they are required to make specific customizations
to a `deap.base.Toolbox` instance that is provided to them at runtime.

Like *Fitness Type* components, the *Individual Type* component constructor is
provided a mapping in the `kwargs` argument containing their custom model INI
configuration (again, identified by the section in the model INI file with the
same name as the component). *Individual Type* component Python classes are
required to derive from the abstract `gabasic.ToolboxContributor` class. This 
class defines one abstract method: `ToolboxContributor.configure_toolbox()`. The
*Individual Type* component is expected to extend the provided toolbox with two
(2) items: an `individual` item that represents a factory callable for
population individuals, and a `population` item that represents a factory
callable for creating an initial random population. The implementation in the
`BitString.configure_toolbox()` method below provides a good example:

```python
  def configure_toolbox(self, toolbox):
    self._private_toolbox.register('bitstring_bool_gen', random.randint, 0, 1)
    toolbox.register(
      'individual',
      tools.initRepeat,
      self._bit_string,
      self._private_toolbox.bitstring_bool_gen,
      self.bitstring_size
    )
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
```

Foregoing the first statement in the method, which simply wraps the generation
of a random binary digit, the last two statements show how the provided toolbox
is extended to include the `individual` and `population` factory callable
instances. Both are based off of facilities provided in the `deap.tools`
package, but they need not be. Documentation of the
`deap.base.Toolbox.register()` contains a thorough explanation of each argument.

### New *Fitness Evaluation*
An external *Fitness Evaluation* component must also be implemented in terms of
the `gabasic.ToolboxContributor` component. Like all other components, the
constructor will be provided a mapping of key-value pairs corresponding to it
in the model INI file.

The component is expected to extend a provided toolbox with a single element
called `evaluate`. The element is expected to be a callable that accepts a GA
individual and returns as a result a *tuple* of evaluations based on the GA
model goals. If the GA model only has one goal, the result must still be a tuple
with one element. This component is by far the most custom in a GA model, and
thus the most prone for customization. The `SumItems` *Fitness Evaluation*
component logic is shown below as a concise example:

```python
class SumItems(ToolboxContributor):
  def __init__(self, **kwargs):
    super(SumItems, self).__init__()

  def configure_toolbox(self, toolbox):
    toolbox.register('evaluate', self)

  def __call__(self, individual):
    return (sum(individual),)
```

As can be seen from the example, the component does not expect any customization
key value pairs. In addition, in the `SumItems.configure_toolbox()`
implementation, the component simply submits its own instance value as the
`evaluate` extension. Since the class provides an implementation for the
`__call__()` method, an instance of `SumItems` is also a callable. The signature
of the `__call__()` implementation properly expects the individual as input and
returns the evaluation tuple.

### New *Crossover Type*
An external crossover operator integrated into `gabasic` is also considered a
*Toolbox Contributor*. It also is afforded the ability to accept configuration
key-value pairs (via the `**kwargs` mapping provided in the constructor), and
must provide an implementation for the `ToolboxContributor.configure_toolbox()`
method.

The component's contribution to the toolbox must be called `mate` and it must
be a callable entity that accepts two individuals as arguments. The callable
must perform the required crossover logic *in place* (i.e., modifying the
individuals provided as input), and must also return a tuple of the two modified
individuals as a result.

### New *Mutation Type*
An external mutation operator is very similar to a *Crossover Type* component,
at least as far as the custom configuration and expectation to be a *Toolbox
Contributor*.

The mutation operator's `ToolboxContributor.configure_toolbox()` implementation
is expected to add a callable under the name `mutate` to the provided toolbox.
The callable is expected to perform the required mutation *in place* (just like
*Crossover Type*) and return the mutated individual as a result.

## Unit Tests

Unit tests have been written for some of the project's components. They can be
run via the Python 3 `unittest` module auto-discovery facility (when run from
the project root directory under the project's virtual environment; see
*Development Environment*):

    (pyenv) $ python3 -m unittest discover -v

## Run One-Max

Part of the validation of the DEAP package included evaluating the ease and
feasibility with which OneMax could be implemented on it. DEAP does not include
configuration file declarative facilities like the CAP 5512 Java-based code
base. The `gabasic` package is the first attempt at adding such a facility.
OneMax can be run as follows:

    (pyenv) $ python3 -m gabasic one_max.ini

## Run Tic-Tac-Toe

The repository contains a baseline configuration file that is able to use the
`gabasic` package to find an optimal Tic-Tac-Toe player policy. To execute the
search, run:

    (pyenv) $ python3 -m gabasic tic_tac_toe.ini
