import boto3


class AwsEcr:
    def __init__(self):
        self._client = None
        pass

    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client('ecr')
        return self._client

    def list_repositories(self):
        repositories = self.client.describe_repositories()
        return [r['repositoryUri'] for r in repositories['repositories']]

    def fetch_images(self, repository_name):
        response = self.client.list_images(repositoryName=repository_name,
                                           filter={'tagStatus': 'TAGGED'})
        return response['imageIds']

    def delete_images(self, repository_name, image_ids):
        if not image_ids:
            return
        return self.client.batch_delete_image(repositoryName=repository_name,
                                              imageIds=image_ids)
