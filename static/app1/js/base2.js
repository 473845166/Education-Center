const {computed,ref,defineComponent} = Vue;
app.component('CounterOne0', defineComponent({
    props: ['index'],
    setup() {
        const images = [
            'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
            'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
        ];
        const currentRate = ref(0);
        const text = computed(() => currentRate.value.toFixed(0) + '%');
        const gradientColor = {
            '0%': 'blue',
            '100%': 'red',
        };
        const activeNames = ref(['1']);
        return {
            text,
            currentRate,
            images,
            rate:70,
            gradientColor,
            activeNames,
        };
    },
    template: `<div class="te">
    <div class="te_s1">
        <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white" lazy-render>
    <van-swipe-item v-for="image in images" :key="image">
        <img :src="image" />
      </van-swipe-item>
    </van-swipe>
</div>
<div class="te_s2">
    <van-circle v-model:current-rate="currentRate"
  :rate="rate"
  :color="gradientColor"
  text="星期一剩余20"/>
  <van-circle v-model:current-rate="currentRate"
  :rate="rate"
  layer-color="#ebedf0"
  text="星期二"/>
  <van-circle v-model:current-rate="currentRate"
  :rate="rate"
  layer-color="#ebedf0"
  text="星期三"/>
  <van-circle v-model:current-rate="currentRate"
  :rate="rate"
  layer-color="#ebedf0"
  text="星期四"/>
  <van-circle v-model:current-rate="currentRate"
  :rate="rate"
  layer-color="#ebedf0"
  text="星期五"/>
</div>
<div>
<h2 class="van-doc-demo-block__title" id="ji-chu-yong-fa">基础用法</h2>
<van-collapse v-model="activeNames">
  <van-collapse-item title="标题1" name="1">
    <p>代码是写出来给人看的，附带能在机器上运行。</p>
    <van-button plain >朴素按钮</van-button>
        <van-button plain >朴素按钮</van-button>
            <van-button plain >朴素按钮</van-button>
                <van-button plain >朴素按钮</van-button>
  </van-collapse-item>
  <van-collapse-item title="标题2" name="2">
    技术无非就是那些开发它的人的共同灵魂。
  </van-collapse-item>
  <van-collapse-item title="标题3" name="3">
    在代码阅读过程中人们说脏话的频率是衡量代码质量的唯一标准。
  </van-collapse-item>
</van-collapse>
</div>
    </div>

`,
}))
app.component('CounterOne1', Vue.defineComponent({
    props: ['index'],
    template: `
    
    `,
}))
app.component('CounterOne2', Vue.defineComponent({
    props: ['index'],
    template: ``,
}))
