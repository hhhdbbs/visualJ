<template>
  <g>
    <path
      class="connector only-watch-el"
      :d="dragLinkPath()"
      @contextmenu.prevent="show"
    />
  </g>
</template>
<script>
export default {
  name: "SimulateArrow",
  props: {
    dragLink: Object
  },
  methods: {
    dragLinkPath() {
      const { fromX, fromY, toX, toY } = this.dragLink;
      return `M ${fromX} ${fromY} Q ${fromX + 30} ${fromY}  ${(toX + fromX) /
        2} ${(fromY + toY) / 2} T ${toX} ${toY}`;
    },
    show() {
      alert(1);
    }
  }
};
</script>
<style scoped>
.connector {
  stroke: hsla(224, 90%, 69%, 0.6);
  stroke-width: 2px;
  fill: none;
  position: relative;
  z-index: 2;
}
.only-watch-el {
  pointer-events: none;
}
</style>
