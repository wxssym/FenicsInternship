import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from scipy.stats import linregress
from .FenUtils import *
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from bokeh.plotting import figure, show
from bokeh.layouts import column,row,gridplot
from bokeh.models import ToolbarBox, CheckboxGroup,ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker, BasicTickFormatter, CustomJS, Range1d,RangeSlider,RadioGroup,Toolbar
from bokeh.palettes import Viridis256
from bokeh.transform import linear_cmap
from bokeh.io import output_notebook, save , curdoc

output_notebook()

fileFormats = {
    'svg' : '.svg',
    'jpeg' : '.jpeg',
    'pdf' : '.pdf',
    'png' : '.png'
}


def FenHist(FENICS,testTable,columns,selectedBoards,show=True,**kwargs):
    
    path = kwargs.get('path',None)
    if show==False and path == None:
        raise Exception('When show = False, you have to provide an output path, using path="yourPath"')
    
    sigma = kwargs.get('sigma', False)
    separate = kwargs.get('separate', False)
    saveFormat = kwargs.get('saveFormat', 'jpeg')
    
    if sigma != False:
        InSigma = dropOutSigma(FENICS,testTable,selectedBoards,sigma,columns=[columns])
        FENICS = FENICS.loc[InSigma]
        testTable = testTable.loc[InSigma]
    
    
    if separate == True and len(selectedBoards) > 1 :
        num_ids = len(selectedBoards)
        num_rows = min(num_ids, 9)
        num_cols = int(np.ceil(num_ids / num_rows))
        plt.figure(figsize=(15,20)) 
        plt.subplots_adjust(wspace=0.2, hspace=0.5)
        alpha = 1
    else :
        alpha = 0.6
        plt.figure(figsize=(15,10)) 
        plt.subplots_adjust(wspace=0.3, hspace=0.5)

    data_min = testTable[columns].min()
    data_max = testTable[columns].max()
    bins = np.linspace(data_min,data_max,15)
       
    color_dict = FenicsColors()
    
    for subplot,id in enumerate(selectedBoards) :
        if subplot == 0:
            FENICS_version,numeric_FENICS_version = Fenics_version(FENICS.Board.version)
        
        id_filter = FENICS[FENICS.Board.id==id].index
        if numeric_FENICS_version == 1 :
            if separate == True and len(selectedBoards) > 1 :
                plt.subplot(num_rows, num_cols, subplot + 1)
                # pd.Series(testTable.iloc[id_filter][columns]).hist(color=color_dict[id],bins=bins,density=False,range=[data_min, data_max],alpha=alpha,label=f'FENICS1 : {id}')
                plt.hist(testTable.loc[id_filter][columns],bins=bins,alpha=alpha,histtype='stepfilled',color=color_dict[id],label=f'{FENICS_version} : {id}')
            else :
                plt.hist(testTable.loc[id_filter][columns],bins=bins,alpha=alpha,histtype='stepfilled',color=color_dict[id],label=f'{FENICS_version} : {id}')
        else :
            if separate == True and len(selectedBoards) > 1 :
                plt.subplot(num_rows, num_cols, subplot + 1)
                # pd.Series(testTable.iloc[id_filter][columns]).hist(color=color_dict[id],bins=bins,density=False,range=[data_min, data_max],alpha=alpha,label=f'FENICS1 : {id}')
                plt.hist(testTable.loc[id_filter][columns],bins=bins,alpha=alpha,histtype='stepfilled',label=f'{FENICS_version} : {id}')
            else :
                plt.hist(testTable.loc[id_filter][columns],bins=bins,alpha=alpha,histtype='stepfilled',label=f'{FENICS_version} : {id}')
                
        if separate == True and len(selectedBoards) > 1:
            if len(columns) == 2:
                plt.xlabel(f'{columns[0]} {columns[1]}')
                plt.title(f'{FENICS_version} {id}')
            else :
                plt.xlabel(f'{columns[0]} {columns[1]} {columns[2]}')
                plt.title(f'{FENICS_version} {id}')
        else :
            if len(columns) == 2:
                plt.xlabel(f'{columns[0]} {columns[1]}');plt.ylabel(f'count')
                plt.title(f'All {FENICS_version} {columns[0]} {columns[1]} Histogram')
            else :
                plt.xlabel(f'{columns[0]} {columns[1]} {columns[2]}');plt.ylabel(f'count')
                plt.title(f'All {FENICS_version} {columns[0]} {columns[1]} {columns[2]}  histogram')
        plt.legend(fontsize=8)
   
    checkFolderAt(path)
    if len(columns) == 2:
        plt.suptitle(f'Fast histogram {columns[0]}:{columns[1]}',fontsize=16) 
        if path != None :
            plt.savefig(f'{path}/Fast_histogram_{columns[0]}:{columns[1]}'+fileFormats[saveFormat])
    elif len(columns) == 3:
        plt.suptitle(f'Slow histogram {columns[0]}:{columns[1]}:{columns[2]}',fontsize=16) 
        if path != None :
            plt.savefig(f'{path}/Slow_histogram_{columns[0]}:{columns[1]}:{columns[2]}'+fileFormats[saveFormat])
    else :
        raise Exception(f'second parameter should be a tuple of 2 if fast, or 3 if slow we got :{len(columns)}')
    
    if not show :
        plt.close()
    else :
        plt.show()


def FenCorr(FENICS,testTable,col1,col2,selectedBoards,show=True,**kwargs):
    
    """
    This function makes a correlation plot of two different FENICS features, it takes:
    FENICS: (DataFrame) dataframe of FENICS data.
    testTable : (DataFrame) of FENICS data FastResult Column, can be obtained by using FenicsTestTable() method.
    col1 : (tuple) tuple of (columns,subcolumn) of the feature, show in the X axis.
    col2 : (tuple) tuple of (columns,subcolumn) of the feature, show in the Y axis.
    selectedBoards : (list) list of ids of the requested FENICS cards, can be list of one card, or more, the plot will adapt accordingly.
    separate : (bool) if you want a single plot of all FENICS, or a separate subplot for each FENICS.
    burns : (bool) if you want a to have a heat map of the burning time of the different FENICS, or not.
    burns_filter : (int) default value is (None), implies to filter the X and Y with burn time threshold higher or equal to the value.
    LR : (bool) is True a linear regression is drawn to link the points.
    show : (bool) is to give you back the plot after saving, or closing the plot without a plt.show().
    """
    
    path = kwargs.get('path',None)
    if show==False and path == None:
        raise Exception('When show = False, you have to provide an output path, using path="yourPath"')
    separate = kwargs.get('separate',False)
    burns = kwargs.get('burns',False)
    burns_filter = kwargs.get('burns_filter',None)
    LR = kwargs.get('LR',True)
    sigma = kwargs.get('sigma',False)
    saveFormat = kwargs.get('saveFormat', 'jpeg')
    
    if sigma != False :
        InSigma = dropOutSigma(FENICS,testTable,selectedBoards,sigma,columns=[col1,col2])
        FENICS = FENICS.loc[InSigma]
        testTable = testTable.loc[InSigma]
    
    if separate == True and len(selectedBoards) > 1 :
        num_ids = len(selectedBoards)
        num_rows = min(num_ids, 7)
        num_cols = int(np.ceil(num_ids / num_rows))
        plt.figure(figsize=(15,20)) 
        plt.subplots_adjust(wspace=0.2, hspace=0.5)
    else :
        plt.figure(figsize=(15,10)) 
        plt.subplots_adjust(wspace=0.3, hspace=0.5)

    color_dict = FenicsColors()
    
    for subplot,id in enumerate(selectedBoards) :
        if subplot == 0:
            FENICS_version,numeric_FENICS_version = Fenics_version(FENICS.Board.version)
            
        if burns_filter != None and isinstance(burns_filter,int):
            id_filter = FENICS[FENICS.Board.id==id][FENICS.Board.burnTime>burns_filter].index
        else :
            id_filter = FENICS[FENICS.Board.id==id].index
        
        x = testTable.loc[id_filter][col1]
        y = testTable.loc[id_filter][col2]
        
        if separate == True and len(selectedBoards) > 1 :
            plt.subplot(num_rows, num_cols, subplot + 1)
                
        if burns == True :
            c=FENICS.loc[id_filter].Board.burnTime
            vmin = 0
            vmax = FENICS.Board.burnTime.max()
        else : 
            c=color_dict[id]
        
        # plt.scatter(x, y, c=c,edgecolor=color_dict[id],label=f'FENICS1 : {id}')
        plt.scatter(x, y, c=c,vmin=vmin,vmax=vmax,label=f'{FENICS_version} : {id}')
        
        if LR :
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            x_line = np.linspace(np.min(x), np.max(x), 100)
            y_line = slope * x_line + intercept
            
            if burns == True :
                plt.plot(x_line, y_line,'r-', alpha=0.7 , label=f'{FENICS_version} : {id} RLine, slope={slope:.4f}')
            else :
                plt.plot(x_line, y_line,'r-', c=color_dict[id], alpha=0.7 , label=f'{FENICS_version} : {id} RLine, slope={slope:.4f}')
        
        if separate == True and len(selectedBoards) > 1:
            if len(col1) == 2:
                plt.xlabel(f'{col1[0]} {col1[1]}')
                plt.title(f'{FENICS_version} {id}')
            else :
                plt.xlabel(f'{col1[0]} {col1[1]} {col1[2]}')
                plt.title(f'{FENICS_version} {id}')
        else :
            if len(col1) == 2:
                plt.xlabel(f'{col1[0]} {col1[1]}');plt.ylabel(f'{col2[0]}  {col2[1]}')
                plt.title(f'All {FENICS_version} {col1[0]} {col1[1]} vs {col2[0]}  {col2[1]}')
            else :
                plt.xlabel(f'{col1[0]} {col1[1]} {col1[2]}');plt.ylabel(f'{col2[0]}  {col2[1]} {col2[2]}')
                plt.title(f'All {FENICS_version} {col1[0]} {col1[1]} {col1[2]} vs {col2[0]}  {col2[1]} {col2[2]} ')
        plt.legend(fontsize=10)
    
    if burns :
        if separate == True and len(selectedBoards) > 1:
            cax = plt.axes([0.93, 0.5, 0.03, 0.2])
            plt.colorbar(cax=cax,orientation='vertical')
        else :
            cax = plt.axes([0.93, 0.5, 0.03, 0.2])
            plt.colorbar(cax=cax,orientation='vertical')
        
    checkFolderAt(path)
    
    if len(col1) == 2:
        plt.suptitle(f'Fast {col1[0]}:{col1[1]} vs {col2[0]}:{col2[1]}',fontsize=16)
        if path !=None :
            plt.savefig(f'{path}/Fast_correlation_between_{col1[0]}_{col1[1]}__{col2[0]}_{col2[1]}'+fileFormats[saveFormat])
    elif len(col1) == 3:
        plt.suptitle(f'Slow {col1[0]}:{col1[1]}:{col1[2]} vs {col2[0]}:{col2[1]}:{col2[2]}',fontsize=16) 
        if path !=None :
            plt.savefig(f'{path}/Slow_correlation_between_{col1[0]}_{col1[1]}_{col1[2]}__{col2[0]}_{col2[1]}_{col2[2]}'+fileFormats[saveFormat])
    else :
        raise Exception(f'second parameter should be a tuple of 2 if fast, or 3 if slow we got :{len(col1)}')
    
    if not show :
        plt.close()
    else :
        plt.show()


def FenBurnEvol(FENICS,testTable,columns,selectedBoards,show=True,**kwargs):

    path = kwargs.get('path',None)
    if show==False and path == None:
        raise Exception('When show = False, you have to provide an output path, using path="yourPath"')
    separate = kwargs.get('separate',False)
    burns = kwargs.get('burns',False)
    unique = kwargs.get('unique',False)
    LR = kwargs.get('LR',True)
    sigma = kwargs.get('sigma',False)
    saveFormat = kwargs.get('saveFormat', 'jpeg')
    
    if sigma != False:
        InSigma = dropOutSigma(FENICS,testTable,sigma,filter_id=selectedBoards,columns=[columns])
        FENICS = FENICS.loc[InSigma]
        testTable = testTable.loc[InSigma]
        
            
    if separate == True and len(selectedBoards) > 1 :
        num_ids = len(selectedBoards)
        num_rows = min(num_ids, 7)
        num_cols = int(np.ceil(num_ids / num_rows))
        plt.figure(figsize=(15,20)) 
        plt.subplots_adjust(wspace=.0,hspace=.0)
    else :
        plt.figure(figsize=(15,10)) 
        plt.subplots_adjust(wspace=0.3, hspace=0.5)
        
        
    xmax = FENICS.Board.burnTime.max()
    ymin = testTable[columns].min()
    ymax= testTable[columns].max()
    color_dict = FenicsColors()
    
    for subplot,id in enumerate(selectedBoards) :
        id_filter = FENICS[FENICS.Board.id==id].index
        x = FENICS.Board.burnTime.loc[id_filter]
        y = testTable[columns].loc[id_filter]
        
        if subplot == 0:
            FENICS_version,numeric_FENICS_version = Fenics_version(FENICS.Board.version)
                
        if unique :
            x,y=uniqueVals(x,y) 
            
        if separate == True and len(selectedBoards) > 1 :
            if subplot == 0 :
                ax1 = plt.subplot(num_rows, num_cols, subplot + 1)
                plt.ylabel(f'{columns[0]} {columns[1]}')  
            else : 
                ax = plt.subplot(num_rows, num_cols, subplot + 1, sharey=ax1,sharex=ax1)
                plt.setp(ax.get_yticklabels(), visible=False)
                plt.setp(ax1.get_xticklabels(), visible=False)
                
            plt.xlim([0, xmax])
            plt.ylim([ymin,ymax])
            
        if numeric_FENICS_version != 2:
            if burns == True :
                c=FENICS.Board.burnTime.loc[id_filter]
                vmin = 0
                vmax = FENICS.Board.burnTime.max()
                plt.scatter(x, y, c=c,vmin=vmin,vmax=vmax,label=f'{FENICS_version} : {id}')
            else : 
                c=color_dict[id]
                plt.scatter(x, y, c=c,label=f'{FENICS_version} : {id}')
        else:
            if burns == True :
                c=FENICS.Board.burnTime.loc[id_filter]
                vmin = 0
                vmax = FENICS.Board.burnTime.max()
                plt.scatter(x, y, c=c,vmin=vmin,vmax=vmax,label=f'{FENICS_version} : {id}')
            else : 
                plt.scatter(x, y,label=f'{FENICS_version} : {id}')
            
            

        
        if LR :
            if numeric_FENICS_version == 2 :              
                slope, intercept, r_value, p_value, std_err = linregress(x, y)
                x_line = np.linspace(np.min(x), np.max(x), 100)
                y_line = slope * x_line + intercept
                plt.plot(x_line, y_line,'r--', alpha=0.7 , label=f'{FENICS_version} : {id} RLine, slope={slope:.4f}')
                
            else :
                before_filter = FENICS[FENICS.Board.id==id][FENICS.Board.burnTime<2772].index
                before_y = testTable[columns].loc[before_filter]
                before_x = FENICS.Board.burnTime.loc[before_filter]
                slope, intercept, r_value, p_value, std_err = linregress(before_x, before_y)
                x_line = np.linspace(np.min(before_x), np.max(before_x), 100)
                y_line = slope * x_line + intercept
                
                if burns == True :
                    plt.plot(x_line, y_line,'r--', alpha=0.7 , label=f'{FENICS_version} : {id} RLine, slope={slope:.4f}')
                else :
                    plt.plot(x_line, y_line,'r--', c=color_dict[id], alpha=0.7 , label=f'{FENICS_version} : {id} bfr, slope={slope:.4f}')
                    
                after_filter = FENICS[FENICS.Board.id==id][FENICS.Board.burnTime>2772].index
                after_y = testTable.loc[after_filter][columns]
                after_x = FENICS.Board.burnTime.loc[after_filter]
                
                slope, intercept, r_value, p_value, std_err = linregress(after_x, after_y)
                x_line = np.linspace(np.min(after_x), np.max(after_x), 100)
                y_line = slope * x_line + intercept
                
                if burns == True :
                    plt.plot(x_line, y_line,'r-', alpha=0.7 , label=f'{FENICS_version} : {id} RLine, slope={slope:.4f}')
                else :
                    plt.plot(x_line, y_line,'r-', c=color_dict[id], alpha=0.7 , label=f'{FENICS_version} : {id} aftr, slope={slope:.4f}')
                    
        if separate != True and len(selectedBoards) == 1:
            plt.xlabel(f'burnTime');plt.ylabel(f'{columns[0]}  {columns[1]}')
            plt.title(f'All {FENICS_version} {columns[0]}  {columns[1]} evolution')
        plt.legend(fontsize=10)
    
    if separate == True and len(selectedBoards)>1:
        plt.xlabel(f'burnTime');
        
    if burns :   
        plt.colorbar() 

    checkFolderAt(path)
    
    if len(columns) == 2:
        plt.suptitle(f'Fast {columns[0]}_{columns[1]} burn evolution',fontsize=16)
        if path != None :
            plt.savefig(f'{path}/Fast_{columns[0]}__{columns[1]}_burnEvolution'+fileFormats[saveFormat])
    elif len(columns) == 3:
        plt.suptitle(f'Slow {columns[0]}_{columns[1]}_{columns[2]} burn evolution',fontsize=16) 
        if path !=None :
            plt.savefig(f'{path}/Slow_{columns[0]}_{columns[1]}_{columns[2]}_burnEvolution'+fileFormats[saveFormat])
    else :
        raise Exception(f'Columns should be a tuple of 2 if fast, or 3 if slow we got :{len(columns)}')
    
    if not show :
        plt.close()
    else :
        plt.show()


def FenSpread(FENICS,testTable,columns,selectedBoards,show=True,**kwargs):
    
    
    path = kwargs.get('path',None)
    if show==False and path == None:
        raise Exception('When show = False, you have to provide an output path, using path="yourPath"')
    burns = kwargs.get('burns',False)
    sigma = kwargs.get('sigma',False)
    saveFormat = kwargs.get('saveFormat', 'jpeg')
    
    if sigma != False:
        InSigma = dropOutSigma(FENICS,testTable,selectedBoards,sigma,columns=[columns])
        FENICS = FENICS.loc[InSigma]
        testTable = testTable.loc[InSigma]
    
    
    FENICS_version,FENICS_version_numeric = Fenics_version(FENICS.Board.version)
    
    plt.figure(figsize=(15,8.43)) 
    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    
    for i,id in enumerate(selectedBoards) :
        if i == 0:
            FENICS_version,numeric_FENICS_version = Fenics_version(FENICS.Board.version)
            
        color_dict = FenicsColors()
        if burns == True :
            c=FENICS[FENICS.Board.id==id].Board.burnTime
            vmin = 0
            vmax = FENICS.Board.burnTime.max()
        else : 
            c=color_dict[id]
        
        filtred_index = FENICS[FENICS.Board.id==id].index
        # x = FENICS.loc[filtred_index].Board.id
        y = testTable.loc[filtred_index][columns]
        x = [i]*len(y)
        plt.scatter(x,y,c=c,vmin=vmin, vmax=vmax,label=f'{FENICS_version} {id}')
        
    labels = [str(id) for id in selectedBoards]
    ticks = range(0,len(selectedBoards))
    plt.xticks(ticks, labels, rotation='vertical')
    
    plt.xlabel(f'{FENICS_version} cards')
    # plt.legend(fontsize=10)
    plt.colorbar(orientation='vertical')
    checkFolderAt(path)
    
    if len(columns) == 2:
        plt.ylabel(f'{columns[0]} : {columns[1]}')  
        plt.suptitle(f'{FENICS_version} Fast {columns[0]}:{columns[1]} data spreading',fontsize=16)
        if path !=None :
            plt.savefig(f'{path}/Fast_{columns[0]}:{columns[1]}_data_spreading'+fileFormats[saveFormat])
    elif len(columns) == 3:
        plt.ylabel(f'{columns[0]} : {columns[1]} : {columns[2]}')
        plt.suptitle(f'{FENICS_version} Slow {columns[0]}:{columns[1]}:{columns[2]} data spreading',fontsize=16)
        if path !=None :
            plt.savefig(f'{path}/Slow_{columns[0]}:{columns[1]}:{columns[2]}_data_spreading'+fileFormats[saveFormat])
    else :
        raise Exception(f'second parameter should be a tuple of 2 if fast, or 3 if slow we got :{len(columns)}')
    
    if not show :
        plt.close()
    else :
        plt.show()


class FenBokehTSNE:
    def __init__(self, data,**kwargs):
        self.data = data
        self.normed = kwargs.get('normalize',False)
        if self.normed:
            self.data = Normalizer(data)
        
        self.perplexity = kwargs.get('perplexity',59)
        self.random_state = kwargs.get('random_state',80)
        self.n_iter = kwargs.get('n_iter',300)
        self.learning_rate = kwargs.get('learning_rate',300)
        self.n_components = kwargs.get('n_components',2)
        self.tsne()

    def tsne(self):
        tsne = TSNE(n_components=self.n_components, perplexity=self.perplexity, random_state=self.random_state, n_iter=self.n_iter,learning_rate=self.learning_rate)
        self.embedding = tsne.fit_transform(self.data)
        self.tsne_x = self.embedding[:,0]
        self.tsne_y = self.embedding[:,1]      



class FenBokehGrapher:
    def __init__(self, datax, datay, *args, **kwargs ):
        self.x = datax
        self.y = datay
        self.colors = kwargs.get('colors', [0 for ii in range(0,len(datax))])
        self.labels = kwargs.get('labels', ["1" for ii in range(0,len(datax))])
        self.source = ColumnDataSource(data=dict(
            x=self.x,
            y=self.y,
            colors = self.colors,
            labels= self.labels,
            index = list(range(0,len(self.x))),
        ))
        self.plot = None
        self.tooltips = kwargs.get('tooltips',None)
        self.args = args

            
    def create_plot(self,title='',axis_xlabel='',axis_ylabel=''):
        # Create a ColumnDataSource
        
        for arg in self.args:
            self.source.add(arg,arg.name)
        
        source2_data = {}
        for key in self.source.data :
            source2_data[key]=[]
        self.source2 = ColumnDataSource(data=source2_data)
        
        # Create a figure
        TOOLS="pan,wheel_zoom,box_zoom,reset,hover,box_select,lasso_select,save"
        self.plot = figure(width=800, height=600, tools=TOOLS, tooltips=self.tooltips)
        self.plot.toolbar.logo = None
        dynamic_range_x = max(self.x)-min(self.x)
        dynamic_range_y = max(self.y)-min(self.y)
        self.plot.x_range = Range1d(min(self.x)-dynamic_range_x*0.02,max(self.x)+dynamic_range_x*0.02)
        self.plot.y_range = Range1d(min(self.y)-dynamic_range_y*0.02,max(self.y)+dynamic_range_y*0.02)
        self.plot.xaxis.axis_label = axis_xlabel
        self.plot.yaxis.axis_label = axis_ylabel
        self.plot.title.text = title


        cmap = linear_cmap("colors", palette=Viridis256, low=min(self.colors), high=max(self.colors))
        
        self.filtred_scatter = self.plot.scatter(x='x', y='y', size=7, fill_color="LightGray", fill_alpha=0.5, line_color = "LightGray", source=self.source2)
        self.selected_scatter = self.plot.scatter(x='x', y='y', size=7, fill_color=cmap, fill_alpha=0.8, line_color=cmap, source=self.source)
        
               
        self.source3 = ColumnDataSource(data=dict(x=[], y=[]))
        if self.linear_fit == True :
            slope, intercept, r_value, p_value, std_err = linregress(self.source.data['x'], self.source.data['y'])
            self.source3.data['x'] = np.linspace(np.min(self.source.data['x']), np.max(self.source.data['x']), 100)
            self.source3.data['y'] = slope *  self.source3.data['x'] + intercept
            self.plot.line(x='x', y='y', color="orange", line_width=5, alpha=0.6, source=self.source3, legend_label=f'slope : {slope}, intercept : {intercept}')
            self.plot.legend.location = "top_left"
            self.plot.legend.click_policy="hide"
            self.legend = self.plot.legend[0]
        else :
            self.legend = None
        
        # Create color mapper for the color bar
        color_mapper = LinearColorMapper(palette=Viridis256, low=min(self.colors), high=max(self.colors))

        # Create color bar with ticker
        color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0), ticker=BasicTicker(), formatter=BasicTickFormatter())
        
        self.plot.add_layout(color_bar, 'right')

    def create_hist(self,title='',axis_xlabel='',axis_ylabel=''):
        self.create_plot(title=title,axis_xlabel=axis_xlabel,axis_ylabel=axis_ylabel)
        # create the horizontal histogram
        hhist, hedges = np.histogram(self.source.data['x'], bins=20)
        hzeros = np.zeros(len(hedges)-1)
        hmax = max(hhist)*1.1
        
        hhist2, hedges2 = np.histogram(self.source2.data['x'], bins=20)
        
        LINE_ARGS = dict(color="#3A5785", line_color=None)

        self.plothorizontal = figure(toolbar_location=None, width=self.plot.width, height=200, x_range=self.plot.x_range,
                                    y_range=(-hmax, hmax), min_border=10, min_border_left=50, y_axis_location="right")
        self.plothorizontal.xgrid.grid_line_color = None
        self.plothorizontal.yaxis.major_label_orientation = np.pi/4
        self.plothorizontal.background_fill_color = "#fafafa"

        self.plothorizontal.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
        self.hh = self.plothorizontal.quad(bottom=hhist2, left=hedges[:-1], right=hedges[1:], top=0,alpha=0.3, color="white", line_color="#3A5785")
        self.hh1 = self.plothorizontal.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
        self.hh2 = self.plothorizontal.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)

        # create the vertical histogram
        vhist, vedges = np.histogram(self.source.data['y'], bins=20)
        vzeros = np.zeros(len(vedges)-1)
        vmax = max(vhist)*1.1
        vhist2, vedges2 = np.histogram(self.source2.data['y'], bins=20)
        
        self.plotvertical = figure(toolbar_location=None, width=200, height=self.plot.height, x_range=(-vmax, vmax),
                                y_range=self.plot.y_range, min_border=10, y_axis_location="right")
        self.plotvertical.ygrid.grid_line_color = None
        self.plotvertical.xaxis.major_label_orientation = np.pi/4
        self.plotvertical.background_fill_color = "#fafafa"

        self.plotvertical.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white", line_color="#3A5785")
        self.vh = self.plotvertical.quad(left=vhist2, bottom=vedges[:-1], top=vedges[1:], right=0, alpha=0.3, color="white", line_color="#3A5785")
        self.vh1 = self.plotvertical.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
        self.vh2 = self.plotvertical.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)
        
        update_hist = CustomJS(args=dict(source=self.source,source2=self.source2,source3=self.source3,hh=self.hh,hh1=self.hh1,legend=self.legend, hh2=self.hh2,vh=self.vh,vh1=self.vh1,vh2=self.vh2,hzeros=hzeros,vzeros=vzeros,hedges=hedges,vedges=vedges),code="""
        var inds = source.selected.indices;
        const x = source.data['x'];
        const y = source.data['y'];
        hzeros=hzeros;
        vzeros=vzeros;
        hedges=hedges;
        vedges=vedges;
        let fit_data = {};
        if (inds.length === 0) 
        {
            hh1.data_source.data["top"]  = hzeros;
            hh2.data_source.data["top"]  = hzeros;
            vh1.data_source.data["right"]  = vzeros;
            vh2.data_source.data["right"]  = vzeros;
            fit_data['x']=[]
            fit_data['y']=[]
            fit_data['slope']=[]
            fit_data['intercept']=[]
            if (legend instanceof Object){
                var new_text = 'no selection';
                legend.items[0].label = new_text;
            }            
        } else {
            var neg_inds = new Array(x.length).fill(true);
            for (var i = 0; i < inds.length; i++) 
            {
                neg_inds[inds[i]] = false;
            }
            
            var hh1_selected = [];
            var vh1_selected = [];
            var hh2_selected = [];
            var vh2_selected = [];
            
            for (var i = 0; i < inds.length; i++) 
            {
            hh1_selected.push(x[inds[i]]);
            vh1_selected.push(y[inds[i]]);
            }
            for (var i = 0; i < neg_inds.length; i++) 
            {
            if (neg_inds[i]) {
                hh2_selected.push(x[i]);
                vh2_selected.push(y[i]);
            }
            
            let linear_fit = linearFit(hh1_selected,vh1_selected)
            fit_data['slope']=linear_fit.slope
            fit_data['intercept']=linear_fit.intercept
            fit_data['x']=linear_fit.x
            fit_data['y']=linear_fit.YValues
            if (legend instanceof Object){
                var new_text = 'slope : ' + linear_fit.slope.toFixed(5) + ', intercept : ' + linear_fit.intercept.toFixed(3);
                legend.items[0].label = new_text;
            }
            // Update the source data with the modified data
            
            //hh.data_source.data["bottom"]  = histogram(source2.data['x'],hedges).counts.map(function(val) {
            //    return -val;
            //});
            
            hh1.data_source.data["top"]  = histogram(hh1_selected,hedges).counts ;
            hh2.data_source.data["top"]  = histogram(hh2_selected,hedges).counts.map(function(val) {
                return -val;
            });
            
            // vh.data_source.data["left"]  = histogram(source2.data['y'],hedges).counts.map(function(val) {
            //    return -val;
            //});
            
            vh1.data_source.data["right"]  = histogram(vh1_selected,vedges).counts ;
            vh2.data_source.data["right"]  = histogram(vh2_selected, vedges).counts.map(function(val) {
                return -val;
            });
            }
        }
        //hh.data_source.change.emit()
        hh1.data_source.change.emit()             
        hh2.data_source.change.emit()

        //vh.data_source.change.emit()
        vh1.data_source.change.emit()
        vh2.data_source.change.emit() 
        
        function histogram(data, binEdges) {
        // Initialize an array to store the bin counts
        var counts = new Array(binEdges.length - 1).fill(0);

        // Loop through the data and increment the appropriate bin count
        for (var i = 0; i < data.length; i++) {
            var value = data[i];
            // Find the bin index for the current value
            for (var j = 0; j < binEdges.length - 1; j++) {
            if (value >= binEdges[j] && value < binEdges[j + 1]) {
                counts[j]++;
                break;
            }
            // Handle the edge case where the value is equal to the maximum bin edge
            if (j === binEdges.length - 2 && value === binEdges[j + 1]) {
                counts[j + 1]++;
                break;
            }
            }
        }

        // Return the bin counts and bin edges as an object
        return {counts: counts, edges: binEdges};
        }
        
        function linspace(start, stop, num){
            if (isNaN(start) || isNaN(stop)) {
                throw new Error("Invalid start or stop value");
            }
            const step = (stop - start) / (num - 1);
            const arr = [];
            for (let i = 0; i < num; i++) {
                arr.push(start + i * step);
            }
            return arr;
        };
        
        function calculateMean(arr) {
            const sum = arr.reduce((acc, val) => acc + val, 0); // Calculate the sum of array elements
            const mean = sum / arr.length; // Divide the sum by the number of elements to get the mean
            return mean;
        };
        
        
        function linearFit(X, y)
        {
            const n = X.length;
            const XMean = calculateMean(X);
            const yMean = calculateMean(y);

            // Calculate the numerator and denominator of the slope (m) of the line
            let numerator = 0;
            let denominator = 0;
            for (let i = 0; i < n; i++) {
                numerator += (X[i] - XMean) * (y[i] - yMean);
                denominator += (X[i] - XMean) ** 2;
            }
            const x = linspace(Math.min(...X), Math.max(...X), 30);
            const slope = numerator / denominator; // Calculate the slope (m) of the line
            const intercept = yMean - slope * XMean; // Calculate the y-intercept (b) of the line
            const YValues = x.map((val) => slope * val + intercept);
            
            return { slope, intercept,x,YValues};
        };
        

        
        console.log(fit_data)
        source3.data = fit_data;
        source3.change.emit();
        
        
        
        """)

        self.source.selected.js_on_change('indices',update_hist)

    def create_slider(self,**kwargs):
        slider_params = kwargs.get('slider_params',{})

        self.range_slider = RangeSlider(start=slider_params.get('min',min(self.colors)),
                                        end=slider_params.get('max',max(self.colors)),
                                        value=(slider_params.get('valmin',min(self.colors)),slider_params.get('valmax',max(self.colors))),
                                        step=slider_params.get('step',20),
                                        title=slider_params.get('title','Filter'),
                                        orientation=slider_params.get('orientation','vertical'),
                                        height=slider_params.get('height',300),
                                        direction=slider_params.get('direction','rtl'))
    
        callback = CustomJS(args=dict(source=self.source,source2=self.source2,source3=self.source3,legend = self.legend,original_data=self.original_data,range_slider=self.range_slider),
                        code="""
                        
        const original_index = original_data['index'];
        const original_colors = original_data['colors'];
        
        var value = range_slider.value;
        var min_value = value[0];
        var max_value = value[1];
        
        let kept_data = {};
        for (const key in original_data) {
            if (original_data.hasOwnProperty(key)) {
                kept_data[key] = [];
            }
        };
        
        let filtred_data = {};
        for (const key in original_data) {
            if (original_data.hasOwnProperty(key)) {
                filtred_data[key] = [];
           }
        };
        
        for (let i = 0; i < original_index.length; i++) {
            if (original_colors[i] >= min_value && original_colors[i] <= max_value) {
                for (const key in original_data) 
                        {
                            kept_data[key].push(original_data[key][i]);
                        }
            } else {
                for (const key in original_data) 
                        {
                            filtred_data[key].push(original_data[key][i]);
                        }
            }
        }
        
        // Update the source data with the modified data
        source2.data = filtred_data;
        source2.change.emit();
        source.data = kept_data;
        source.change.emit();

        
        function linspace(start, stop, num){
            if (isNaN(start) || isNaN(stop)) {
                throw new Error("Invalid start or stop value");
            }
            const step = (stop - start) / (num - 1);
            const arr = [];
            for (let i = 0; i < num; i++) {
                arr.push(start + i * step);
            }
            return arr;
        };
        
        function calculateMean(arr) {
            const sum = arr.reduce((acc, val) => acc + val, 0); // Calculate the sum of array elements
            const mean = sum / arr.length; // Divide the sum by the number of elements to get the mean
            return mean;
        };
        
        
        function linearFit(X, y)
        {
            const n = X.length;
            const XMean = calculateMean(X);
            const yMean = calculateMean(y);

            // Calculate the numerator and denominator of the slope (m) of the line
            let numerator = 0;
            let denominator = 0;
            for (let i = 0; i < n; i++) {
                numerator += (X[i] - XMean) * (y[i] - yMean);
                denominator += (X[i] - XMean) ** 2;
            }
            const x = linspace(Math.min(...X), Math.max(...X), 30);
            const slope = numerator / denominator; // Calculate the slope (m) of the line
            const intercept = yMean - slope * XMean; // Calculate the y-intercept (b) of the line
            const YValues = x.map((val) => slope * val + intercept);
            
            return { slope, intercept,x,YValues};
        };
        
        let fit_data = {};
        let linear_fit = linearFit(kept_data.x,kept_data.y)
        fit_data['x']=linear_fit.x
        fit_data['y']=linear_fit.YValues
        if (legend instanceof Object) {
            var new_text = 'slope : ' + linear_fit.slope.toFixed(5) + ', intercept : ' + linear_fit.intercept.toFixed(3);
            legend.items[0].label = new_text;
        }
        // Update the source data with the modified data
        
        console.log(fit_data)
        source3.data = fit_data;
        source3.change.emit();
    """)
        self.range_slider.js_on_change('value', callback)
        
    def create_checkboxes(self, **kwargs):
        unique_labels = kwargs.get('labels_filter',pd.unique(self.labels))
        self.checkbox_group = CheckboxGroup(labels=[str(i) for i in unique_labels], active=list(range(len(unique_labels))),width=40)
        callback = CustomJS(args=dict(source=self.source,source2=self.source2,source3=self.source3,legend = self.legend,original_data=self.original_data,checkbox_group=self.checkbox_group),
                        code="""
        const selected_checkboxes = checkbox_group.active.map(i => checkbox_group.labels[i]);
        
        const original_index = original_data['index'];
        const original_labels = original_data['labels'];

        let kept_data = {};
        for (const key in original_data) {
            if (original_data.hasOwnProperty(key)) {
                kept_data[key] = [];
            }
        };
        
        let filtred_data = {};
        for (const key in original_data) {
            if (original_data.hasOwnProperty(key)) {
                filtred_data[key] = [];
            }
        };

        for (let i = 0; i < original_index.length; i++) {
                if (selected_checkboxes.includes(original_labels[i].toString()))
                {
                    for (const key in original_data) 
                        {
                            kept_data[key].push(original_data[key][i]);
                        }
                } else {
                    for (const key in original_data) 
                        {
                            filtred_data[key].push(original_data[key][i]);
                        }
                }
        }
        
        source2.data = filtred_data;
        source2.change.emit();
        source.data = kept_data;
        source.change.emit();
        
        function linspace(start, stop, num){
            if (isNaN(start) || isNaN(stop)) {
                throw new Error("Invalid start or stop value");
            }
            const step = (stop - start) / (num - 1);
            const arr = [];
            for (let i = 0; i < num; i++) {
                arr.push(start + i * step);
            }
            return arr;
        };
        
        function calculateMean(arr) {
            const sum = arr.reduce((acc, val) => acc + val, 0); // Calculate the sum of array elements
            const mean = sum / arr.length; // Divide the sum by the number of elements to get the mean
            return mean;
        };
        
        
        function linearFit(X, y)
        {
            const n = X.length;
            const XMean = calculateMean(X);
            const yMean = calculateMean(y);

            // Calculate the numerator and denominator of the slope (m) of the line
            let numerator = 0;
            let denominator = 0;
            for (let i = 0; i < n; i++) {
                numerator += (X[i] - XMean) * (y[i] - yMean);
                denominator += (X[i] - XMean) ** 2;
            }
            const x = linspace(Math.min(...X), Math.max(...X), 30);
            const slope = numerator / denominator; // Calculate the slope (m) of the line
            const intercept = yMean - slope * XMean; // Calculate the y-intercept (b) of the line
            const YValues = x.map((val) => slope * val + intercept);
            
            return { slope, intercept,x,YValues};
        };
        
        let fit_data = {};
        let linear_fit = linearFit(kept_data.x,kept_data.y)
        fit_data['x']=linear_fit.x
        fit_data['y']=linear_fit.YValues
        if (legend instanceof Object) {
            var new_text = 'slope : ' + linear_fit.slope.toFixed(5) + ', intercept : ' + linear_fit.intercept.toFixed(3);
            legend.items[0].label = new_text;
        }
        // Update the source data with the modified data
        
        console.log(fit_data)
        source3.data = fit_data;
        source3.change.emit();
        """)
        self.checkbox_group.js_on_change('active', callback) 
        
    def create_radiocheckbox(self,**kwargs):
        
        if 'radio_categories' in kwargs.keys():
            category_indexes = {}
            radio_labels = ['select all','select none']
            for i,category in enumerate(kwargs['radio_categories']):
                radio_labels.append(category['name'])
                category_indexes[i+2] = category['indexes']
                
            self.radio_group = RadioGroup(labels=radio_labels, active=0,width=80)
        else :
            category_indexes = False
            self.radio_group = RadioGroup(labels=['select all','select none'], active=0,width=80)
        
        callback = CustomJS(args=dict(checkbox_group=self.checkbox_group,category_indexes=category_indexes), code="""
            console.log(category_indexes)
            const selected_option = cb_obj.active;
            const checkboxes = checkbox_group.active;
            const labels = checkbox_group.labels;
            // If "Select All" is checked, check all checkboxes
            if (selected_option === 0) {
                checkbox_group.active = Array.from({length: labels.length}, (_, i) => i);
            }
            // If "Deselect All" is checked, uncheck all checkboxes
            else if (selected_option === 1) {
                checkbox_group.active = [];
            }
            else if (selected_option in category_indexes) {
                const active = []
                category_indexes[selected_option].forEach(element => appendActive(active,labels,element))
                checkbox_group.active = active;
                console.log(active)
            }
            
            function appendActive(active,labels,element) {
                active.push(checkbox_group.labels.indexOf(element.toString()));
            }
            
            
        """)
        self.radio_group.js_on_click(callback)
    
    def selection_callback(self):
        callback = CustomJS(args=dict(source=self.source,source3=self.source3,legend=self.legend),code="""
        var inds = source.selected.indices;
        const x = source.data['x'];
        const y = source.data['y'];
        
        let fit_data = {};
        if (inds.length === 0) 
        {
            fit_data['x']=[]
            fit_data['y']=[]
            fit_data['slope']=[]
            fit_data['intercept']=[]
            
            if (legend instanceof Object)
            {
                var new_text = 'no selection';
                legend.items[0].label = new_text;
            }            
        } 
        else 
        {
            var hh1_selected = [];
            var vh1_selected = [];
            for (var i = 0; i < inds.length; i++) 
            {
                hh1_selected.push(x[inds[i]]);
                vh1_selected.push(y[inds[i]]);
            }
            
            let linear_fit = linearFit(hh1_selected,vh1_selected)
            fit_data['slope']=linear_fit.slope
            fit_data['intercept']=linear_fit.intercept
            fit_data['x']=linear_fit.x
            fit_data['y']=linear_fit.YValues
            
            if (legend instanceof Object)
            {
                var new_text = 'slope : ' + linear_fit.slope.toFixed(5) + ', intercept : ' + linear_fit.intercept.toFixed(3);
                legend.items[0].label = new_text;
            }
        }
        
        function linspace(start, stop, num){
            if (isNaN(start) || isNaN(stop)) {
                throw new Error("Invalid start or stop value");
            }
            const step = (stop - start) / (num - 1);
            const arr = [];
            for (let i = 0; i < num; i++) {
                arr.push(start + i * step);
            }
            return arr;
        };
        
        function calculateMean(arr) {
            const sum = arr.reduce((acc, val) => acc + val, 0); // Calculate the sum of array elements
            const mean = sum / arr.length; // Divide the sum by the number of elements to get the mean
            return mean;
        };
        
        function linearFit(X, y)
        {
            const n = X.length;
            const XMean = calculateMean(X);
            const yMean = calculateMean(y);

            // Calculate the numerator and denominator of the slope (m) of the line
            let numerator = 0;
            let denominator = 0;
            for (let i = 0; i < n; i++) {
                numerator += (X[i] - XMean) * (y[i] - yMean);
                denominator += (X[i] - XMean) ** 2;
            }
            const x = linspace(Math.min(...X), Math.max(...X), 30);
            const slope = numerator / denominator; // Calculate the slope (m) of the line
            const intercept = yMean - slope * XMean; // Calculate the y-intercept (b) of the line
            const YValues = x.map((val) => slope * val + intercept);
            
            return { slope, intercept,x,YValues};
        }

        source3.data = fit_data;
        source3.change.emit();
        """)

        self.source.selected.js_on_change('indices',callback)
    
    def create_combo_filter(self,**kwargs):
        
        slider_params = kwargs.get('slider_params',{})

        self.range_slider = RangeSlider(start=slider_params.get('min',min(self.colors)),
                                        end=slider_params.get('max',max(self.colors)),
                                        value=(slider_params.get('valmin',min(self.colors)),slider_params.get('valmax',max(self.colors))),
                                        step=slider_params.get('step',20),
                                        title=slider_params.get('title','Color'),
                                        orientation=slider_params.get('orientation','vertical'),
                                        height=slider_params.get('height',300),
                                        direction=slider_params.get('direction','rtl'))
        
        unique_labels = kwargs.get('labels_filter',pd.unique(self.labels))
        self.checkbox_group = CheckboxGroup(labels=[str(i) for i in unique_labels], active=list(range(len(unique_labels))),width=40)
        
        callback = CustomJS(args=dict(source=self.source,source2=self.source2,source3=self.source3,legend = self.legend,original_data=self.original_data,checkbox_group=self.checkbox_group,range_slider=self.range_slider),
                        code="""
                        
        const selected_checkboxes = checkbox_group.active.map(i => checkbox_group.labels[i]);                
                        
        const original_index = original_data['index'];
        const original_colors = original_data['colors'];
        const original_labels = original_data['labels'];
        
        var value = range_slider.value;
        var min_value = value[0];
        var max_value = value[1];
        
        let kept_data = {};
        for (const key in original_data) {
            if (original_data.hasOwnProperty(key)) {
                kept_data[key] = [];
            }
        };
        
        let filtred_data = {};
        for (const key in original_data) {
            if (original_data.hasOwnProperty(key)) {
                filtred_data[key] = [];
           }
        };
        
        for (let i = 0; i < original_index.length; i++) 
        {
            if (original_colors[i] >= min_value && original_colors[i] <= max_value) 
            {
                if (selected_checkboxes.includes(original_labels[i].toString()))
                {
                    for (const key in original_data) 
                        {
                            kept_data[key].push(original_data[key][i]);
                        }
                } 
                else 
                {
                    for (const key in original_data) 
                        {
                            filtred_data[key].push(original_data[key][i]);
                        }
                }
            }
            else 
                {
                    for (const key in original_data) 
                        {
                            filtred_data[key].push(original_data[key][i]);
                        }
                }
        }
        
        // Update the source data with the modified data
        source2.data = filtred_data;
        source2.change.emit();
        source.data = kept_data;
        source.change.emit();
        
        
        function linspace(start, stop, num){
            if (isNaN(start) || isNaN(stop)) {
                throw new Error("Invalid start or stop value");
            }
            const step = (stop - start) / (num - 1);
            const arr = [];
            for (let i = 0; i < num; i++) {
                arr.push(start + i * step);
            }
            return arr;
        };
        
        function calculateMean(arr) {
            const sum = arr.reduce((acc, val) => acc + val, 0); // Calculate the sum of array elements
            const mean = sum / arr.length; // Divide the sum by the number of elements to get the mean
            return mean;
        };
        
        
        function linearFit(X, y)
        {
            const n = X.length;
            const XMean = calculateMean(X);
            const yMean = calculateMean(y);

            // Calculate the numerator and denominator of the slope (m) of the line
            let numerator = 0;
            let denominator = 0;
            for (let i = 0; i < n; i++) {
                numerator += (X[i] - XMean) * (y[i] - yMean);
                denominator += (X[i] - XMean) ** 2;
            }
            const x = linspace(Math.min(...X), Math.max(...X), 30);
            const slope = numerator / denominator; // Calculate the slope (m) of the line
            const intercept = yMean - slope * XMean; // Calculate the y-intercept (b) of the line
            const YValues = x.map((val) => slope * val + intercept);
            
            return { slope, intercept,x,YValues};
        };
        
        let fit_data = {};
        let linear_fit = linearFit(kept_data.x,kept_data.y)
        fit_data['x']=linear_fit.x
        fit_data['y']=linear_fit.YValues
        if (legend instanceof Object) {
            var new_text = 'slope : ' + linear_fit.slope.toFixed(5) + ', intercept : ' + linear_fit.intercept.toFixed(3);
            legend.items[0].label = new_text;
        }
        // Update the source data with the modified data
        
        source3.data = fit_data;
        source3.change.emit();
        """)
        
        self.range_slider.js_on_change('value', callback)
        self.checkbox_group.js_on_change('active', callback) 
    
    def filters_tool(self,filters = [('Combo')]):
        self.filters = row()
        
        for filter in filters :                
            if len(filter)==2:
                if filter[0] == 'Checkbox':
                    self.create_checkboxes(**filter[1])
                    self.create_radiocheckbox(**filter[1])
                    self.filters.children.append(column(self.checkbox_group,self.radio_group))
                elif filter[0] == 'Slider' :
                    self.create_slider(**filter[1])
                    self.filters.children.append(self.range_slider)
                elif filter[0] == 'Combo':
                    self.create_combo_filter(**filter[1])
                    self.create_radiocheckbox(**filter[1])
                    self.filters.children.append(row(column(self.checkbox_group),self.radio_group,self.range_slider))
            else :
                if filter == 'Checkbox':
                    self.create_checkboxes()
                    self.create_radiocheckbox()
                    self.filters.children.append(row(self.checkbox_group,self.radio_group))
                elif filter == 'Slider' :
                    self.create_slider()
                    self.filters.children.append(self.range_slider)
                elif filter == 'Combo':
                    self.create_combo_filter()
                    self.create_radiocheckbox()
                    self.filters.children.append(row(column(self.checkbox_group),self.radio_group,self.range_slider))
                
    def plotter(self,plotType='scatter',filters=[('Combo')],title='',axis_xlabel='',axis_ylabel='',linear_fit = False,showGraph=True):
        self.linear_fit = linear_fit

        if plotType == 'scatter':
            self.create_plot(title=title,axis_xlabel=axis_xlabel,axis_ylabel=axis_ylabel)
            self.original_data = dict(self.source.data)
            
            if linear_fit == True:
                self.selection_callback()
            
            if filters != True :
                # self.create_buttons()
                self.filters_tool(filters)
                self.layout = row(self.plot,self.filters)
                if showGraph==True:
                    show(self.layout)
            else :
                self.layout = row(self.plot)
                if showGraph==True:
                    show(self.layout)
                
        elif plotType == 'histogram' :
            self.create_hist(title=title,axis_xlabel=axis_xlabel,axis_ylabel=axis_ylabel)
            self.original_data = dict(self.source.data)
            if filters != False :
                # self.create_buttons()
                self.filters_tool(filters)
                self.layout = row(gridplot([[self.plot, self.plotvertical], [self.plothorizontal, None]], merge_tools=True),self.filters)
                
                if showGraph==True:
                    show(self.layout)
            else :
                self.layout = gridplot([[self.plot, self.plotvertical], [self.plothorizontal, None]], merge_tools=True)
                if showGraph==True:
                    show(self.layout)
 
    def save_as_html(self,path='',filename='default.html'):
        checkFolderAt(path)
    # Save the figure as an HTML file
        if ~path.endswith('/') and path != '':
            path = path+'/'
        if not filename.endswith('.html') :
            filename = filename+'.html'
        checkFolderAt(path)
        save(self.layout, path+filename)
        
    def show(self):
        show(self.layout)

# def FenTSNE(features,
#             burning_times,
#             perplexity = 30,
#             random_state=42,
#             n_iter=1000,
#             thresholds=None,
#             superior=True,
#             edgecolor=None,
#             title=None,
#             path = '/users/divers/atlas/sisaid/home2/output/tsne/default_dir',
#             show= True,
#             save = True,
#             return_values=False):
    
#     tsne = TSNE(n_components=2, perplexity=perplexity, random_state=random_state,n_iter=n_iter)

# # Fit the t-SNE model to the feature data and obtain the lower-dimensional embedding
#     embedding = tsne.fit_transform(features)
    
#     plt.figure(figsize=(15,15)) 
            
#     if thresholds != None and len(thresholds)>1:
#         FenProjectionsThreshold(embedding[:, 0],embedding[:, 1],burning_times, perplexity, thresholds, edgecolor=edgecolor,path=path,superior=superior,title=title,show=show)
#     else :              
#         FenProjections(embedding[:, 0],embedding[:, 1],c=burning_times,edgecolor=edgecolor,vmin = 0 , vmax=burning_times.max() ,cmap='viridis',path=path,title=title,show=show)
        
#     if not show and save :
#         plt.close()
#     else :
#         plt.show()
        
#     if return_values :
#         return embedding[:, 0],embedding[:, 1]

# def FenProjectionsThreshold(embedding_x,
#                             embedding_y,
#                             burning_times,
#                             perplexity,
#                             thresholds,
#                             edgecolor=None,
#                             superior=True,
#                             bins=20,
#                             path ='/users/divers/atlas/sisaid/home2/output/tsne/default_dir',
#                             title=None,
#                             show=False,
#                             save = True):
    
#     plt.figure(figsize=(15,20))
#     for subplot,threshold in enumerate(thresholds) :
#         if subplot == 0 :
#             ax1 = plt.subplot(len(thresholds), 3, 3*subplot  + 1)
#         else :
#             plt.subplot(len(thresholds), 3, 3*subplot  + 1,sharey=ax1,sharex=ax1)
#             plt.setp(ax1.get_xticklabels(), visible=False)
        
#         if superior :
#             x= embedding_x[burning_times>=threshold]
#             y= embedding_y[burning_times>=threshold]
#             c= burning_times[burning_times>=threshold]
#             plt.title(f'superior to {threshold} Hours')
#         else :
#             x= embedding_x[burning_times<=threshold]
#             y= embedding_y[burning_times<=threshold]
#             c= burning_times[burning_times<=threshold]
#             plt.title(f'Inferior to {threshold} Hours')

#         # Plot the lower-dimensional embedding as a scatter plot, using the burning time as color
#         plt.scatter(x,y, c=c,edgecolor=edgecolor,vmin = 0 , vmax=burning_times.max() ,cmap='viridis')
        
#         if subplot == 0 :
#             ax2 = plt.subplot(len(thresholds), 3, 3*subplot  + 2)
#             plt.title(f'Y histogram projection')
#         else :
#             plt.subplot(len(thresholds),3,3*subplot+2,sharey=ax2,sharex=ax2)
#             plt.setp(ax2.get_xticklabels(), visible=False)
        
#         plt.hist(y,bins=bins, orientation='horizontal')
        
#         if subplot == 0:
#             ax3 = plt.subplot(len(thresholds),3,3*subplot+3)
#             plt.title(f'X histogram projection')
#         else :
#             plt.subplot(len(thresholds), 3, 3*subplot  + 3, sharey=ax3,sharex=ax3)
#             plt.setp(ax3.get_xticklabels(), visible=False)
            
#         plt.hist(x, bins=bins, orientation='vertical')
      
#     if title != None :
#         plt.suptitle(f'{title}',fontsize=16)
        
#     cax = plt.axes([0.93, 0.5, 0.03, 0.2])
#     plt.colorbar(cax=cax,orientation='vertical')
#     plt.subplots_adjust(hspace=.0)
    
#     checkFolderAt(path)
#     if save :
#         if title != None :
#             plt.savefig(f'{path}/TSNE_per_burnTime_{title.replace(" ","_")}.jpeg')  
#         else : 
#             plt.savefig(f'{path}/TSNE_per_burnTime_{perplexity}.jpeg')     
    
#     if not show :
#         plt.close()
#     else :
#         plt.show()


# def FenProjections(x,
#                    y,
#                    c=None,
#                    edgecolor=None,
#                    vmin=None,vmax=None,
#                    cmap=None,
#                    path ='/users/divers/atlas/sisaid/home2/output/projections/default_dir',
#                    title=None,
#                    show=False,
#                    save = True):
    
#     fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 3], 'width_ratios': [3, 1]})

#     if len(c)<1 :
#         # plot the scatter plot in the bottom row
#         axes[1, 0].scatter(x, y)
#         axes[1, 0].set_xlabel('X')
#         axes[1, 0].set_ylabel('Y')
#     else :
#         im = axes[1, 0].scatter(x, y, c=c, edgecolor=edgecolor, vmin=vmin, vmax=vmax, cmap=cmap)
#         axes[1, 0].set_xlabel('X')
#         axes[1, 0].set_ylabel('Y')
#         cbar_ax = fig.add_axes([0.85, 0.7, 0.02, 0.2]) # left, bottom, width, height
#         cbar = fig.colorbar(im, cax=cbar_ax, orientation='vertical')
#         cbar.ax.tick_params(labelsize=10)

#     # plot the X projection histogram in the top left
#     axes[0, 0].hist(x, bins=20)
#     axes[0, 0].set_ylabel('Frequency')
#     axes[0, 0].spines['top'].set_visible(False)
#     axes[0, 0].spines['right'].set_visible(False)
#     axes[0, 0].spines['bottom'].set_visible(False)
#     axes[0, 0].spines['left'].set_visible(False)
#     axes[0, 0].tick_params(axis='both', which='both', length=0)
#     axes[0, 0].grid(False)
#     plt.setp(axes[0, 0].get_xticklabels(), visible=False)
#     # plot the Y projection histogram in the top right
#     axes[1, 1].hist(y, bins=20, orientation='horizontal')
#     axes[1, 1].set_xlabel('Frequency')
#     axes[1, 1].spines['top'].set_visible(False)
#     axes[1, 1].spines['right'].set_visible(False)
#     axes[1, 1].spines['bottom'].set_visible(False)
#     axes[1, 1].spines['left'].set_visible(False)
#     axes[1, 1].tick_params(axis='both', which='both', length=0)
#     plt.setp(axes[1, 1].get_yticklabels(), visible=False)
#     axes[1, 1].grid(False)
    
#     axes[0, 1].set_xticks([])
#     axes[0, 1].set_yticks([])
#     axes[0, 1].spines['top'].set_visible(False)
#     axes[0, 1].spines['right'].set_visible(False)
#     axes[0, 1].spines['bottom'].set_visible(False)
#     axes[0, 1].spines['left'].set_visible(False)
#     plt.subplots_adjust(hspace=.0,wspace=.0) 
    
#     checkFolderAt(path)
#     if save :
#         if title != None :
#             plt.suptitle(f'{title}',fontsize=16)
#             plt.savefig(f'{path}/projection_scatter_{title.replace(" ","_")}.jpeg') 
#         else : 
#             plt.savefig(f'{path}/projection_scatter.jpeg')  
    
#     if not show and save :
#         plt.close()
#     else :
#         plt.show()
        
        
