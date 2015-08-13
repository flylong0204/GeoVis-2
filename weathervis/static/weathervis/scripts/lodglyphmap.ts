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
        protected scale: number;
        protected projection: any;
        protected jsonData: any;
        protected glyphData: any;
        protected svg: any;
        protected tempDegreeCenter: [number, number];
        protected currentRenderLevel: number;
        
		constructor(widgetId: string, px: number, py: number, 
            w: number, h: number) {
            super(widgetId, px, py, w, h);
            
            $(this.contentElement).mouseenter(() => {
                this.isHoveringContent = true;
            });
            
            $(this.contentElement).mouseleave(() => {
                this.isHoveringContent = false;
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
		loadMap() {
            d3.json('/static/us.json', (error: any, data: any) => {                
                var topo = topojson.feature(data, data.objects.states);
                this.jsonData = topo;               
                
                var center = d3.geo.centroid(topo);
                this.scale = 150;
                this.projection = d3.geo.mercator().scale(this.scale).center(center)
                                    .translate([this.w / 2, this.h / 2]);
                var path = d3.geo.path().projection(this.projection);
                var bounds  = path.bounds(topo);
                var hscale  = this.scale * this.w  / (bounds[1][0] - bounds[0][0]);
                var vscale  = this.scale * this.h / (bounds[1][1] - bounds[0][1]);
                this.scale   = (hscale < vscale) ? hscale : vscale;
                var newCenter = this.projection.invert([(bounds[1][0] + bounds[0][0]) / 2, (bounds[1][1] + bounds[0][1]) / 2]);;

                // new projection
                this.projection = d3.geo.mercator().center(newCenter)
                  .scale(this.scale).translate([this.w / 2, this.h / 2]);
                this.renderMap();
            });
		}
        
        loadGlyph() {
            var requestStr = '/weathervis/linearOpt?level=' + this.currentRenderLevel;
            d3.json(requestStr, (error: any, data: any) => {
                var rawData = JSON.parse(data)
                this.glyphData = rawData;
                this.renderGlyph();
            }); 
        }
        
        onMouseDown(e: MouseEvent) {
            if (this.isHoveringContent) {
                this.isDragging = true;
                var mouseCenter = [e.clientX - this.divDom.offsetLeft, e.clientY - this.divDom.offsetTop];
                this.tempDegreeCenter = this.projection.invert(mouseCenter);
            }
            super.onMouseDown(e);
        }
        
        onMouseMove(e: MouseEvent) {
            if (e.button == 0 && this.isHoveringContent &&  this.isDragging) {
                var mouseCenter: [number, number] = [e.clientX - this.divDom.offsetLeft, e.clientY - this.divDom.offsetTop];
                console.log(this.isHoveringContent);
                this.projection = d3.geo.mercator().scale(this.scale).center(this.tempDegreeCenter)
                                    .translate(mouseCenter);
                this.tempDegreeCenter = this.projection.invert(mouseCenter);
                
                this.render();
            }
            super.onMouseMove(e);
        }
        
        onMouseUp(e: MouseEvent) {
            super.onMouseUp(e);
        }
        
        onWheel(e: any) {
            var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
            var mouseCenter: [number, number] = [this.w / 2, this.h / 2];
            var degreeCenter = this.projection.invert(mouseCenter);
            this.scale = this.scale * (1 + delta * 0.05);
            this.projection = d3.geo.mercator().scale(this.scale).center(degreeCenter)
                                    .translate(mouseCenter);
            var tempRenderingLevel = Math.round(this.scale / 150);
            if (tempRenderingLevel != this.currentRenderLevel) {
               this.currentRenderLevel = tempRenderingLevel;
               this.loadGlyph(); 
            }
            
            this.render();
        }
        
        renderMap() {
            var path = d3.geo.path().projection(this.projection);
            path = path.projection(this.projection);
            this.svg.selectAll("path").remove();
            this.svg.selectAll("path")
                    .data(this.jsonData.features)
                    .enter()
                    .append("path")
                    .attr("d", path);
        }
        
        renderGlyph() {
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
        }
        
        render() {
            this.renderMap();
            this.renderGlyph();
        }
	}
}