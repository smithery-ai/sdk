# JavaScript SDK for ngrok

[![npm.rs][npm-badge]][npm-url]
[![MIT licensed][mit-badge]][mit-url]
[![Apache-2.0 licensed][apache-badge]][apache-url]
[![Continuous integration][ci-badge]][ci-url]

[npm-badge]: https://img.shields.io/npm/v/@ngrok/ngrok.svg
[npm-url]: https://www.npmjs.com/package/@ngrok/ngrok
[mit-badge]: https://img.shields.io/badge/license-MIT-blue.svg
[mit-url]: https://github.com/ngrok/ngrok-rust/blob/main/LICENSE-MIT
[apache-badge]: https://img.shields.io/badge/license-Apache_2.0-blue.svg
[apache-url]: https://github.com/ngrok/ngrok-rust/blob/main/LICENSE-APACHE
[ci-badge]: https://github.com/ngrok/ngrok-javascript/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/ngrok/ngrok-javascript/actions/workflows/ci.yml

`ngrok-javascript` is the official Node.js SDK for ngrok that requires no binaries. Quickly enable secure production-ready connectivity to your applications and services directly from your code.

[ngrok](https://ngrok.com) is a globally distributed gateway that provides secure connectivity for applications and services running in any environment.

# Installation

Using npm:

```shell
npm install @ngrok/ngrok
```

Using yarn:

```shell
yarn add @ngrok/ngrok
```

Using pnpm:

```shell
pnpm add @ngrok/ngrok
```

# Quickstart

1. [Install `@ngrok/ngrok`](#installation)
2. Export your authtoken from [the ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken) as `NGROK_AUTHTOKEN` in your terminal
3. Add the following code to your application to establish connectivity via the [forward method](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-forward-minimal.js) through port `8080` over `localhost`:

    ```jsx
    // Require ngrok javascript sdk
    const ngrok = require("@ngrok/ngrok");
    // import ngrok from '@ngrok/ngrok' // if inside a module
    
    (async function() {
      // Establish connectivity
      const listener = await ngrok.forward({ addr: 8080, authtoken_from_env: true });
    
      // Output ngrok url to console
      console.log(`Ingress established at: ${listener.url()}`);
    })();

    process.stdin.resume();
    ```

That's it! Your application should now be available through the url output in your terminal. 

> **Note**
> You can find more examples in [the examples directory](https://github.com/ngrok/ngrok-javascript/tree/main/examples).

# Documentation

A quickstart guide and a full API reference are included in the [ngrok-javascript documentation](https://ngrok.github.io/ngrok-javascript/).

### Authorization

To use ngrok you'll need an authtoken. To obtain one, sign up for free at [ngrok.com](https://dashboard.ngrok.com/signup) and retrieve it from the [authtoken page of your ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken). Once you have copied your authtoken, you can reference it in several ways.

You can set it in the `NGROK_AUTHTOKEN` environment variable and pass `authtoken_from_env: true` to the [forward](https://ngrok.github.io/ngrok-javascript/functions/forward.html) method:

```jsx
await ngrok.forward({ authtoken_from_env: true, ... });
```

Or pass the authtoken directly to the [forward](https://ngrok.github.io/ngrok-javascript/functions/forward.html) method:

```jsx
await ngrok.forward({ authtoken: token, ... });
```

Or set it for all connections with the [authtoken](https://ngrok.github.io/ngrok-javascript/functions/authtoken.html) method:

```jsx
await ngrok.authtoken(token);
```

### Connection

The [forward](https://ngrok.github.io/ngrok-javascript/functions/forward.html) method is the easiest way to start an ngrok session and establish a listener to a specified address. The [forward](https://ngrok.github.io/ngrok-javascript/functions/forward.html) method returns a promise that resolves to the public URL of the listener.

With no arguments the [forward](https://ngrok.github.io/ngrok-javascript/functions/forward.html) method will start an HTTP listener to `localhost` port `80`:

```jsx
const ngrok = require("@ngrok/ngrok");
// import ngrok from '@ngrok/ngrok' // if inside a module

(async function() {
  console.log( (await ngrok.forward()).url() );
})();
```

You can pass the port number to forward on `localhost`:

```jsx
const listener = await ngrok.forward(4242);
```

Or you can specify the host and port via a string:

```jsx
const listener = await ngrok.forward("localhost:4242");
```

More options can be passed to the `forward` method to customize the connection:

```jsx
const listener = await ngrok.forward({ addr: 8080, basic_auth: "ngrok:online1line" });
const listener = await ngrok.forward({ addr: 8080, oauth_provider: "google", oauth_allow_domains: "example.com" });
```

The (optional) `proto` parameter is the listener type, which defaults to `http`. To create a TCP listener:

```jsx
const listener = await ngrok.forward({ proto: 'tcp', addr: 25565 });
```

See [Full Configuration](#full-configuration) for the list of possible configuration options.

### Disconnection

The [close](https://ngrok.github.io/ngrok-javascript/classes/Listener.html#close) method on a listener will shut it down, and also stop the ngrok session if it is no longer needed. This method returns a promise that resolves when the listener is closed.

```jsx
const listener = await ngrok.getListenerByUrl(url);
await listener.close();
```

Or use the [disconnect](https://ngrok.github.io/ngrok-javascript/functions/disconnect.html) method with the `url()` of the listener to close (or id() for a Labeled Listener):

```jsx
await ngrok.disconnect(listener.url());
```

Or omit the `url()` to close all listeners:

```jsx
await ngrok.disconnect();
```

### Listing Listeners

To list all current non-closed listeners use the [listeners](https://ngrok.github.io/ngrok-javascript/functions/listeners.html) method:

```jsx
const listeners = await ngrok.listeners();
```

### Builders

For more control over Sessions and Listeners, the builder classes can be used.

A minimal example using the builder class looks like [the following](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-http-minimum.js):

```jsx
async function create_listener() {
  const session = await new ngrok.NgrokSessionBuilder().authtokenFromEnv().connect();
  const listener = await session.httpEndpoint().listen();
  console.log("Ingress established at:", listener.url());
  listener.forward("localhost:8081");
}
```

See here for a [Full Configuration Example](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-http-full.js)

### TLS Backends

As of version `0.7.0` there is backend TLS connection support, validated by a filepath specified in the `SSL_CERT_FILE` environment variable, or falling back to the host OS installed trusted certificate authorities. So it is now possible to do this to forward:

```jsx
await ngrok.forward({ addr: "https://127.0.0.1:3000", authtoken_from_env: true });
```

If the service is using certs not trusted by the OS, such as self-signed certificates, add an environment variable like this before running: `SSL_CERT_FILE=/path/to/ca.crt`. There is also a `verify_upstream_tls: false` option to disable certification verification.

### Async Programming

All methods return a `Promise` and are suitable for use in asynchronous
programming. You can use callback chaining with `.then()` and `.catch()` syntax
or the `await` keyword to wait for completion of an API call.

#### Error Handling

All asynchronous functions will throw an error on failure to set up a session or listener,
which can be caught and dealt with using try/catch or then/catch statements:

```jsx
new ngrok.NgrokSessionBuilder().authtokenFromEnv().connect()
    .then((session) => {
        session.httpEndpoint().listen()
            .then((tun) => {})
            .catch(err => console.log('listener setup error: ' + err))
    })
    .catch(err => console.log('session setup error: ' + err))
    .await;
```

### Full Configuration

This example shows [all the possible configuration items of ngrok.forward](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-forward-full.js):

```jsx
const listener = await ngrok.forward({
  // session configuration
  addr: `localhost:8080`, // or `8080` or `unix:${UNIX_SOCKET}`
  authtoken: "<authtoken>",
  authtoken_from_env: true,
  on_status_change: (addr, error) => {
    console.log(`disconnected, addr ${addr} error: ${error}`);
  },
  session_metadata: "Online in One Line",
  // advanced session connection configuration
  server_addr: "example.com:443",
  root_cas: "trusted",
  session_ca_cert: fs.readFileSync("ca.pem", "utf8"),  
  // listener configuration
  metadata: "example listener metadata from javascript",
  domain: "<domain>",
  proto: "http",
  proxy_proto: "", // One of: "", "1", "2"
  schemes: ["HTTPS"],
  labels: "edge:edghts_2G...",  // Along with proto="labeled"
  app_protocol: "http2",
  // module configuration
  basic_auth: ["ngrok:online1line"],
  circuit_breaker: 0.1,
  compression: true,
  allow_user_agent: "^mozilla.*",
  deny_user_agent: "^curl.*",
  ip_restriction_allow_cidrs: ["0.0.0.0/0"],
  ip_restriction_deny_cidrs: ["10.1.1.1/32"],
  crt: fs.readFileSync("crt.pem", "utf8"),
  key: fs.readFileSync("key.pem", "utf8"),
  mutual_tls_cas: [fs.readFileSync('ca.crt', 'utf8')],
  oauth_provider: "google",
  oauth_allow_domains: ["<domain>"],
  oauth_allow_emails: ["<email>"],
  oauth_scopes: ["<scope>"],
  oauth_client_id: "<id>",
  oauth_client_secret: "<secret>",
  oidc_issuer_url: "<url>",
  oidc_client_id: "<id>",
  oidc_client_secret: "<secret>",
  oidc_allow_domains: ["<domain>"],
  oidc_allow_emails: ["<email>"],
  oidc_scopes: ["<scope>"],
  pooling_enabled: false,
  traffic_policy: "<policy_json>",
  request_header_remove: ["X-Req-Nope"],
  response_header_remove: ["X-Res-Nope"],
  request_header_add: ["X-Req-Yup:true"],
  response_header_add: ["X-Res-Yup:true"],
  verify_upstream_tls: false,
  verify_webhook_provider: "twilio",
  verify_webhook_secret: "asdf",
  websocket_tcp_converter: true,
});
```

The [Config](https://ngrok.github.io/ngrok-javascript/interfaces/Config.html) interface also shows all the available options.

# Examples

Degit can be used for cloning and running an example directory like this:
```bash
npx degit github:ngrok/ngrok-javascript/examples/<example> <folder-name>
cd <folder-name>
npm i
```
For example:
```bash
npx degit github:ngrok/ngrok-javascript/examples/express express && cd express && npm i
```

#### Frameworks
- [AWS App Runner](https://github.com/ngrok/ngrok-sdk-serverless-example)
- [Express](https://github.com/ngrok/ngrok-javascript/blob/main/examples/express)
- [Fastify Example](https://github.com/ngrok/ngrok-javascript/blob/main/examples/fastify)
- [Hapi Example](https://github.com/ngrok/ngrok-javascript/blob/main/examples/hapi)
- [Koa Example](https://github.com/ngrok/ngrok-javascript/blob/main/examples/koa)
- [Nest.js](https://github.com/ngrok/ngrok-javascript/blob/main/examples/nestjs)
- [Next.js](https://github.com/ngrok/ngrok-javascript/blob/main/examples/nextjs)
- [Remix](https://github.com/ngrok/ngrok-javascript/blob/main/examples/remix)
- [Svelte](https://github.com/ngrok/ngrok-javascript/blob/main/examples/svelte)
- [Typescript](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-typescript.ts)
- [Vue](https://github.com/ngrok/ngrok-javascript/blob/main/examples/vue)
- [Winston (Logging)](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-winston.js)

#### Listeners
* [ngrok.forward (minimal)](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-forward-minimal.js)
* [ngrok.forward (full)](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-forward-full.js)
* [HTTP (ngrok.listener)](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-listen.js)
* [HTTP (SessionBuilder minimal)](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-http-minimum.js)
* [HTTP (SessionBuilder full)](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-http-full.js)
* [Labeled](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-labeled.js)
* [TCP](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-tcp.js)
* [TLS](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-tls.js)
* [Windows Pipe](https://github.com/ngrok/ngrok-javascript/blob/main/examples/ngrok-windows-pipe.js)

# Platform Support

Pre-built binaries are provided on NPM for the following platforms:

| OS         | i686 | x64 | aarch64 | arm |
| ---------- | -----|-----|---------|-----|
| Windows    |   ✓  |  ✓  |    ✓    |     |
| MacOS      |      |  ✓  |    ✓    |  ✓  |
| Linux      |      |  ✓  |    ✓    |  ✓  |
| Linux musl |      |  ✓  |    ✓    |     |
| FreeBSD    |      |  ✓  |         |     |
| Android    |      |     |    ✓    |  ✓  |

> **Note**
> `ngrok-javascript`, and [ngrok-rust](https://github.com/ngrok/ngrok-rust/) which it depends on, are open source, so it may be possible to build them for other platforms.
> 
> On Windows, ensure you have [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version) installed.
>
>  We currently support MacOS 10.13+. 

# Dependencies

- [NAPI-RS](https://napi.rs/), an excellent system to ease development and building of Rust plugins for NodeJS.

# Changelog

Changes to `ngrok-javascript` are tracked under [CHANGELOG.md](https://github.com/ngrok/ngrok-javascript/blob/main/CHANGELOG.md).


# Join the ngrok Community

- Check out [our official docs](https://docs.ngrok.com)
- Read about updates on [our blog](https://blog.ngrok.com)
- Open an [issue](https://github.com/ngrok/ngrok-javascript/issues) or [pull request](https://github.com/ngrok/ngrok-javascript/pulls)
- Join our [Slack community](https://ngrok.com/slack)
- Follow us on [X / Twitter (@ngrokHQ)](https://twitter.com/ngrokhq)
- Subscribe to our [Youtube channel (@ngrokHQ)](https://www.youtube.com/@ngrokhq)

# License

This work is dual-licensed under [Apache, Version 2.0](LICENSE-APACHE) and [MIT](LICENSE-MIT).
You can choose between one of them if you use this work.

### Contributions

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in `ngrok-javascript` by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
