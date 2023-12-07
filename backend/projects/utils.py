class ImagePath:
    @staticmethod
    def project_image_path(instance, filename):
        return f'projects/{instance.project.id}/{filename}'


def get_or_create_deleted_user(model):
    return model.objects.get_or_create(
        email='deleted@deleted.ru',
        is_active=False,
        role=model.DELETED,
    )[0]
