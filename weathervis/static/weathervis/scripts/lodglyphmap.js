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
            var _this = this;
            _super.call(this, widgetId, px, py, w, h);
            $(this.contentElement).mouseenter(function () {
                _this.isHoveringContent = true;
            });
            $(this.contentElement).mouseleave(function () {
                _this.isHoveringContent = false;
                console.log('mouse leave');
            });
            // construct svg
            this.svg = d3.select('#' + this.contentDivId)
                .append("svg")
                .attr('id', this.widgetId + '-svg')
                .attr("width", this.w)
                .attr("height", this.h - 27);
            this.currentRenderLevel = 1;
            this.loadMap();
            this.loadGlyph();
        }
        // render the map
        LODGlyphMap.prototype.loadMap = function () {
            var _this = this;
            d3.json('/static/us.json', function (error, data) {
                var topo = topojson.feature(data, data.objects.states);
                _this.jsonData = topo;
                var center = d3.geo.centroid(topo);
                _this.scale = 150;
                _this.projection = d3.geo.mercator().scale(_this.scale).center(center)
                    .translate([_this.w / 2, _this.h / 2]);
                var path = d3.geo.path().projection(_this.projection);
                var bounds = path.bounds(topo);
                var hscale = _this.scale * _this.w / (bounds[1][0] - bounds[0][0]);
                var vscale = _this.scale * _this.h / (bounds[1][1] - bounds[0][1]);
                if (hscale < vscale) {
                    _this.scale = hscale;
                    _this.degreePerPixel = (bounds[1][0] - bounds[0][0]) / _this.w;
                }
                else {
                    _this.scale = vscale;
                    _this.degreePerPixel = (bounds[1][1] - bounds[0][1]) / _this.w;
                }
                _this.currentRenderLevel = Math.round(_this.degreePerPixel * 150 / _this.scale / 1 * 45);
                var newCenter = _this.projection.invert([(bounds[1][0] + bounds[0][0]) / 2, (bounds[1][1] + bounds[0][1]) / 2]);
                ;
                // new projection
                _this.projection = d3.geo.mercator().center(newCenter)
                    .scale(_this.scale).translate([_this.w / 2, _this.h / 2]);
                _this.renderMap();
            });
        };
        LODGlyphMap.prototype.loadGlyph = function () {
            var _this = this;
            var requestStr = '/weathervis/linearOpt?level=' + this.currentRenderLevel + '&a=1&b=0.5&c=0.01';
            d3.json(requestStr, function (error, data) {
                var rawData = JSON.parse(data);
                _this.glyphData = rawData;
                _this.renderGlyph();
            });
        };
        LODGlyphMap.prototype.onMouseDown = function (e) {
            if (this.isHoveringContent) {
                this.isDragging = true;
                var mouseCenter = [e.clientX - this.divDom.offsetLeft, e.clientY - this.divDom.offsetTop];
                this.tempDegreeCenter = this.projection.invert(mouseCenter);
            }
            _super.prototype.onMouseDown.call(this, e);
        };
        LODGlyphMap.prototype.onMouseMove = function (e) {
            if (e.button == 0 && this.isHoveringContent && this.isDragging) {
                var mouseCenter = [e.clientX - this.divDom.offsetLeft, e.clientY - this.divDom.offsetTop];
                console.log(this.isHoveringContent);
                this.projection = d3.geo.mercator().scale(this.scale).center(this.tempDegreeCenter)
                    .translate(mouseCenter);
                this.tempDegreeCenter = this.projection.invert(mouseCenter);
                this.render();
            }
            _super.prototype.onMouseMove.call(this, e);
        };
        LODGlyphMap.prototype.onMouseUp = function (e) {
            _super.prototype.onMouseUp.call(this, e);
        };
        LODGlyphMap.prototype.onWheel = function (e) {
            var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
            var mouseCenter = [this.w / 2, this.h / 2];
            var degreeCenter = this.projection.invert(mouseCenter);
            this.scale = this.scale * (1 + delta * 0.05);
            this.projection = d3.geo.mercator().scale(this.scale).center(degreeCenter)
                .translate(mouseCenter);
            var tempRenderingLevel = Math.round(this.degreePerPixel * 150 / this.scale / 1 * 45);
            if (tempRenderingLevel != this.currentRenderLevel) {
                this.currentRenderLevel = tempRenderingLevel;
                this.loadGlyph();
            }
            this.render();
        };
        LODGlyphMap.prototype.renderMap = function () {
            var path = d3.geo.path().projection(this.projection);
            path = path.projection(this.projection);
            this.svg.selectAll("path").remove();
            this.svg.selectAll("path")
                .data(this.jsonData.features)
                .enter()
                .append("path")
                .attr("d", path);
        };
        LODGlyphMap.prototype.renderGlyph = function () {
            var radiusScale = this.projection([1, 0])[0] - this.projection([0, 0])[0];
            this.svg.selectAll('circle').remove();
            for (var i in this.glyphData) {
                var item = this.glyphData[i];
                this.svg.append('circle')
                    .attr('cx', this.projection([item['lon'], item['lat']])[0])
                    .attr('cy', this.projection([item['lon'], item['lat']])[1])
                    .attr('r', item['r'] * radiusScale)
                    .attr('stroke', 'green')
                    .attr('fill', 'green');
            }
        };
        LODGlyphMap.prototype.render = function () {
            this.renderMap();
            this.renderGlyph();
        };
        return LODGlyphMap;
    })(GeoVis.RenderingBoard);
    WeatherVis.LODGlyphMap = LODGlyphMap;
})(WeatherVis || (WeatherVis = {}));
//# sourceMappingURL=lodglyphmap.js.map