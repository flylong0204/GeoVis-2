var GeoVis;
(function (GeoVis) {
    var EventMapper = (function () {
        function EventMapper() {
            this.eventHanlders = new Array();
        }
        EventMapper.prototype.registerEvent = function (objId, obj) {
            this.eventHanlders[objId] = obj;
        };
        EventMapper.prototype.removeEvent = function (objId) {
            this.eventHanlders[objId] = null;
        };
        EventMapper.prototype.raiseEvent = function (objId, e) {
            var obj = this.eventHanlders[objId];
            if (obj != null)
                this.execEvent(obj, e);
        };
        EventMapper.prototype.execEvent = function (obj, e) {
            if (e.type == 'mousedown') {
                obj.onMouseDown(e);
            }
            else if (e.type == 'mousemove') {
                obj.onMouseMove(e);
            }
            else if (e.type == 'mouseup') {
                obj.onMouseUp(e);
            }
            else if (e.type == 'mousewheel') {
                obj.onWheel(e);
            }
        };
        return EventMapper;
    })();
    GeoVis.EventMapper = EventMapper;
    var Utility = (function () {
        function Utility() {
        }
        Utility.eventMapper = new EventMapper();
        return Utility;
    })();
    GeoVis.Utility = Utility;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=utility.js.map