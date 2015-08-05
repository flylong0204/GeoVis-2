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

        raiseEvent(objId: string, eventName: string, e: MouseEvent) {
            var obj = this.eventHanlders[objId];
            if (obj != null) this.execEvent(obj, eventName, e);
        }
        
        execEvent(obj: any, eventName: string, e: MouseEvent) {
            if (eventName == 'mousedown') {
               obj.onMouseDown(e); 
            } else if (eventName == 'mousemove') {
               obj.onMouseDrag(e); 
            } else if (eventName == 'mosueup') {
               obj.onMouseUp(e); 
            }
        }
    }
    
    export class Utility {
        public static eventMapper = new EventMapper();   
    }
}

