from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.base_spec_check import BaseK8Check


class PodDisruptionBudget(BaseK8Check):

    def __init__(self):

        name = "PodDisruptionBudget should be greater than 1"
        id = "HelloFresh-PodDisruptionBudget-1"

        supported_kind = ['PodDisruptionBudget']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def get_resource_id(self, conf, ):
        if "namespace" in conf["metadata"]:
            return "{}.{}.{}".format(conf["kind"], conf["metadata"]["name"], conf["metadata"]["namespace"])
        else:
            return "{}.{}.default".format(conf["kind"], conf["metadata"]["name"])

    def scan_spec_conf(self, conf, entity_type):
        if conf['spec']['minUnavailable'] > 1:
            return CheckResult.PASSED
        else:
            return CheckResult.FAILED


check = PodDisruptionBudget()
