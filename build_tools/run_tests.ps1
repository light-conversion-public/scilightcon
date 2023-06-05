#coverage run -m pytest --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html:doc/docs/htmlcov --ignore=examples


pip install pytest pytest-azurepipelines
pip install pytest-cov
pytest --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html:doc/docs/htmlcov --ignore=examples


Move-Item -Path ./doc/docs/htmlcov/index.html -Destination ./doc/docs/htmlcov/coverage.html -ErrorAction Ignore