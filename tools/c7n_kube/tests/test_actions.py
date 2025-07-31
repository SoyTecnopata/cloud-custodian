# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from common_kube import KubeTest


class TestDeleteAction(KubeTest):
    def test_delete_action(self):
        factory = self.replay_flight_data()
        p = self.load_policy(
            {
                "name": "delete-namespace",
                "resource": "k8s.namespace",
                "filters": [{"metadata.name": "test"}],
                "actions": [{"type": "delete"}],
            },
            session_factory=factory,
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        client = factory().client("Core", "V1")
        namespaces = client.list_namespace().to_dict()["items"]
        test_namespace = [n for n in namespaces if n["metadata"]["name"] == "test"][0]
        self.assertEqual(test_namespace["status"]["phase"], "Terminating")

    def test_delete_namespaced_resource(self):
        factory = self.replay_flight_data()
        p = self.load_policy(
            {
                "name": "delete-service",
                "resource": "k8s.service",
                "filters": [{"metadata.name": "hello-node"}],
                "actions": [{"type": "delete"}],
            },
            session_factory=factory,
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        client = factory().client("Core", "V1")
        namespaces = client.list_service_for_all_namespaces().to_dict()["items"]
        hello_node_service = [n for n in namespaces if n["metadata"]["name"] == "hello-node"]
        self.assertFalse(hello_node_service)


class TestPatchAction(KubeTest):
    def test_patch_action(self):
        factory = self.replay_flight_data()
        p = self.load_policy(
            {
                "name": "test-patch",
                "resource": "k8s.deployment",
                "filters": [{"metadata.name": "hello-node"}, {"spec.replicas": 1}],
                "actions": [{"type": "patch", "options": {"spec": {"replicas": 2}}}],
            },
            session_factory=factory,
        )
        resources = p.run()
        self.assertEqual(len(resources), 1)
        client = factory().client("Apps", "V1")
        deployments = client.list_deployment_for_all_namespaces().to_dict()["items"]
        hello_node_deployment = [d for d in deployments if d["metadata"]["name"] == "hello-node"][0]
        self.assertEqual(hello_node_deployment["spec"]["replicas"], 2)


class TestOffHourOnHourFilters(KubeTest):
    def test_deployment_offhour_filter_registration(self):
        """Test that OffHour filter is properly registered for deployments"""
        from c7n_kube.resources.apps.deployment import Deployment
        self.assertIn('offhour', Deployment.filter_registry)
        self.assertIn('onhour', Deployment.filter_registry)

    def test_statefulset_offhour_filter_registration(self):
        """Test that OffHour filter is properly registered for statefulsets"""
        from c7n_kube.resources.apps.statefulset import StatefulSet
        self.assertIn('offhour', StatefulSet.filter_registry)
        self.assertIn('onhour', StatefulSet.filter_registry)

    def test_daemonset_offhour_filter_registration(self):
        """Test that OffHour filter is properly registered for daemonsets"""
        from c7n_kube.resources.apps.daemonset import DaemonSet
        self.assertIn('offhour', DaemonSet.filter_registry)
        self.assertIn('onhour', DaemonSet.filter_registry)

    def test_replicaset_offhour_filter_registration(self):
        """Test that OffHour filter is properly registered for replicasets"""
        from c7n_kube.resources.apps.replicaset import ReplicaSet
        self.assertIn('offhour', ReplicaSet.filter_registry)
        self.assertIn('onhour', ReplicaSet.filter_registry)

    def test_pod_offhour_filter_registration(self):
        """Test that OffHour filter is properly registered for pods"""
        from c7n_kube.resources.core.pod import Pod
        self.assertIn('offhour', Pod.filter_registry)
        self.assertIn('onhour', Pod.filter_registry)

    def test_custom_resource_offhour_filter_registration(self):
        """Test that OffHour filter is properly registered for custom resources"""
        from c7n_kube.resources.crd import CustomNamespacedResourceDefinition, CustomResourceDefinition
        self.assertIn('offhour', CustomNamespacedResourceDefinition.filter_registry)
        self.assertIn('onhour', CustomNamespacedResourceDefinition.filter_registry)
        self.assertIn('offhour', CustomResourceDefinition.filter_registry)
        self.assertIn('onhour', CustomResourceDefinition.filter_registry)

    def test_deployment_offhour_policy_validation(self):
        """Test that deployment offhour policy validates correctly"""
        factory = self.replay_flight_data()
        p = self.load_policy(
            {
                "name": "test-deployment-offhour",
                "resource": "k8s.deployment",
                "filters": [
                    {
                        "type": "offhour",
                        "default_tz": "et",
                        "offhour": 19
                    }
                ],
                "actions": [{"type": "patch", "options": {"spec": {"replicas": 0}}}],
            },
            session_factory=factory,
        )
        # Policy should validate without errors
        self.assertIsNotNone(p)

    def test_deployment_onhour_policy_validation(self):
        """Test that deployment onhour policy validates correctly"""
        factory = self.replay_flight_data()
        p = self.load_policy(
            {
                "name": "test-deployment-onhour",
                "resource": "k8s.deployment",
                "filters": [
                    {
                        "type": "onhour",
                        "default_tz": "et",
                        "onhour": 7
                    }
                ],
                "actions": [{"type": "patch", "options": {"spec": {"replicas": 2}}}],
            },
            session_factory=factory,
        )
        # Policy should validate without errors
        self.assertIsNotNone(p)
