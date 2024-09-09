import dash
from dash import html, dcc  # Updated import here
import dash_bootstrap_components as dbc
import feffery_antd_components as fac

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def build_menu():
    menu_items = [
        {
            'component': 'SubMenu',
            'props': {'key': f'{sub_menu}', 'title': f'子菜单{sub_menu}'},
            'children': [
                {
                    'component': 'ItemGroup',
                    'props': {
                        'key': f'{sub_menu}-{item_group}',
                        'title': f'菜单项分组{sub_menu}-{item_group}',
                    },
                    'children': [
                        {
                            'component': 'Item',
                            'props': {
                                'key': f'{sub_menu}-{item_group}-{item}',
                                'title': f'菜单项{sub_menu}-{item_group}-{item}',
                            }
                        }
                        for item in range(1, 3)
                    ]
                }
                for item_group in range(1, 3)
            ]
        }
        for sub_menu in range(1, 5)
    ]
    return fac.AntdMenu(
        menuItems=menu_items,
        mode='inline',
        theme='dark',
        style={'width': '100%', 'height': '100%'}
    )

def render_images():
    demo_contents = [
        fac.AntdDivider('', innerTextOrientation='left'),
        fac.AntdImage(
            src=[f'/assets/image/icon{i}.png' for i in range(1, 9)],
            multiImageMode='unfold',
            height=550,
        ),
    ]
    return html.Div(demo_contents)

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1("页面标题", className="text-center py-3"), width=12), style={'backgroundColor': '#f8f9fa'}),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                # Left half for the menu
                dbc.Col(build_menu(), width=8, style={'height': '90vh', 'overflow': 'auto'}),
                
                # Right half for additional content
                dbc.Col(html.Div("其他内容区域预留", id="other-content"), width=2, style={'height': '90vh'})
            ]),
        ], width=3),

        # Main content area
        dbc.Col([
            render_images()  # Insert the image demo here
        ], width=9)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
