import pandas as pd
import dash
from dash import Dash,callback, dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State
from fuzzywuzzy import fuzz
import json
from polyfuzz import PolyFuzz
from polyfuzz.models import EditDistance,TFIDF



f = open('data.json')
data = json.load(f)

# df = pd.read_csv(
#         'https://gist.githubusercontent.com/chriddyp/'
#         'c78bf172206ce24f77d6363a2d754b59/raw/'
#         'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
#         'usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.loc[:,['first_name','last_name','company_name','address','city','county','state']]])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.loc[:,['first_name','last_name','company_name','address','city','county','state']]
        ]) for i in range(min(len(dataframe), max_rows))]
    )

df=pd.read_csv('us-500.csv')


#df=pd.read_csv('us-500.csv')


app = dash.Dash(__name__)
application = app.server


app.layout = html.Div([
        
    
        html.Div([
        html.H2(children='Denied Party Screening'), 
  dcc.RadioItems(
                id='show-table',
                options=[{'label': i, 'value': i} for i in ['Dynamic', 'Fixed','NLP']],
                #value='Variable',
                labelStyle={'display': 'inline-block'}
            ) ,
  
  


 html.Div( [
    # Create Div to place a conditionally visible element inside
    html.Div( [
        # Create element to hide/show, in this case an 'Input Component'

    html.Div(dcc.Input(id='input-box', type='search',placeholder="Enter FirstName")),
     html.Div(dcc.Slider( id='slider',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),

     html.Div(dcc.Input(id='input-box2', type='search',placeholder="Enter LastName")),
     html.Div(dcc.Slider( id='slider2',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),     
     
     
     html.Div(dcc.Input(id='input-box3', type='search',placeholder="Enter Comapany Name")),
     html.Div(dcc.Slider( id='slider3',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),

     html.Div(dcc.Input(id='input-box4', type='search',placeholder="Enter Address")),
     html.Div(dcc.Slider( id='slider4',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),     

    html.Div(dcc.Input(id='input-box5', type='search',placeholder='Provide City(not mandatory)...')),
    html.Div(dcc.Slider( id='slider5',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),     

    html.Div(dcc.Input(id='input-box6', type='search',placeholder='Provide Country(not mandatory)...')),
    html.Div(dcc.Slider( id='slider6',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),     
    html.Div(dcc.Input(id='input-box7', type='search',placeholder='Provide State(not mandatory)...')),
    html.Div(dcc.Slider( id='slider7',min=0,marks=None,
        max=100,
        step=10,value=50,updatemode='drag', tooltip = { 'always_visible': True })),     

 
 
   
    html.Div([
        html.Button(id='submit-button',                
                children='Submit'
    )
        
    ]),
    
  ], style={'width': '30%','float':'left'}),
        
   html.Div([      
    html.Table(id="table1"),
    
    #dash_table.DataTable(
       # id='table1', data=df.to_dict('records'),
       # columns=[{"name": i, "id": i} for i in df.columns], )
    
   
], style={'width': '68%','float':'right','margin-top': '-83px'}), 

    


        
 

        
 

    ],id = 'div-to-hide2', style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
    ),
 
 
   html.Div( [
    # Create Div to place a conditionally visible element inside
    html.Div( [
        # Create element to hide/show, in this case an 'Input Component'

    html.Div(dcc.Input(id='inputbox', type='search',placeholder="Enter FirstName")),
     html.Div(dcc.Slider( id='slide',min=0,marks=None,
        max=100,
        step=10,value=0,updatemode='drag', tooltip = { 'always_visible': True })),

     html.Div(dcc.Input(id='inputbox2', type='search',placeholder="Enter LastName")),
     html.Div(dcc.Slider( id='slide2',min=0,marks=None,
        max=100,
        step=10,value=0,updatemode='drag', tooltip = { 'always_visible': True })),     
     
     
     html.Div(dcc.Input(id='inputbox3', type='search',placeholder="Enter Comapany Name")),
     html.Div(dcc.Slider( id='slide3',min=0,marks=None,
        max=100,
        step=10,value=0,updatemode='drag', tooltip = { 'always_visible': True })),

     html.Div(dcc.Input(id='inputbox4', type='search',placeholder="Enter Address")),
     html.Div(dcc.Slider( id='slide4',min=0,marks=None,
        max=100,
        step=10,value=0,updatemode='drag', tooltip = { 'always_visible': True })),     

    html.Div(dcc.Input(id='inputbox5', type='search',placeholder='Provide City(not mandatory)...')),
    html.Div(dcc.Slider( id='slide5',min=0,marks=None,
        max=100,
        step=10,value=0,updatemode='drag', tooltip = { 'always_visible': True })),     

    html.Div(dcc.Input(id='inputbox6', type='search',placeholder='Provide Country(not mandatory)...')),
    html.Div(dcc.Slider( id='slide6',min=0,marks=None,
        max=100,
        step=10,value=0,updatemode='drag', tooltip = { 'always_visible': True })),     
   

 
 
   
    html.Div([
        html.Button(id='submit-but3',                
                children='Submit'
    )
        
    ]),
    
  ],id = 'div1', style={'width': '30%','float':'left'}),
        
   html.Div([      
    html.Table(id="table3"),
    
    #dash_table.DataTable(
       # id='table1', data=df.to_dict('records'),
       # columns=[{"name": i, "id": i} for i in df.columns], )
    
   
], style={'width': '68%','float':'right','margin-top': '-83px'}), 

    


        
 
    ],id = 'div-to-hide3', style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
    ), 
  
  
  
       
     html.Div( [
        # Create element to hide/show, in this case an 'Input Component'
     html.Div( [
        # Create element to hide/show, in this case an 'Input Component'
   
    html.Div(dcc.Input(id='input', type='search',placeholder="Enter FirstName")),
 

     html.Div(dcc.Input(id='input2', type='search',placeholder="Enter LastName")),
        
     
     
     html.Div(dcc.Input(id='input3', type='search',placeholder="Enter Comapany Name")),
     

     html.Div(dcc.Input(id='input4', type='search',placeholder="Enter Address")),
         

    html.Div(dcc.Input(id='input5', type='search',placeholder='Provide City(not mandatory)...')),
      

    html.Div(dcc.Input(id='input6', type='search',placeholder='Provide Country(not mandatory)...')),
    
    html.Div(dcc.Input(id='input7', type='search',placeholder='Provide State(not mandatory)...')),
     

 
 
   
    html.Div([
        html.Button(id='submit-but',                
                children='Submit'
    )
        
    ]),
    
  ], style={'width': '30%','float':'left'}),
        
   html.Div([      
    html.Table(id="table2"),
    
    #dash_table.DataTable(
       # id='table1', data=df.to_dict('records'),
       # columns=[{"name": i, "id": i} for i in df.columns], )
    
   
], style={'width': '68%','float':'right','margin-top': '-83px'}), 

    


        
 

     
        
 

    ],id = 'div-to-hide', style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
    )
              
        
     ])

])






@app.callback(Output('table2','children'),
            [Input('submit-but','n_clicks')],
           
            [State('input', 'value')],
            
            [State('input2', 'value')],
           
            [State('input3', 'value')],
           
            [State('input4', 'value')],
            
            [Input('input5','value')],
            
            [Input('input6','value')],
             
            [Input('input7','value')],
            
            
           
            )




def update_datatable1(n_clicks,value2,value3,value4,value5,value6,value7,value8):
    
    
    df=pd.read_csv('us-500.csv')
    #df["name"].replace(',','', regex=True, inplace=True)
    #df["name"].replace("'","", regex=True, inplace=True)
    #df["name"].replace("-","", regex=True, inplace=True)
    

    

          
    if n_clicks:
        
                          
        #return dt.DataTable(data=data, columns=columns)
        if value2 is not None:
            def get_ratio(row):
                name = row['first_name']
                return fuzz.token_sort_ratio(name, value2)
        
            df = df[df.apply(get_ratio, axis=1) > data['fname']]
        
        if value3 is not None:   
            def get_ratio2(row):
                name = row['last_name']
                return fuzz.token_sort_ratio(name, value3)
    
            df = df[df.apply(get_ratio2, axis=1) > data['lname']]
            
        if value4 is not None:
            def get_ratio3(row):
                name = row['company_name']
                return fuzz.token_sort_ratio(name, value4)
    
            df = df[df.apply(get_ratio3, axis=1) > data['cname']]
         
        if value5 is not None:   
            def get_ratio4(row):
                name = row['address']
                return fuzz.token_sort_ratio(name, value5)
    
            df = df[df.apply(get_ratio4, axis=1) > data['add']]
            
        if value6 is not None:   
            def get_ratio5(row):
                name = row['city']
                return fuzz.token_sort_ratio(name, value6)
    
            df = df[df.apply(get_ratio5, axis=1) > data['city']]      

        if value7 is not None:   
            def get_ratio6(row):
                name = row['county']
                return fuzz.token_sort_ratio(name, value7)
    
            df = df[df.apply(get_ratio6, axis=1) > data['country']]    
            
        if value8 is not None:   
            def get_ratio6(row):
                name = row['state']
                return fuzz.token_sort_ratio(name, value8)
    
            df = df[df.apply(get_ratio6, axis=1) > data['state']]                
     
 
        df = df[['first_name','last_name','company_name','address','city','county','state']]            
            
        return generate_table(df)
    


@app.callback(Output('table1','children'),
            [Input('submit-button','n_clicks')],
            [Input('slider','value')],
            [State('input-box', 'value')],
            [Input('slider2','value')],
            [State('input-box2', 'value')],
            [Input('slider3','value')],
            [State('input-box3', 'value')],
            [Input('slider4','value')],
            [State('input-box4', 'value')],
             [Input('slider5','value')],
            [Input('input-box5','value')],
             [Input('slider6','value')],
            [Input('input-box6','value')],
              [Input('slider7','value')],
            [Input('input-box7','value')],
            
            
           
            )




def update_datatable3(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,sd1,dr1,sd2,dr2,sd3,dr3):
    
    
    df=pd.read_csv('us-500.csv')
    #df["name"].replace(',','', regex=True, inplace=True)
    #df["name"].replace("'","", regex=True, inplace=True)
    #df["name"].replace("-","", regex=True, inplace=True)
    

    

          
    if n_clicks:
        
                          
        #return dt.DataTable(data=data, columns=columns)
        if value2 is not None:
            def get_ratio(row):
                name = row['first_name']
                return fuzz.token_sort_ratio(name, value2)
        
            df = df[df.apply(get_ratio, axis=1) > value1]
        
        if value4 is not None:   
            def get_ratio2(row):
                name = row['last_name']
                return fuzz.token_sort_ratio(name, value4)
    
            df = df[df.apply(get_ratio2, axis=1) > value3]
            
        if value6 is not None:
            def get_ratio6(row):
                name = row['company_name']
                return fuzz.token_sort_ratio(name, value6)
    
            df = df[df.apply(get_ratio6, axis=1) > value5]
         
        if value8 is not None:   
            def get_ratio3(row):
                name = row['address']
                return fuzz.token_sort_ratio(name, value8)
    
            df = df[df.apply(get_ratio3, axis=1) > value7]
        
        if dr1 is not None:
            def get_ratio4(row):
                name = row['city']
                return fuzz.token_sort_ratio(name,dr1)
    
            df = df[df.apply(get_ratio4, axis=1) > sd1]
            
        if dr2 is not None:    
            def get_ratio5(row):
                name = row['county']
                return fuzz.token_sort_ratio(name, dr2)
    
            df = df[df.apply(get_ratio5, axis=1) > sd2]            
            
        if dr3 is not None:    
            def get_ratio7(row):
                name = row['state']
                return fuzz.token_sort_ratio(name,dr3)
    
            df = df[df.apply(get_ratio7, axis=1) > sd3]  
            
 
        df = df[['first_name','last_name','company_name','address','city','county','state']]            
            
        return generate_table(df)
    
            

@app.callback(Output('table3','children'),
            [Input('submit-but3','n_clicks')],
            [Input('slide','value')],
            [State('inputbox', 'value')],
            [Input('slide2','value')],
            [State('inputbox2', 'value')],
            [Input('slide3','value')],
            [State('inputbox3', 'value')],
            [Input('slide4','value')],
            [State('inputbox4', 'value')],
             [Input('slide5','value')],
            [Input('inputbox5','value')],
             [Input('slide6','value')],
            [Input('inputbox6','value')],

            
            
           
            )




def update_datatable(n_clicks,value1,value2,value3,value4,value5,value6,value7,value8,sd1,dr1,sd2,dr2):
    
    
    df=pd.read_csv('us-500.csv')
    #df["name"].replace(',','', regex=True, inplace=True)
    #df["name"].replace("'","", regex=True, inplace=True)
    #df["name"].replace("-","", regex=True, inplace=True)
    

    

          
    if n_clicks:
        
        tfidf = TFIDF(min_similarity=0)                 
        #return dt.DataTable(data=data, columns=columns)
        if value2 is not None:
            #str1 = value2
            model = PolyFuzz(tfidf)
            model.match(df.first_name.tolist(),[ str(value2)])
            df1= model.get_matches()
            df2 = pd.concat([df, df1], axis=1)
            df2 = df2[df2['Similarity'] > value1/100]
            df= df2.copy()
            df = df[['first_name','last_name','company_name','address','city','county','state']] 
            df.reset_index(drop=True, inplace=True)
        
        if value4 is not None:   
         
            
            model = PolyFuzz(tfidf)
            model.match(df.last_name.tolist(),[ str(value4)])
            df1= model.get_matches()
            df2 = pd.concat([df, df1], axis=1)
            df2 = df2[df2['Similarity'] > value3/100]
            df= df2.copy()
            df = df[['first_name','last_name','company_name','address','city','county','state']] 
            df.reset_index(drop=True, inplace=True)
            
        if value6 is not None:
            
            
            model = PolyFuzz(tfidf)
            model.match(df.company_name.tolist(),[ str(value6)])
            df1= model.get_matches()
            df2 = pd.concat([df, df1], axis=1)
            df2 = df2[df2['Similarity'] > value5/100]
            df= df2.copy()
            df = df[['first_name','last_name','company_name','address','city','county','state']] 
            df.reset_index(drop=True, inplace=True)
            
        if value8 is not None:   
           
            
            model = PolyFuzz(tfidf)
            model.match(df.address.tolist(),[ str(value8)])
            df1= model.get_matches()
            df2 = pd.concat([df, df1], axis=1)
            df2 = df2[df2['Similarity'] > value7/100]
            df= df2.copy()
            df = df[['first_name','last_name','company_name','address','city','county','state']] 
            df.reset_index(drop=True, inplace=True)
        
        if dr1 is not None:
           
            model = PolyFuzz(tfidf)
            model.match(df.city.tolist(),[ str(dr1)])
            df1= model.get_matches()
            df2 = pd.concat([df, df1], axis=1)
            df2 = df2[df2['Similarity'] > sd1/100]
            df= df2.copy()
            df = df[['first_name','last_name','company_name','address','city','county','state']] 
            df.reset_index(drop=True, inplace=True)
            
        if dr2 is not None:    
           
            model = PolyFuzz(tfidf)
            model.match(df.county.tolist(),[ str(dr2)])
            df1= model.get_matches()
            df2 = pd.concat([df, df1], axis=1)
            df2 = df2[df2['Similarity'] > sd2/100]
            df= df2.copy()
            df = df[['first_name','last_name','company_name','address','city','county','state']] 
            df.reset_index(drop=True, inplace=True)   
            
 
            
 
        df = df[['first_name','last_name','company_name','address','city','county','state']]            
            
        return generate_table(df)   
            


@app.callback(
   Output( component_id='div-to-hide', component_property='style'),


 
   [Input(component_id='show-table', component_property='value')])
   
def toggle_container(toggle_value):
    print(toggle_value, flush=True)
    if toggle_value == 'Fixed':
        return {'display': 'block'}
    else:
        return {'display': 'none'} 
    
@app.callback(
   Output( component_id='div-to-hide2', component_property='style'),


 
   [Input(component_id='show-table', component_property='value')])
   



def toggle_container2(toggle_value):
    print(toggle_value, flush=True)
    if toggle_value == 'Dynamic':
        return {'display': 'block'}
    else:
        return {'display': 'none'} 
     

@app.callback(
   Output( component_id='div-to-hide3', component_property='style'),


 
   [Input(component_id='show-table', component_property='value')])
   
def toggle_container3(toggle_value):
    print(toggle_value, flush=True)
    if toggle_value == 'NLP':
        return {'display': 'block'}
    else:
        return {'display': 'none'}      





if __name__ == '__main__':
    application.run()