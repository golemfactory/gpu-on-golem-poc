from typing import List, Optional, Tuple
from django.shortcuts import reverse

from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status

from .models import Cluster


class ClusterViewSetTest(APITestCase):
    json_data = {
        "uuid": "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
        "package_type": "automatic",
        "status": "Starting",
        "additional_params": {},
        "size": 5,
    }

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def create_dummy_db_object(
        self,
        uuid: str = "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
        package_type: str = "automatic",
        cluster_status: str = "Starting",
        additional_params: dict = {},
        size: int = 5
    ) -> Tuple[Cluster, dict]:
        json_data = {
            "uuid": uuid,
            "package_type": package_type,
            "status": cluster_status,
            "additional_params": additional_params,
            "size": size,
        }
        return Cluster.objects.create(**json_data), json_data

    def test_post_one_object_to_db(self):
        response = self.client.post(reverse('cluster-list'), data=self.json_data, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        cluster = Cluster.objects.filter(uuid=self.json_data["uuid"]).first()
        self.assertEquals(self.json_data["package_type"], cluster.package_type)
        self.assertEquals(self.json_data["status"], cluster.status)
        self.assertEquals(self.json_data["additional_params"], cluster.additional_params)
        self.assertEquals(self.json_data["size"], cluster.size)


    def test_read_one_object_from_db(self):
        cluster, json_data = self.create_dummy_db_object()

        get_response = self.client.get(reverse('cluster-detail', args=[json_data["uuid"]]))
        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(get_response.data["package_type"], cluster.package_type)
        self.assertEquals(get_response.data["status"], cluster.status)
        self.assertEquals(get_response.data["additional_params"], cluster.additional_params)
        self.assertEquals(get_response.data["size"], cluster.size)

    def test_read_list_of_3_db_objects(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }

        [self.create_dummy_db_object(uuid=uuid) for uuid in uuids]

        list_response = self.client.get(reverse('cluster-list'))
        self.assertEquals(list_response.status_code, status.HTTP_200_OK)

        response_uuids = set([list_element["uuid"] for list_element in list_response.data])
        self.assertEquals(response_uuids, uuids)

    def test_optimistic_delete(self):
        post_response, self.json_data = self.create_dummy_db_object()

        delete_response = self.client.delete(reverse('cluster-detail', args=[self.json_data["uuid"]]))
        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Cluster.objects.filter(uuid=self.json_data["uuid"]).exists())