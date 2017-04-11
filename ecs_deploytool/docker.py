import os
import sys
from subprocess import Popen, PIPE

import boto3

from .command import Command


class Docker:
    def __init__(self, ecr_url, region):
        self.ecr_url = ecr_url
        self.region = region

    def fetch_image(self, image):
        """
        Fetch a base image from ECR and tag it as base_image:latest
        """
        command_temp = """
        eval $(aws ecr get-login --region {region})
        docker pull {ecr_url}/{image};
        docker tag  {ecr_url}/{image} {image};
        """

        command = command_temp.format(
                region=self.region,
                ecr_url=self.ecr_url,
                image=image.image_with_tag
                )
        Command.run(command)

    def push_image(self, src_image, dst_image):
        command_temp = """
        docker tag {src_image} {ecr_url}/{dst_image};
        eval $(aws ecr get-login --region {region});
        docker push {ecr_url}/{dst_image};
        docker rmi {ecr_url}/{dst_image};
        """
        command = command_temp.format(
                        ecr_url=self.ecr_url,
                        src_image=src_image.image_with_tag,
                        dst_image=dst_image.image_with_tag,
                        region=self.region)
        Command.run(command)
