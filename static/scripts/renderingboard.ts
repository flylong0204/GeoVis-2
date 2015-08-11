module GeoVis {
	export class RenderingBoard extends Widget{
        protected boardName: string;
        protected titleDivId: string;
        protected contentDivId: string;
        protected titleELement: HTMLElement;
        protected contentElement: HTMLElement; 
        protected isHoveringContent: boolean;
        
		constructor(widgetId: string, px: number = 0, py: number = 0, w: number = 100, h: number = 100){
			super(widgetId, px, py, w, h);
            this.boardName = "Rendering Board";
            
            this.titleDivId = this.widgetId + '-title';
            this.contentDivId = this.widgetId + '-content';
            this.titleELement = document.createElement('div');
            this.titleELement.setAttribute('class', 'panel-title');
            this.titleELement.setAttribute('id', this.titleDivId);
            this.titleELement.innerText = this.boardName;
            this.contentElement = document.createElement('div');
            this.contentElement.setAttribute('class', 'panel-content');
            this.contentElement.setAttribute('id', this.contentDivId);
            this.contentElement.setAttribute('offsetTop', '20');
            this.divDom.appendChild(this.titleELement);
            this.divDom.appendChild(this.contentElement);
            
            this.isHoveringContent = false;
		}
        
        render() {
            
        }
        
        onMouseDown(e: MouseEvent) {
            if (this.titleELement == e.target) {
                this.isDragging = true;
                this.diffX = e.clientX - this.divDom.offsetLeft;
                this.diffY = e.clientY - this.divDom.offsetTop;
                this.divDom.style.zIndex = '10';
            }
        }
        
        onMouseMove(e: MouseEvent) {
            if (e.button == 0 && this.isDragging == true && !this.isHoveringContent) {
                this.divDom.style.left = (e.clientX - this.diffX) + 'px';
                this.divDom.style.top = (e.clientY - this.diffY) + 'px'; 
            }
        }
        
        onMouseUp(e: MouseEvent) {
            this.diffX = 0;
            this.diffY = 0;
            this.isDragging = false;
            this.divDom.style.zIndex = '1';
        }
	}
}