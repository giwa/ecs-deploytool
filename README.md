# ECS Deploytool

This script helps deloying docker image to ecs. ECS deploytool gives capabilities that deploy docker application to ECS. This repository does not support building docker iamges.

## Usage

### Install


### Prerequisite `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` are exposed as enviromental variables.

```
Usage: ecs-deploytool [OPTIONS] CONFIG COMMAND [ARGS]...

Options:
  --env TEXT  Deploy environment
  --help      Show this message and exit.

Commands:
  deploy_service         Deploy ECS service deploytool...
  fetch_image            fetch a docker image from ECR
  keep_images            keep images in repository (default 5)
  keep_task_definitions  keep task definitions (default 5)
  list_repositories      list repository in ECR
  push_image             push a docker image to ECR
```

### Example
Fetch an image
```
DEPLOY_ENV=staging deploytool ./example/deploy.ini fetch_image ecr/image_name
```


## Development

`-e` is development flag in pip
```
pip install -e .
```
