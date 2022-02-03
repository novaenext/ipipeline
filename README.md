# **ipipeline**

A micro framework for building and executing pipelines from different domains.

## **Features**

- **Simplicity:** high-level interfaces that can be used to perform complex tasks.

- **Flexibility:** freedom to build the pipeline according to the requirements of the problem.

- **Scalability:** pipeline execution through concurrency or parallelism (coming soon).

## **Installation**

ipipeline is installed from the Python Package Index (PyPI).

```shell
pip install ipipeline
```

## **Documentation**

To learn how this package works, follow the [documentation]() (coming soon).

## **Contribution**

To learn how to contribute to this repository, follow the [contribution](https://github.com/novaenext/ipipeline/blob/master/CONTRIBUTING.md) file.

## **License**

To learn about the legal rights linked to this repository, follow the [license](https://github.com/novaenext/ipipeline/blob/master/LICENSE.md) file.

## **Example**

This example was divided into sections to explain the main features of the package. In case of questions about a specific detail the package contains docstrings for all modules, classes, methods and functions.

### **Imports**

The ipipeline package tries to keep things simple, therefore all the work is done through the pipeline interface imported as Pipeline and the execution interface imported as SequentialExecutor.

```python
import logging

from ipipeline.execution import SequentialExecutor
from ipipeline.structure import Pipeline


logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO
)
```

### **Tasks**

The functions below represent the user tasks that need to be executed in a certain order which forms a workflow with the following idea: data is extracted from somewhere, then transformed in two different ways and finally loaded to somewhere. Although this example only contains functions, the methods of an instance can also be used.

```python
def extract() -> list:
    return [1, 2]


def transform1(x: int) -> int:
    return x + 1


def transform2(y: int) -> int:
    return y * 2


def load(x: int, y: int, z: int) -> None:
    print(f'loading - x: {x}, y: {y}, z: {z}')
```

### **Pipeline**

A pipeline is the entry point for the user tasks, through it the nodes (tasks) and connections (relationships between tasks) added are represented as a graph (workflow). The graph is used by the executor and is not visible to the user.

```python
pipeline = Pipeline('p1', tags=['example'])
pipeline.add_node(
    'n1', extract, outputs=['x', 'y'], tags=['extract']
)
pipeline.add_node(
    'n2', transform1, inputs={'x': 'c.x'}, outputs=['x'], tags=['transform1']
)
pipeline.add_node(
    'n3', transform2, inputs={'y': 'c.y'}, outputs=['y'], tags=['transform2']
)
pipeline.add_node(
    'n4', load, inputs={'x': 'c.x', 'y': 'c.y', 'z': 8}, tags=['load']
)
pipeline.add_conn('c1', 'n1', 'n2')
pipeline.add_conn('c2', 'n1', 'n3')
pipeline.add_conn('c3', 'n2', 'n4')
pipeline.add_conn('c4', 'n3', 'n4')
```

Based on the workflow defined, the pipeline was built with four nodes and four connections. Two aspects deserve attention here, the inputs and outputs parameters of the add_node method.

The outputs parameter, when declared, indicates that during the pipeline execution, the function returns must be stored in the catalog with specific names. For example, the outputs parameter of the 'n1' node expects to store two items in the catalog with the names 'x' and 'y' which are obtained from the returns of the function.

The inputs parameter, when declared, indicates that during the pipeline execution, the function receives a dictionary with its arguments. For example, the inputs parameter of the 'n4' node expects to receive a dictionary where the 'x' and 'y' values are obtained from the catalog and the 'z' value is obtained directly. The 'c.' prefix assumes the existence of an item ('c.<item_id>') or a list of items ('c.[<item_id>, ..., <item_id>]') in the catalog stored by the predecessor nodes.

The connections determine the order in which the nodes are executed. For example, 'c1' connection indicates a relationship between 'n1' node (source) and 'n2' node (destination) where the 'n2' node depends on the execution of the 'n1' node. A node can dependent on another node even though it does not use the outputs of its predecessor.

### **Executor**

An executor is responsible for executing a pipeline from the topological order (execution order) of the graph. Therefore, it is expected that the connections between the nodes form a DAG (Directed Acyclic Graph), if this does not happen, an error is raised. Behind the scenes, a catalog is created to store the node returns that are requested by other nodes during the execution.

```python
executor = SequentialExecutor()
executor.add_pipeline(pipeline)
topo_order = executor.obtain_topo_order()
executor.execute_pipeline(topo_order)
```

Below are the log results generated by the execution. It is recommended to turn off the logs in cases where there are many nodes or the pipeline is called many times inside a loop.

```shell
[2022-02-03 16:43:26] INFO ipipeline.execution.executors - topo_order: [['n1'], ['n2', 'n3'], ['n4']]
[2022-02-03 16:43:26] INFO ipipeline.execution.executors - node.id: n1, node.tags: ['extract']
[2022-02-03 16:43:26] INFO ipipeline.execution.executors - node.id: n2, node.tags: ['transform1']
[2022-02-03 16:43:26] INFO ipipeline.execution.executors - node.id: n3, node.tags: ['transform2']
[2022-02-03 16:43:26] INFO ipipeline.execution.executors - node.id: n4, node.tags: ['load']
loading - x: 2, y: 4, z: 8
```

According to the defined workflow, the nodes were executed in the expected order. The inner lists of the topological order must always be executed in order, however, the elements within them can be executed simultaneously. As in this example the SequentialExecutor class was used, the nodes were executed as if the topological order were a flat list.

### **CLI**

The package provides a CLI with two commands called project and execution. The project command creates a project in the file system that provides a standard structure for organizing the tasks that interact with the package. Let's assume the project path is the home directory and the project name is iexample, therefore the command would be entered like this:

```shell
python -m ipipeline project ~ iexample
```

The result of this command would be the following structure:

```text
iexample
|
|----iexample
|    |
|    |----configs
|    |
|    |----pipelines
|    |
|    |----tasks
|    |
|    |----__init__.py
|    |
|    |----__main__.py
|    |
|    |----exceptions.py
|
|----io
|
|----requirements
|
|----tests
|
|----.gitignore
|
|----CONTRIBUTING.md
|
|----LICENSE.md
|
|----MANIFEST.in
|
|----README.md
|
|----setup.py
```

The example code provided would fit into this structure as follows:

- The configurations is moved to the configs package.

- The tasks are moved to the tasks package.

- The pipeline is moved to the pipelines package.

- The executor is moved to the main module.

With these modifications this project can be executed with the following command:

```shell
python -m iexample
```

Another option to execute this project without having to deal with the execution interface would be through the execution command. For this, the pipeline building process must be wrap in a function that returns the pipeline instance. Let's suppose that the wrapper function is called build_pipeline and the module where it was declared is called etl (inside the iexample.pipelines package), therefore the command would be as follows:

```shell
python -m ipipeline execution iexample.pipelines.etl build_pipeline sequential
```
