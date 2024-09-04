import dash
from dash import html
from dash.dependencies import Input, Output

external_css = ['https://cesium.com/downloads/cesiumjs/releases/1.76/Build/Cesium/Widgets/widgets.css']
external_scripts = [{'src':'https://cesium.com/downloads/cesiumjs/releases/1.76/Build/Cesium/Cesium.js'}]

app = dash.Dash(__name__, 
                title='Cesium Earth Viewer with 2D Texture',
                external_scripts=external_scripts,
                external_stylesheets=external_css)

app.layout = html.Div(id='blah',
                      children=[
                          'Cesium Earth Viewer...',
                          html.Div(id='cesiumContainer', style={'height': '600px', 'width': '100%'})
                      ])

app.clientside_callback(
    '''
    function(id) {
        Cesium.Ion.defaultAccessToken = "your_access_token";  // 如果你有Cesium Ion的令牌可以在此处替换
        var viewer = new Cesium.Viewer(id, {
            imageryProvider: new Cesium.SingleTileImageryProvider({
                url : '/assets/sticklmgs/00010.png'  // 假设图片位于/assets/目录下
            }),
            baseLayerPicker: false,
            timeline: false,
            animation: false
        });
        viewer.scene.globe.enableLighting = false;
        return true;
    }
    ''',
    Output('cesiumContainer', 'data-done'),
    Input('cesiumContainer', 'id')
)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
