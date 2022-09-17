const winston = require('winston');

if (!('toJSON' in Error.prototype))
  Object.defineProperty(Error.prototype, 'toJSON', {
    value: function () {
      const alt = {};
      Object.getOwnPropertyNames(this).forEach((key) => (alt[key] = this[key]), this);
      return alt;
    },
    configurable: true,
    writable: true,
  });

/** @type {Object.<string, import('winston').Logger>} */
const loggers = {};

module.exports.resetDefaultMeta = () => {
  for (const key in loggers) {
    loggers[key].defaultMeta = {};
  }
};

module.exports.getLogger = (name = 'default') => {
  if (!loggers[name]) {
    loggers[name] = winston.createLogger({
      level: process.env.LOG_LEVEL || 'debug',
      format: winston.format.combine(
        winston.format.errors({ stack: true }),
        winston.format.timestamp(),
        winston.format((info) => {
          info.level = info.level.toUpperCase();
          const infoOrdered = {};
          infoOrdered['timestamp'] = info['timestamp'];
          infoOrdered['level'] = info['level'];
          infoOrdered['message'] = info['message'];
          Object.assign(infoOrdered, info);
          if (info instanceof Error) {
            infoOrdered.code = info.code || info.name;
            infoOrdered.name = info.name;
            infoOrdered.stackTrace = info.stack;
            delete infoOrdered.stack;
          }
          return infoOrdered;
        })(),
        winston.format.json()
      ),
      transports: [new winston.transports.Console()],
      defaultMeta: {},
    });
  }
  return loggers[name];
};
