/// <reference path="weathervislib.d.ts" />


module WeatherVis {
	export class LODGlyphMap {
		constructor(private divId: string) {
			var dataset = [ 5, 10, 13, 19, 21, 25, 22, 18, 15, 13, 11, 12, 15, 20, 18, 17, 16, 18, 23, 25 ];
			var w = 500;
var h = 100;
var svg = d3.select('#' + divId)
.append("svg")
.attr("width", w)
.attr("height", h);
svg.selectAll("rect")
.data(dataset)
.enter()
.append("rect")
.attr("x", 0)
.attr("y", 0)
.attr("width", 20)
.attr("height", 100);
		}

		loadMap() {
				
		}

		loadGlyph() {

		}
	}
}