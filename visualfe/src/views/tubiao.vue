<template>
  <div class="d-flex">
    <div id="main" style="width: 40%;height:330px;"></div>
    <div id="main2" style="width: 60%;height:330px;"></div>
  </div>
</template>
<script>
export default {
  name: "TaskList",
  data() {
    return {
      taskStatus: { Start: "Start", Pause: "Pause", Run: "Run", End: "End" },
      taskList: []
    };
  },
  mounted() {
    var myChart = this.$echarts.init(document.getElementById("main"));

    myChart.setOption({
      backgroundColor: "#FFF",
      title: {
        text: "任务状态图",
        x: "center",
        y: "bottom",
        textStyle: {
          color: "#000"
        }
      },
      tooltip: {
        trigger: "item"
      },
      visualMap: {
        show: false,
        min: 80,
        max: 600,
        inRange: {
          colorLightness: [0, 1]
        }
      },
      series: [
        {
          name: "Access From",
          type: "pie",
          radius: "55%",
          center: ["50%", "50%"],
          data: [
            {
              value: 1,
              name: "Start",
              itemStyle: {
                color: "#388E3C"
              }
            },
            {
              value: 5,
              name: "Fail",
              itemStyle: {
                color: "#DD2C00"
              }
            },
            {
              value: 7,
              name: "End",
              itemStyle: {
                color: "#283593"
              }
            },
            {
              value: 3,
              name: "Run",
              itemStyle: {
                color: "#4527A0"
              }
            }
          ].sort(function(a, b) {
            return a.value - b.value;
          }),
          roseType: "radius",
          label: {
            color: "rgba(0,0,0, 1)"
          },
          labelLine: {
            lineStyle: {
              color: "rgba(0,0,0, 1)"
            },
            smooth: 0.2,
            length: 10,
            length2: 20
          },
          animationType: "scale",
          animationEasing: "elasticOut",
          animationDelay: function(idx) {
            return Math.random() * 200;
          }
        }
      ]
    });

    myChart = this.$echarts.init(document.getElementById("main2"));

    var option = {
      title: {
        text: "任务统计图",
        x: "center",
        y: "bottom",
        textStyle: {
          color: "#000"
        }
      },
      legend: {},
      tooltip: {
        trigger: "axis",
        showContent: false
      },
      dataset: {
        source: [
          ["product", "4/1", "4/2", "4/3", "4/4", "4/5", "4/6"],
          ["应用-彩色增强", 1, 5, 7, 3, 15, 3],
          ["应用-飞机特征提取", 2, 3, 5, 3, 1, 7],
          ["应用-获取河流数据", 12, 15, 14, 6, 15, 5],
          ["应用-信息提取", 2, 4, 5, 5, 5, 8]
        ]
      },
      xAxis: { type: "category" },
      yAxis: { gridIndex: 0 },
      grid: { top: "55%" },
      series: [
        {
          type: "line",
          smooth: true,
          seriesLayoutBy: "row",
          emphasis: { focus: "series" }
        },
        {
          type: "line",
          smooth: true,
          seriesLayoutBy: "row",
          emphasis: { focus: "series" }
        },
        {
          type: "line",
          smooth: true,
          seriesLayoutBy: "row",
          emphasis: { focus: "series" }
        },
        {
          type: "line",
          smooth: true,
          seriesLayoutBy: "row",
          emphasis: { focus: "series" }
        },
        {
          type: "pie",
          id: "pie",
          radius: "30%",
          center: ["50%", "25%"],
          emphasis: {
            focus: "self"
          },
          label: {
            formatter: "{b}: {@2012} ({d}%)"
          },
          encode: {
            itemName: "product",
            value: "2012",
            tooltip: "2012"
          }
        }
      ]
    };
    myChart.on("updateAxisPointer", function(event) {
      const xAxisInfo = event.axesInfo[0];
      if (xAxisInfo) {
        const dimension = xAxisInfo.value + 1;
        myChart.setOption({
          series: {
            id: "pie",
            label: {
              formatter: "{b}: {@[" + dimension + "]} ({d}%)"
            },
            encode: {
              value: dimension,
              tooltip: dimension
            }
          }
        });
      }
    });
    myChart.setOption(option);
  }
};
</script>
