# Betty Fixer

Betty Fixer is a tool designed to automatically fix coding style issues in C files based on the Betty coding style guidelines. It performs corrections to ensure that the code complies with the Betty style, making it more readable and consistent.

## Features

- **Betty Style Fixes**: Automatically corrects coding style issues following the Betty style guidelines.
- **Vi Script Execution**: Runs a Vi script for each fixed file, making it convenient for developers to review and further modify the code.
- **Create header.h**: You can now create header file by specifing header file name after flag -H .

## Prerequisites

Before using Betty Fixer, ensure you have the following installed:

- [Betty](https://github.com/holbertonschool/Betty) - The Betty linter for C code.
- [Vi Editor](https://www.vim.org/) - The Vi editor for script execution.

## Getting Started

1. Clone the repository:

    ```bash
    pip install bettyfixer
    ```

2. Run Betty Fixer on your C files:

    ```bash
    bettyfixer file1.c file2.c ...
    ```

3. To create header file run:

    ```bash
    bettyfixer -H <header_name>.h ...
    ```


## Contributing

If you'd like to contribute to Betty Fixer, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure the code style follows the project conventions.
4. Test your changes thoroughly.
5. Create a pull request with a clear description of your changes.


Happy coding!



### Creaters: [@Moealsir](https://github.com/Moealsir) && [@malazmuzamil98](https://github.com/malazmuzamil98)
