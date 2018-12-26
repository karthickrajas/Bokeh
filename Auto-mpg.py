# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox, gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, MultiSelect
from bokeh.plotting import figure
from bokeh.sampledata.autompg import autompg

import pandas as pd
df = pd.read_csv('data\\auto-mpg.csv')


def make_plot(df):

	#Set up data
	source = ColumnDataSource(df)

	#Set up plot
	options = dict(plot_width=250, plot_height=250,
	               tools="pan,wheel_zoom,box_zoom,box_select,lasso_select,reset")
	p1 = figure(title="MPG by Year", **options)
	p1.circle("yr", "mpg", color="blue", source=source)
	p2 = figure(title="HP vs. Displacement", **options)
	p2.circle("hp", "displ", color="green", source=source)
	p3 = figure(title="MPG vs. Displacement", **options)
	p3.circle("mpg", "displ", size="cyl", line_color="red", fill_color=None, source=source)
	p = gridplot([[p1, p2, p3]], toolbar_location="right")

	return p

p = make_plot(autompg)

# Set up widgets
mpg = Slider(title="mpg", value=9.0, start=9.0, end=50.0, step=1)
cyl = Slider(title="cyl", value=3.0, start=3.0, end=8.0, step=1)
hp = Slider(title="hp", value=40, start=40, end=240, step=20)
yr = Slider(title="yr", value=70, start=70, end=82, step=1)
origin = MultiSelect(title="origin", value=["1", "2", "3"],
                     options=[("1", "Japanese"), ("2", "German"), ("3", "American")])

#Set up callbacks
def update_data(attrname, old, new):

    # Get the current slider values
    m = mpg.value
    c = cyl.value
    h = hp.value
    y = yr.value
    o = origin.value
    o_int = [int(i) for i in o]

    # Generate new data
    data = autompg[(autompg.mpg >= m)
    			   & (autompg.cyl >= c)
    			   & (autompg.hp >= h)
    			   & (autompg.yr >= y)
    			   & (autompg.origin.isin(o_int))].reset_index(drop=True)
    
    layout.children[1] = make_plot(data)
    

for w in [mpg, cyl, hp, yr, origin]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs_1 = widgetbox(mpg, cyl, hp)
inputs_2 = widgetbox(yr, origin)
inputs_row = row(inputs_1, inputs_2, width=800)
layout = column(inputs_row, p, width=800)

curdoc().add_root(layout)
curdoc().title = "AutoMPG"