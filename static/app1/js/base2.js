const {computed, ref, defineComponent} = Vue;
app.component('CounterOne0', defineComponent({
    props: ['index'],
    setup() {
        const images = [
            'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
            'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
        ];
        const currentRate = ref(0);
        const show = ref(false);

        const activeNames = ref(['1']);
        return {
            currentRate,
            images,
            activeNames,
            show,
        };
    },
    template: `<div class="te">
<van-action-sheet v-model:show="show" title="标题">
  <div class="content">内容</div>
</van-action-sheet>
    <div class="te_s1">
        <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white" lazy-render>
    <van-swipe-item v-for="image in images" :key="image">
        <img :src="image" />
      </van-swipe-item>
    </van-swipe>
</div>
<div>
<h2 class="van-doc-demo-block__title" id="ji-chu-yong-fa">基础用法</h2>
<van-collapse v-model="activeNames">
  <van-collapse-item title="标题1" name="1">
    <p>代码是写出来给人看的，附带能在机器上运行。</p>
    <van-button @click="show = !show" round type="danger" style="width: 100%">立即预约</van-button>
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
app.component('CounterOne1', {
    props: ['index'],
    template: `
<div class="van-doc-demo-block">
  <div class="van-doc-demo-block__title">已经预约</div>
  <div class="van-doc-demo-block__card">
    <van-cell name="slider" is-link title="基础用法" @click="show = true" />
    
        <van-dialog v-model:show="show" title="标题" show-cancel-button>
          <img src="https://fastly.jsdelivr.net/npm/@vant/assets/apple-3.jpeg" />
        </van-dialog>
  </div>
</div>
        
    `,
    setup() {
        const show = ref(false);
        const themeVars = Vue.reactive({
      rateIconFullColor: '#07c160',
      sliderBarHeight: '4px',
      sliderButtonWidth: '20px',
      sliderButtonHeight: '20px',
      sliderActiveBackground: '#07c160',
      buttonPrimaryBackground: '#07c160',
      buttonPrimaryBorderColor: '#07c160',
    });
        return {
            show,themeVars
        }
    }
})
app.component('CounterOne2', {
    props: ['index'],
    template: `
    <div style="margin:20px;">
        <van-card
                desc="描述信息：用户正常"
                title="{{ request.user.info1.nickname }}"
                thumb="{{ request.user.info1.headimgurl }}"
        />
    </div>
    <div style="margin-top:30px;margin-bottom: 10px">
        <van-cell title="更新个人信息" label="同步微信头像昵称" is-link @click="up_center()"/>
    </div>
    <div style="margin-top:30px;margin-bottom: 10px;">
        <van-cell title="修改资料" is-link @click="up_user"/>
    </div>
    <div style="margin-top:30px;margin-bottom: 10px">
        <van-cell title="联系站长qq" is-link @click="qq"/>
    </div>
    <div style="margin-top:30px;margin-bottom: 10px">
        <van-cell title="退出登录" is-link @click="logout"/>
    </div>  
    `,
    data() {
        return {
            show: ref(false),
        }
    },
    methods: {
        up_center () {
                    const dome_host = '{{ dome_host|safe }}';
                    const APPID = '{{ APPID|safe }}';
                    vant.showConfirmDialog({
                        title: '更新昵称，头像',
                        message:
                            '确定更新吗？',
                    })
                        .then(() => {
                            location.href = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=' + APPID + '&redirect_uri=http://' + dome_host + '/up_wx&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
                        })
                        .catch(() => {
                            // on cancel
                        });
                },
        up_user() {
            location.href = 'up_data'
        },
        logout() {
            vant.showConfirmDialog({
                title: '退出登录',
                message:
                    '确定退出吗？',
            })
                .then(() => {
                    location.href = "/logout/"
                })
                .catch(() => {
                    // on cancel
                });
        },
        qq() {
            location.href = 'https://wpa.qq.com/msgrd?v=3&site=qq&menu=yes&uin=473845166'
        }
    }
})
