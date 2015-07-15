# jjpp
Simple command line jinja2 preprocessor 

Usage:

`jjpp [config .yml or .json] [jinja2 templates...]`

By default the output is on *stdout* but `do output('path')` within a template can be used to set the output file (the last call to `output()` win.
