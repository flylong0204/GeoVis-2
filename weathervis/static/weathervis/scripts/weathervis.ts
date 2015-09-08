/// <reference path="weathervislib.d.ts" />
/// <reference path="lodglyphmap.ts" />
/// <reference path="../../../../static/scripts/utility.ts" />
/// <reference path="../../../../static/scripts/functionpanel.ts" />



module WeatherVis {
	export class TempVis {
		private lodMapId: string;
		private lodMap: LODGlyphMap;
        private functionPanel: GeoVis.FunctionPanel;

		constructor(private divId: string) {
			this.lodMapId = divId + 'LodMap';
            var divDom = document.getElementById(divId);
            
			// construct html dives
            var lodMapDivDom = document.createElement('div');
			var divHtml = "<div class='rendering-div'"
                        + "id='" + this.lodMapId + "'></div>";
            lodMapDivDom.innerHTML = divHtml;
            divDom.appendChild(lodMapDivDom);
            
			// construct objects
			this.lodMap = new LODGlyphMap(this.lodMapId, 0, 0, 700, 500);
            // this.functionPanel = new GeoVis.FunctionPanel('tool-div');
            
            // 
		}

		render() {
		    
		}
	}
}

var temp = new WeatherVis.TempVis('map-div');