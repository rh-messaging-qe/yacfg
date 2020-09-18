# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Pull Request Process

1. Pull request requirements
    - briefly describe proposed change (What, How, and Why)

1. Change Requirements:
    - Existing tests must be passing
    - Code changes has to be covered by tests and tests must be passing.
    - Code must follow PEP8, and mypy and flake8 checks must pass.
    - YAML files are valid, yamllint must pass.
    - yacfg profile file is either valid YAML or jinja2 template located in profiles/ dir
        - profile must pass generation with default values
        - profile must have valid exported tuning if applicable
    - yacfg template is valid jinja2 template located in temaplates/ dir
        - for a template valid profiles must exists either as default or example, that is usable
        - template must pass generation with this profile
    - TIP: use `tox` and/or `pre-commit` before committing
    
1. Update the `README.md` and `docs/` with details of changes to the interface, usage, and examples.
1. Pull Request will be merged by a maintainer after review and sign-off.
