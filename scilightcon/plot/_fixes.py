from ..utils._runtime import compare_versions

def resize_mode():
    import PIL

    if (compare_versions(PIL.__version__, "9.5.0") >= 0):
        return PIL.Image.LANCZOS
    else:
        return PIL.Image.ANTIALIAS