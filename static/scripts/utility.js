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
        EventMapper.prototype.raiseEvent = function (objId, eventName, e) {
            var obj = this.eventHanlders[objId];
            if (obj != null)
                this.execEvent(obj, eventName, e);
        };
        EventMapper.prototype.execEvent = function (obj, eventName, e) {
            if (eventName == 'mousedown') {
                obj.onMouseDown(e);
            }
            else if (eventName == 'mousemove') {
                obj.onMouseDrag(e);
            }
            else if (eventName == 'mosueup') {
                obj.onMouseUp(e);
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