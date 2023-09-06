from typing import List, Optional, Tuple
from django.shortcuts import reverse

from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status

from .models import Cluster


class ClusterViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def create_cluster_object(
        self,
        uuid: str = "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
        package: str = Cluster.Package.AUTOMATIC,
        status: str = Cluster.Status.PENDING,
        additional_params = None,
        size: int = 5
    ) -> Cluster:
        return Cluster.objects.create(
            uuid=uuid,
            package=package,
            status=status,
            additional_params=dict() if additional_params is None else additional_params,
            size=size
        )

    def test_post_one_object_to_db(self):
        cluster_data = {
            "uuid": "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "package": Cluster.Package.AUTOMATIC,
            "status": Cluster.Status.PENDING,
            "additional_params": {},
            "size": 5,
        }

        response = self.client.post(reverse('cluster-list'), data=cluster_data, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        cluster = Cluster.objects.get(uuid=cluster_data["uuid"])
        self.assertEquals(cluster_data["package"], cluster.package)
        self.assertEquals(cluster_data["status"], cluster.status)
        self.assertEquals(cluster_data["additional_params"], cluster.additional_params)
        self.assertEquals(cluster_data["size"], cluster.size)


    def test_read_one_object_from_db(self):
        cluster = self.create_cluster_object()

        get_response = self.client.get(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(get_response.data["package"], cluster.package)
        self.assertEquals(get_response.data["status"], cluster.status)
        self.assertEquals(get_response.data["additional_params"], cluster.additional_params)
        self.assertEquals(get_response.data["size"], cluster.size)

    def test_read_list_of_3_db_objects(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }
        for uuid in uuids:
            self.create_cluster_object(uuid=uuid)

        list_response = self.client.get(reverse('cluster-list'))

        self.assertEquals(list_response.status_code, status.HTTP_200_OK)
        response_uuids = {list_element["uuid"] for list_element in list_response.data}
        self.assertSetEqual(response_uuids, uuids)

    def test_optimistic_delete(self):
        cluster = self.create_cluster_object()

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid, )))

        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cluster.objects.filter(uuid=cluster.uuid).exists())
