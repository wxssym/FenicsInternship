# FenGraphs module
FenGraphs is a module that regroup functions that plot different plot types specific to the different FENICS boards using `matplotlib.pyplot` library and `Bokeh` interactive plotting library.

## Functions

### Fenics features Histograms
#### FenGraphs.FenHist() ####
_func_  **FenGraphs.FenHist(<i>FenDataFrame,testTable,columns,selectedBoards,show=True,\*\*kwargs</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L27-L112)

Function that plot an **histogram** of the provided Fenics boards IDs, separatly or grouped.

> ###### Parameters######
>>***FenDataFrame*** (pandas.DataFrame) :
>>>FENICS dataframe with board informations.
>
>>***testTable*** (pandas.DataFrame) :
>>>FENICS Fast/Slow DataFrame with boards result values.
>
>>***columns*** (tuple) :
>>>Tuple of columns that are being plotted ***(MainCol,SubCol)*** for Fast channel. ***(Gain,MainCol,SubCol)*** for Slow channel.
>
>>***selectedBoards*** (list) :
>>>List of boards IDs to plot as histogram.
>
>>***show*** (bool, optional) ,***default***=True :
>>>Show histograms in the cell output. By ***default*** it is **true**, but for any reasons someone needs to get plots saved without being showed, this can be turned off, a ***path*** to save the histogram needs to be provided. 


>###### Other parameters######

>>***path*** (string, optional), ***default***=False :
>>>A save directory for the histogram if show is set to **False**.

>>***separate*** (bool, optional), ***default***=False :
>>>Plot the given FENICS boards separatly **True**, or grouped in one histogram **False**.

>>***sigma*** (integer, optional), ***default***=False :
>>>within how many sigma deviation values are accepted. Data values within the \(mean \pm n\sigma \) are kept on the wanted column/DataFrame.

>>***saveFormat*** (string, optional), ***default***='jpeg' :
>>>change the output format of the saved histogram : **JPEG, PDF, SVG, PNG**


&nbsp;
&nbsp;
&nbsp;
&nbsp;


### Fenics features Correlations
#### FenGraphs.FenCorr() ####
_func_ **FenGraphs.FenCorr(<i>FenDataFrame,testTable,col1,col2,selectedBoards,show=True,\*\*kwargs</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L115-L233)

This function makes a correlation plot of two different FENICS features as a matplotlib.pyplot.plot(feature1,feature2) optimized for FENICS boards.
> ###### Parameters ######
>>***FenDataFrame*** (pandas.DataFrame) :
>>>FENICS dataframe with board informations.
>
>>***testTable*** (pandas.DataFrame) :
>>>FENICS Fast/Slow DataFrame with boards result values.
>
>>***col1,col2*** (tuples) :
>>>Tuples of plotted correlated features. ***(MainCol,SubCol)*** for Fast channel. ***(Gain,MainCol,SubCol)*** for Slow channel.
>
>>***selectedBoards*** (list) :
>>>List of boards IDs to plot as histogram.
>
>>***show*** (bool, optional) ,***default***=True :
>>>Show plot in the cell output. By ***default*** it is **true**, but for any reasons someone needs to get plots saved without being showed, this can be turned off, a ***path*** to save the plot needs to be provided. 


>###### Other parameters######

>>***path*** (string, optional), ***default***=False :
>>>A save directory for the correlation plot if show is set to **False**.

>>***separate*** (bool, optional), ***default***=False :
>>>Plot the given FENICS boards separatly **True**, or grouped in one correlation plot **False**.

>>***sigma*** (integer, optional), ***default***=False :
>>>within how many sigma deviation values are accepted. Data values within the \(mean \pm n\sigma \) are kept on the wanted column/DataFrame.

>>**burns** (bool,optional), ***default***=False :
>>>Use burntimes as a third axis with a color bar.

>>**burns_filter** (integer,optional), **default**=None :
>>>A burn-time value in burn-hours at when you want a filter.

>>**LR** (bool,optional), ***default***=False :
>>>Linear regression of the plotted data, One linear regression for one board plotted.

>>***saveFormat*** (string, optional), ***default***='jpeg' :
>>>change the output format of the saved correlation plot : **JPEG, PDF, SVG, PNG**


&nbsp;
&nbsp;
&nbsp;
&nbsp;



### Fenics features burn-evolution
#### FenGraphs.FenBurnEvol() ####
_func_ **FenGraphs.FenBurnEvol(<i>FenDataFrame,testTable,columns,selectedBoards,show=True,\*\*kwargs</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L236-L374)

This function makes an evolution plot of a selected feature with the corresponding burn-time as a matplotlib.pyplot.plot(burn-time,feature) optimized for FENICS boards.

>###### Parameters ######
>>***FenDataFrame*** (pandas.DataFrame) :
>>>FENICS dataframe with board informations.
>
>>***testTable*** (pandas.DataFrame) :
>>>FENICS Fast/Slow DataFrame with boards result values.
>
>>***columns*** (tuples) :
>>>Feature to plot its evolution with burn-time. ***(MainCol,SubCol)*** for Fast channel. ***(Gain,MainCol,SubCol)*** for Slow channel.
>
>>***selectedBoards*** (list) :
>>>List of boards IDs to plot as histogram.
>
>>***show*** (bool, optional) ,***default***=True :
>>>Show plot in the cell output. By ***default*** it is **true**, but for any reasons someone needs to get plots saved without being showed, this can be turned off, a ***path*** to save the plot needs to be provided. 


>###### Other parameters ######

>>***path*** (string, optional), ***default***=False :
>>>A save directory for the plot if show is set to **False**.

>>***separate*** (bool, optional), ***default***=False :
>>>Plot the given FENICS boards separatly **True**, or grouped in one plot **False**.

>>***sigma*** (bool, optional), ***default***=False :
>>>Keep one point per burn-hour, by calculating a \(Mean\) of the repeated values in one burn-time.

>>***unique*** (integer, optional), ***default***=False :
>>>within how many sigma deviation values are accepted. Data values within the \(mean \pm n\sigma \) are kept on the wanted column/DataFrame.

>>**burns** (bool,optional), ***default***=False :
>>>Use burntimes as a third axis with a color bar.

>>**burns_filter** (integer,optional), **default**=None :
>>>A burn-time value in burn-hours at when you want a filter.

>>**LR** (bool,optional), ***default***=False :
>>>Linear regression of the plotted data, One linear regression for one board plotted.

>>***saveFormat*** (string, optional), ***default***='jpeg' :
>>>change the output format of the saved plot : **JPEG, PDF, SVG, PNG**

&nbsp;
&nbsp;
&nbsp;
&nbsp;


### Fenics features jitter
#### FenGraphs.FenSpread() ####
_func_ **FenGraphs.FenSpread(<i>FenDataFrame,testTable,columns,selectedBoards,show=True,\*\*kwargs</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L377-L441)


A jitter plot for FENICS features for each selected board, can be customized with a burning indicator with a color bar.

>###### Parameters ######
>>***FenDataFrame*** (pandas.DataFrame) :
>>>FENICS dataframe with board informations.
>
>>***testTable*** (pandas.DataFrame) :
>>>FENICS Fast/Slow DataFrame with boards result values.
>
>>***columns*** (tuples) :
>>>Feature to plot its evolution with burn-time. ***(MainCol,SubCol)*** for Fast channel. ***(Gain,MainCol,SubCol)*** for Slow channel.
>
>>***selectedBoards*** (list) :
>>>List of boards IDs to plot as histogram.
>
>>***show*** (bool, optional) ,***default***=True :
>>>Show plot in the cell output. By ***default*** it is **true**, but for any reasons someone needs to get plots saved without being showed, this can be turned off, a ***path*** to save the plot needs to be provided. 


>###### Other parameters ######

>>***path*** (string, optional), ***default***=False :
>>>A save directory for the plot if show is set to **False**.

>>***sigma*** (bool, optional), ***default***=False :
>>>Keep one point per burn-hour, by calculating a \(Mean\) of the repeated values in one burn-time.

>>**burns** (bool,optional), ***default***=False :
>>>Use burntimes as a third axis with a color bar.

>>***saveFormat*** (string, optional), ***default***='jpeg' :
>>>change the output format of the saved correlation plot : **JPEG, PDF, SVG, PNG**


## Classes

### Fenics interactive plots framework ###
#### FenBokehGrapher####
_Class_ **FenGraphs.FenBokehGrapher(x,y,\*args,\*\*kwargs)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L466-L1289)

A class for creating interactive Bokeh graphs.

> <h6> Attributes </h6>

>>***x*** (list) :
>>>The x-coordinate data for the graph.

>>***y*** (list) :
>>>The y-coordinate data for the graph. Size needs to correspond to the size of x.

>>***\*args*** (list, optional) :
>>>Additional data lists to customize the data tool tips

>>***colors*** (list, optional), ***default***= list of zeros :
>>>A third dimension using colors and (optional) sliders for filtering.

>>***labels*** (list, optional), ***default***= list of "1" :
>>>A label field to identify each x and y in the plot and use (optional) filtering checkboxes.

>>***source*** (bokeh.source object, optional), ***default***= None :
>>>A bokeh.DataSource object that is generated using bokeh.ColumnDataSource.

>>***plot*** (bokeh.glyph object, optional), ***default***= None :
>>>A bokeh.glyph object that can be generated using FenBokehGrapher.create_plot().

>>***tooltips*** (bokeh.tooltips object, optional), ***default***= None : 
>>>A bokeh.tooltips object that handles the tooltips and naming of the data showed.

> <h6> Methods </h6>

>>[\_\_init\_\_(___x,y,\*args,\*\*kwargs___)](../FenGraphs/#fenbokehgrapher) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L467-L481)
>>>FenBokehGrapher initialization of the object structure and attributes using the declared attributes. 

>>[create_plot(___title,axis\_xlabel,axis\_ylabel___)](../FenGraphs/#fenbokehgraphercreate_plot) [`source`](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L484-L532)
>>>Create a bokeh.glyph object.

>>[create_hist(___title,axis\_xlabel,axis\_ylabel___)](../FenGraphs/#fenbokehgraphercreate_hist) [`source`](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L534-L733)
>>>Create a bokeh.histograms for lasso selection interaction.

>>[create_slider(___\*\*kwargs___)](../FenGraphs/#fenbokehgraphercreate_slider) [`source`](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L735-L846)
>>>Create a bokeh slider object and the HTML DOM.

>>[create_checkboxes(___\*\*kwargs___)](../FenGraphs/#fenbokehgraphercreate_checkboxes) [`source`](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L848-L946)
>>>Create a bokeh checkboxes object with HTML DOM.

>>[create_radiocheckbox(___\*\*kwargs___)](../FenGraphs/#fenbokehgraphercreate_radiocheckbox) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L948-L988)
>>>Create a bokeh radio group object with HTML DOM.

>>[selection_callback()](../FenGraphs/#fenbokehgrapherselection_callback) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L990-L1076)
>>>A javascript callback event when changes are done to filtering tools.

>>[create_combo_filter(___\*\*kwargs___)](../FenGraphs/#fenbokehgraphercreate_combo_filter) [`source`](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1078-L1211)
>>>Create a combo filter with sliders and checkboxes.

>>[filters_tool(___filters = [('Combo')]___)](../FenGraphs/#fenbokehgrapherfilters_tool) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1213-L1240)
>>>Function that merge declared filters in one filter bokeh layout.

>>[plotter(___plotType='scatter',filters=[('Combo')], title='',axis\_xlabel='',axis\_ylabel='',linear\_fit = False,showGraph=True___)](../FenGraphs/#fenbokehgrapherfilters_tool) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1242-L1276)
>>>Function that gather all Bokeh graphical objects and filters layout. and display them.

>>[save_as_html(___x,y,\*args,\*\*kwargs___)](../FenGraphs/#fenbokehgraphersave_as_html) [``source``]([source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1278-L1289)
)

>>>Function that saves the plotter layout in an HTML file.


#### FenBokehGrapher.create_plot ####

_ClassMethod_  **FenBokehGrapher.create_plot(___x,y,\*args,\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L484-L532)

Create a bokeh.glyph object.
This function is called when plottype is set to "Scatter"

> ###### Parameters ######
>>***title*** (string, optional) , *default* = ''  :
>>>Custom title for the plot
>
>>***axis_xlabel*** (string, optional) , *default* = ''  :
>>>Custom label for the x axis.
>
>>***axis_ylabel*** (string, optional) , *default* = ''  :
>>>Custom label for the Y axis.
>

#### FenBokehGrapher.create_hist ####

_ClassMethod_  **FenBokehGrapher.create_hist(___title='',axis\_xlabel='',axis\_ylabel=''___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L534-L733)

Create a double projection histograph object and a JavaScript event listner for Bokeh selection tools and a scatter plot.
This function is called when plottype is set to "Histogram"

> ###### Parameters ######
>>***title*** (string, optional) , *default* = ''  :
>>>Custom title for the plot
>
>>***axis_xlabel*** (string, optional) , *default* = ''  :
>>>Custom label for the x axis.
>
>>***axis_ylabel*** (string, optional) , *default* = ''  :
>>>Custom label for the Y axis.
>



#### FenBokehGrapher.create_slider ####

_ClassMethod_  **FenBokehGrapher.create_slider(___\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L735-L846)

Create a Slider filtering HTML dom object using Bokeh, and creates a custom JavaScript listner that filter the colors property of FenBokehGraph object. different parameters can be customized using the kwargs parameters.

Called when filters=[('Slider')]

> ###### Other parameters ######
>>***min*** (integer, optional) , *default* = min(self.colors)  :
>>>default start value at the creation of the slider.
>
>>***max*** (integer, optional) , *default* = max(self.colors)  :
>>>default end value at the creation of the slider.
>
>>***valmin*** (integer, optional) , *default* = min(self.colors)  :
>>>minimum value of the slider.
>
>>***valmax*** (integer, optional) , *default* = max(self.colors)  :
>>>maximum value of the slider.
>
>>***step*** (float, optional) , *default* = 20.0  :
>>>At what stepping values, the cursors of the sliders will move.
>
>>***title*** (string, optional) , *default* = 'Filter'  :
>>>Title of the slider.
>
>>***orientation*** (string, optional) , *default* = 'vertical'  :
>>>Orientation of the slider (vertical / horizontal).
>
>>***height*** (integer, optional) , *default* = 300  :
>>>The apparent size in the HTML file in pixels.
>
>>***direction*** (string, optional) , *default* = 'rtl'  :
>>>Direction of the min-max/max-min values of the slider.

>>>'rtl' : right to left

>>>'ltr' : left to right


#### FenBokehGrapher.create_checkboxes ####

_ClassMethod_  **FenBokehGrapher.create_checkboxes(___\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L848-L946)

Create an HTML dom object of checkbox groups using Bokeh, and creates a custom JavaScript listner that filter points by their attibuted label in FenBokehGraph object. different parameters can be customized using the kwargs parameters.

Called when filters=[('Checkbox')]

> ###### Other parameters ######
>>***labels_filter*** (list, optional) , *default* = pd.unique(FenGrapher.labels)  :
>>>List of labels that is wanted to be filtred (recommended when the number of labels is higher than 8)

>>>It is also recommended to gather similar labels in one big label in a radiocheckbox. Example : Life-Time tests FENICS boards together, and FENICS NIEL/TID together.

#### FenBokehGrapher.create_radiocheckbox ####

_ClassMethod_  **FenBokehGrapher.create_radiocheckbox(___\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L948-L988)


Create an HTML dom object of radiocheckboxes using Bokeh, and creates a custom JavaScript listner that filter points by their attibuted label in FenBokehGraph object as groups comapred to the FenBokehGrapher.create_checkboxes(). a default "Select all" "Select none" are available, different parameters can be customized using the kwargs parameters.

> ###### Other parameters ######
>>***radio_categories*** (list, optional) :
>>>List of dictionaries each category to filter in one dictionary. The dictionary structure should be as : 'name' key for the radiocheck box name, and a 'index' key with a list of labels to filter at same time.


#### FenBokehGrapher.selection_callback ####

_ClassMethod_  **FenBokehGrapher.selection_callback()**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L990-L1076)

A callback that recalculate the slope according to the selected points with the selection tools of bokeh. It is called when Linear_regression is True.

> ###### Returns ######
>>a JavaScript event listner.
#### FenBokehGrapher.create_combo_filter ####

_ClassMethod_  **FenBokehGrapher.create_combo_filter(___\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1078-L1211)

Create a slider and a checkbox filtering HTML dom with a common filtering JavaScript event listner to handle both filtering simultaneously.

Called when filters=[('Combo')]

> ###### Other parameters ######
>>***min*** (integer, optional) , *default* = min(self.colors)  :
>>>default start value at the creation of the slider.
>
>>***max*** (integer, optional) , *default* = max(self.colors)  :
>>>default end value at the creation of the slider.
>
>>***valmin*** (integer, optional) , *default* = min(self.colors)  :
>>>minimum value of the slider.
>
>>***valmax*** (integer, optional) , *default* = max(self.colors)  :
>>>maximum value of the slider.
>
>>***step*** (float, optional) , *default* = 20.0  :
>>>At what stepping values, the cursors of the sliders will move.
>
>>***title*** (string, optional) , *default* = 'Filter'  :
>>>Title of the slider.
>
>>***orientation*** (string, optional) , *default* = 'vertical'  :
>>>Orientation of the slider (vertical / horizontal).
>
>>***height*** (integer, optional) , *default* = 300  :
>>>The apparent size in the HTML file in pixels.
>
>>***direction*** (string, optional) , *default* = 'rtl'  :
>>>Direction of the min-max/max-min values of the slider.

>>> 'rtl' : right to left

>>> 'ltr' : left to right

>>***labels_filter*** (list, optional) , *default* = pd.unique(FenGrapher.labels)  :
>>>List of labels that is wanted to be filtred

>>***radio_categories*** (list, optional) :
>>>List of dictionaries each category to filter in one dictionary. The dictionary structure should be as : 'name' key for the radiocheck box name, and a 'index' key with a list of labels to filter at same time.



#### FenBokehGrapher.filters_tool ####

_ClassMethod_  **FenBokehGrapher.filters_tool(___filters = [('Combo')]___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1213-L1240)

Function that is responsible of the layout hiarchy of the different filter declared.

> ###### Parameters ######

>>***filters*** (list, optional) , *default* = [('Combo')] :
>>>List of tupples  of filters to be added, a second tupple level can be added as a dictionary of kwargs to customize the filter.

> ###### Example ######
        ##Custom combo filter
        custom_filter = [('Combo',
        ##Custom checkbox groups
        dict(labels_filter=FEN1_ids,
        ##Custon radio categories kwarg argument
        radio_categories=[dict(name = 'FEN1 LTT',indexes=FEN1_ids),
                          dict(name = 'FEN1 FAILED',indexes=FENICS_fail),]))]

#### FenBokehGrapher.plotter ####

_ClassMethod_  **FenBokehGrapher.plotter(___plotType='scatter',filters=[('Combo')],title='',axis\_xlabel='',axis\_ylabel='',linear\_fit = False, showGraph=True___)**
Is the function that plots and show the plot of FenBokehGrapher object.
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1242-L1276)

>###### Parameters ######

>>***plotType*** (string (case sensitive), optional) , *default* = 'scatter' :
>>>Plot type, with or without projection histograms.

>>***filters*** (list of tuples, optional) , *default* = [('Combo')] :
>>>List of custom filters and their parametrization.

>>***title*** (string, optional) , *default* = ''  :
>>>Custom title for the plot
>
>>***axis_xlabel*** (string, optional) , *default* = ''  :
>>>Custom label for the x axis.
>
>>***axis_ylabel*** (string, optional) , *default* = ''  :
>>>Custom label for the Y axis.
>
>>***linear_fir*** (bool, optional) , *default* = False  :
>>>Add a linear fit to the resulting plot with a selection event listner using Bokeh selection tools.
>
>>***showGraph*** (bool, optional) , *default* = True  :
>>>Option to select whatever you want a resulting graph in the output cell or not.

#### FenBokehGrapher.save_as_html ####

_ClassMethod_  **FenBokehGrapher.save_as_html(___x,y,\*args,\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L1278-L1289)

A function that save the plot object and the filtring tools into an HTML file.

> ###### Parameters ######

>>***path*** (string, optional) , *default* = '' :
>>>Path to the output directory, by default it saves the plot in the current running environnement main directory.

>>***filename*** (string, optional) , *default* = 'default.html' :
>>>Custom output name of the HTML file.

> ###### Returns ######

>> An HTML file that is openable on any HTML/JS capable environnement, lighter weight than PNG (around 100ko)

&nbsp;
&nbsp;


### Fenics t-SNE calcualtions ###
#### FenBokehTSNE ####
_Class_ **FenGraphs.FenBokehTSNE(___data,\*\*kwargs___)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L444-L462)

A class that uses Scikit-learn t-SNE package.

> <h6> Attributes </h6>

>>***data***(numpy array or pandas DataFrame):
>>>The input data for t-SNE.

>>***normed*** (bool, optional):
>>>Specifies whether to normalize the input data. Default is False.

>>***perplexity*** (integer, optional):
>>>The perplexity parameter of t-SNE. It balances the attention given to local and global aspects of the data. Default is 59.

>>***random_state*** (integer, optional):
>>>The random seed for t-SNE. It ensures reproducibility of the results. Default is 80.

>>***n_iter*** (integer, optional):
>>>The maximum number of iterations for t-SNE optimization. Default is 59.

>>***learning_rate*** (integer, optional):
>>>The learning rate for t-SNE optimization. Higher values lead to faster convergence but may result in less accurate embeddings. Default is 59.



> <h6> Methods </h6>



>>[\_\_init\_\_(___x,y,\*args,\*\*kwargs___)](../FenGraphs/#fenbokehtsne) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L445-L456)

>>>FenBokehGrapher initialization of the object structure and attributes using the declared attributes. Do a norming operation if attribute is declared.

>>[tsne()](../FenGraphs/#fenbokehtsnetsne) [``source``](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenGraphs.py#L458-L462)

>>>Initiate t-SNE calculation. Uses Scikit-learn t-SNE fit and calculaltions, results with two local attributes (self.tsne_x and self.tsne_y).
