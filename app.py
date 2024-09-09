# Import packages
import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html,callback,ALL,MATCH
from dash import dash_table
from collections import OrderedDict
import dash_mantine_components as dmc
from flask import Flask,redirect, url_for
from dash_iconify import DashIconify

server = Flask(__name__)
#dash mantine组件需要react18以上
dash._dash_renderer._set_react_version('18.2.0')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]+dmc.styles.ALL,suppress_callback_exceptions=True,use_pages=True)
application = app.server

#PLOTLY_LOGO = "/assets/cdem_icon.png"

headbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="80px",id='icon_img'),className="ms-2"),
                        # dbc.Col(dbc.NavbarBrand("cdem", className="ms-2")),
                        dmc.ActionIcon(
                            DashIconify(id='sidebar-btn-icon',icon="icon-park-outline:menu-unfold-one", width=20),
                            variant="transparent",
                            id="sidebar-btn",
                            className="sidebar-btn",
                            color='#aaa',
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            )
        ],
        style={
            "padding":"0",
            "justify-content": "space-around"
        }
    ),
    color="var(--sidebarColor)",
    dark=True,
    className='header'
)

nav_config=[
    {
        "title":"首页",
        "relative_path":'/',
        "icon":"carbon:home",
        "icon_color":"yellowgreen"
    },
    {
        "title":"新建作业",
        "relative_path":'/addnew',
        "icon":"mdi:invoice-text-new-outline",
        "icon_color":"coral"
    },
    {
        "title":"我的作业",
        "relative_path":'/homeworkpage',
        "icon":"bi:person-workspace",
        "icon_color":"darkturquoise"
    },
    # {
    #     "title":"后处理测试",
    #     "relative_path":'/postprocess',
    #     "icon":"bi:person-workspace",
    #     "icon_color":"darkturquoise"
    # }
]

def NavList(fold=False):
    if fold:
        return [
            dbc.NavLink(
                [
                    html.Div([DashIconify(icon=page['icon'],color=page["icon_color"],height=25,style={"margin":"auto"})],
                        title=page["title"],
                        style={
                            "display":"flex"
                        }
                        )
                    # page["title"]
                ], 
                href=page["relative_path"], 
                active="exact",
                id={"type":'page',"page":page["title"]}
            ) for page in nav_config
        ]
    else:
        return [
                dbc.NavLink(
                    [
                        DashIconify(icon=page['icon'],color=page["icon_color"],height=25,style={"marginRight":"1rem","marginLeft":"0.5rem"}),
                        html.Span(page["title"])
                    ], 
                    href=page["relative_path"], 
                    active="exact",
                    id={"type":'page',"page":page["title"]}
                ) for page in nav_config
            ]

sidebar = html.Div(
    [
        headbar,
        dbc.Nav(
            NavList(),
            id='Navlist',
            vertical=True,
            pills=True,
        )
    ],
    id='sidebar',
    # style=SIDEBAR_STYLE,
    className="sidebar"
)

subheader=dbc.Navbar(
    dbc.Container(
        [
            dmc.Breadcrumbs(
                id='breadcrumbs',
                children=[
                    dcc.Link("首页", href="/"),
                ],
            ),
        ]
    ),
    id='Navbar',
    className='Navbar'
)
content = html.Div([
    dash.page_container],id="page-content", className='content')

app.layout = dmc.MantineProvider(html.Div([dcc.Location(id="url"),sidebar,content]))


# @callback(
#     Output('breadcrumbs','children'),
#     Input('url','pathname')
# )
# def update_breadcrumbs(path):
#     print(path)
#     for page in dash.page_registry.values():
#         if page['path']==path and path!='/':
#             return [
#                 dcc.Link("首页", href="/"),
#                 dcc.Link(page['title'], href=page['path'])
#             ]
#     return [
#         dcc.Link("首页", href="/"),
#     ]


#折叠样式回调
@callback(
    Output('sidebar-btn','children'),
    Output('sidebar-btn','className'),
    Output('sidebar','className'),
    # Output('Navbar','className'),
    Output('page-content','className'),
    Output('Navlist','children'),
    Output('icon_img','height'),
    Input('sidebar-btn',"n_clicks"),
    prevent_initial_call=True
)
def clickfold(n_clicks):
    if n_clicks%2==0:
        icon=DashIconify(id='sidebar-btn-icon',icon="icon-park-outline:menu-unfold-one", width=20)
        return icon,'sidebar-btn','sidebar','content',NavList(),'80px'
    else:
        icon=DashIconify(id='sidebar-btn-icon',icon="icon-park-outline:menu-fold-one", width=20)
        return icon,'sidebar-btn-fold','sidebar_fold','content_fold',NavList(True),'50px'



# Run the app
if __name__ == '__main__':
    app.run(debug=True)