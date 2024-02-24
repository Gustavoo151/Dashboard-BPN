from dash import dash, dash_table
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

app = dash.Dash(__name__)

df = pd.read_csv('C:/Users\joseg\PycharmProjects\Dashboards Interativos com Python/testeCSVAlterado.csv')

# Criando o gráfico de barras com a relação entre Dp e Dn
figura_Dp_Dn = go.Figure(
    data=[
        go.Bar(
            x=[0],
            y=[df['Dp'][0]],
            text=[f'{df["Dp"][0]}'],
            textposition='auto',
            name='Com baixo peso',
            marker=dict(color=['#7D8AFF'])
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
figura_Dp_Dn.update_layout(title_text='Total de exemplos na base de dados')
figura_Dp_Dn.update_yaxes(title_text='Número de crianças')
figura_Dp_Dn.update_xaxes(tickvals=[0, 1], ticktext=['Com baixo peso', 'Sem baixo peso'])
######################################################################

# Tabela de descrição dos subgrupos

# Criando um DataFrame com as descrições dos subgrupos
subgroups_df = df[['A', 'I', 'SUPP', 'itemDom', 'desc', 'FP', 'quali', 'lift', 'conf', 'cov', 'chi', 'pvalue', 'sup_p',]]

table_descricao_subgrupos = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in subgroups_df.columns],
    data=subgroups_df.to_dict('records'),
)


######################################################################

app.layout = html.Div(id="div1", children=[
    # Adicionando o título
    html.H1(children='Análise de Peso Baixo ao Nascer (BPN)', id="h1"),

    html.Label('Mostrar Alvos do Dataset:'),
    dcc.Dropdown(
        options=[
            {'label': 'Sim', 'value': 's'},
            {'label': 'Não', 'value': 'n'},
        ],
        value='s', style={"margin-bottm": "25px"}
    ),

    html.Label('Selecione um ID:'),
    dcc.Dropdown(
        id='id-dropdown',
        options=[{'label': str(id_value), 'value': id_value} for id_value in df['id'].unique()],
        value=df['id'].unique()[0],
        style={"margin-bottom": "25px"}
    ),

    html.Div(id='desc-output', style={"margin-bottom": "25px"}),

    # Adicionando a tabela de descrição dos subgrupos
    table_descricao_subgrupos

    # Adicionando o gráfico de Total de exemplos na base de dados
    dcc.Graph(id='Relação de numero de exemplos da base', figure=figura_Dp_Dn),


])


@app.callback(
    Output('datatable', 'data'),
    [Input('alvo-dropdown', 'value')]
)
def update_table(selected_alvo):
    if selected_alvo == 'all':
        return df.drop(
            ['A', 'I', 'SUPP', 'itemDom', 'desc', 'FP', 'quali', 'lift', 'conf', 'cov', 'chi', 'pvalue', 'sup_p',
             'sup_n'
             ], axis=1).to_dict('records')
    else:
        filtered_df = df[df['alvo'] == selected_alvo]
        return filtered_df.drop(['desc', 'itemDom'], axis=1).to_dict('records')


@app.callback(
    Output('desc-output', 'children'),
    [Input('id-dropdown', 'value')]
)
def update_output(selected_id):
    selected_desc = df.loc[df['id'] == selected_id, 'desc'].values[0]
    return f'Descrição para o ID {selected_id}: {selected_desc}'


if __name__ == '__main__':
    app.run_server(debug=True)
