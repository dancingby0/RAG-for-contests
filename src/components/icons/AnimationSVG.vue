<script setup lang="ts">
import {defineProps} from 'vue';
const props = defineProps<{
  stage:number
  content:string[]
}>()
// messageA , accA; messageB,accB


</script>

<template>
  <svg width="640" height="480" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
    <g class="layer">
      <title>Layer 1</title>
      <!--stage 1/9-->
      <path v-if="stage!=1&&stage!=9" d="m11.37,256l55.5,-37.5l55.5,37.5l-55.5,37.5l-55.5,-37.5z" fill="rgb(159.5, 206.5, 255)" id="svg_2" stroke="#000000"/>
      <path v-if="stage==1||stage==9" d="m11.37,256l55.5,-37.5l55.5,37.5l-55.5,37.5l-55.5,-37.5z" fill="rgb(179, 224.5, 156.5)" id="svg_2" stroke="#000000"/>
      <text fill="#000000" font-family="Serif" font-size="24" id="svg_3" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(0.70823 0 0 0.707242 39.7721 21.6594)" x="38.91" xml:space="preserve" y="341.22">前端界面</text>

      <!--stage 8-->
      <line v-if="stage!=8" fill="none" id="svg_26" stroke="#000000" transform="matrix(1 0 0 1 0 0)" x1="137.68" x2="241.68" y1="269.33" y2="270.33"/>
      <path v-if="stage!=8" d="m138.06,269.91l-13.37,-18l24.04,18l-24.04,18l13.37,-18z" fill="none" id="svg_25" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(178.686 136.714 269.91)"/>
      <line v-if="stage==8" fill="none" id="svg_26" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0)" x1="137.68" x2="241.68" y1="269.33" y2="270.33"/>
      <path v-if="stage==8" d="m138.06,269.91l-13.37,-18l24.04,18l-24.04,18l13.37,-18z" fill="none" id="svg_25" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(178.686 136.714 269.91)"/>
      <text v-if="stage==8" fill="#000000" font-family="Serif" font-size="24" id="svg_24" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) matrix(0.58731 0 0 0.743094 137.509 55.8078)" x="103.31" xml:space="preserve" y="309.96">{{props.content[0]}}</text>

      <!--stage 2-->
      <line v-if="stage!=2" fill="none" id="svg_23" stroke="#000000" transform="matrix(1 0 0 1 0 0)" x1="127.4" x2="237.4" y1="244.83" y2="245.83"/>
      <path v-if="stage!=2" d="m240.78,246.41l-13.37,-18l24.04,18l-24.04,18l13.37,-18z" fill="none" id="svg_22" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <line v-if="stage==2" fill="none" id="svg_23" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0)" x1="127.4" x2="237.4" y1="244.83" y2="245.83"/>
      <path v-if="stage==2" d="m240.78,246.41l-13.37,-18l24.04,18l-24.04,18l13.37,-18z" fill="none" id="svg_22" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0)"/>
      <text v-if="stage==2" fill="#000000" font-family="Serif" font-size="24" id="svg_21" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) matrix(0.58731 0 0 0.743094 137.509 55.8078)" x="75.59" xml:space="preserve" y="244.68">{{props.content[0]}}</text>

      <!--stage 6 B-->
      <line v-if="stage!=6" fill="none" id="svg_20" stroke="#000000" transform="matrix(1 0 0 1 0 0)" x1="390.14" x2="498.8" y1="313.36" y2="382.61"/>
      <path v-if="stage!=6" d="m488,389.48l20.69,8.65l-29.86,-3.2l11.48,-27.75l-2.3,22.3l-0.01,0z" fill="none" id="svg_19" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(-119.757 493.764 382.657)"/>
      <line v-if="stage==6" fill="none" id="svg_20" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0)" x1="390.14" x2="498.8" y1="313.36" y2="382.61"/>
      <path v-if="stage==6" d="m488,389.48l20.69,8.65l-29.86,-3.2l11.48,-27.75l-2.3,22.3l-0.01,0z" fill="none" id="svg_19" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(-119.757 493.764 382.657)"/>
      <text v-if="stage==6" fill="#000000" font-family="Serif" font-size="24" id="svg_18" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) rotate(33.255 434.638 365.091) matrix(0.58731 0 0 0.743094 137.509 55.8078)" x="505.91" xml:space="preserve" y="424.17">{{props.content[1]}}</text>

      <!--stage 4 B-->
      <line v-if="stage!=4" fill="none" id="svg_17" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(32.5157 458.134 328.181)" x1="379.51" x2="536.76" y1="328.54" y2="327.82"/>
      <path v-if="stage!=4" d="m394,293.95l20.69,8.65l-29.86,-3.2l11.48,-27.75l-2.3,22.3l-0.01,0z" fill="none" id="svg_16" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(67.3303 399.764 287.126)"/>
      <line v-if="stage==4" fill="none" id="svg_17" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(32.5157 458.134 328.181)" x1="379.51" x2="536.76" y1="328.54" y2="327.82"/>
      <path v-if="stage==4" d="m394,293.95l20.69,8.65l-29.86,-3.2l11.48,-27.75l-2.3,22.3l-0.01,0z" fill="none" id="svg_16" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(67.3303 399.764 287.126)"/>
      <text v-if="stage==4" fill="#000000" font-family="Serif" font-size="24" id="svg_15" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) rotate(33.1368 484.638 328.561) matrix(0.58731 0 0 0.743094 137.509 55.8078)" x="591.05" xml:space="preserve" y="375.01">{{props.content[2]}},{{props.content[3]}}</text>

      <!--stage 3/7-->
      <path v-if="stage!=3&&stage!=7" d="m245.85,262.58l71.5,-53.5l71.5,53.5l-71.5,53.5l-71.5,-53.5z" fill="rgb(159.5, 206.5, 255)" id="svg_14" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <path v-if="stage==3||stage==7" d="m245.85,262.58l71.5,-53.5l71.5,53.5l-71.5,53.5l-71.5,-53.5z" fill="rgb(179, 224.5, 156.5)" id="svg_14" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <text fill="#000000" font-family="Serif" font-size="24" id="svg_13" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0)" x="317.81" xml:space="preserve" y="273.91">服务器</text>

      <!--stage 5 A-->
      <path v-if="stage!=5" d="m482.76,77.62l62.5,-38l62.5,38l-62.5,38l-62.5,-38z" fill="rgb(159.5, 206.5, 255)" id="svg_12" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <path v-if="stage==5" d="m482.76,77.62l62.5,-38l62.5,38l-62.5,38l-62.5,-38z" fill="rgb(179, 224.5, 156.5)" id="svg_12" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <text fill="#000000" font-family="Serif" font-size="24" id="svg_11" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) matrix(0.558211 0 0 0.773608 213.308 114.524)" x="597.42" xml:space="preserve" y="-38.73">RAG客户端A</text>

      <!--stage 4 A-->
      <line v-if="stage!=4" fill="none" id="svg_10" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(-41.0159 425.391 156.927)" x1="341.1" x2="509.68" y1="156.43" y2="157.43"/>
      <path v-if="stage!=4" d="m480.12,113.92l20.69,8.65l-29.86,-3.2l11.48,-27.75l-2.3,22.3l-0.01,0z" fill="none" id="svg_9" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(174.371 485.883 107.1)"/>
      <line v-if="stage==4" fill="none" id="svg_10" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(-41.0159 425.391 156.927)" x1="341.1" x2="509.68" y1="156.43" y2="157.43"/>
      <path v-if="stage==4" d="m480.12,113.92l20.69,8.65l-29.86,-3.2l11.48,-27.75l-2.3,22.3l-0.01,0z" fill="none" id="svg_9" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(174.371 485.883 107.1)"/>
      <text v-if="stage==4" fill="#000000" font-family="Serif" font-size="24" id="svg_8" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) rotate(-41.0147 415.921 143.535) matrix(0.58731 0 0 0.743094 137.509 55.8078)" x="473.76" xml:space="preserve" y="126.02">{{props.content[0]}}</text>

      <!--stage 6 A-->
      <line v-if="stage!=6" fill="none" id="svg_7" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(-40.9308 436.527 181.591)" x1="361.17" x2="511.89" y1="181.57" y2="181.61"/>
      <path v-if="stage!=6" d="m-114.79,206.95l-13.37,-18l24.04,18l-24.04,18l13.37,-18z" fill="none" id="svg_6" stroke="#000000" transform="matrix(1 0 0 1 0 0) rotate(-5.6214 378.056 233.17) matrix(-0.859772 0.510678 -0.510678 -0.859772 383.89 470.407)"/>
      <line v-if="stage==6" fill="none" id="svg_7" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(-40.9308 436.527 181.591)" x1="361.17" x2="511.89" y1="181.57" y2="181.61"/>
      <path v-if="stage==6" d="m-114.79,206.95l-13.37,-18l24.04,18l-24.04,18l13.37,-18z" fill="none" id="svg_6" stroke="rgb(179, 224.5, 156.5)" transform="matrix(1 0 0 1 0 0) rotate(-5.6214 378.056 233.17) matrix(-0.859772 0.510678 -0.510678 -0.859772 383.89 470.407)"/>
      <text v-if="stage==6" fill="#000000" font-family="Serif" font-size="24" id="svg_5" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) rotate(-41.8131 455.526 184.47) matrix(0.58731 0 0 0.743094 137.509 55.8078)" x="541.48" xml:space="preserve" y="181.11">{{props.content[0]}},{{props.content[1]}}</text>

      <!--stage 5 B-->
      <path v-if="stage!=5" d="m498.3,405.38l62.5,-38l62.5,38l-62.5,38l-62.5,-38z" fill="rgb(159.5, 206.5, 255)" id="svg_4" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <path v-if="stage==5" d="m498.3,405.38l62.5,-38l62.5,38l-62.5,38l-62.5,-38z" fill="rgb(179, 224.5, 156.5)" id="svg_4" stroke="#000000" transform="matrix(1 0 0 1 0 0)"/>
      <text fill="#000000" font-family="Serif" font-size="24" id="svg_1" stroke="#000000" stroke-width="0" text-anchor="middle" transform="matrix(1 0 0 1 0 0) matrix(0.558211 0 0 0.773608 228.851 442.287)" x="597.42" xml:space="preserve" y="-38.73">RAG客户端B</text>
    </g>
  </svg>
</template>

<style scoped>

</style>

