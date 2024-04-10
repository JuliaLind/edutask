import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

"""
Module that tests the get_user_by_email method of
class UserController. The tests in this
module ensure that the warning
message is printed only in the scenario
where email address matches more than 1 user.
In all other cases no message should be printed.
"""

valid_email = 'jane.doe@email.com'
user = {
    'firstName': 'Jane',
    'email': 'jane.doe@email.com'
}
second_user = {
    'firstName': 'Hanna',
    'email': 'jane.doe@email.com'
}
# mockedDAO = MagicMock()
# sut = UserController(dao=mockedDAO)

@pytest.fixture
def sut():
    mockedDAO = MagicMock()
    mockedsut = UserController(dao=mockedDAO)
    return mockedsut

@pytest.mark.unit
def test_get_user_by_email_match_two_print(sut, capsys):
    """
    Tests get_user_by_email method with valid email.
    Two users match. No database failure.
    Assert that a warning message containing the
    email address is printed
    """
    # mockedDAO.find.return_value = [user, second_user]
    sut.dao.find.return_value = [user, second_user]

    sut.get_user_by_email(email=valid_email)
    printed = capsys.readouterr()

    assert valid_email in printed.out


@pytest.mark.unit
@pytest.mark.parametrize('user_email, user_array', [
    (valid_email, [user]),
    (valid_email, [])
    ])
def test_get_user_by_email_match_no_print(sut, capsys, user_email, user_array):
    """
    Tests get_user_by_email method with:
    1. valid email - no match,
    2. valid email - exactly one match,
    In none of these cases should the
    print-function have been called
    """
    # mockedDAO.find.return_value = user_array
    sut.dao.find.return_value = user_array

    sut.get_user_by_email(email=user_email)
    printed = capsys.readouterr()

    assert printed.out == ""


@pytest.mark.unit
def test_get_user_by_email_invalid_no_print(sut, capsys):
    """
    Tests get_user_by_email method with invalid email,
    The print function should not have been called
    """

    # catch the value error so we can check
    # that the print function is not called before
    # ValueError is raised when the function
    # is called with invalid email
    with pytest.raises(ValueError):
        sut.get_user_by_email(email="invalidemail.com")
    printed = capsys.readouterr()

    assert printed.out == ""

@pytest.mark.unit
def test_get_user_by_email_db_failure_no_print(sut, capsys):
    """
    Tests get_user_by_email method with valid email, there should be no printout when Exeption is raised due to database failure
    """

    sut.dao.find.side_effect = Exception("DBfailure")
    # catch the value error so we can check
    # that the print function is not called before
    # ValueError is raised when the function
    # is called with invalid email
    with pytest.raises(Exception):
        sut.get_user_by_email(email=valid_email)
    printed = capsys.readouterr()

    assert printed.out == ""