<template>
  <div id="o_point_edit">
    <div id="o_point_edit_body">
      <div
        id="o_point_edit_circle"
        style="width:100%;"
        class="d-flex justify-center"
      >
        <div
          v-for="(item, i) in opInformation.input_num"
          :key="i"
          style="width:20%"
        >
          <svg
            class="icon edit_circle edit_circle_top"
            aria-hidden="true"
            @mouseup="$emit('linkEnd', $event, index, taskID, i)"
          >
            <use xlink:href="#icon-yuanquan"></use>
          </svg>
        </div>
      </div>
      <div
        id="o_point_edit_circle"
        style="width:100%;top:100%;"
        class="d-flex justify-center"
      >
        <div
          v-for="(item, i) in opInformation.output_num"
          :key="i"
          style="width:20%"
        >
          <svg
            class="icon edit_circle edit_circle_top"
            aria-hidden="true"
            @mousedown="
              $emit(
                'linkPre',
                $event,
                index,
                taskID,
                opInformation.input_num + i
              )
            "
          >
            <use xlink:href="#icon-yuanquan"></use>
          </svg>
        </div>
      </div>
      <div style="position:relative" :class="false ? 'pane-node-content selected' : 'pane-node-content'">
        <i :type="`icon icon-data`" />
        <span class="icon" style="width: 26px;height: 26px;"/>
        <span class="name">{{ opInformation.name }}</span>
        <v-btn
          @click="$emit('delTask', index, taskID)"
          text
          style=";position:relative;padding-bottom:5px;padding-left:10px;padding-right:0px;min-width:0"
        >
          <svg class="icon" aria-hidden="true" style="color:#B71C1C;background-color:transparent;font-size:20px">
            <use xlink:href="#icon-shanchu"></use>
          </svg>
        </v-btn>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "OPointEdit",
  props: {
    opInformation: Object,
    taskID: Number,
    index: Number
  },
  methods: {}
};
</script>
<style scoped>
#o_point_edit {
  position: relative;
  width: 300px;
}
#o_point_edit_body {
  position: absolute;
  z-index: 1;
}
#o_point_edit_circle {
  position: absolute;
  left: 0;
  z-index: 3;
}
.edit_circle {
  position: relative;
  color: rgb(216, 229, 247);
}
.edit_circle_top {
  left: 50%;
  transform: translate(-50%, -80%);
}
.pane-node-content {
  box-sizing: border-box;
  width: 180px;
  height: 30px;
  background-color: hsla(0, 0%, 100%, 0.9);
  border: 1px solid #289de9;
  border-radius: 15px;
  font-size: 12px;
  -webkit-transition: background-color 0.2s;
  transition: background-color 0.2s;
}
.pane-node-content .icon {
  margin: 1px;
  border-radius: 100%;
  float: left;
  color: #fff;
  font-size: 26px;
  background-color: #289de9;
}
.pane-node-content .name {
  margin-left: 2px;
  width: 135px;
  line-height: 28px;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
  height: 26px;
  background: transparent;
  border: none;
}
.selected {
  background: rgba(227, 244, 255, 0.9) !important;
}
</style>
