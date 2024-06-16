import unittest
from unittest.mock import patch, MagicMock
from models.item import Item
from models.user import User
from services.item_service import ItemService

class ItemServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.item_service = ItemService()

    @patch('models.user.User.objects')
    def test_create_item_success(self, mock_user_objects):
        # Mock user lookup to return a user
        user_id = 'user_id'
        mock_user_objects.return_value.first.return_value = User(id=user_id)

        data = {'name': 'Test Item', 'description': 'This is a test item'}
        with patch.object(Item, 'save', return_value=None) as mock_save:
            result = self.item_service.create_item(data, user_id)
            self.assertIn('id', result)
            self.assertEqual(result['name'], 'Test Item')
            self.assertEqual(result['description'], 'This is a test item')
            mock_save.assert_called_once()

    @patch('models.item.Item.objects')
    def test_get_item_success(self, mock_item_objects):
        # Mock item lookup to return an item with a user
        item_id = 'item_id'
        mock_user = User(id='user_id')
        mock_item = Item(id=item_id, name='Test Item', description='This is a test item', user=mock_user)
        mock_item_objects.return_value.first.return_value = mock_item

        result = self.item_service.get_item(item_id)
        self.assertEqual(result['id'], item_id)
        self.assertEqual(result['name'], 'Test Item')
        self.assertEqual(result['description'], 'This is a test item')

    @patch('models.item.Item.objects')
    def test_get_items_success(self, mock_item_objects):
        # Mock item lookup to return a list of items
        user_id = 'user_id'
        mock_item_objects.return_value = [
            Item(id='1', name='Item 1', description='Description 1', user=User(id=user_id)),
            Item(id='2', name='Item 2', description='Description 2', user=User(id=user_id))
        ]

        result = self.item_service.get_items(user_id)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Item 1')
        self.assertEqual(result[1]['name'], 'Item 2')

    @patch('models.item.Item.objects')
    def test_update_item_success(self, mock_item_objects):
        # Mock item lookup to return an item
        item_id = 'item_id'
        mock_item = Item(id=item_id, name='Old Name', description='Old Description')
        mock_item_objects.return_value.first.return_value = mock_item

        data = {'name': 'New Name', 'description': 'New Description'}
        with patch.object(Item, 'update') as mock_update:
            # Call the update_item method
            result = self.item_service.update_item(item_id, data)

            # Assert that the update method of the mocked item is called with the expected arguments
            mock_update.assert_called_once_with(set__name='New Name', set__description='New Description',
                                                set__created_at=mock_item.created_at)

            # Assert that the result matches the expected message
            self.assertEqual(result, {"message": "Item updated successfully"})

    @patch('models.item.Item.objects')
    def test_delete_item_success(self, mock_item_objects):
        # Mock item lookup to return an item
        item_id = 'item_id'
        mock_item = MagicMock()
        mock_item_objects.return_value.first.return_value = mock_item

        result = self.item_service.delete_item(item_id)
        self.assertEqual(result, {"message": "Item deleted successfully"})

        # Assert that the delete method of the mocked item object is called
        mock_item.delete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
