var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
var GeoVis;
(function (GeoVis) {
    var FunctionPanel = (function (_super) {
        __extends(FunctionPanel, _super);
        function FunctionPanel(panelId) {
            _super.call(this, panelId);
            this.panelId = panelId;
            this.divDom = document.getElementById(panelId);
            var divHtml = "<div class='panel-title'"
                + "id='" + panelId + "-title'>Tool</div> <div class='panel-content'"
                + "id='" + panelId + "-content'>Test</div>";
            this.divDom.innerHTML = divHtml;
            GeoVis.Utility.eventMapper.registerEvent(panelId + '-title', this);
        }
        return FunctionPanel;
    })(GeoVis.Widget);
    GeoVis.FunctionPanel = FunctionPanel;
})(GeoVis || (GeoVis = {}));
//# sourceMappingURL=functionpanel.js.map