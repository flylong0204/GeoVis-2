/// <reference path='utility.ts' />

module GeoVis {
	export class Widget {
        protected diffX = 0.0;
        protected diffY = 0.0;
        protected divDom: HTMLElement;
        protected isDragging: boolean;
        
        constructor(protected widgetId, protected px: number, protected py: number, protected w: number, protected h: number) {
            this.divDom = document.getElementById(widgetId);
            this.divDom.style.left = px + 'px';
            this.divDom.style.top = py + 'px';
            this.divDom.style.width = w + 'px';
            this.divDom.style.height = h + 'px';
            GeoVis.Utility.eventMapper.registerEvent(this.widgetId, this);
            this.isDragging = false;
        }
        
        onMouseDown(e: MouseEvent) {
            
        }
        
        onMouseMove(e: MouseEvent) {
            
        }
        
        onMouseUp(e: MouseEvent) {
            
        }
        
        onWheel(e: any) {
//            var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
//            
//            var w = 100;
//            var str = this.divDom.style.width.substr(0, this.divDom.style.width.length - 2);
//            if (str.length !== 0)
//                w = parseInt(str);
//            var h = 100;
//            str = this.divDom.style.height.substr(0, this.divDom.style.width.length - 2);
//            if (str.length !== 0)
//                h = parseInt(str);
//            this.divDom.style.width = Math.round(w * (1 + delta * 0.1)) + 'px';
//            this.divDom.style.height = Math.round(h * (1 + delta * 0.1)) + 'px';
        }
    }
}