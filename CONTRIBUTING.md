# **Contributing**

Every contribution is welcome and important for the maintainability of the repository. This document explains the guidelines related to code, style and versioning to facilitate and standardize the collaboration.

## **Guidelines**

### **Code**

[PEP 20](https://www.python.org/dev/peps/pep-0020/) must be followed during the development as it is strictly related to good programming principles and patterns. All the code, comments and documentation must be written in english. The files must use UTF-8 as the default encoding and LF as the control character for newline.

[PEP 8](https://www.python.org/dev/peps/pep-0008/) is used for the code style. Prefer short but meaningful names and if necessary, use an underscore as a separator. Use nouns and others (except verbs) to define the name of the packages, modules, classes and variables. Use verbs to define the name of the methods and functions. The indentation must be equal to 4 spaces.

[PEP 484](https://www.python.org/dev/peps/pep-0484/), [PEP 257](https://www.python.org/dev/peps/pep-0257/) and [NumPy style guide](https://numpydoc.readthedocs.io/en/latest/format.html) must be followed to create readable documentation.

### **Versioning**

Follow [semantic versioning](https://semver.org/) to keep track the version number (major.minor.patch) of the repository. Major is for incompatible changes, minor for backward compatible changes and patch for backward compatible fixes.

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

The subject must use a verb in the imperative form without period at the end. A blank line between the subject and body (if any) is required. All the content must be wrapped in 72 characters.

**Branch template:** \<type\>_issue\<id\> or \<type\>_issues\<id\>-\<id\>.
