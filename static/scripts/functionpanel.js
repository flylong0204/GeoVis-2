var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var GeoVis;
(function (GeoVis) {
    var FunctionPanel = (function (_super) {
        __extends(FunctionPanel, _super);
        function FunctionPanel(panelId, px, py, w, h, isHorizontal) {
            if (px === void 0) { px = 0; }
            if (py === void 0) { py = 0; }
            if (w === void 0) { w = 40; }
            if (h === void 0) { h = 400; }
            if (isHorizontal === void 0) { isHorizontal = false; }
            _super.call(this, panelId, px, py, w, h);
            this.panelId = panelId;
            this.isHorizontal = isHorizontal;
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
            }
            else {
            }
        }
        FunctionPanel.prototype.onMouseDown = function (e) {
            if (this.titleELement == e.target) {
                this.isDragging = true;
                this.diffX = e.clientX - this.divDom.offsetLeft;
                this.diffY = e.clientY - this.divDom.offsetTop;
                this.divDom.style.zIndex = '10';
            }
        };
        FunctionPanel.prototype.onMouseMove = function (e) {
            if (e.button == 0 && this.isDragging == true) {
                this.divDom.style.left = (e.clientX - this.diffX) + 'px';
                this.divDom.style.top = (e.clientY - this.diffY) + 'px';
            }
        };
        FunctionPanel.prototype.onMouseUp = function (e) {
            this.diffX = 0;
            this.diffY = 0;
            this.isDragging = false;
            this.divDom.style.zIndex = '1';
        };
        return FunctionPanel;
    })(GeoVis.Widget);
    GeoVis.FunctionPanel = FunctionPanel;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=functionpanel.js.map