# ipipeline

A micro framework to flexibly build and execute pipelines from different domains.

## Features

- **Simplicity:** high-level classes with a simple interface that can be used to perform complex tasks.

- **Flexibility:** freedom to build the relationships of the pipeline nodes and change the states of a given node at runtime if necessary.

- **Scalability:** execution of the pipeline nodes through concurrency or parallelism as dependencies between them are resolved (coming soon).

## Installation

ipipeline is installed from the Python Package Index (PyPI) via the command:

```shell
pip install ipipeline
```

## Documentation

To learn how this package works, follow the [documentation]() (coming soon).

## Contribution

To learn how to contribute to this repository, follow the [contribution](https://github.com/novaenext/ipipeline/blob/master/CONTRIBUTING.md) file.

## License

To learn about the legal rights linked to this repository, follow the [license](https://github.com/novaenext/ipipeline/blob/master/LICENSE.md) file.

## Example

While the documentation is being written, this example will cover the main features of the package. The code will be divided into sections where each of them will be explained separately for a better understanding.

**Configurations:**

The ipipeline package offers two high-level interfaces that do all the complex work in a simplified way. The first is the pipeline interface represented by the Pipeline class and the second is the execution interface represented by the SequentialExecutor class.

```python
import logging

from ipipeline.control import SequentialExecutor
from ipipeline.structure import Pipeline


logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO
)
```

**Tasks:**

The functions below represent the user tasks that need to be executed in a certain order which forms a workflow with the following idea: data is collected from somewhere, then processed in two different ways and finally displayed on the screen. Although this example only contains functions, the methods of an instance can also be used.

```python
def collect() -> list:
    return [1, 2]


def process1(x: int) -> int:
    return x + 1


def process2(y: int) -> int:
    return y * 2


def display(x: int, y: int, z: int) -> None:
    print(f'results - x: {x}, y: {y}, z: {z}')
```

**Building:**

The pipeline instance is the entry point for the user code, through it nodes (tasks) and connections (relationships between tasks) can be added. This process internally builds a graph (workflow) that is not directly used by the user.

```python
pipeline = Pipeline('p1', tags=['example'])
pipeline.add_node(
    'n1', collect, outputs=['x', 'y'], tags=['collect']
)
pipeline.add_node(
    'n2', process1, inputs={'x': 'c.x'}, outputs=['x'], tags=['process1']
)
pipeline.add_node(
    'n3', process2, inputs={'y': 'c.y'}, outputs=['y'], tags=['process2']
)
pipeline.add_node(
    'n4', display, inputs={'x': 'c.x', 'y': 'c.y', 'z': 8}, tags=['display']
)
pipeline.add_conn('c1', 'n1', 'n2')
pipeline.add_conn('c2', 'n1', 'n3')
pipeline.add_conn('c3', 'n2', 'n4')
pipeline.add_conn('c4', 'n3', 'n4')
```

Based on the workflow defined in the Tasks section, the pipeline instance was built with four nodes and four connections. Two aspects deserve attention here, the inputs and outputs parameters of the add_node method.

When declared, the outputs parameter indicates that a node will return one or more values that will be stored in the catalog (not visible to the user) as items during the pipeline execution. For example, the outputs parameter of the 'n1' node expects the collect function to return a sequence with two elements that will be stored in the catalog with the names 'x' and 'y'.

When declared, the inputs parameter indicates that a node will receive a dictionary with the function arguments. The dictionary can have default values or values obtained from the catalog during the pipeline execution. For example, the inputs parameter of the 'n4' node expects the 'c.x' ('c.<item_id>') value to be obtained from the catalog. Note, the 'c.' prefix assumes that there is an item in the catalog that was stored by a predecessor node.

The connections help determine the order in which the nodes will be executed. For example, 'c1' connection defines that there is a relationship between 'n1' node and 'n2' node where the 'n2' node depends on the execution of the 'n1' node. Note, a node can be declared dependent on another node even though it does not use the outputs of its predecessor node.

**Execution:**

Once the pipeline was built, it can be inserted into an executor. Through the graph inside the pipeline the execution order (topological order) of the nodes is determined by the dependencies between them. Therefore, it is expected that the connections between the nodes form a DAG (Directed Acyclic Graph), if this does not happen, an error will be raised.

```python
executor = SequentialExecutor(pipeline)
executor.execute_pipeline(executor.obtain_topo_order())
```

Currently, only the sequential execution is supported, but soon the executions through concurrency and parallelism will be added.

**Results:**

Below are the log results generated by the pipeline execution. In cases where there are a lot of nodes or the pipeline is called many times inside a loop, it is recommended to turn off the logs.

```shell
[2021-10-26 12:00:21] INFO ipipeline.control.execution - topo_order: [['n1'], ['n2', 'n3'], ['n4']]
[2021-10-26 12:00:21] INFO ipipeline.control.execution - node - id: n1, tags: ['collect']
[2021-10-26 12:00:21] INFO ipipeline.control.execution - node - id: n2, tags: ['process1']
[2021-10-26 12:00:21] INFO ipipeline.control.execution - node - id: n3, tags: ['process2']
[2021-10-26 12:00:21] INFO ipipeline.control.execution - node - id: n4, tags: ['display']
results - x: 2, y: 4, z: 8
```

According to the defined workflow, the nodes were executed in the expected order. The inner lists of the topological order must always be executed in order, however, the elements within them can be executed simultaneously. As in this case the SequentialExecutor class was used, the nodes will be executed as if the topological order were a flat list.
