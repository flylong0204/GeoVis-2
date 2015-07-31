/// <reference path="../../../DefinitelyTyped/threejs/three.d.ts" />
/// <reference path="property.ts" />
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var Core;
(function (Core) {
    var BasicElement = (function () {
        function BasicElement() {
        }
        BasicElement.prototype.addProperty = function (type, value) {
            this.prop[type] = value;
        };
        return BasicElement;
    })();
    Core.BasicElement = BasicElement;
    var Point = (function (_super) {
        __extends(Point, _super);
        function Point(p) {
            _super.call(this);
            this.prop['pos'] = p;
        }
        return Point;
    })(BasicElement);
    Core.Point = Point;
    var Line = (function (_super) {
        __extends(Line, _super);
        function Line(p1, p2) {
            _super.call(this);
            this.prop['pos1'] = p1;
            this.prop['pos2'] = p2;
        }
        return Line;
    })(BasicElement);
    Core.Line = Line;
})(Core || (Core = {}));
