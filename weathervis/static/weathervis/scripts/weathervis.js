/// <reference path="weathervislib.d.ts" />
/// <reference path="lodglyphmap.ts" />
var WeatherVis;
(function (WeatherVis) {
    var TempVis = (function () {
        function TempVis(divId) {
            this.divId = divId;
            this.lodMapId = divId + 'LodMap';
            // construct html dives
            d3.select('#' + divId).append('div')
                .attr('id', this.lodMapId)
                .attr('width', '400px')
                .attr('height', '400px');
            // construct objects
            this.lodMap = new WeatherVis.LODGlyphMap(this.lodMapId);
        }
        TempVis.prototype.render = function () {
        };
        return TempVis;
    })();
    WeatherVis.TempVis = TempVis;
})(WeatherVis || (WeatherVis = {}));
var temp = new WeatherVis.TempVis('map_div');
//# sourceMappingURL=weathervis.js.map