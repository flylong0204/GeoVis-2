/// <reference path='utility.ts' />

module GeoVis {
	export class Widget {
        protected divDom: HTMLElement;
        
        constructor(protected widgetId, protected px: number = 0, protected py: number = 0, protected w: number = 0, protected h: number = 0) {
            GeoVis.Utility.eventMapper.registerEvent(this.widgetId, this);
        }
        
        onMouseDown(e: MouseEvent) {
            
        }
        
        onMouseMove(e: MouseEvent) {
            
        }
        
        onMouseUp(e: MouseEvent) {
            
        }
        
        onWheel(e: any) {
            
        }
    }
}