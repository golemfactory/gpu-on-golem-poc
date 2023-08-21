from django.shortcuts import reverse

from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status


class ClustersViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def create_dummy_db_object(self):
        json_data = {
            "uuid": "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "package_type": "automatic",
            "status": "Starting",
            "additional_params": {},
            "size": 5,
        }
        return self.client.post(reverse('clusters-list'), data=json_data, format="json"), json_data

    def test_post_one_object_to_db(self):
        response, json_data = self.create_dummy_db_object()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_read_one_object_from_db(self):
        post_response, json_data = self.create_dummy_db_object()

        get_response = self.client.get(reverse('clusters-detail', args=[json_data["uuid"]]))
        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        for keyword in json_data.keys():
            self.assertEquals(json_data[keyword], get_response.data[keyword])

    def test_read_list_of_3_db_objects(self):
        uuids = {
                "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
                "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
                "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }

        post_responses = [self.client.post(reverse('clusters-list'), data={
            "uuid": uuid,
            "package_type": "automatic",
            "status": "Starting",
            "additional_params": {},
            "size": 5,
        }, format="json") for uuid in uuids]
        self.assertEquals(
            [post_responses[i].data["uuid"] for i in range(len(post_responses))].sort(),
            list(uuids).sort()
        )

    def test_optimistic_delete(self):
        post_response, json_data = self.create_dummy_db_object()

        delete_response = self.client.delete(reverse('clusters-detail', args=[json_data["uuid"]]))
        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        get_after_delete_response = self.client.get(reverse('clusters-detail', args=[json_data["uuid"]]))
        self.assertEquals(get_after_delete_response.status_code, status.HTTP_404_NOT_FOUND)