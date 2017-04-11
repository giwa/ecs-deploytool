import boto3


class AwsEcsException(Exception):
    def __init__(self, msg=None):
        self.msg = msg if msg is not None else self.__name__

    def __str__(self):
        return repr(self.msg)


class AwsEcs:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client('ecs')
        return self._client

    def update_task_definition(self, family, container_definitions, volumes):
        response = self.client.register_task_definition(
            family=family,
            containerDefinitions=container_definitions,
            volumes=volumes)
        return response['taskDefinition']['taskDefinitionArn']

    def update_service(self, cluster, service, desired_count, task_definition_arn, max, min):
        response = self.client.update_service(
            cluster=cluster,
            service=service,
            desiredCount=desired_count,
            taskDefinition=task_definition_arn,
            deploymentConfiguration={
                'maximumPercent': max,
                'minimumHealthyPercent': min
            }
        )
        return response

    def fetch_task_definitions(self, family, next_token=''):
        response = self.client.list_task_definitions(familyPrefix=family,
                                                     sort='DESC',
                                                     nextToken=next_token)
        return response['taskDefinitionArns']

    def deregister_task_definition(self, task_definition_arn):
        return self.client.deregister_task_definition(taskDefinition=task_definition_arn)
