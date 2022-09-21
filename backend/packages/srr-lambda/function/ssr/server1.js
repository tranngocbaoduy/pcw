// #!/usr/bin/env node

// const fs = require('fs');
// const express = require('express');
// const { createBundleRenderer } = require('vue-server-renderer');

// const bundleRenderer = createBundleRenderer(
//   // Load SSR bundle
//   require('./dist/vue-ssr-bundle.json'),
//   {
//     template: fs.readFileSync('./index.html', 'utf-8')
//   }
// );

// // Khởi tạo express
// const app = express();

// // Serve static assets from ./dist on the /dist route.
// app.use('/dist', express.static('dist'));

// // Render tất cả routes
// app.get('*', (req, res) => {
//   bundleRenderer
//     .renderToStream({ url: req.path })
//     .pipe(res);
// });

// app.listen(8080);


const serverless = require('serverless-http');
const express = require('express');
const app = express();
const fs = require('fs');
const { createBundleRenderer } = require('vue-server-renderer');

const bundleRenderer = createBundleRenderer(
  // Load SSR bundle
  require('./dist/vue-ssr-bundle.json'),
  {
    template: fs.readFileSync('./index.html', 'utf-8')
  }
);
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Serve static assets from ./dist on the /dist route.
app.use('/dist', express.static('dist'));

// Render tất cả routes
app.get('*', (req, res) => {
  bundleRenderer
    .renderToStream({ url: req.path })
    .pipe(res);
});

// app.listen(3000, () => console.log(`Listening on: 3000`));
exports.lambdaHandler = serverless(app);

// serverless config credentials --provider aws --key AKIAS2TFO5CFGMNQWS4L ?secret 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
