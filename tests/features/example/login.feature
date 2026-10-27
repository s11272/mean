@qtest_TC101
Feature: System Login

  Scenario: Successful login with valid credentials
    Given the user opens the login page
    When the user logs in as "admin" with password "secret"
    Then the flash message "Welcome, admin!" is displayed