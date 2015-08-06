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
        
        onWheel(e: any) {
            var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
            
            var w = 100;
            var str = this.divDom.style.width.substr(0, this.divDom.style.width.length - 2);
            if (str.length !== 0)
                w = parseInt(str);
            var h = 100;
            str = this.divDom.style.height.substr(0, this.divDom.style.width.length - 2);
            if (str.length !== 0)
                h = parseInt(str);
            this.divDom.style.width = Math.round(w * (1 + delta * 0.1)) + 'px';
            this.divDom.style.height = Math.round(h * (1 + delta * 0.1)) + 'px';
        }
    }
}