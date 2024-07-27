import json

from django.test import TestCase
from django.contrib.auth.models import User
from graphene_django.utils.testing import GraphQLTestCase

from .models import Device


class DeviceModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='password')
        self.device = Device.objects.create(
            name='Test Device',
            created_by=self.user,
            modified_by=self.user
        )

    def test_device_creation(self):
        self.assertEqual(self.device.name, 'Test Device')
        self.assertTrue(isinstance(self.device, Device))
        self.assertEqual(Device.objects.count(), 1)


class DeviceGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_URL = 'http://localhost:8000/app/v1/graphql/'

    def setUp(self):
        self.user = User.objects.create(
            username='testuser', password='password')
        self.device = Device.objects.create(
            name='Test Device',
            created_by=self.user,
            modified_by=self.user
        )

    def test_create_device_mutation(self):
        response = self.query(
            '''
            mutation {
            createDevice(name: "New Device") {
                device {
                id
                name
                     }
                }
                }
            '''
        )
        print(response.content)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createDevice']
                         ['device']['name'], 'New Device')

    def test_update_device_mutation(self):
        device = Device.objects.create(
            name='Device to Delete',
            created_by=self.user,
            modified_by=self.user
        )
        response = self.query(
            '''
            mutation {
            updateDevice(id: %d, name: "Updated Device") {
                device {
                id
                name
                }
            }
            }
            ''' % device.id
        )
        print(response.content)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateDevice']
                         ['device']['name'], 'Updated Device')

    def test_delete_device_mutation(self):

        device = Device.objects.create(
            name='Device to Delete',
            created_by=self.user,
            modified_by=self.user
        )
        response = self.query(
            '''
            mutation {
                deleteDevice(id: %d) {
                    success
                }
            }
            ''' % device.id
        )
        print(response.content)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['deleteDevice']['success'])
