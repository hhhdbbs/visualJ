<template>
  <v-card height="100%">
    <v-card-title>更多参数设置</v-card-title>
    <v-card-text>
      <v-row v-for="item in disabledInfo" :key="item.name">
        <v-col cols="12">
          <v-text-field
            :label="item.name"
            v-model="item.value"
            disabled
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row v-for="item in abledInfo" :key="item.name">
        <v-col cols="8">
          <v-text-field
            :label="item.name"
            v-model="item.value"
            :hint="item.description"
          ></v-text-field>
        </v-col>
        <v-col cols="4" v-if="item.parameter_type=='output'">
          <v-checkbox
            v-model="item.export"
            label="导出"
          ></v-checkbox>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
export default {
  name: "OperatorInfo",
  props: {
    abledInfo: Array,
    disabledInfo: Array
  },
  data(){
    return{
      dd:false
    }
  },
  methods: {}
};
</script>
