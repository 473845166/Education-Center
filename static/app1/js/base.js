const Main = {
    data() {
        const active = Vue.ref(0);
        const show = true;
        const icon = {
            active1: '/static/app1/icon/立即预约 (1).png',
            inactive1:
                '/static/app1/icon/立即预约.png',
            active2: '/static/app1/icon/_历史小.png',
            inactive2:
                '/static/app1/icon/bg-history.png',
            active3: '/static/app1/icon/个人中心 个人中心2.png',
            inactive3:
                '/static/app1/icon/个人中心.png',
        };
        return {
            show,
            icon,
            active,
            currentComponent: `CounterOne${active.value}`,
            index: active
        }
    },
    mounted() {
        setTimeout(() => {
            this.show = false;
        }, 500); // 等待三秒钟后将show设置为true
    },
    methods: {
        onChange(index) {
            NProgress.start();
            this.currentComponent = `CounterOne${index}`
            this.index = index
            NProgress.done();
        }
    }
};
window.main = Main