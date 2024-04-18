import pytest
from unittest.mock import patch
from src.util.dao import DAO

database_name = 'test'
collection_name = 'tests'

collection_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["email"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "'name' must be a string"
            },
            "email": {
                "bsonType": "string",
                "description": "'email' must be a string and is required"
            },
        }
    }
}

valid_users = [
    {'name': 'john', 'email': 'john.smith@gmail.com'},
    {'name': 'jane', 'email': 'jane.doe@gmail.com'},
    {'name': 'john', 'email': 'john.smurd@gmail.com'}
]

invalid_users = [
    {'name': 'bad john'},
    {'name': 'bad jane', 'email': None}
]

@pytest.fixture(scope="module")
def database(mongodb):
    '''
    This fixture creates a database instance and returns it.
    It also creates a collection with a schema validator.
    The database instance is module-scoped and will be shared by all tests requesting it.
    '''
    database = mongodb[database_name]

    if collection_name not in database.list_collection_names():
        database.create_collection(collection_name, validator=collection_validator)
    
    yield database

    database[collection_name].drop()

class TestCreate:
    @pytest.fixture(scope="class")
    def dao(self, database):
        with patch('src.util.dao.pymongo.MongoClient') as mock_client:
            # Replace the edutask database with the test database
            mock_client.return_value.edutask = database

            dao = DAO(collection_name)

            return dao

    @pytest.mark.integration
    @pytest.mark.parametrize("user", valid_users)
    def test_return_user(self, dao, user):
       
        result = dao.create(user)

        # Assert that the result is as expected
        assert result == user

    @pytest.mark.integration
    @pytest.mark.parametrize("user", valid_users)
    def test_db_contains_user(self, mongodb, user):
        # Check if the user is in the database
        assert mongodb.test[collection_name].find_one({"_id": user["_id"]}) == user

    