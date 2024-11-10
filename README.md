# Testing Demo

A short description of the project

---

*Documentation**: [https://a-matta.github.io/testing_demo](https://a-matta.github.io/testing_demo)

**Source Code**: [https://github.com/a-matta/testing_demo](https://github.com/a-matta/testing_demo)

---

## Development

* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.12+
* Clone this repository
* Create a virtual environment and activate it
  ```sh
  poetry shell
  ```
* Install the dependencies
  ```sh
  poetry install
  ```
* Install playwright dependencies
  ```sh
  playwright install
  ```
* Running the tests
  ```sh
  # Uses PyInvoke
  inv tests
  ```

---

This project was generated using the [playwright-python-cookiecutter](https://github.com/a-matta/playwright-python-cookiecutter) template.
