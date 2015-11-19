var ClusterControl = (function(){
    function ClusterControl() {
        this.datasetIndex = 0;
        this.dataset = null;

        this.pointNum = 0;
        this.clusterNum = 0;
        this.clusterIndex = {};
    }

    ClusterControl.prototype.clear = function() {
        this.pointNum = 0;
        this.clusterIndex = {};
    }

    ClusterControl.prototype.init = function(pointNum) {
        this.pointNum = pointNum;
    }

    ClusterControl.prototype.addCluster = function(contour) {
        var cluster = {};
        cluster.pointCount = 0;
        cluster.points = [];
        cluster.color = [];
        cluster.color[0] = Math.random();
        cluster.color[1] = Math.random();
        cluster.color[2] = Math.random();
        for (var i = 0; i < this.dataset.length; ++i) {
            var p = {};
            p.x = this.dataset[i][0];
            p.y = 1.0 - this.dataset[i][1];
            if (this.rayCasting(p, contour)) {
                cluster.points[cluster.pointCount] = i;
                cluster.pointCount++;
            }
        }
        this.clusterIndex[this.clusterNum] = cluster;
        this.clusterNum++;
    }

    ClusterControl.prototype.removeCluster = function(id) {
        delete this.clusterIndex(id);
    }

    ClusterControl.prototype.getPointColor = function() {
        var colors = new Float32Array( this.dataset.length * 3 );

        for (var i = 0; i < this.dataset.length; ++i) {
            colors[3 * i] = this.dataset[i][2] * 0.9;
            colors[3 * i + 1] = this.dataset[i][2] * 0.9;
            colors[3 * i + 2] = this.dataset[i][2] * 0.9;
        }

        for (var i = 0; i < this.clusterNum; ++i) 
            if (this.clusterIndex[i] !== null) {
                for (var j = 0; j < this.clusterIndex[i].pointCount; ++j) {
                    var pIndex = this.clusterIndex[i].points[j];
                    colors[3 * pIndex] = this.clusterIndex[i].color[0];
                    colors[3 * pIndex + 1] = this.clusterIndex[i].color[1];
                    colors[3 * pIndex + 2] = this.clusterIndex[i].color[2];
                }
            }

        return colors;
    }
    /**
   * @description 射线法判断点是否在多边形内部
   * @param {Object} p 待判断的点，格式：{ x: X坐标, y: Y坐标 }
   * @param {Array} poly 多边形顶点，数组成员的格式同 p
   * @return {String} 点 p 和多边形 poly 的几何关系
   */
    ClusterControl.prototype.rayCasting = function(p, poly) {
        var px = p.x,
            py = p.y,
            flag = false

        for(var i = 0, l = poly.length, j = l - 1; i < l; j = i, i++) {
          var sx = poly[i].x,
              sy = poly[i].y,
              tx = poly[j].x,
              ty = poly[j].y

              // 点与多边形顶点重合
        if((sx === px && sy === py) || (tx === px && ty === py)) {
            return 'on'
        }
              
        // 判断线段两端点是否在射线两侧
        if((sy < py && ty >= py) || (sy >= py && ty < py)) {
        // 线段上与射线 Y 坐标相同的点的 X 坐标
            var x = sx + (py - sy) * (tx - sx) / (ty - sy)
              
            // 点在多边形的边上
            if(x === px) {
                return 'on'
            }
              
            // 射线穿过多边形的边界
            if(x > px) {
                flag = !flag
            }
        }
    }

    // 射线穿过多边形边界的次数为奇数时点在多边形内
    return flag ? true : false
  }

    return ClusterControl;
})();

var cControl = new ClusterControl();
