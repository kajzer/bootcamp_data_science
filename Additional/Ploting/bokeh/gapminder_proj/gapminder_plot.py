import pandas as pd
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Slider, Select
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row
from bokeh.palettes import Spectral6
from bokeh.models import HoverTool

data = pd.read_csv('gapminder_tidy.csv', index_col='Year')
regions_list = data.region.unique().tolist()

source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country'      : data.loc[1970].Country,
    'pop'      : (data.loc[1970].population / 20000000) + 2,
    'region'      : data.loc[1970].region,
})

xmin, xmax = min(data.fertility), max(data.fertility)
ymin, ymax = min(data.life), max(data.life)

color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

def update_plot(attr, old, new):
    yr = slider.value
    x = x_select.value
    y = y_select.value
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    source.data = new_data

    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    plot.title.text = 'Gapminder data for %d' % yr
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y

plot = figure(title='Gapminder Data for 1970', 
                plot_height=400, 
                plot_width=700, 
                x_range=(xmin, xmax), 
                y_range=(ymin, ymax)
                )

plot.circle(x='x',
            y='y', 
            fill_alpha=0.8, 
            source=source,
            color=dict(field='region', transform=color_mapper),
            legend='region',
            size='pop'
            )

hover = HoverTool(tooltips=[('Country', '@country')])
plot.add_tools(hover)
plot.xaxis.axis_label ='Fertility (children per woman)'
plot.yaxis.axis_label = 'Life Expectancy (years)'
plot.legend.location = 'top_right'

slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')
slider.on_change('value', update_plot)

x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data'
)
x_select.on_change('value', update_plot)
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data'
)
y_select.on_change('value', update_plot)

layout = row(widgetbox(slider, x_select, y_select), plot)

curdoc().add_root(layout)
curdoc().title = 'Gapminder'