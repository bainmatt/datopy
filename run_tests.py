# Run doctests for all specified modules as a unittest suite
# To execute main (__main__) & module-level (non-testing/callable) helper code:
# (option 1) run (|>) script in dedicated terminal
# (option 2) execute script in terminal (`python <script_name>.py`) with wd=repo
# To execute selection and share declarations with global namespace: shift+enter

if __name__ == "__main__":
    import doctest
    import unittest

    for f in ('display_dataset', 'nb_utils', 'media_scrape'):
        temp_module = __import__(f)
        test_suite = doctest.DocTestSuite(temp_module)
        unittest.TextTestRunner().run(test_suite)