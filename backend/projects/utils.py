class ImagePath:
    @staticmethod
    def project_image_path(instance, filename):
        return f'projects/{instance.project.id}/{filename}'
