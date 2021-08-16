

# ActionStats

## Description
This is a small toy library class that tracks actions and average times. 


## Usage

I used the vscode remote development from my development environment.
It is written in python 3 and dependencies are managed using pip.
Dependencies are recorded in requirements.txt. See the '.devcontainer/Dockerfile' for the pip invocation used. 

No installer exists yet. To run your own code, with the actionStats folder in your python path:


``` 
python
>>> from actionStats import actionStats
>>> actionTracker = actionStats()
>>> actionTracker.addAction('{"action":"jump", "time":100}')
True
>>> actionTracker.getStats()
'[{"action": "jump", "avg": 100}]'
```
