from .models import FileManagement

def get_file_management():
    try:
        return FileManagement.objects.first()
    except FileManagement.DoesNotExist:
        return None