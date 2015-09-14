/// <reference path="weathervislib.d.ts" />
/// <reference path="lodglyphmap.ts" />
/// <reference path="lodparawidget.ts" />
var WeatherVis;
(function (WeatherVis) {
    var WeatherVisMain = (function () {
        function WeatherVisMain(divId) {
            this.divId = divId;
            this.lodMap = new WeatherVis.LODGlyphMap('center-div-board', 100, 100, 400, 300, "1");
            this.newMap1 = new WeatherVis.LODGlyphMap('center-div-board', 100, 400, 400, 300, "2");
            this.newMap2 = new WeatherVis.LODGlyphMap('center-div-board', 500, 100, 400, 300, "3");
            this.newMap3 = new WeatherVis.LODGlyphMap('center-div-board', 500, 400, 400, 300, "4");
        }
        WeatherVisMain.prototype.updateViews = function () {
            this.lodMap.loadGlyph();
            this.lodMap.render();
            this.newMap1.loadGlyph();
            this.newMap1.render();
            this.newMap2.loadGlyph();
            this.newMap2.render();
            this.newMap3.loadGlyph();
            this.newMap3.render();
        };
        return WeatherVisMain;
    })();
    WeatherVis.WeatherVisMain = WeatherVisMain;
})(WeatherVis || (WeatherVis = {}));
var vis = new WeatherVis.WeatherVisMain('center-div');
//# sourceMappingURL=weathervis.js.map