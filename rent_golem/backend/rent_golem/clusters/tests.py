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
            owner,
            cluster_id: str = "dcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            package: str = Cluster.Package.AUTOMATIC,
            status: str = Cluster.Status.PENDING,
            additional_params=None,
            size: int = 2,
    ) -> Cluster:
        return Cluster.objects.create(
            id=cluster_id,
            package=package,
            status=status,
            additional_params=dict() if additional_params is None else additional_params,
            size=size,
            owner=owner
        )

    def test_post_one_object_to_db_as_registered_user(self):
        cluster_data = {
            "package": Cluster.Package.AUTOMATIC,
            "additional_params": {},
            "size": 5,
        }

        self.client.force_authenticate(user=self.owner)

        response = self.client.post(reverse('cluster-list'), data=cluster_data, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        cluster = Cluster.objects.get(id=response.data["id"])
        self.assertEquals(cluster_data["package"], cluster.package)
        self.assertEquals(Cluster.Status.PENDING, cluster.status)
        self.assertEquals(cluster_data["additional_params"], cluster.additional_params)
        self.assertEquals(cluster_data["size"], cluster.size)

    def test_if_post_one_object_to_db_as_anonymous_will_fail(self):
        cluster_data = {
            "package": Cluster.Package.AUTOMATIC,
            "additional_params": {},
            "size": 5,
        }
        clusters_count_before_request = Cluster.objects.all().count()

        response = self.client.post(reverse('cluster-list'), data=cluster_data, format="json")

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(Cluster.objects.all().count(), clusters_count_before_request)

    def test_read_one_object_from_db_as_registered_user(self):
        cluster = self.create_cluster_object(self.owner)
        self.client.force_authenticate(user=self.owner)

        get_response = self.client.get(reverse('cluster-detail', args=(cluster.id,)))

        self.assertEquals(get_response.status_code, status.HTTP_200_OK)
        self.assertEquals(get_response.data["id"], cluster.id)
        self.assertEquals(get_response.data["package"], cluster.package)
        self.assertEquals(get_response.data["status"], cluster.status)
        self.assertEquals(get_response.data["additional_params"], cluster.additional_params)
        self.assertEquals(get_response.data["size"], cluster.size)
        self.assertIn('created_at', get_response.data)
        self.assertIn('last_update', get_response.data)

    def test_read_list_of_3_db_objects_as_registered_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }
        for uuid in uuids:
            self.create_cluster_object(self.owner, cluster_id=uuid)

        self.client.force_authenticate(user=self.owner)

        list_response = self.client.get(reverse('cluster-list'))

        self.assertEquals(list_response.status_code, status.HTTP_200_OK)
        response_uuids = {list_element["id"] for list_element in list_response.data}
        self.assertSetEqual(response_uuids, uuids)

    def test_read_list_of_3_db_objects_as_anonymous_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda"
        }
        for uuid in uuids:
            self.create_cluster_object(self.owner, cluster_id=uuid)

        list_response = self.client.get(reverse('cluster-list'))

        self.assertEquals(list_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_read_list_of_3_db_objects_and_1_deleted_as_registered_user(self):
        uuids = {
            "acec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "bcec5482-59ef-4c0e-9ea4-4e5451c3cbda",
            "ccec5482-59ef-4c0e-9ea4-4e5451c3cbda",
        }
        for uuid in uuids:
            self.create_cluster_object(self.owner, cluster_id=uuid)
        cluster = self.create_cluster_object(self.owner, cluster_id="dcec5482-59ef-4c0e-9ea4-4e5451c3cbda")
        cluster.is_deleted = True
        cluster.save()

        self.client.force_authenticate(user=self.owner)

        list_response = self.client.get(reverse('cluster-list'))

        self.assertEquals(list_response.status_code, status.HTTP_200_OK)
        response_uuids = {list_element["id"] for list_element in list_response.data}
        self.assertSetEqual(response_uuids, uuids)

    def test_update_by_owner(self):
        cluster = self.create_cluster_object(self.owner)

        self.client.force_authenticate(user=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.id,)),
            data={'size': 3}
        )

        cluster.refresh_from_db()
        self.assertEquals(update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(cluster.size, 3)

    def test_update_2_fields_by_owner_should_update_only_size(self):
        cluster = self.create_cluster_object(self.owner)

        self.client.force_authenticate(user=self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.id,)),
            data={'size': 3, 'additional_params': {'xyz': '123'}},
            format='json'
        )

        cluster.refresh_from_db()
        self.assertEquals(update_response.status_code, status.HTTP_200_OK)
        self.assertEquals(cluster.size, 3)
        self.assertEquals(cluster.additional_params, {})

    def test_update_by_user_not_owner(self):
        cluster = self.create_cluster_object(self.owner)

        self.client.force_authenticate(user=self.insignificant_user)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.id, )),
            data={'size': 3},
        )

        cluster.refresh_from_db()
        self.assertEquals(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(cluster.size, 2)

    def test_update_by_anonymous_user(self):
        cluster = self.create_cluster_object(self.owner)

        update_response = self.client.patch(
            reverse('cluster-detail', args=(cluster.id, )),
            data={'size': 3}
        )

        cluster.refresh_from_db()
        self.assertEquals(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(cluster.size, 2)

    def test_put_turned_off(self):
        cluster = self.create_cluster_object(self.owner)
        self.client.force_authenticate(user=self.owner)

        put_response = self.client.put(
            reverse('cluster-detail', args=(cluster.id, )),
            data={'size': 3}
        )

        cluster.refresh_from_db()
        self.assertEquals(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEquals(cluster.size, 2)

    def test_delete_by_owner(self):
        cluster = self.create_cluster_object(self.owner)

        self.assertFalse(cluster.is_deleted)

        self.client.force_authenticate(user=self.owner)
        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.id,)))

        cluster.refresh_from_db()
        self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(cluster.is_deleted)

    def test_delete_by_user_not_owner(self):
        cluster = self.create_cluster_object(self.owner)

        self.assertFalse(cluster.is_deleted)

        self.client.force_authenticate(user=self.insignificant_user)
        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.id,)))

        cluster.refresh_from_db()
        self.assertEquals(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(cluster.is_deleted)

    def test_delete_by_anonymous_user(self):
        cluster = self.create_cluster_object(self.owner)

        self.assertFalse(cluster.is_deleted)

        delete_response = self.client.delete(reverse('cluster-detail', args=(cluster.id,)))

        cluster.refresh_from_db()
        self.assertEquals(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(cluster.is_deleted)
