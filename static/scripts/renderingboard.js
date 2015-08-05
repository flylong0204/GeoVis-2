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
            _super.call(this, widgetId);
            this.px = px;
            this.py = py;
            this.w = w;
            this.h = h;
            this.divDom = document.getElementById(widgetId);
        }
        RenderingBoard.prototype.render = function () {
        };
        return RenderingBoard;
    })(GeoVis.Widget);
    GeoVis.RenderingBoard = RenderingBoard;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=renderingboard.js.map