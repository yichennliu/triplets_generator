# Read Me !

### Steps to build the project

```python
# Create a virtual environment, choose the folder
python3 -m venv <Thesis>

# activate the environmet
source Thesis/bin/activate 

# optional, loading Jupyter notebook
    # install ipykernel
    pip install --user ipykernel
   
    # add virtual environment to Jupyter
    python -m ipykernel install --user --name=<Thesis>
   
# installing requirements
pip install -r requirements.txt

# removing virtual environment after 
deactivate

# removing files
rm -r <Thesis>

	# removing jupyter kernel, list and delete
	jupyter kernelspec list
	jupyter kernelspec uninstall <Thesis>

```

