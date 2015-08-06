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
        Widget.prototype.onWheel = function (e) {
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
        };
        return Widget;
    })();
    GeoVis.Widget = Widget;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=widgets.js.map