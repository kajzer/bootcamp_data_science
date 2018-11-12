# Perform the necessary imports
from bokeh.io import curdoc
from bokeh.layouts import widgetbox
from bokeh.models import Slider

slider = Slider(title='my slider', start=0, end=10, step=0.1, value=2)
layout = widgetbox(slider)

curdoc().add_root(layout)