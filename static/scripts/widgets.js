/// <reference path='utility.ts' />
var GeoVis;
(function (GeoVis) {
    var Widget = (function () {
        function Widget(widgetId) {
            this.widgetId = widgetId;
            this.diffX = 0.0;
            this.diffY = 0.0;
        }
        Widget.prototype.onMouseDown = function (e) {
            this.diffX = e.clientX - this.divDom.offsetLeft;
            this.diffY = e.clientY - this.divDom.offsetTop;
        };
        Widget.prototype.onMouseMove = function (e) {
        };
        Widget.prototype.onMouseUp = function (e) {
            this.diffX = 0;
            this.diffY = 0;
        };
        Widget.prototype.onMouseDrag = function (e) {
            this.divDom.style.left = (e.clientX - this.diffX) + 'px';
            this.divDom.style.top = (e.clientY - this.diffY) + 'px';
        };
        return Widget;
    })();
    GeoVis.Widget = Widget;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=widgets.js.map