module.exports = {
  pwa: {
    workbox: {
      config: {
        debug: true,
      },
    },
    //workboxPluginMode: 'GenerateSW',
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      swSrc: 'src/service-worker.js',
    },
  },
  transpileDependencies: ['vuetify'],
  pluginOptions: {
    i18n: {
      locale: 'vn',
      fallbackLocale: 'vn',
      localeDir: 'locales',
      enableInSFC: false,
    },
  },

  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      // https://github.com/jaketrent/html-webpack-template
      args[0].title = 'PCW ー Trang web so sánh giá hàng đầu';
      args[0].lang = 'vi-VN';
      // args[0].meta = [
      //   {
      //     name: 'title',
      //     content: 'PCW ー Trang web so sánh giá hàng đầu',
      //   },
      //   {
      //     name: 'description',
      //     content: 'Tìm ra giá phù hợp cho tất cả sản phẩm mà bạn tìm kiếm - Hỗ trợ so sánh trên nhiều nền tảng bán hàng online',
      //   },
      //   {
      //     name: 'og:type',
      //     content: 'website',
      //   },
      //   {
      //     name: 'og:site_name',
      //     content: 'x-pcw.store',
      //   },
      //   {
      //     name: 'og:url',
      //     content: 'https://x-pcw.store',
      //   },
      //   {
      //     name: 'og:image',
      //     content: 'logo.png'
      //   },
      //   {
      //     name: 'og:image:type',
      //     content: 'image/png',
      //   },
      //   {
      //     name: 'og:image:width',
      //     content: '600',
      //   },
      //   {
      //     name: 'og:image:height',
      //     content: '200',
      //   },
      // ];
      return args;
    });
    config.module
      .rule('i18n')
      .resourceQuery(/blockType=i18n/)
      .type('javascript/auto')
      .use('i18n')
      .loader('@kazupon/vue-i18n-loader')
      .end();

    config.plugins.delete('preload');
    config.plugins.delete('prefetch');
  },
};
