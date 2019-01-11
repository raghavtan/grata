# import os
#
# from kubernetes import client
# from kubernetes import config as kube_config
#
# from src.listeners import CreateSingleton
# from utilities import logger
#
#
# class KubernetesClient(metaclass=CreateSingleton):
#     """
#
#     """
#
#     def __init__(self, config):
#         """
#
#         :param config:
#         """
#         try:
#             config_file_path = os.path.join(config.home_path, config.kube_config)
#             kube_config.load_kube_config(config_file_path, context="aws_kube-prod")
#             self.kube_client_v1 = client.V1Node()
#         except Exception as e:
#             logger.exception(e)
#             raise
#
#     def manage_node(self,node_name,level):
#         color = dict(OK=True, WARNING=False, CRITICAL=False)
#         state=color[level]
#         self.kube_client_v1.spec()
#
#
#     def close(self):
#         """
#
#         :return:
#         """
#         try:
#             if self.config.enable_queue:
#                 self.publisher.flush(timeout=5)
#                 self.publisher.close()
#         except Exception as e:
#             logger.error(e)
#         logger.debug("Closed Kafka connection pool")
