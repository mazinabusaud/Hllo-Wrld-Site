from django.core.exceptions import ValidationError

allowed=['.zip','.gz']
def validate_file_extension(value):
    if ((not value.name.endswith('.tar')) and (not value.name.endswith('.zip'))):
        raise ValidationError(u'Error: Please only upload tar or zip files!')

def file_size(value):
    maxsize = 5242880
    if value.size > maxsize:
        raise ValidationError('Error: File exceeds max size of 5 MB')