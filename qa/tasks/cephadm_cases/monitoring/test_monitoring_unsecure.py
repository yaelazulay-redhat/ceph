"""
Unsecure monitoring stack integration tests.

``qa/suites/orch/cephadm/workunits/task/test_monitoring_stack_unsecure.yaml``
leaves ``mgr/cephadm/secure_monitoring_stack`` off and deploys prometheus,
alertmanager, grafana, and node-exporter. The methods match
``test_monitoring_stack_basic.yaml`` (HTTP for prometheus / alertmanager /
node-exporter; Grafana is still HTTPS).
"""

from __future__ import annotations

from tasks.cephadm_cases.monitoring.base import MonitoringTestCase


class TestMonitoringUnsecure(MonitoringTestCase):
    """Checks from ``test_monitoring_stack_basic.yaml`` against an unsecure stack."""

    def test_node_exporter_metrics(self) -> None:
        """Each host node-exporter metrics endpoint must be responsive.

        Same check as ``test_monitoring_stack_basic.yaml`` (curl each
        host ``:9100``). Without the secure stack that is
        ``http://<addr>:9100/metrics``.
        """
        self.assertFalse(
            self.secure_monitoring_enabled(),
            'suite start must leave mgr/cephadm/secure_monitoring_stack off')
        self.assert_node_exporter_metrics()

    def test_grafana_api_health(self) -> None:
        """Grafana ``/api/health`` must report ``database == "ok"``.

        Grafana is always HTTPS. Without ``get-credentials`` the scrape
        uses ``-k``, same as ``test_monitoring_stack_basic.yaml``.
        """
        self.assertFalse(
            self.secure_monitoring_enabled(),
            'suite start must leave mgr/cephadm/secure_monitoring_stack off')
        self.assert_grafana_api_health()

    def test_ceph_mon_down_alert(self) -> None:
        """Stopping one monitor must raise CephMonDown on HTTP endpoints.

        Prometheus ``/api/v1/alerts`` must show the alert firing, and
        Alertmanager ``/api/v2/alerts`` must show it active. The monitor is
        started again, and both endpoints must drop the alert before this
        returns.
        """
        self.assertFalse(
            self.secure_monitoring_enabled(),
            'suite start must leave mgr/cephadm/secure_monitoring_stack off')
        self.assert_ceph_mon_down_alert()

    def test_mgr_prometheus_exports_health_metric(self) -> None:
        """The mgr Prometheus module must export ceph_health_status.

        ``ceph mgr services`` publishes the module URL. Without
        ``secure_monitoring_stack`` that URL is http, and ``<url>metrics``
        must include a ``ceph_health_status`` sample.
        """
        self.assertFalse(
            self.secure_monitoring_enabled(),
            'suite start must leave mgr/cephadm/secure_monitoring_stack off')
        self.assert_mgr_prometheus_exports_health()
