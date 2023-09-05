from typing import List, Optional, Tuple
from django.shortcuts import reverse

from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status

from .models import Cluster
from accounts.models import User


class ClusterViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.owner = User.objects.create_user(email="test@test.com", password="test1234")
        self.insignificant_user = User.objects.create_user(email="test2@test.com", password="test1234")

    def create_cluster_object(
            self,
            uuid: str = "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            package_type: str = Cluster.Package.AUTOMATIC,
            status: str = Cluster.Status.STARTING,
            additional_params=None,
            size: int = 5,
            owner: User = None
    ) -> Cluster:
        if owner is None:
            owner = User.objects.create_user(email="test@test.com", password="test1234")
        return Cluster.objects.create(
            uuid=uuid,
            package_type=package_type,
            status=status,
            additional_params=dict() if additional_params is None else additional_params,
            size=size,
            owner=owner
        )

    def test_post_one_object_to_db_as_registered_user(self):
        cluster_data = {
            "uuid": "aaec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "package_type": Cluster.Package.AUTOMATIC,
            "status": Cluster.Status.STARTING,
            "additional_params": {},
            "size": 5,
            "owner": self.owner.id
        }

        jwt = self.client.post(
            reverse("token_obtain_pair"), data={"email": self.owner.email, "password": "test1234"}
        ).data["access"]

        response = self.client.post(
            reverse('cluster-list'), data=cluster_data, headers={"Authorization": f"Bearer {jwt}"}, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        cluster = Cluster.objects.get(uuid=cluster_data["uuid"])
        self.assertEquals(cluster_data["package_type"], cluster.package_type)
        self.assertEquals(cluster_data["status"], cluster.status)
        self.assertEquals(cluster_data["additional_params"], cluster.additional_params)
        self.assertEquals(cluster_data["size"], cluster.size)
        self.assertEquals(cluster_data["owner"], self.owner.id)

    def test_post_one_object_to_db_as_anonymous_user(self):
        cluster_data = {
            "uuid": "aaec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "package_type": Cluster.Package.AUTOMATIC,
            "status": Cluster.Status.STARTING,
            "additional_params": {},
            "size": 5,
            "owner": self.owner.id
        }

        response = self.client.post(reverse('cluster-list'), data=cluster_data, format="json")

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Cluster.objects.filter(uuid=cluster_data["uuid"]).exists())

    def test_read_one_object_from_db_as_registered_user(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        get_response = self.client.get(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(get_response.data["package_type"], cluster.package_type)
        self.assertEquals(get_response.data["status"], cluster.status)
        self.assertEquals(get_response.data["additional_params"], cluster.additional_params)
        self.assertEquals(get_response.data["size"], cluster.size)
        self.assertEquals(get_response.data["owner"], self.owner.id)

    def test_read_list_of_3_db_objects_as_registered_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }
        for uuid in uuids:
            self.create_cluster_object(uuid=uuid, owner=self.owner)

        jwt = self.client.post(
            reverse("token_obtain_pair"), data={"email": self.owner.email, "password": "test1234"}
        ).data["access"]

        list_response = self.client.get(reverse('cluster-list'), headers={"Authorization": f"Bearer {jwt}"})

        self.assertEquals(list_response.status_code, status.HTTP_200_OK)
        response_uuids = {list_element["uuid"] for list_element in list_response.data}
        self.assertSetEqual(response_uuids, uuids)

    def test_read_list_of_3_db_objects_as_anonymous_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }
        for uuid in uuids:
            self.create_cluster_object(uuid=uuid, owner=self.owner)

        list_response = self.client.get(reverse('cluster-list'))

        self.assertEquals(list_response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Update
    def test_update_by_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        jwt = self.client.post(
            reverse("token_obtain_pair"), data={"email": self.owner.email, "password": "test1234"}
        ).data["access"]

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid,)),
            data={'size': cluster.size + 1},
            headers={"Authorization": f"Bearer {jwt}"}
        )

        self.assertEquals(update_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(Cluster.objects.filter(uuid=cluster.uuid).exists())
        self.assertEquals(Cluster.objects.filter(uuid=cluster.uuid).first().size, 6)


    def test_update_by_owner_2_variables(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid,)),
            data={'size': cluster.size + 1, 'package_type': Cluster.Package.AUTOMATIC}
        )

        self.assertEquals(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Cluster.objects.filter(uuid=cluster.uuid).exists())
        self.assertEquals(Cluster.objects.filter(uuid=cluster.uuid).first().size, 5)

    def test_update_by_user_not_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        jwt_insignificant_user = self.client.post(
            reverse("token_obtain_pair"), data={"email": self.insignificant_user.email, "password": "test1234"}
        ).data["access"]

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid, )),
            data={'size': cluster.size+1},
            headers={"Authorization": f"Bearer {jwt_insignificant_user}"}
        )

        self.assertEquals(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Cluster.objects.filter(uuid=cluster.uuid).exists())
        self.assertEquals(Cluster.objects.filter(uuid=cluster.uuid).first().size, 5)

    def test_update_by_anonymous_user(self):
        cluster = self.create_cluster_object(owner=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid, )),
            data={'size': cluster.size+1}
        )

        self.assertEquals(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Cluster.objects.filter(uuid=cluster.uuid).exists())
        self.assertEquals(Cluster.objects.filter(uuid=cluster.uuid).first().size, 5)

    def test_put_turned_off(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        put_response = self.client.put(
            reverse('cluster-detail', args=(cluster.uuid, )),
            data={'size': cluster.size+1}
        )

        self.assertEquals(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Delete
    def test_delete_by_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cluster.objects.filter(uuid=cluster.uuid).exists())

    def test_delete_by_user_not_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.insignificant_user)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Cluster.objects.filter(uuid=cluster.uuid).exists())

    def test_delete_by_anonymous_user(self):
        cluster = self.create_cluster_object(owner=self.owner)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Cluster.objects.filter(uuid=cluster.uuid).exists())
