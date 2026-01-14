1. tests/test_login_errors.py

Role: Test orchestration (WHAT to test)

This file:

Defines the test scenarios

Loads test data

Executes login actions

Asserts expected behavior

What it does step-by-step:

Reads all login scenarios from JSON (data-driven)

Runs the same test logic for each case

Verifies:

Correct error message appears

Error can be closed

Test continues even if some cases fail

Why this file exists:

Keeps test logic separate from UI details

Makes adding new test cases trivial (just update JSON)

Fully matches the assignment requirement: “Tester les scénarios de connexion échouée”

2. pages/login_page.py

Role: Page Object (HOW to interact with the page)

This file:

Knows where elements are

Knows how to interact with the login page

Contains:

Locators (username, password, login button, error message, close button)

Methods:

load() → opens the page

login() → performs login

get_error_message() → reads dynamic error

close_error() → clicks the close button

is_error_closed() → validates error dismissal

Why this file exists:

If a selector changes → fix it once here

Tests stay readable and short

This is the industry-standard Page Object Model (POM)

3. data/login_errors.json

Role: Test data (WITH WHAT values to test)

This file:

Stores all login scenarios

Drives the test execution

Contains:

Invalid users

Empty fields

Locked user

Special characters

Intentionally “wrong” valid users (to prove failure handling)

Why this file exists:

No hard-coded data in tests

Easy to add/remove cases

Non-technical people can update tests

Makes the test future-proof and scalable

4. utils/json_reader.py

Role: Data loader (HOW data is read)

This file:

Reads JSON safely

Returns Python objects to pytest

Why this file exists:

Avoids duplicating file-reading logic

Centralizes data access

Makes switching JSON → YAML/CSV later easy

5. conftest.py

Role: Test infrastructure (ENVIRONMENT setup)

This file:

Creates and tears down the Selenium WebDriver

Shares the browser across tests using fixtures

Why this file exists:

No browser setup inside test files

Pytest auto-detects it

CI-friendly and clean

6. screenshots/ (optional but recommended)

Role: Debugging artifacts

This folder:

Stores screenshots when tests fail

Why this exists:

Critical for CI/CD

Helps explain failures to teachers or teammates

Industry best practice

Why this structure is GOOD for your assignment

Your teacher asked for:

Dynamic error handling ✔

Error message validation ✔

Error close button ✔

Multiple scenarios ✔

You delivered:

Data-driven testing

Page Object Model

Clear failure reporting

Test continuation on failure

This is well above beginner level.
