import os


def remove_parents_from_titles(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".rst"):
                # old_filepath = os.path.join(root, file)
                # new_filename = file.rsplit('.', 1)[-1]  # Get everything after the last dot
                # new_filepath = os.path.join(root, new_filename)

                # TODO FIX THIS
                # os.rename(old_filepath, new_filepath)
                pass


if __name__ == "__main__":
    paths = ["datopy/", "models/",]
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for path in paths:
        full_path = os.path.abspath(os.path.join(script_dir, path))
        remove_parents_from_titles(full_path)
