from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

# 이미지 라벨링 부분
class ImageMetadataConfig(AppConfig):
    name = 'image_metadata'