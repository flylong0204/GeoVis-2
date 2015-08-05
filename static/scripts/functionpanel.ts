module GeoVis {
    export class FunctionPanel extends Widget {
        constructor(public panelId: string) {
            super(panelId);
            
            this.divDom = document.getElementById(panelId);
            var divHtml = "<div class='panel-title'"
                        + "id='" + panelId + "-title'>Tool</div> <div class='panel-content'"
                        + "id='" + panelId + "-content'>Test</div>";
            this.divDom.innerHTML = divHtml;
            
            GeoVis.Utility.eventMapper.registerEvent(panelId + '-title', this);
        }
    } 
}