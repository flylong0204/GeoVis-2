var RenderingControl = (function() {
    function RenderingControl() {
        this.currentLine = [];

        this.dom = null;
        this.left = 0;
        this.top = 0;
        this.width = 0;
        this.height = 0;
    }

    RenderingControl.prototype.update = function() {
        this.left = $(this.dom).offset().left;
        this.top = $(renderer.domElement).offset().top;
    }

    RenderingControl.prototype.addNewLine = function(x, y) {
        this.currentLine = [];
        var p = {};
        p.x = x;
        p.y = y;
        this.currentLine[0] = p;
    }

    RenderingControl.prototype.addPoint = function(x, y) {
        var currentLen = this.currentLine.length;
        var p = {};
        p.x = x;
        p.y = y;
        this.currentLine[currentLen] = p;
    }

    RenderingControl.prototype.completeLine = function() {
        this.currentLine = [];
    }

    return RenderingControl;
})();

var pRen = new RenderingControl();