module GeoVis {
	export class RenderingBoard extends Widget{
		constructor(widgetId: string, protected px: number, protected py: number, protected w: number, protected h: number){
			super(widgetId);
            
            this.divDom = document.getElementById(widgetId);
		}
        
        render() {
            
        }
	}
}