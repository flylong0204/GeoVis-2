/// <reference path="../core/core.ts" />
var Widgets;
(function (Widgets) {
    var BasicWidget = (function () {
        function BasicWidget() {
        }
        BasicWidget.prototype.render = function () { };
        return BasicWidget;
    })();
    Widgets.BasicWidget = BasicWidget;
    var PointWidget = (function () {
        function PointWidget(p) {
            this.p = p;
        }
        PointWidget.prototype.setPos = function (value) {
            this.p.prop['pos'] = value;
        };
        PointWidget.prototype.setColor = function (value) {
        };
        PointWidget.prototype.render = function () { };
        return PointWidget;
    })();
    Widgets.PointWidget = PointWidget;
})(Widgets || (Widgets = {}));
//# sourceMappingURL=widgets.js.map