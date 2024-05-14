### Setup virtual environmrnt for python
Run the following
```sh
python -m venv <venvname>
```
This will create virtual environment linked to which python distribution you call. For example if you have anaconda distribution run `.../anaconda3/bin/python -m venv <venvname>`. To check which `python` is executed run `which python`.

VS Code will auto detect virtual environments and load it. When needed activate the environment, run the script file with
```sh
.../<venvname>/bin/activate
```
Add the virtual environment folder to `.gitignore` for avoiding it to synch with remote repository.



### Setup repo as editable python package
Create a `pyproject.toml` file in the repository root directory. Provide package name,version and dependencies. Install as editable package by running the following at repsitory root directoy

```sh
pip install -e .
```
You need the following requirements
- `pip` version later than 21.3 : `python.exe -m pip install --upgrade pip`
- `Cython` package : `pip install Cython`

This will look for sibling directory `src` for source files.



### Hide unwanted files in VS Code sidebar.
Right click on sidebar explorer pane > open folder settings > Serach for "exclude" and look for "Files:exclude". Add pattern there. Note to add corresponding pattern in git ignore too, otherwise the invisible files might get synched.