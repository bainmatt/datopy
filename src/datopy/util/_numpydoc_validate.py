"""
This module contains tools for running targeted numpydoc docstring validation.
"""

import re
import inspect
import numpydoc
from numpydoc.validate import validate


# -- Core functionality ------------------------------------------------------


def numpydoc_validate(
    obj: str,
    numpydoc_validation_checks: dict[str, bool] = {
        "all": True,
        "EX01": False,
        "SA01": False,
        "ES01": False,
    },
    numpydoc_validation_exclude: list[str] = [
        r'\.undocumented_method$',
        r'\.__repr__$',
    ],
    numpydoc_validation_override_SS05: list[str] = [
        r'^Process ',
        r'^Assess ',
        r'^Access ',
    ],
    excluded_objects: list[str] = []
) -> None:
    """
    Run docstring validation for a given callable object.

    Usage::

            numpydoc_validate("absolute.path.to.object")

    Parameters
    ----------
    obj : str
        An absolute path to the callable object to be validated.

    numpydoc_validation_checks : dict, optional
        A dictionary containing (error code, boolean) pairs indicating which validation tests to override.

    numpydoc_validation_exclude : list, optional
        A list of regex patterns to exclude specific objects from validation based on their path.

    numpydoc_validation_override_SS05 : list, optional
        A list of regex patterns to override the SS05 check based on error message content.

    excluded_objects : list[str]
        A list of additional patterns to skip during validation.

    Returns
    -------
    None
        Prints validation messages as (error code, message) pairs for detected validation errors.
    """
    # TODO: instead skip by type? NamedTuple, namedtuple, type, dataclass
    if any(pattern in obj for pattern in excluded_objects):
        print(f"Skipping {obj}")
        return None

    results = validate(obj)

    msg = f"Validating: {obj}"
    print(f"\n{msg}\n{'-'*len(msg)}")

    # for error in results["errors"]:
    #     if error[0] not in numpydoc_validation_checks.keys():
    #         print(error, "\n")

    for error in results["errors"]:
        if (error[0] in numpydoc_validation_checks and not numpydoc_validation_checks[error[0]]):
            continue

        if any(re.match(pattern, obj) for pattern in numpydoc_validation_exclude):
            continue

        if error[0] == "SS05" and any(
            re.match(pattern, error[1])
            for pattern in numpydoc_validation_override_SS05
        ):
            continue

        print(error, "\n")


def get_callable_objects(module) -> list[str]:
    """
    Return absolute paths to all callable objects defined in the given module.

    Usage::

            callable_objects = get_callable_objects(module_name)

    """
    all_members = inspect.getmembers(module)
    path = module.__name__
    callable_objects = []

    for name, member in all_members:
        # Check if member is a class
        if inspect.isclass(member) and inspect.getmodule(member) == module:
            class_name = member.__name__
            callable_objects.append(
                f"{path}.{class_name}"
            )

            # Retrieve all methods
            class_methods = inspect.getmembers(
                member, predicate=inspect.isfunction
            )
            for method_name, method in class_methods:
                if inspect.isfunction(method):
                    callable_objects.append(
                        f"{path}.{class_name}.{method.__name__}"
                    )

        # Check if member is callable
        elif callable(member) and inspect.getmodule(member) == module:
            callable_objects.append(
                f"{path}.{member.__name__}"
            )

    return callable_objects


def numpydoc_validate_module(
    module,
    excluded_objects: list[str] = []
) -> None:
    """
    Run docstring validation for all 'defined objects in a given module.

    Usage::

            numpydoc_validate_module(module_name)

    """
    callable_objects = get_callable_objects(module)
    for obj in callable_objects:
        numpydoc_validate(obj, excluded_objects=excluded_objects)


if __name__ == "__main__":
    from datopy import _examples
    excluded_objects = ["Album", "Book", "Film", "DataModel", "MediaQuery"]
    numpydoc_validate_module(_examples, excluded_objects=excluded_objects)
