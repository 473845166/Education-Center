const {computed, ref, defineComponent} = Vue;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
app.component('CounterOne0', defineComponent({
    props: ['index'],
    setup() {
        const images = [
            'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
            'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
        ];
        const currentRate = ref(0);
        const show = ref(false);
        const activeNames = ref();
        const checked = ref();
        const record = (pk) => {
            show.value = true
            axios({
                method: 'post',
                url: '/get_model/',
                headers: {'X-CSRFToken': csrftoken},
                data: JSON.stringify({'id': pk})
            }).then(res => {
                rds.value = res.data
            });
        }
        const submit = () => {
            axios({
                method: 'post',
                url: '',
                headers: {'X-CSRFToken': csrftoken},
                data: JSON.stringify({'checked': checked.value})
            }).then(res => {
                vant.showDialog({
                    message: res.data.mgs,
                    theme: 'round-button',
                }).then(() => {
                    // on close
                });
            }).catch(error => {
                console.log(error)
                vant.showDialog({
                    message: error.response.data,
                }).then(() => {
                    // on close
                });
            });
            console.log(checked.value, 'checked')
            show.value = false
        }
        const rds = ref([])
        return {
            currentRate,
            images,
            activeNames,
            show,
            sl,
            checked,
            record,
            submit,
            rds,
        };
    },
    mounted() {
        this.$refs.collapse.toggleAll(true);
    },
    template: `<div class="te">
<van-action-sheet v-model:show="show" title="选择时段">
  <div class="content">
  <van-radio-group v-model="checked">
  <van-cell-group inset>
    <van-cell v-for="rd in rds" :title="rd.fields.start_time+'至'+rd.fields.end_time"  clickable @click="checked = rd.pk">
      <template #right-icon>
        <van-radio :name="rd.pk" />
      </template>
    </van-cell>
  </van-cell-group>
</van-radio-group>
            <van-button @click="submit" round type="primary" style="width: 100%;position: fixed;bottom: 0;left: 0;right: 0;">确定</van-button>
</div>
</van-action-sheet>
    <div class="te_s1">
        <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white" lazy-render>
    <van-swipe-item v-for="image in images" :key="image">
        <img :src="image" />
      </van-swipe-item>
    </van-swipe>
</div>
    <div>
        <h2 class="van-doc-demo-block__title" id="ji-chu-yong-fa">可预约</h2>
        <van-collapse v-model="activeNames" ref="collapse">
          <van-collapse-item v-for="i in sl" :title="i.fields.event">
            <p v-if="i.status==1" style="color: red">开放时间 {{ i.fields.start_time }}至{{ i.fields.end_time }}</p>
            <p v-else >开放时间 {{ i.fields.start_time }}至{{ i.fields.end_time }}</p>
            <van-button @click="record(i.pk)" round type="danger" style="width: 100%">立即预约</van-button>
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
    <van-cell v-for="re in record" :name="re.reserve__pk" is-link :title="re.reserve__event" @click="cat_record(re.pk)" />
        <van-dialog v-if="info" cancel-text="取消更改" v-model:show="show" title="详细" show-cancel-button>
          <div style="margin: 20px"><h5>预约事件：{{info.reserve__event}} </h5></div>
          <div  class="van-doc-demo-block__title">预约人：{{ info.user__name }}</div>
          <p style="margin: 20px">电话：{{info.user__telephone_number}}</p>
          <p style="margin: 20px">时间：{{ info.submit }}</p>
          <van-tag round type="primary" style="margin: 20px">公司：{{ info.user__company }}</van-tag>
        </van-dialog>
  </div>
</div>
    `,
    setup() {
        const show = ref(false);
        const cat_record = (index) => {
            show.value = true
            axios({
                method: 'post',
                url: '/get_record/',
                headers: {'X-CSRFToken': csrftoken},
                data: index
            }).then(res => {
                console.log(res.data.info)
                info.value = res.data.info[0]
            });
        }
        const info = ref()
        return {
            show, record, cat_record, info
        }
    }
})
app.component('CounterOne2', {
    props: ['index'],
    template: `
        <van-dialog v-model:show="show" title="详细">
          <p style="margin: 20px">姓名：{{ my_info[0].fields.name }}</p>
          <p style="margin: 20px">电话：{{ my_info[0].fields.telephone_number }}</p>
          <p style="margin: 20px">公司：{{ my_info[0].fields.company }}</p>
        </van-dialog>
    <div style="margin:20px;">
        <van-card
                desc="描述信息：用户正常"
                :title="name"
                thumb="static/app1/icon/头像 简约男士.png"
        />
    </div>
    <div style="margin-top:30px;margin-bottom: 10px">
        <van-cell title="查看信息" label="个人资料" is-link @click="show = !show"/>
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
            show: ref(false), my_info, name: my_info[0].fields.name
        }
    },
    methods: {
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
