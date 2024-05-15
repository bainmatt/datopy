"""
Utility for automatically updating versions in specialized requirements files.
"""

def sync_versions(
    requirements_file: str = "requirements.txt",
    suffixes: list[str] = ["dev", "optional", ""]
) -> None:
    """
    Synchronize versions in sub-requirements files with requirements.txt.

    WIP.

    Notes
    -----
    This function searches the supplied requirements file and cross-checks
    it against ...

    To ensure up-to-date requirement listings it is recommended to run the
    following prior to running this function:

    `$ pip list --format=freeze > requirements_pip.txt`

    Parameters
    ----------
    requirements_file : str, default="requirements.txt"
        Path to the main requirements file built with pip.
    """

    # TODO simplify this with simple CLI recipe and add to Makefile
    # TODO automatically run for dev/optional/docs from default or args
    # Read the contents of requirements.txt
    with open(requirements_file, 'r') as f:
        requirements = f.readlines()

    # Extract package names from requirements.txt
    required_packages = {line.strip().split('=')[0] for line in requirements}

    # Read the contents of requirements_dev.txt
    with open(requirements_file, 'r') as f:
        dev_requirements = f.readlines()

    # Update lines in requirements_dev.txt that match package names in requirements.txt
    updated_requirements_dev = []
    for line in dev_requirements:
        package_name = line.strip().split('=')[0]
        if package_name in required_packages:
            # Replace the line with the corresponding line from requirements.txt
            for req_line in requirements:
                if package_name == req_line.strip().split('=')[0]:
                    updated_requirements_dev.append(req_line)
                    break
        else:
            updated_requirements_dev.append(line)

    # Write the updated requirements_dev.txt file
    with open(requirements_file, 'w') as f:
        f.writelines(updated_requirements_dev)