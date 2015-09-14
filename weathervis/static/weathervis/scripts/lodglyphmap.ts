/// <reference path="weathervislib.d.ts" />

declare var topojson: any;

module WeatherVis {
	export class UnGlyph {
		value: number;
		lon: number;
		lat: number;
	}

	export class LODGlyphMap extends GeoVis.Widget{ 
        private isHoveringContent: boolean;
        private isDragging: boolean;

        protected scale: number;
        protected degreePerPixel: number;
        protected projection: any;
        protected jsonData: any;
        protected glyphData: any;
        protected svg: any;
        protected tempDegreeCenter: [number, number];
        protected currentRenderLevel: number;
        protected color: any;
        protected forecastData: any;
        protected lineFunction: any;
        
		constructor(private parentDivId: string, px: number, py: number, w: number, h: number, level: string = "2") {
            super(parentDivId + '-lodmap' + level, px, py, w, h);            
            
            this.divDom = document.getElementById(this.widgetId);
            this.color = new Array('#fee8c8', '#fdbb84', '#e34a33');
            
            this.currentRenderLevel = parseInt(level);
            
            $('#' + this.widgetId).dialog({
                autoOpen: true,
                height: h,
                width: w,
                position: [px, py],
                modal: false,
                resizable: false,
                title: this.widgetId,
                zIndex: 10
            });
            
            GeoVis.Utility.eventMapper.registerEvent(this.widgetId, this);

            this.initParameters();
            
            $(this.divDom).mouseenter(() => {
                this.isHoveringContent = true;
            });
            
            $(this.divDom).mouseleave(() => {
                this.isHoveringContent = false;
            });
		}
        
        initParameters() {
            this.isHoveringContent = false;
            this.isDragging = false;
            
            // construct svg
            this.svg = d3.select('#' + this.widgetId)
                .append("svg")
                .attr('id', this.widgetId + '-svg')
                .attr("width", '100%')
                .attr("height", '98%');
            
            this.loadMap();
            
            this.loadGlyph();
        }

        // render the map
        loadMap() {
            d3.json('/static/us.json', (error: any, data: any) => {                
                var topo = topojson.feature(data, data.objects.states);
                this.jsonData = topo;               
                
                this.w = this.divDom.offsetWidth;
                this.h = this.divDom.offsetHeight * 0.98;
                
                var center = d3.geo.centroid(topo);
                this.scale = 150;
                this.projection = d3.geo.mercator().scale(this.scale).center(center)
                                    .translate([this.w / 2, this.h / 2]);
                var path = d3.geo.path().projection(this.projection);
                var bounds  = path.bounds(topo);
                var hscale  = this.scale * this.w  / (bounds[1][0] - bounds[0][0]);
                var vscale  = this.scale * this.h / (bounds[1][1] - bounds[0][1]);
                if (hscale < vscale){
                    this.scale   = hscale;
                    this.degreePerPixel = (bounds[1][0] - bounds[0][0]) / this.w;
                } else {
                    this.scale = vscale; 
                    this.degreePerPixel = (bounds[1][1] - bounds[0][1]) / this.w;
                }
                //this.currentRenderLevel = Math.round(this.degreePerPixel * 150 / this.scale / 1 * 45);
                    
                var newCenter = this.projection.invert([(bounds[1][0] + bounds[0][0]) / 2, (bounds[1][1] + bounds[0][1]) / 2]);;

                // new projection
                this.projection = d3.geo.mercator().center(newCenter)
                  .scale(this.scale).translate([this.w / 2, this.h / 2]);
                
                // load forecast map
                var requestStr = '/weathervis/getApcpForecast';
                d3.json(requestStr, (error: any, data: any) => {
                    this.forecastData = JSON.parse(data);
                    
                    this.renderMap();
                }); 
            });
        }
        
        loadGlyph() {
            var requestStr = '/weathervis/getOptResult?level=' + this.currentRenderLevel;
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
        }
        
        onMouseMove(e: MouseEvent) {
            if (e.button == 0 && this.isHoveringContent &&  this.isDragging) {
                var mouseCenter: [number, number] = [e.clientX - this.divDom.offsetLeft, e.clientY - this.divDom.offsetTop];
                this.projection = d3.geo.mercator().scale(this.scale).center(this.tempDegreeCenter)
                                    .translate(mouseCenter);
                this.tempDegreeCenter = this.projection.invert(mouseCenter);
                
                this.render();
            }
        }
        
        onMouseUp(e: MouseEvent) {
            this.isDragging = false;
        }
        
        onWheel(e: any) {
            var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
            var mouseCenter: [number, number] = [this.w / 2, this.h / 2];
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
        }
        
        renderMap() {
            var path = d3.geo.path().projection(this.projection);
            path = path.projection(this.projection);
            this.svg.selectAll("path").remove();
            this.svg.selectAll("path")
                    .data(this.jsonData.features)
                    .enter()
                    .append("path")
                    .attr("d", path)
                    .attr("stroke", "gray")
                    .attr("fill", "none");;
            
            this.lineFunction = d3.svg.line()
                                .x(function(d) { return this.projection([d[0], d[1]])[0]; })
                                .y(function(d) { return this.projection([d[0], d[1]])[1]; })
                                .interpolate('linear');
            for (var i in this.forecastData) {
                for (var j in this.forecastData[i]) {
                    this.svg.append("path")
                        .attr("d", this.lineFunction(this.forecastData[i][j]))
                        .attr("stroke", this.color[i])
                        .attr("stroke-width", 2)
                        .attr("fill", "none"); 
                }
                
            }
            
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
                    .attr('stroke-width', 2)
                    .attr('fill', 'none');
            }   
        }
        
        render() {
            this.renderMap();
            this.renderGlyph();
        }
	}
}