# **ipipeline**

ipipeline is a micro framework to build and execute pipelines from different domains.

## **Features**

- **Simplicity:** high-level interfaces that can be used to perform complex tasks.

- **Flexibility:** freedom to build according to the requirements of the problem.

- **Scalability:** execution through concurrency or parallelism (coming soon).

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

The ipipeline package tries to keep things simple, therefore all the work is done through a few interfaces.

```python
import logging

from ipipeline.control import SequentialExecutor
from ipipeline.structure import Catalog, Pipeline


logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO
)
```

### **Tasks**

The functions below represent tasks that need to be executed in a certain order which forms a flow of tasks with the following idea: the data is extracted from a source, then transformed in different ways, and finally loaded to a destination. The focus in this example is not on the code block of the functions, but on the dependencies between them.

```python
def extract_data(path: str, encoding: str = None) -> list:
    data = [2, 4]

    return data


def transform_data1(data: list) -> list:
    sum_data = [num + 2 for num in data]

    return sum_data


def transform_data2(data: list) -> list:
    sub_data = [num - 2 for num in data]

    return sub_data


def load_data(sum_data: list, sub_data: list, path: str) -> None:
    pass
```

### **Pipeline**

A pipeline stores a flow of tasks represented by nodes (tasks) and links (dependencies). The links between the nodes must compose a directed acyclic graph which is used to find a linear ordering for the execution.

```python
pipeline = Pipeline('p1', tags=['example'])
pipeline.add_node(
    'n1', 
    extract_data, 
    pos_inputs=['src_path'], 
    key_inputs={'encoding': 'encoding'}, 
    outputs=['data'], 
    tags=['extract']
)
pipeline.add_node(
    'n2', 
    transform_data1, 
    pos_inputs=['data'], 
    outputs=['sum_data'], 
    tags=['transform1']
)
pipeline.add_node(
    'n3', 
    transform_data2, 
    pos_inputs=['data'], 
    outputs=['sub_data'], 
    tags=['transform2']
)
pipeline.add_node(
    'n4', 
    load_data, 
    pos_inputs=['sum_data', 'sub_data', 'dst_path'], 
    tags=['load']
)
pipeline.add_link('l1', 'n1', 'n2')
pipeline.add_link('l2', 'n1', 'n3')
pipeline.add_link('l3', 'n2', 'n4')
pipeline.add_link('l4', 'n3', 'n4')
```

The pipeline produces a graph as shown in the image below.

![graph](https://raw.githubusercontent.com/novaenext/ipipeline/master/images/graph.png)

### **Catalog**

A catalog stores the items (arguments) of an execution. When a node is executed, its return is stored in the catalog linked to the name defined in the outputs parameter, creating a key:value pair. This pair is made available to all other nodes that depend on it as an argument. Therefore, the pos_inputs and key_inputs parameters are references to the keys of the arguments stored in the catalog. It is possible to pass default arguments to the nodes before the execution takes place as shown below.

```python
catalog = Catalog('c1', tags=['example'])
catalog.set_item('src_path', 'src/file')
catalog.set_item('dst_path', 'dst/file')
catalog.set_item('encoding', 'utf-8') 
```

### **Executor**

An executor is responsible to execute a pipeline from the topological ordering of the graph built from the relationships between the nodes. The result of the execution is the catalog populated with the returns of the functions.

```python
executor = SequentialExecutor()
ordering = executor.get_ordering(pipeline)
catalog = executor.execute_pipeline(pipeline, catalog, ordering)
```

The log generated while executing is shown below.

```shell
[2022-07-01 09:30:00] INFO ipipeline.control.executors - ordering: [['n1'], ['n2', 'n3'], ['n4']]
[2022-07-01 09:30:00] INFO ipipeline.control.executors - pipeline.id: p1, pipeline.tags: ['example']
[2022-07-01 09:30:00] INFO ipipeline.control.executors - catalog.id: c1, catalog.tags: ['example']
[2022-07-01 09:30:00] INFO ipipeline.control.executors - node.id: n1, node.tags: ['extract']
[2022-07-01 09:30:00] INFO ipipeline.control.executors - node.id: n2, node.tags: ['transform1']
[2022-07-01 09:30:00] INFO ipipeline.control.executors - node.id: n3, node.tags: ['transform2']
[2022-07-01 09:30:00] INFO ipipeline.control.executors - node.id: n4, node.tags: ['load']
```

The ordering list has inner lists that represent groups of nodes that must be executed sequentially and the nodes within these groups can be executed simultaneously. As in this case the sequential executor was used, the benefit of simultaneous execution was skipped, but soon new executors will be created to take advantage of this.

### **CLI**

The package provides a CLI with two commands called project and execution. The project command builds a project in the file system that provides a standard structure for organizing the code. Let's assume the project path is the home directory and the project name is example, therefore the command would be entered like this:

```shell
python -m ipipeline project ~ example
```

The execution command executes a pipeline according to the location of the modules and functions that build the pipeline and the catalog. The pipeline and catalog building process can be wrapped into separate functions called, for example, build_pipeline and build_catalog. Let's assume both functions are in the __main__ module of the example project, therefore the command would be as follows:

```shell
python -m ipipeline execution SequentialExecutor example.__main__ example.__main__ build_pipeline build_catalog
```
