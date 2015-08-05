/// <reference path="weathervislib.d.ts" />
/// <reference path="../../../../static/scripts/renderingboard.ts" />
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var WeatherVis;
(function (WeatherVis) {
    var UnGlyph = (function () {
        function UnGlyph() {
        }
        return UnGlyph;
    })();
    WeatherVis.UnGlyph = UnGlyph;
    var LODGlyphMap = (function (_super) {
        __extends(LODGlyphMap, _super);
        function LODGlyphMap(widgetId, px, py, w, h) {
            _super.call(this, widgetId, px, py, w, h);
            this.divDom = document.getElementById(widgetId);
            GeoVis.Utility.eventMapper.registerEvent(this.widgetId, this);
            this.loadMap();
        }
        // render the map
        LODGlyphMap.prototype.loadMap = function () {
            var svg = d3.select('#' + this.widgetId)
                .append("svg")
                .attr("width", this.w)
                .attr("height", this.h);
            d3.json('/static/us-10m.json', function (data) {
                var topo = topojson.feature(data, data.objects.states);
                var prj = d3.geo.mercator();
                var path = d3.geo.path().projection(prj);
                svg.selectAll("path").data(topo.features).enter().append("path").attr("d", path);
            });
        };
        // render the glyph
        LODGlyphMap.prototype.updateGlyph = function (value) {
        };
        return LODGlyphMap;
    })(GeoVis.RenderingBoard);
    WeatherVis.LODGlyphMap = LODGlyphMap;
})(WeatherVis || (WeatherVis = {}));
//# sourceMappingURL=lodglyphmap.js.map