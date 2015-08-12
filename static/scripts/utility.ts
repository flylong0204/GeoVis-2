module GeoVis {
    export class EventMapper {
        private eventHanlders = new Array< any >();

        constructor() {

        }

        registerEvent(objId: string, obj: any) {
            this.eventHanlders[objId] = obj;
        }

        removeEvent(objId: string) {
            this.eventHanlders[objId] = null;
        }

        raiseEvent(objId: string, e: MouseEvent) {
            var obj = this.eventHanlders[objId];
            if (obj != null) this.execEvent(obj, e);
        }
        
        raiseEventAll(e: MouseEvent) {
            for (var obj in this.eventHanlders)
                this.execEvent(this.eventHanlders[obj], e);
        }
        
        execEvent(obj: any, e: MouseEvent) {
            if (e.type == 'mousedown') {
               obj.onMouseDown(e); 
            } else if (e.type == 'mousemove') {
               obj.onMouseMove(e); 
            } else if (e.type == 'mouseup') {
               obj.onMouseUp(e); 
            } else if (e.type == 'mousewheel') {
               obj.onWheel(e); 
            }
        }
    }
    
    export class Utility {
        public static eventMapper = new EventMapper();   
    }
}

