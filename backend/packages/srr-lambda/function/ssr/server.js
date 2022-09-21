// https://gist.github.com/furkan3ayraktar/2ba5e34985addc4107dc417399be2b9d
const path = require('path');
const https = require('https');
const zlib = require('zlib');
const logger = require('./logging').getLogger();

const downloadContent = (url, callback) => {
    https.get(url, (res) => {
        let response;
        let body = '';
        if (res.headers['content-encoding'] === 'gzip') {
            response = res.pipe(zlib.createGunzip());
        } else {
            response = res;
        }
        response.on('data', (chunk) => {
            body += chunk;

        });
        response.on('end', () => {
            callback(true, body, res.headers);
        });
    }).on('error', (e) => callback(false, e));
};

const fetchMetaData = (url, callback) => {
    downloadContent(url, (isOk, result, headers) => {
        if (!isOk) {
            console.log('Error fetching meta data:', result);
            callback(false);
        } else {
            const metaData = JSON.parse(result).data;
            console.log('[META DATA] =>', metaData)
            let metaTags = '';
            if (metaData) {
                if (metaData.title) {
                    metaTags += '<title>' + metaData.title + '</title>';
                    metaTags += '<meta property=\"og:title\" content=\"' + metaData.title + '\" />';
                }

                if (metaData.description) {
                    metaTags += '<meta name=\"description\" content=\"' + metaData.description + '\" />';
                    metaTags += '<meta property=\"og:description\" content=\"' + metaData.description + '\" />';
                }

                if (metaData['viewport']) metaTags += '<meta name=\"viewport\" content=\"' + metaData['viewport'] + '\" />';
                if (metaData['robots']) metaTags += '<meta name=\"robots\" content=\"' + metaData['robots'] + '\" />';
                if (metaData['keywords']) metaTags += '<meta name=\"keywords\" content=\"' + metaData['keywords'] + '\" />';
                if (metaData['og:type']) metaTags += '<meta name=\"og:type\" content=\"' + metaData['og:type'] + '\" />';
                if (metaData['og:site_name']) metaTags += '<meta name=\"og:site_name\" content=\"' + metaData['og:site_name'] + '\" />';
                if (metaData['og:url']) metaTags += '<meta name=\"og:url\" content=\"' + metaData['og:url'] + '\" />';
                if (metaData['og:image']) metaTags += '<meta name=\"og:image\" content=\"' + metaData['og:image'] + '\" />';
                if (metaData['og:image:width']) metaTags += '<meta name=\"og:image:width\" content=\"' + metaData['og:image:width'] + '\" />';
                if (metaData['og:image:height']) metaTags += '<meta name=\"og:image:height\" content=\"' + metaData['og:image:height'] + '\" />';
            }

            callback(true, metaTags, headers);
        }
    });
};

const fetchIndexHtmlAndCreateCloudFrontResponse = (url, metaTags, metaHeaders, callback) => {
    console.log('[FETCH CONTENT URL] =>', url)
    downloadContent(url, (isOk, result, headers) => {
        if (!isOk) {
            console.log('Error fetching content:', result);
            callback(false);
        } else {
            // We have <title>House of Radon</title> inside the actual index.html. We use that part to replace with actual metadata.
            const finalBody = result.replace('<title>PCW ー Trang web so sánh giá hàng đầu</title>', metaTags);
            const buffer = zlib.gzipSync(finalBody);
            const base64EncodedBody = buffer.toString('base64');

            const responseHeaders = {
                'content-type': [{ key: 'Content-Type', value: 'text/html' }],
                'content-encoding': [{ key: 'Content-Encoding', value: 'gzip' }],
                'accept-ranges': [{ key: 'Accept-Ranges', value: 'bytes' }]
            };

            let eTag = '';

            if (metaHeaders) {
                const metaEtag = metaHeaders['etag'];

                if (metaEtag) {
                    eTag = metaEtag.replace(/"/g, '');
                }
            }

            if (headers) {
                const lastModified = headers['last-modified'];
                const cacheControl = headers['cache-control'];
                const contentETag = headers['etag'];

                if (lastModified) {
                    responseHeaders['last-modified'] = [{ key: 'Last-Modified', value: lastModified }]
                }

                if (cacheControl) {
                    responseHeaders['cache-control'] = [{ key: 'Cache-Control', value: cacheControl }]
                }

                if (contentETag) {
                    eTag += contentETag.replace(/"/g, '');;
                }
            }

            if (eTag !== '') {
                responseHeaders['etag'] = [{ key: 'ETag', value: eTag }]
            }

            const newResponse = {
                status: '200',
                statusDescription: 'OK',
                headers: responseHeaders,
                body: base64EncodedBody,
                bodyEncoding: 'base64',
            };

            callback(true, newResponse);
        }
    });
};

function isGetMetaData(request) {
    const BASE_URL = 'https://x-pcw.store'
    const urlObj = new URL(`${BASE_URL}${request.uri}`)
    const parsedPath = path.parse(urlObj.pathname);
    if (['.js', '.css', '.html', '.png', '.jpeg', '.jpg', '.json'].includes(parsedPath.ext)) return false;
    if (Object.keys(urlObj.searchParams).includes('isMeta')) return false;
    let isCanGetMetaData = (parsedPath.ext === '' || parsedPath.ext.includes('.'))
    if (isCanGetMetaData) return getMetaURL(request, parsedPath)
    return ''
}

function getMetaURL(request, parsedPath) {
    const BASE_URL_API = 'https://16c8z3zwx3.execute-api.ap-southeast-1.amazonaws.com'
    const STAGE_NAME = 'dev'
    let metaUrl = '';
    if (request.uri.includes('/category/')) {
        const id = parsedPath.base;
        metaUrl = `${BASE_URL_API}/${STAGE_NAME}/api/meta-data?action=category&id=${id}`;
    } else if (request.uri.split('.').length > 2) {
        const listStringUri = request.uri.split('.');
        const idCategory = listStringUri[listStringUri.length - 1].slice(6, 11);
        const idProd = listStringUri[listStringUri.length - 2]
        metaUrl = `${BASE_URL_API}/${STAGE_NAME}/api/meta-data?action=product&idCate=${idCategory}&id=${idProd}`;
    } else {
        metaUrl = `${BASE_URL_API}/${STAGE_NAME}/api/meta-data?action=default`;
    }
    return metaUrl
}

exports.lambdaHandler = (event, context, callback) => {
    const { request, config } = event.Records[0].cf;
    const BASE_URL = 'https://x-pcw.store'
    const metaUrl = isGetMetaData(request);
    console.log('[START] => ', request.uri)
    if (metaUrl != '') {
        fetchMetaData(metaUrl, (isOk, metaTags, metaHeaders) => {
            console.log('[GET META URL] => ', isOk, metaUrl, metaTags)
            if (!isOk) {
                return callback(null, request); // Return same request so CloudFront can process as usual.
            } else {
                const contentUrl = `${BASE_URL}/index.html`;
                const contentUrlObj = new URL(contentUrl)
                contentUrlObj.searchParams.append('isMeta', true);
                fetchIndexHtmlAndCreateCloudFrontResponse(contentUrlObj.href, metaTags, metaHeaders, (isOk, newResponse) => {
                    console.log('[GET CONTENT URL] => ', isOk, contentUrl)
                    if (!isOk) {
                        return callback(null, request);
                    } else {
                        return callback(null, newResponse);
                    }
                });
            }
        });
    } else {
        return callback(null, request);
    }
};