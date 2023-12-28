import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table
from dash.dash_table.Format import Group

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  # Aqui vai ser meu CSS

app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)  # Aqui vai ser meu app (Dash

pf = pd.DataFrame({  # Aqui vai ser meu dataFrame
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df = pd.read_csv('C:/Users\joseg\PycharmProjects\Dashboards Interativos com Python/testeCSVAlterado.csv')


fig2 = px.bar(df, x="id", y="lift", color="quali", title="Análise de Lift, Qualidade e Confiança por Entrada")


# ======================================================================================================================
# Layout

# O app.layout é o que vai ser renderizado na tela
app.layout = dash.html.Div(id ="div1",
    children=[  # O Children é o que vai ser renderizado dentro do app.layout
        dash.html.H1(children='Dash Board Análise de Baixo Peso ao Nascer', id="h1"),  # Aqui vai ser meu titulo

        html.Label('Selecione um ID:'),
        dcc.Dropdown(
            id='id-dropdown',
            options=[{'label': str(id_value), 'value': id_value} for id_value in df['id'].unique()],
            value=df['id'].unique()[0],  # Valor inicial do dropdown
            style={"margin-bottom": "25px"}
        ),

        html.Div(id='desc-output', style={"margin-bottom": "25px"}),

        dcc.Graph(  # Aqui vai ser meu grafico
            id='graph2',
            figure=fig2
        ),




        html.Label('Mostrar Alvos do Dataset:'),
        dcc.Dropdown(
            options=[
                {'label': 'Sim', 'value': 's'},  # Aqui vai ser meu dropdown
                {'label': 'Não', 'value': 'n'},
            ],
            value='s', style={"margin-bottm": "25px"} # Aqui vai ser o valor inicial do meu dropdown
        ),
        dash_table.DataTable(
            id='datatable',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df[df['alvo'] == 's'].to_dict('records'),  # Inicialmente, exibe os dados para 'Sim'
        ), # Aqui vai ser meu grafico com base no dropdown e selecionando o alvo




    ]
)

# Callback para atualizar a tabela com base na seleção do dropdown
@app.callback(
    Output('datatable', 'data'),
    [Input('alvo-dropdown', 'value')]
)
def update_table(selected_alvo):
    if selected_alvo == 'all':
        return df.to_dict('records')
    else:
        filtered_df = df[df['alvo'] == selected_alvo]
        return filtered_df.to_dict('records')


# Callback para atualizar o conteúdo com base no ID selecionado
@app.callback(
    Output('desc-output', 'children'),
    [Input('id-dropdown', 'value')]
)
def update_output(selected_id):
    selected_desc = df.loc[df['id'] == selected_id, 'desc'].values[0]
    return f'Descrição para o ID {selected_id}: {selected_desc}'


# ======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True)


# Para executar o programa, digite no terminal: python app.py