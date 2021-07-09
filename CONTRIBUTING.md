# Contributing

Every contribution is welcome and important for the project's maintainability. This document explains the guidelines related to code, style and versioning to make it easier for everyone to understand and collaborate.

## Guidelines

### Code

[PEP 20](https://www.python.org/dev/peps/pep-0020/) must be followed during development as it is strictly related to good programming principles and patterns. All code, comments and documentation must be written in english. The files must use UTF-8 as the default encoding and LF as the control character for newline.

[PEP 8](https://www.python.org/dev/peps/pep-0008/) is used for the code style and the conventions adopted follow below:

**Imports:**

```python
# built-in
import os
import sys

# third party
import numpy as np

# local application
from module import func, Class
```

**Functions:**

```python
# line length <= 79
def func(param1, param2=[1, 2]):
    pass

func('arg1')

# line length > 79
def func(
    param1, 
    param2=[1, 2]
):
    pass

func(
    'arg1'
)

```

**Classes:**

```python
# line length <= 79
class Class:    
    def method(self, param1, param2=[1, 2]):
        pass

obj = Class()
obj.method('arg1')

# line length > 79
class Class:
    def method(
        self, 
        param1, 
        param2=[1, 2]
    ):
        pass

obj = Class()
obj.method(
    'arg1'
)
```

**Conditions:**

```python
# line length <= 79
if var1 == 1 and var2 not in [1, 2]:
    pass

if var1 + var2:
    pass

# line length > 79
if (
    var1 == 1 
    and var2 not in [1, 2]
):
    pass

if (
    var1 
    + var2
):
    pass
```

**Loops:**

```python
# line length <= 79
for i in [1, 2]:
    pass

while x <= i <= y:
    pass

# line length > 79
for i in [
    1, 2
]:
    pass

while (
    x <= i <= y
):
    pass
```

**Containers:**

```python
# line length <= 79
list1 = [1, 2]
tuple1 = (1, 2)
set1 = {1, 2}
dict1 = {'key1': 1, 'key2': 2}

# line length > 79
list1 = [
    1, 2
]
tuple1 = (
    1, 2
)
set1 = {
    1, 2
}
dict1 = {
    'key1': 1, 'key2': 2
}
```

**Operations:**

```python
var1 += 1
var3 = var1 + var2
var5 = var1*var2 + var3*var4
var5 = (var1+var2) * (var3+var4)
```

**Documentation:**

```python
# line length <= 72
def func():
    """Function docstring."""

# line length > 72
def func():
    """Function 
    docstring.
    """   
```

Prefer short but meaningful names and if necessary, use an underscore as a separator. Use nouns and others (except verb) to define the name of variables, constants, classes, modules and packages and verb for functions and methods. The indentation must be equal to 4 spaces.

[PEP 484](https://www.python.org/dev/peps/pep-0484/), [PEP 257](https://www.python.org/dev/peps/pep-0257/) and [a guide to NumPy documentation](https://numpy.org/doc/stable/docs/howto_document.html) must be followed to create readable documentation.

### Versioning

Follow [semantic versioning](https://semver.org/) to keep track the version number (major.minor.patch) of the project. Major is for incompatible changes, minor for backward compatible changes and patch for backward compatible fixes.

The repository follows the [GitHub flow](https://guides.github.com/introduction/flow/) which is a simple yet powerful branch-based workflow. Commits, issues and pull requests are based on the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) as well as [git](https://git-scm.com/) recommendations. The pull request must have a reference to the issues it intends to solve. Follow the templates and types below:

**Commit template:**

> \<type\>(\<scope\>): \<subject\>
>
> \<body\>
>
> \<footer\>

The type must be one of the following:

- **build:** package build procedures.
- **doc:** documentation procedures.
- **feat:** new code features.
- **fix:** code fixing.
- **perf:** performance improvements.
- **refac:** code refactoring.
- **style:** code styling.
- **test:** test procedures.

The subject must use a capitalized verb in the imperative form without period at the end. A blank line between the subject and body (if any) is required. All content must be wrapped in 72 characters.

**Branch template:** \<type\>_issue\<id\> or \<type\>_issues\<id\>-\<id\>.
