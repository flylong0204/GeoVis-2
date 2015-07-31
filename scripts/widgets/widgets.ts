/// <reference path="../core/core.ts" />

module Widgets {
    export class BasicWidget {
        render() {}
    }
    
    export class PointWidget {
        constructor(public p: Core.Point) {    
        }
        
        setPos(value: THREE.Vector3){
            this.p.prop['pos'] = value;
        }
        
        setColor(value: THREE.Vector3){

        }

        render() {}
    }
}