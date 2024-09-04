document.addEventListener("DOMContentLoaded", function() {
    if (typeof d3 === 'undefined') {
        console.error("D3.js library not loaded.");
        return;
    }

    // 选择容器元素
    var container = d3.select("#globe-container");

    // 设置宽度和高度
    var width = 800, height = 800;

    // 创建SVG元素
    var svg = container.append("svg")
        .attr("width", width)
        .attr("height", height);

    // 添加你的D3.js代码，生成3D地球并映射纹理

    // 例如：
    // 创建投影
    var projection = d3.geoOrthographic()
        .scale(300)
        .translate([width / 2, height / 2]);

    // 创建地球路径
    var path = d3.geoPath().projection(projection);

    // 添加地球
    svg.append("path")
        .datum({type: "Sphere"})
        .attr("d", path)
        .style("fill", "lightblue");

    // 继续添加其他D3.js代码，比如拖拽、缩放等功能
});
