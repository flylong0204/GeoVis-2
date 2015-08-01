/// <reference path="weathervislib.d.ts" />

/// <reference path="lodglyphmap.ts" />


module WeatherVis {
	export class TempVis {
		private lodMapId: string;
		private lodMap: LODGlyphMap;

		constructor(private divId: string) {
			this.lodMapId = divId + 'LodMap';
			// construct html dives
			d3.select('#' + divId).append('div')
				.attr('id', this.lodMapId)
				.attr('width', '400px')
				.attr('height', '400px');

			// construct objects
			this.lodMap = new LODGlyphMap(this.lodMapId);
		}

		render() {
			
		}
	}
}

var temp = new WeatherVis.TempVis('map_div');