def compare_versions(installed_version, required_version):
    """
    Compare two version strings to determine if one is greater, lower, or equal to the other.

    Args:
        installed_version (str): The version of the installed package (e.g., '1.2.3').
        required_version (str): The required version to compare against (e.g., '1.2.3').

    Returns:
        int: 
            - Returns 0 if the versions are equal.
            - Returns -1 if the installed version is lower than the required version.
            - Returns 1 if the installed version is greater than the required version.
    """
    def version_tuple(v):
        return tuple(map(int, (v.split("."))))
    
    installed_tuple = version_tuple(installed_version)
    required_tuple = version_tuple(required_version)
    
    if installed_tuple == required_tuple:
        return 0
    elif installed_tuple > required_tuple:
        return 1
    else:
        return -1
