var ClusterControl = (function(){
    function ClusterControl() {
        this.datasetIndex = 0;
        this.dataset = null;

        this.pointNum = 0;
        this.clusterIndex = {};
    }

    ClusterControl.prototype.clear = function() {
        this.pointNum = 0;
        this.clusterIndex = {};
    }

    ClusterControl.prototype.init = function(pointNum) {
        this.pointNum = pointNum;
    }

    ClusterControl.prototype.addCluster = function(id, cluster) {
        this.clusterIndex[id] = cluster;
    }

    ClusterControl.prototype.removeCluster = function(id) {
        delete this.clusterIndex(id);
    }

    return ClusterControl;
})();

var cControl = new ClusterControl();
