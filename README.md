# Testing Demo

Demonstrate testing of a UI and API with Pytest and Playwright.

The sample application allows the following:
1. Web UI
   1. Allows user registration
   2. Login to view user details
   3. Logout
2. API
   1. Allows user registration
   2. Fetch auth token
   3. Get user details
   4. Get list of all users
   5. Update user details

---

**Source Code**: [https://github.com/a-matta/testing_demo_playwright_python](https://github.com/a-matta/testing_demo_playwright_python)

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
* Run the application
  ```sh
  # Uses PyInvoke
  inv app
  ```
* Running the tests
  ```sh
  inv tests
  ```

---

This project was generated using the [playwright-python-cookiecutter](https://github.com/a-matta/playwright-python-cookiecutter) template.
