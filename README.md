# Python-Playwright

| Item              |        Meaning                | Why we use it                                                  |
| ----------------- | ----------------------------- | -------------------------------------------------------------- |
| `@pytest.fixture` | Marks a function as a fixture | Tells pytest: "This function prepares something for my tests." |
| `return`          | Gives something back          | Provides data/object to the test                               |
| `yield`           | Gives something + cleanup     | Useful when you need to clean up after the test                |
| `scope`           | Controls fixture lifetime     | Decides how often the fixture runs                             |


| Command                                                                                             | Meaning                                  |
| ----------------------------------------------------------------------------------------------------| ---------------------------------------  |
| `pytest`                                                                                            | Run all tests                            |
| `pytest -m smoke`                                                                                   | Run only `smoke` marked(tag) tests       |
| `pytest -s`                                                                                         | Show `print()` output                    |
| `pytest -s -m smoke`                                                                                | Run smoke tests + show `print()` output  |
| `pytest tests/test_2_inventory_page.py::test_tc_002_add_single_product_to_cart`                     | Run a specific test (`test_3`) in a file |
| `pytest tests/test_2_inventory_page.py::test_tc_002_add_single_product_to_cart --headed`            | Run the test in headed mode              |
| `pytest test_login.py --browser webkit`                                                             | Browser opened in specific browser       |

**Parallel testing:**
- Run tests on all CPU cores: `pytest -n auto`
- Run tests on a specific number of cores (e.g., 4): pytest -n 4

**Pytest-html reports:**
- `pytest --html=report.html ./tests`

**Allure pytest reports:**
- `npm install -g allure-commandline` (without this installation, allure will not work)
- `pytest --alluredir=allure_result_folder ./tests`
- `allure serve allure_result_folder`

**Playwight Trace viewer:**
`pytest --tracing on`

**Options for tracing are:**
- on: Record trace for each test
- off: Do not record trace. (default)
- retain-on-failure: Record trace for each test, but remove all traces from successful test runs.
- This will record the trace and place it into the file named trace.zip in your test-results directory.
- Opening the trace: playwright show-trace trace.zip


**playwright Locators**
- #css with ID using #ID
- #css with Class using .Class