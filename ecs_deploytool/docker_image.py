import re


class DockerImageException(Exception):
    def __init__(self, msg=None):
        self.msg = msg if msg is not None else self.__name__

    def __str__(self):
        return repr(self.msg)


class DockerImage:
    IMAGE_REGEX = re.compile('^(?P<image>[a-zA-AZ0-9\-/]+):(?P<tag>[a-zA-Z0-9\-/]+)')

    def __init__(self, image):
        self._original_image = image
        self._parse_image_name(image)

    def _parse_image_name(self, image):
        m = self.IMAGE_REGEX.match(image)
        if m:
            image = m.groupdict()
            self.image = image['image']
            self.tag = image.get('tag', 'latest')
        else:
            raise DockerImageException('image should follow foramt, image:tag')

    @property
    def image_with_tag(self):
        return f'{self.image}:{self.tag}'
