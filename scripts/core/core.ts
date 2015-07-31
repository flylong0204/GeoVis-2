/// <reference path="../../../DefinitelyTyped/threejs/three.d.ts" />
/// <reference path="property.ts" />

module Core {
    export class BasicElement {
        public prop: Core.Property;
        
        addProperty(type: string, value: any){
            this.prop[type] = value;
        }
    }
    
    export class Point extends BasicElement {
        
        constructor(p: THREE.Vector3) {
            super();
            this.prop['pos'] = p;
        }
    }
    
    export class Line extends BasicElement {
        constructor(p1: THREE.Vector3, p2: THREE.Vector3) {
            super();
            this.prop['pos1'] = p1;
            this.prop['pos2'] = p2;
        }
    }
}