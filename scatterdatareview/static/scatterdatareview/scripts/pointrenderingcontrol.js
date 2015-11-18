var RenderingControl = (function() {
    function RenderingControl() {
        this.lines = [];
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

        var lineNum = this.lines.length;
        this.lines[lineNum] = this.currentLine;

        this.currentLine[0] = x;
        this.currentLine[1] = y; 
    }

    RenderingControl.prototype.addPoint = function(x, y) {
        var currentLen = this.currentLine.length;
        this.currentLine[currentLen] = x;
        this.currentLine[currentLen + 1] = y;
    }

    RenderingControl.prototype.completeLine = function() {
        
    }

    return RenderingControl;
})();

var pRen = new RenderingControl();