Feature: Order Transaction
  Tests related to Order Transactions


  Scenario Outline: Verify order success message shown in details page
    Given place the item order with <username> and <password>
    And the user is on landing page
    When I login to portal with <username> and <password>
    And navigate to orders page
    And select the orderID
    Then order message is successfuly displayed
    Examples:
      | username            | password |
      |rahulshetty@gmail.com| Iamking@000|