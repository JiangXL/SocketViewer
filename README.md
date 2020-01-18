# SocketViewer
GUI Viewer to Transfer image, Send commands, Sync variable state in Socket

## Requirements
pyqtgraph 0.11.0 is required for GUIViewer.py and VariableViewer.py

pip install git+https://github.com/pyqtgraph/pyqtgraph@develop

## RoadMap

## Design Layout
GUIViewer.py
``` bash
Layout

```

## Files List

|--------------------|------------------------------------------------
| GUIViewer.py       | Camera Frame Viewer connected by socket
| SocketTransfer.py  | Socket library transfers camera frame for GUIViewer.py
| ParameterViewer.py | Microscopy parameter viewer and controller
| SocketSync.py      | Socket library synchronizes parameters for ParameterViewer.py
| test.tif           | unit16 test image 
