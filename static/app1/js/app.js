const {createApp, ref} = Vue;

try {
    main;
} catch (error) {
    console.error(error); // 输出错误信息，例如 "ReferenceError: App is not defined"
    const main = {};
}

const app = createApp(main)
window.app = app

