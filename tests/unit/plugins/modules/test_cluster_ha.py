from __future__ import absolute_import, division, print_function
__metaclass__ = type￼
import sys
import pytest

from ansible_collections.bardielle.vmware.plugins.modules import cluster_ha

from .common.utils import (
    AnsibleExitJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestAffinity(ModuleTestCase):

    def __prepare(self, mocker):
        init_mock = mocker.patch.object(cluster_ha.PyVmomi, "__init__")
        init_mock.return_value = None

        find_datacenter_by_name = mocker.patch.object(cluster_ha.VmwareDrs, "find_datacenter_by_name")
        find_datacenter_by_name.return_value = {}
        find_cluster_by_name = mocker.patch.object(cluster_ha.VmwareDrs, "find_cluster_by_name")
        find_cluster_by_name.return_value = {}

    def test_configure_ha(self, mocker):
        self.__prepare(mocker)
        configure_ha_mock = mocker.patch.object(cluster_ha.VmwareDrs, "configure_ha")
        configure_ha_mock.return_value = True, None

        set_module_args(
            enable=True,
            ha_host_monitoring="enable",
            ha_vm_monitoring="vmAndAppMonitoring",
            host_isolation_response="powerOff",
        )

        with pytest.raises(AnsibleExitJson) as c:
            cluster_ha.main()

        assert c.value.args[0]["changed"] == True
