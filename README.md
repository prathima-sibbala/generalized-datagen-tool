nodes represent entities and edges represent relationship across entities
output of .py file will be as below:
associations are {'customers0': ['systems0-0', 'systems1-0', 'vcenter0-0', 'vcenter1-0'], 'systems0-0': ['volumes0-0-0', 'volumes1-0-0'], 'systems1-0': ['volumes0-1-0', 'volumes1-1-0'], 'volumes0-0-0': ['snapshots0-0-0-0', 'snapshots1-0-0-0'], 'volumes1-0-0': ['snapshots0-1-0-0', 'snapshots1-1-0-0'], 'volumes0-1-0': ['snapshots0-0-1-0', 'snapshots1-0-1-0'], 'volumes1-1-0': ['snapshots0-1-1-0', 'snapshots1-1-1-0'], 'snapshots0-0-0-0': ['clones0-0-0-0-0', 'clones1-0-0-0-0'], 'snapshots1-0-0-0': ['clones0-1-0-0-0', 'clones1-1-0-0-0'], 'snapshots0-1-0-0': ['clones0-0-1-0-0', 'clones1-0-1-0-0'], 'snapshots1-1-0-0': ['clones0-1-1-0-0', 'clones1-1-1-0-0'], 'snapshots0-0-1-0': ['clones0-0-0-1-0', 'clones1-0-0-1-0'], 'snapshots1-0-1-0': ['clones0-1-0-1-0', 'clones1-1-0-1-0'], 'snapshots0-1-1-0': ['clones0-0-1-1-0', 'clones1-0-1-1-0'], 'snapshots1-1-1-0': ['clones0-1-1-1-0', 'clones1-1-1-1-0']}
customers0:
- systems0-0
- systems1-0
- vcenter0-0
- vcenter1-0
snapshots0-0-0-0:
- clones0-0-0-0-0
- clones1-0-0-0-0
snapshots0-0-1-0:
- clones0-0-0-1-0
- clones1-0-0-1-0
snapshots0-1-0-0:
- clones0-0-1-0-0
- clones1-0-1-0-0
snapshots0-1-1-0:
- clones0-0-1-1-0
- clones1-0-1-1-0
snapshots1-0-0-0:
- clones0-1-0-0-0
- clones1-1-0-0-0
snapshots1-0-1-0:
- clones0-1-0-1-0
- clones1-1-0-1-0
snapshots1-1-0-0:
- clones0-1-1-0-0
- clones1-1-1-0-0
snapshots1-1-1-0:
- clones0-1-1-1-0
- clones1-1-1-1-0
systems0-0:
- volumes0-0-0
- volumes1-0-0
systems1-0:
- volumes0-1-0
- volumes1-1-0
volumes0-0-0:
- snapshots0-0-0-0
- snapshots1-0-0-0
volumes0-1-0:
- snapshots0-0-1-0
- snapshots1-0-1-0
volumes1-0-0:
- snapshots0-1-0-0
- snapshots1-1-0-0
volumes1-1-0:
- snapshots0-1-1-0
- snapshots1-1-1-0

- graph representation will be as below:
- <img width="551" alt="image" src="https://github.com/prathima-sibbala/generalized-datagen-tool/assets/139799062/71c86a2e-56bc-4956-b06a-4e66495de519">
