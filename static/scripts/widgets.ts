/// <reference path='utility.ts' />

module GeoVis {
	export class Widget {
        private diffX = 0.0;
        private diffY = 0.0;
        protected divDom: HTMLElement;
        
        constructor(protected widgetId) {
           
        }
        
        onMouseDown(e: any) {
            this.diffX = e.clientX - this.divDom.offsetLeft;
            this.diffY = e.clientY - this.divDom.offsetTop;
        }
        
        onMouseMove(e: any) {
            
        }
        
        onMouseUp(e: any) {
            this.diffX = 0;
            this.diffY = 0;
        }
        
        onMouseDrag(e: any) {
            this.divDom.style.left = (e.clientX - this.diffX) + 'px';
            this.divDom.style.top = (e.clientY - this.diffY) + 'px';
        }
    }
}