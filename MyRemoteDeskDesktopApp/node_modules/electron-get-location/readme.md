# electron-get-location

> Get user's accurate location in Electron for macOS

## Install

```
$ npm install electron-get-location
```

Requires macOS 10.11 or later.

## Usage

```js
const getLocation = require('electron-get-location')

;(async () => {
	console.log(await getLocation())
	//=> 2.3455,34,33122
})()
```

## Inspired

Inspired by the one and only [Sindre Sorhus](https://sindresorhus.com). Support him on his Patreon: https://www.patreon.com/sindresorhus

- [is-camera-on-cli](https://github.com/sindresorhus/is-camera-on-cli) - CLI for this module

## Support Me

https://patreon.com/morajabi

## License

MIT © [Sindre Sorhus](https://sindresorhus.com)
