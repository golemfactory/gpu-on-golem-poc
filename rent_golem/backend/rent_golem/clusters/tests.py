from django.shortcuts import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from clusters.models import Cluster
from accounts.models import User


class ClusterViewSetTest(APITestCase):
    def setUp(self) -> None:
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

        self.client.force_authenticate(user=self.owner)

        response = self.client.post(reverse('cluster-list'), data=cluster_data, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        cluster = Cluster.objects.get(uuid=cluster_data["uuid"])
        self.assertEquals(cluster_data["package_type"], cluster.package_type)
        self.assertEquals(cluster_data["status"], cluster.status)
        self.assertEquals(cluster_data["additional_params"], cluster.additional_params)
        self.assertEquals(cluster_data["size"], cluster.size)
        self.assertEquals(cluster_data["owner"], cluster.owner_id)

    def test_if_post_one_object_to_db_as_anonymous_will_fail(self):
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
        self.assertEquals(get_response.data["owner"], cluster.owner_id)

    def test_read_list_of_3_db_objects_as_registered_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }
        for uuid in uuids:
            self.create_cluster_object(uuid=uuid, owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        list_response = self.client.get(reverse('cluster-list'))

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

    def test_read_list_of_3_db_objects_and_1_deleted_as_registered_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda",
        }
        for uuid in uuids:
            self.create_cluster_object(uuid=uuid, owner=self.owner)
        cluster = self.create_cluster_object(uuid="dcec5482-59ef-4c0e-9ea4-4e5451c3cbda", owner=self.owner)
        cluster.is_deleted = True
        cluster.save()

        self.client.force_authenticate(user=self.owner)

        list_response = self.client.get(reverse('cluster-list'))

        self.assertEquals(list_response.status_code, status.HTTP_200_OK)
        response_uuids = {list_element["uuid"] for list_element in list_response.data}
        self.assertSetEqual(response_uuids, uuids)

    def test_update_by_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid,)),
            data={'size': cluster.size + 1}
        )

        self.assertEquals(update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(Cluster.objects.get(uuid=cluster.uuid).size, 6)

    def test_update_2_fields_by_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid,)),
            data={'size': cluster.size + 1, 'package_type': Cluster.Package.JUPYTER}
        )

        cluster.refresh_from_db()
        self.assertEquals(update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(cluster.size, 6)
        self.assertEquals(cluster.package_type, Cluster.Package.AUTOMATIC)

    def test_update_by_user_not_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.client.force_authenticate(user=self.insignificant_user)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid, )),
            data={'size': cluster.size+1},
        )

        self.assertEquals(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Cluster.objects.get(uuid=cluster.uuid).size, 5)

    def test_update_by_anonymous_user(self):
        cluster = self.create_cluster_object(owner=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.uuid, )),
            data={'size': cluster.size+1}
        )

        self.assertEquals(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Cluster.objects.get(uuid=cluster.uuid).size, 5)

    def test_put_turned_off(self):
        cluster = self.create_cluster_object(owner=self.owner)
        self.client.force_authenticate(user=self.owner)

        put_response = self.client.put(
            reverse('cluster-detail', args=(cluster.uuid, )),
            data={'size': cluster.size+1}
        )

        self.assertEquals(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_by_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.assertFalse(Cluster.objects.get(uuid=cluster.uuid).is_deleted)

        self.client.force_authenticate(user=self.owner)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Cluster.objects.get(uuid=cluster.uuid).is_deleted)

    def test_delete_by_user_not_owner(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.assertFalse(Cluster.objects.get(uuid=cluster.uuid).is_deleted)

        self.client.force_authenticate(user=self.insignificant_user)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Cluster.objects.get(uuid=cluster.uuid).is_deleted)

    def test_delete_by_anonymous_user(self):
        cluster = self.create_cluster_object(owner=self.owner)

        self.assertFalse(Cluster.objects.get(uuid=cluster.uuid).is_deleted)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.uuid,)))

        self.assertEquals(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Cluster.objects.get(uuid=cluster.uuid).is_deleted)
