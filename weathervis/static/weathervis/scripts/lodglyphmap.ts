/// <reference path="weathervislib.d.ts" />
/// <reference path="../../../../static/scripts/renderingboard.ts" />

declare var topojson: any;

module WeatherVis {
	export class UnGlyph {
		value: number;
		lon: number;
		lat: number;
	}

	export class LODGlyphMap extends GeoVis.RenderingBoard {
		constructor(widgetId: string, px: number, py: number, w: number, h: number) {
            super(widgetId, px, py, w, h);
            
            this.divDom = document.getElementById(widgetId);
            GeoVis.Utility.eventMapper.registerEvent(this.widgetId, this);
            
            this.loadMap();
		}

		// render the map
		loadMap() {
			var svg = d3.select('#' + this.widgetId)
                .append("svg")
                .attr("width", this.w)
                .attr("height", this.h);
            
            d3.json('/static/us-10m.json', function(data) {                
                var topo = topojson.feature(data, data.objects.states);
                var prj = d3.geo.mercator();
                var path = d3.geo.path().projection(prj);
                svg.selectAll("path").data(topo.features).enter().append("path").attr("d", path);
            });
		}

		// render the glyph
		updateGlyph(value: UnGlyph[]) {
			
		}
	}
}