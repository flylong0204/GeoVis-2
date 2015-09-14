/// <reference path='utility.ts' />
var GeoVis;
(function (GeoVis) {
    var Widget = (function () {
        function Widget(widgetId, px, py, w, h) {
            if (px === void 0) { px = 0; }
            if (py === void 0) { py = 0; }
            if (w === void 0) { w = 0; }
            if (h === void 0) { h = 0; }
            this.widgetId = widgetId;
            this.px = px;
            this.py = py;
            this.w = w;
            this.h = h;
            GeoVis.Utility.eventMapper.registerEvent(this.widgetId, this);
        }
        Widget.prototype.onMouseDown = function (e) {
        };
        Widget.prototype.onMouseMove = function (e) {
        };
        Widget.prototype.onMouseUp = function (e) {
        };
        Widget.prototype.onWheel = function (e) {
        };
        return Widget;
    })();
    GeoVis.Widget = Widget;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=widgets.js.map