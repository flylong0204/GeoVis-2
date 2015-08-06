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
            
            this.loadMask();
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
        
        loadMask() {
            d3.json('http://127.0.0.1:8000/geovismain/datavalue?', (error: any, data: any) => {                
                var canvas = document.createElement('canvas');
                canvas.setAttribute('width', '200');
                canvas.setAttribute('height', '200');
                canvas.setAttribute('id', 'testcanvas');
                var pdom = document.getElementById(this.widgetId);
                pdom.appendChild(canvas);
                var c: any = document.getElementById('testcanvas');
                var ctx: any = c.getContext('2d');
                
                ctx.fillStyle = '#FF0000';
                ctx.fillRect(0, 0, 150, 70);
            }); 
        }
	}
}