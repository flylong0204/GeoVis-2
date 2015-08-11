var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var GeoVis;
(function (GeoVis) {
    var RenderingBoard = (function (_super) {
        __extends(RenderingBoard, _super);
        function RenderingBoard(widgetId, px, py, w, h) {
            if (px === void 0) { px = 0; }
            if (py === void 0) { py = 0; }
            if (w === void 0) { w = 100; }
            if (h === void 0) { h = 100; }
            _super.call(this, widgetId, px, py, w, h);
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
        RenderingBoard.prototype.render = function () {
        };
        RenderingBoard.prototype.onMouseDown = function (e) {
            if (this.titleELement == e.target) {
                this.isDragging = true;
                this.diffX = e.clientX - this.divDom.offsetLeft;
                this.diffY = e.clientY - this.divDom.offsetTop;
                this.divDom.style.zIndex = '10';
            }
        };
        RenderingBoard.prototype.onMouseMove = function (e) {
            if (e.button == 0 && this.isDragging == true && !this.isHoveringContent) {
                this.divDom.style.left = (e.clientX - this.diffX) + 'px';
                this.divDom.style.top = (e.clientY - this.diffY) + 'px';
            }
        };
        RenderingBoard.prototype.onMouseUp = function (e) {
            this.diffX = 0;
            this.diffY = 0;
            this.isDragging = false;
            this.divDom.style.zIndex = '1';
        };
        return RenderingBoard;
    })(GeoVis.Widget);
    GeoVis.RenderingBoard = RenderingBoard;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=renderingboard.js.map