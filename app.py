from dash import dash, dash_table
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__)

df = pd.read_csv('C:/Users/joseg/PycharmProjects/Dashboards Interativos com Python/RID_DM_peso_familia_410750_WRAccAND_sim0.4k10ks2.csv')

# Criando o gráfico de barras com a relação entre Dp e Dn
figura_Dp_Dn = go.Figure(
    data=[
        go.Bar(
            x=[0],
            y=[df['Dp'][0]],
            text=[f'{df["Dp"][0]}'],
            textposition='auto',
            name='Com baixo peso'
        ),
        go.Bar(
            x=[1],
            y=[df['Dn'][0]],
            text=[f'{df["Dn"][0]}'],
            textposition='auto',
            name='Sem baixo peso',
            marker=dict(color=['#4252DD'])
        )
    ]
)
figura_Dp_Dn.update_layout(title_text='Total de exemplos da cidade')
figura_Dp_Dn.update_yaxes(title_text='Número de crianças')
figura_Dp_Dn.update_xaxes(tickvals=[0, 1], ticktext=['Com baixo peso', 'Sem baixo peso']),
######################################################################


# Total de exemplos na base de dados do subgrupo
@app.callback(
    Output('exemplos_subgrupo_bar', 'figure'),
    [Input('id-dropdown', 'value')]
)
def exemplos_subgrupo_bar(selected_id):
    selected_row = df.loc[df['id'] == selected_id]
    tp = selected_row['TP'].values[0]
    fp = selected_row['FP'].values[0]

    figura_Tp_Fp = go.Figure(
        data=[
            go.Bar(
                x=['TP'],
                y=[tp],
                text=[f'{tp}'],
                textposition='auto',
                name='',
                marker=dict(color=['#7D8AFF'])
            ),
            go.Bar(
                x=['FP'],
                y=[fp],
                text=[f'{fp}'],
                textposition='auto',
                name='',
                marker=dict(color=['#4252DD'])
            )
        ]
    )
    figura_Tp_Fp.update_layout(title_text='Total de exemplos no subgrupo', barmode='group')
    figura_Tp_Fp.update_yaxes(title_text='Número de crianças')
    figura_Tp_Fp.update_xaxes(tickvals=[0, 1], ticktext=['Com baixo peso', 'Sem baixo peso'])

    return figura_Tp_Fp

######################################################################

# Tabela de descrição dos subgrupos

# Criando um DataFrame com as descrições dos subgrupos geral
subgroups_df = df[df['alvo'] == 's'][['id', 'Dp', 'Dn', 'D', 'FP', 'lift']]

table_descricao_subgrupos = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in subgroups_df.columns],
    data=subgroups_df.to_dict('records'),
    style_table={'overflowY': 'auto', 'maxHeight': '300px', 'width': '600px'},
)
######################################################################


# Tabela de descrição dos subgrupos individual
@app.callback(
    Output('desc-output', 'children'),
    [Input('id-dropdown', 'value')]
)
def update_output(selected_id):
    selected_desc = df.loc[df['id'] == selected_id, 'desc'].values[0]
    selected_desc = (selected_desc
                     .replace("=", ": ")
                     .replace("_", " ")
                     .replace("cod ", "")
                     .replace(': s', ': Sim')
                     .replace(': n', ': Não')
                     .replace('female', 'Feminino')
                     .replace('age', 'Idade')
                     .replace('qtd', 'Quantidade')
                     .replace('Son/daughter', 'Filho/Filha')
                     .replace('redepublica', 'Rede Pública')
                     .title()
                     .split("@"))
    desc_df = pd.DataFrame(selected_desc, columns=['Descrição:'])
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in desc_df.columns],
        data=desc_df.to_dict('records'),
        style_table={'overflowY': 'auto', 'maxHeight': 'auto'},
        style_cell={'textAlign': 'left'}
    )
######################################################################


# Texto com porcentagem de crianças com baixo peso na cidade
@app.callback(
    Output('porcentage_cidade_output', 'children'),
    [Input('id-dropdown', 'value')]
)
def update_percentage_text(selected_id):
    selected_row = df.loc[df['id'] == selected_id]
    percentage = (selected_row['Dp'] / selected_row['D']) * 100
    return [html.Span(f'A ', className='text-normal'),
            html.Span('cidade de nome_cidade teve', className='text-highlight'),
            html.Br(),
            html.Span(f'uma taxa de ', className='text-taxa'),
            html.Br(),
            html.Span(f'{percentage.values[0]:.2f}%', className='text-percentage'),
            html.Br(),
            html.Span('de crianças com ', className='text-normal'),
            html.Span('baixo peso', className='text-BPN'),
            html.Br(),
            html.Span(f'ao nascer (BPN)', className='text-BPN2')]
######################################################################


# Texto mostrando o valor de lift do subgrupo
@app.callback(
    Output('lift-text-output', 'children'),
    [Input('id-dropdown', 'value')]
)
def update_lift_text(selected_id):
    selected_lift = df.loc[df['id'] == selected_id, 'lift'].values[0]
    return [html.Span('As crianças deste ', className='text-normal-lift'),
            html.Span('subgrupo', className='text-highlight-lift'),
            html.Br(),
            html.Span(f'tiveram uma taxa de ', className='text-normal-lift-center'),
            html.Br(),
            html.Span(f'{selected_lift*100:.2f}%', className='text-percentage'),
            html.Br(),
            html.Span('de chance ter ', className='text-normal-lift'),
            html.Span('Baixo Peso ', className='text-highlight-lift'),
            html.Br(),
            html.Span('Ao Nascer (BPN)', className='text-highlight-lift-center'),
    ]
######################################################################


# Mostrar texto com o valor do suporte
@app.callback(
    Output('supp-text-output', 'children'),
    [Input('id-dropdown', 'value')]
)
def update_supp_text(selected_id):
    selected_supp = df.loc[df['id'] == selected_id, 'SUPP'].values[0]
    return f'Valor de SUPP para o ID {selected_id}: {selected_supp}'
######################################################################


# Layout do app
app.layout = html.Div(id="div1", children=[

    # Adicionando o título
    html.H1(children='Análise de Baixo Peso ao Nascer (BPN)', id="h1", className='text-title'),

    # Adicionando o título dos subgrupos
    html.H2(children='Subgrupos desta cidade:'),

    html.Div(id='Tabela-texto-explicativo', children=[
        # Adicionando a tabela de descrição dos subgrupos
        table_descricao_subgrupos,

        #  Texto explicativo sobre o BPN
        html.Plaintext(children='O baixo peso ao nascer, definido como um peso inferior a 2.500 gramas,\n'
                                'é um problema de saúde pública que afeta milhões de bebês em todo o mundo. \n'
                                'Essa condição está associada a diversos fatores de risco, tanto para a mãe\n'
                                'quanto para o bebê, e pode ter consequências graves a curto e longo prazo.\n \n'
                                ' Este dashboard tem como objetivo auxiliar na compreensão do caso brasileiro \n'
                                'de baixo peso ao nascer, utilizando um algoritmo de mineração de subgrupos nas\n'
                                'bases de dados do SINASC (Sistema de Informação sobre Nascidos Vivos) e CADU \n'
                                '(Cadastro Único de Programas Sociais).', className='text-intro'),
    ], style={'display': 'flex'}),

    html.Div(id="Graficos-cidade", children=[
            # Adicionando o gráfico de Total de exemplos na base de dados
            dcc.Graph(id='Relação de numero de exemplos da base', figure=figura_Dp_Dn,  style={'margin-left': '120px', 'margin-top': '30px', 'width': '800px', 'height': '400px'}),
            # Texto com porcentagem de crianças com baixo peso na cidade
            html.Div(id='porcentage_cidade_output', style={'margin-left': '60px', 'margin-top': '80px'}),
        ], style={'display': 'flex'}),

    html.Div(style={'border-top': '3px solid black', 'height': '1px', 'margin': '20px 0'}),


    # Titulo para o dash board dos subgrupos individuais
    html.H1(children='Análise por Subgrupo', id="h1", className='text-title'),

    html.Label('Selecione ou digite o ID do subgrupo:', style={"font-size": "20px"}),
        dcc.Dropdown(
            id='id-dropdown',
            options=[{'label': str(id_value), 'value': id_value} for id_value in df['id'].unique()],
            value=df['id'].unique()[0],
            style={"margin-bottom": "25px"},
        ),


    html.Div(id="Graficos-subgrupo", children=[
        # Adicionando a tabela de descrição dos subgrupos individual
        html.Div(id='desc-output', style={"margin-bottom": "25px", 'width': '600px'}, className='tabela-descricao', ),

        # Adicionando o gráfico de barras com a relação entre TP e FP absolutos
        dcc.Graph(id='exemplos_subgrupo_bar', figure=figura_Dp_Dn, style={'width': '700px', 'height': '500px'}),

        # Texto mostrando o valor de lift do subgrupo
        html.Div(id='lift-text-output', style={'margin-top': '60px'}),

    ], style={'display': 'flex'}),
])

if __name__ == '__main__':
    app.run_server(debug=True)
