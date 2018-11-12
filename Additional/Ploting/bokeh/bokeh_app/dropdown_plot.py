from bokeh.io import curdoc
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import widgetbox, row
from bokeh.models import Select
import numpy as np
import pandas as pd

df = pd.read_csv('literacy_birth_rate.csv')
df.dropna(inplace=True)
df.population = pd.to_numeric(df.population)
df['fertility'] = pd.to_numeric(df['fertility'])
df['female literacy'] = pd.to_numeric(df['female literacy'])
fertility = df['fertility'].values.tolist()
female_literacy = df['female literacy'].values.tolist()
population = df['population'].values.tolist()

source = ColumnDataSource(data={
    'x' : fertility,
    'y' : female_literacy
})

plot = figure()
plot.circle('x', 'y', source=source)

def update_plot(attr, old, new):
    if new == 'female_literacy':
        source.data = {
            'x':fertility,
            'y':female_literacy
        }
    else:
        source.data = {
            'x':fertility,
            'y':population
        }

select = Select(title="distribution",
                options=['female_literacy', 'population'],
                value='female_literacy'
                )
select.on_change('value', update_plot)

layout = row(select, plot)

curdoc().add_root(layout)