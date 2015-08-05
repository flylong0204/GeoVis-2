/// <reference path="weathervislib.d.ts" />
/// <reference path="lodglyphmap.ts" />
/// <reference path="../../../../static/scripts/utility.ts" />
/// <reference path="../../../../static/scripts/functionpanel.ts" />
var WeatherVis;
(function (WeatherVis) {
    var TempVis = (function () {
        function TempVis(divId) {
            this.divId = divId;
            this.lodMapId = divId + 'LodMap';
            var divDom = document.getElementById(divId);
            // construct html dives
            var lodMapDivDom = document.createElement('div');
            var divHtml = "<div class='rendering-div'"
                + "id='" + this.lodMapId + "'>Tool</div>";
            lodMapDivDom.innerHTML = divHtml;
            divDom.appendChild(lodMapDivDom);
            // construct objects
            this.lodMap = new WeatherVis.LODGlyphMap(this.lodMapId, 0, 0, 400, 400);
            this.functionPanel = new GeoVis.FunctionPanel('tool-div');
        }
        TempVis.prototype.render = function () {
        };
        return TempVis;
    })();
    WeatherVis.TempVis = TempVis;
})(WeatherVis || (WeatherVis = {}));
var temp = new WeatherVis.TempVis('map-div');
//# sourceMappingURL=weathervis.js.map