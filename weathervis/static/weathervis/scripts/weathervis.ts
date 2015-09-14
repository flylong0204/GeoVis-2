/// <reference path="weathervislib.d.ts" />
/// <reference path="lodglyphmap.ts" />
/// <reference path="lodparawidget.ts" />


module WeatherVis {
	export class WeatherVisMain {
		private lodMap: LODGlyphMap;
        private newMap1: LODGlyphMap;
        private newMap2: LODGlyphMap;
        private newMap3: LODGlyphMap;

		constructor(private divId: string) {
            this.lodMap = new LODGlyphMap('center-div-board', 100, 100, 400, 300, "1");
            this.newMap1 = new LODGlyphMap('center-div-board', 100, 400, 400, 300, "2");
            this.newMap2 = new LODGlyphMap('center-div-board', 500, 100, 400, 300, "3");
            this.newMap3 = new LODGlyphMap('center-div-board', 500, 400, 400, 300, "4");
		}
        
        updateViews() {
            this.lodMap.loadGlyph();
            this.lodMap.render();
            this.newMap1.loadGlyph();
            this.newMap1.render();
            this.newMap2.loadGlyph();
            this.newMap2.render();
            this.newMap3.loadGlyph();
            this.newMap3.render();
        }
	}
}

var vis = new WeatherVis.WeatherVisMain('center-div');    