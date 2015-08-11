module GeoVis {
    export class FunctionPanel extends Widget {
        protected titleDivId: string;
        protected contentDivId: string;
        private titleELement: HTMLElement;
        private contentElement: HTMLElement;
        
        constructor(public panelId: string, px: number = 0, py: number = 0, w: number = 40, h: number = 400, protected isHorizontal: boolean = false) {
            super(panelId, px, py, w, h);
            
            this.divDom = document.getElementById(panelId);
            this.titleDivId = panelId + '-title';
            this.contentDivId = panelId + '-content';
            this.titleELement = document.createElement('div');
            this.titleELement.setAttribute('class', 'panel-title');
            this.titleELement.innerText = 'Tool';
            this.contentElement = document.createElement('div');
            this.contentElement.setAttribute('class', 'panel-content');
            this.divDom.appendChild(this.titleELement);
            this.divDom.appendChild(this.contentElement);
            
            // update the element style according to this.isHorizontal
            if (this.isHorizontal) {
                
            } else {
                
            }
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
            if (e.button == 0 && this.isDragging == true) {
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