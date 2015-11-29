var ClusterControl = (function(){
    function ClusterControl() {
        this.datasetIndex = 0;
        this.dataset = null;
        this.currentColor = {};
        this.currentColor.r = 255.0;
        this.currentColor.g = 0.0;
        this.currentColor.b = 0.0;

        this.pointNum = 0;
        this.clusterNum = 0;
        this.finalClusterCount = 0;
        this.clusterIndex = {};
    }

    ClusterControl.prototype.clear = function() {
        this.pointNum = 0;
        this.clusterIndex = {};
    }

    ClusterControl.prototype.getFinalLabel = function() {
        var finalLabel = [];
        for (var i = 0; i < this.dataset.length; ++i) finalLabel[i] = -1;
        this.finalClusterCount = 0;
        for (var i = 0; i < this.clusterNum; ++i) 
            if (this.clusterIndex[i]) {
                for (var j = 0; j < this.clusterIndex[i].pointCount; ++j) {
                    var pIndex = this.clusterIndex[i].points[j];
                    finalLabel[pIndex] = this.finalClusterCount;
                }
                this.finalClusterCount++;
            }
        var isUnlabeled = false;
        for (var i = 0; i < this.dataset.length; ++i)
            if (finalLabel[i] == -1) {
                isUnlabeled = true;
                finalLabel[i] = this.finalClusterCount;
            }
        if (isUnlabeled) this.finalClusterCount++;
        return finalLabel;
    }

    ClusterControl.prototype.getClusterData = function() {
        var cData = [];
        for (var i = 0; i < this.clusterNum; ++i) 
            if (this.clusterIndex[i]) {
                var newCluster = {};
                newCluster["Name"] = "Cluster";
                newCluster["PointCount"] = this.clusterIndex[i].pointCount;
                var colorStr = "RGB" + parseInt(this.clusterIndex[i].color[0] * 255) + "," 
                                + parseInt(this.clusterIndex[i].color[1] * 255) + "," 
                                + parseInt(this.clusterIndex[i].color[2] * 255);
                
                newCluster["Color"] = "background:" + colorStr.colorHex();
                newCluster["Delete"] = "delete.png";
                newCluster["ID"] = i;
                cData.push(newCluster);
            }
        return cData;
    }

    var reg = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/;  
    /*RGB颜色转换为16进制*/  
    String.prototype.colorHex = function(){  
        var that = this;  
        if(/^(rgb|RGB)/.test(that)){  
            var aColor = that.replace(/(?:||rgb|RGB)*/g,"").split(",");  
            var strHex = "#";  
            for(var i=0; i<aColor.length; i++){  
                var hex = Number(aColor[i]).toString(16);  
                if(hex === "0"){  
                    hex += hex;   
                }  
                strHex += hex;  
            }  
            if(strHex.length !== 7){  
                strHex = that;    
            }  
            return strHex;  
        }else if(reg.test(that)){  
            var aNum = that.replace(/#/,"").split("");  
            if(aNum.length === 6){  
                return that;      
            }else if(aNum.length === 3){  
                var numHex = "#";  
                for(var i=0; i<aNum.length; i+=1){  
                    numHex += (aNum[i]+aNum[i]);  
                }  
                return numHex;  
            }  
        }else{  
            return that;      
        }  
    }

    ClusterControl.prototype.setCurrentColor = function(color) {
        this.currentColor = color;
    }

    ClusterControl.prototype.init = function(pointNum) {
        this.pointNum = pointNum;
    }

    ClusterControl.prototype.addCluster = function(contour) {
        var cluster = {};
        cluster.pointCount = 0;
        cluster.points = [];
        cluster.color = [];
        cluster.color[0] = this.currentColor.r / 255.0;
        cluster.color[1] = this.currentColor.g / 255.0;
        cluster.color[2] = this.currentColor.b / 255.0;
        for (var i = 0; i < this.dataset.length; ++i) {
            var p = {};
            p.x = this.dataset[i][0];
            p.y = 1.0 - this.dataset[i][1];
            if (this.rayCasting(p, contour)) {
                cluster.points[cluster.pointCount] = i;
                cluster.pointCount++;
            }
        }
        if (cluster.pointCount == 0) return;
        this.clusterIndex[this.clusterNum] = cluster;
        this.clusterNum++;
    }

    ClusterControl.prototype.removeCluster = function(id) {
        delete this.clusterIndex[id];
    }

    ClusterControl.prototype.getPointColor = function() {
        var colors = new Float32Array( this.dataset.length * 3 );

        for (var i = 0; i < this.dataset.length; ++i) {
            colors[3 * i] = this.dataset[i][2] * 0.9;
            colors[3 * i + 1] = this.dataset[i][2] * 0.9;
            colors[3 * i + 2] = this.dataset[i][2] * 0.9;
        }

        for (var i = 0; i < this.clusterNum; ++i) 
            if (this.clusterIndex[i]) {
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
