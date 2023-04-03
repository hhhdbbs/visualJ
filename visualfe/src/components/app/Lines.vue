<template>
  <g @mouseup="mouseUp">
    <g v-for="(item, index) in lines" :key="index">
      <path
        :class="hoverIndex == index ? 'editLine' : 'defaultLine'"
        :d="dragLinkPath(item)"
        @mouseover="pathHover(index)"
        @mouseup="handlePath($event, index)"
      />
    </g>
    <g
      v-if="menuInfo.showMenu"
      :transform="
        `translate(${menuInfo.menuPos.offsetX}, ${menuInfo.menuPos.offsetY})`
      "
    >
      <foreignObject width="140" height="30" style="overflow: visible;">
        <div style="width:100%">
          <v-btn width="100%" color="error" @mouseup="deleteLine($event)"
            >删除</v-btn
          >
        </div>
      </foreignObject>
    </g>
  </g>
</template>
<script>
export default {
  name: "Lines",
  props: {
    lines: Array,
    menuInfo: Object
  },
  data() {
    return {
      hoverIndex: -1
    };
  },
  methods: {
    mouseUp() {
      //  this.menuInfo.showMenu = false;
    },
    initPos() {
      let { left, top } = document
        .getElementById("svgContent")
        .getBoundingClientRect();
      this.Pos = { x: left, y: top };
    },
    pathHover(index) {
      this.hoverIndex = index;
    },
    pathOut() {
      this.hoverIndex = -1;
    },
    deleteLine(e) {
      // console.log(this.hoverIndex)
      this.lines.splice(this.hoverIndex, 1);
      this.menuInfo.showMenu = false;
      window.event ? (window.event.cancelBubble = true) : e.stopPropagation();
      this.hoverIndex = -1;
    },
    dragLinkPath(dragLink) {
      var {
        from_node_circle: { pos_x: fromX, pos_y: fromY },
        to_node_circle: { pos_x: toX, pos_y: toY }
      } = dragLink;
    
      return `M ${fromX} ${fromY} Q ${fromX + 30} ${fromY}  ${(toX + fromX) /
        2} ${(fromY + toY) / 2} T ${toX} ${toY}`;
    },
    handlePath(e, index) {
      const { offsetX, offsetY } = e;
      const menuPos = {
        offsetX,
        offsetY
      };
      this.$emit("showMenu", menuPos);
      e.preventDefault();
      window.event ? (window.event.cancelBubble = true) : e.stopPropagation();
    }
  }
};
</script>
<style scoped>
.defaultLine {
  stroke: #00c0ff;
  stroke-width: 2px;
  fill: transparent;
  cursor: pointer;
  stroke-dasharray: 5px;
  stroke-dashoffset: 1000px;
  animation: grown 40s infinite linear;
}
@keyframes grown {
  to {
    stroke-dashoffset: 0;
  }
}
@keyframes line_success {
  0% {
    stroke-dashoffset: 100%;
  }
  100% {
    stroke-dashoffset: 0%;
  }
}
.editLine {
  stroke: hsla(12, 91%, 42%, 0.6);
  stroke-width: 5px;
  fill: transparent;
  cursor: pointer;
}
</style>
