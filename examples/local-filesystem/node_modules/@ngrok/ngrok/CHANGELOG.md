## 1.5.0
Adds `poolingEnabled` to listener builders, allowing the endpoint to pool with other endpoints with the same host/port/binding

## 1.4.1

- Fix `traffic_policy` naming for `ngrok.forward`

## 1.4.0

- Rename `policy` to `traffic_policy`
- Fix quickstart example in README
- Add Microsoft Visual C++ Redistributable requirement for Windows to documentation

## 1.3.0:

- Add `rootCas` to session builder and `root_cas` to `ngrok.forward`. Setting this to `host` will use the host's trusted certificates to connect for the ngrok session.
- Add `session_ca_cert` and `server_addr` to `ngrok.forward`, which correspond to the same functions in the session builder.

## 1.2.0:

- Add `verifyUpstreamTls` to listener builders and `verify_upstream_tls` to `ngrok.forward`. Setting this to false will skip verification of the upstream application's TLS certificate.

## 1.1.1:

- Add `appProtocol(string)` to the labeled listener builder. Setting this to "http2" will enable HTTP/2 support to the backend application.

## 1.1.0:

- Add `appProtocol(string)` to http listener builder, and `app_protocol: string` as a `ngrok.forward()` argument. Setting this to "http2" will enable HTTP/2 support to the backend application.

## 1.0.0:

- Add policy support to Listener builders and `ngrok.forward`

## 0.9.1:

- Move to `ngrok.forward` from `ngrok.connect`, keeping an alias.
- Rename to `ngrok-javascript`.
- Smaller number of files packaged.

## 0.9.0:

- `ngrok.connect` now returns the full `Listener` object.

## 0.8.0:

- Add `allowUserAgent` and `denyUserAgent` options to HTTP listeners.
- Add `clientId` and `clientSecret` options to OAuth.

## 0.7.1:

- Fix for windows pipe pathing.

## 0.7.0:

- Add `listen_and_forward` and `listen_and_serve` to listener builders.
- Update to latest version of underlying rust library, allowing TLS backends.

## 0.6.0:

- Flattened `listener.forwardPipe()` and `listener.forwardTcp()` into `listener.forward()`. Determination will be made based on `addr` input.
- Add `ngrok.listeners()` and `session.listeners()` to get a list of current non-closed listeners for the process or session, respectively.
- Add `errorCode` field to thrown errors, where possible.
- More heuristics for automatic unix socket file placement.
- Connect heuristic improved for strings parseable as numbers.

## 0.5.2:

- Cleanly return from a listener forward call after a `session.close()`.

## 0.5.1:

- `consoleLog` return signature.

## 0.5.0:

- Add `Session.clientInfo()`.
- Rename to `ngrok-nodejs`.

## 0.4.1:

- Clean shutdown when run from npm.
- Unblock Svelte postinstall script.

## 0.4.0:

- Move to a single listener type for simplicity.
- Documentation updates.

## 0.3.0:

- Added `ngrok.connect(Config)`, `ngrok.authtoken()`, and `ngrok.disconnect(url)`.
- Examples cleanup.

## 0.2.0:

- Now have examples for Express, Fastify, Hapi, Koa, Nest.js, Next.js, Remix, Svelte, and Vue.
- Add `prettier` auto code formatting.

## 0.1.1:

- Bump `ngrok-rust` to `0.11.3`.
- Migrate `ca_cert` to the upstream call in `ngrok-rust`.

## 0.1.0:

- Added `ca_cert`, `handle_heartbeat`, and `handle_disconnection` to Session.

## 0.0.12:

- Added Session.close().
- Cleanly shutdown when listen is called with a pre-configured listener.

## 0.0.11:

- Cleanly shutdown on all platforms when there are callbacks registered.

## 0.0.10:

- Child client versioning support.

## 0.0.9:

- Support for named pipes on Windows.

## 0.0.8:

- Support callbacks for logging, include console.log and Winston handlers.
- Can now pass listeners directly to net.Server.listen().
- Clean shutdown on SIGINT after ngrok.listen(server).
- Typedoc generation of documentation.

## 0.0.7:

- Improved memory management, removing need to keep NodeJS from garbage collecting certain objects.
- Support callbacks for remote operations (stop, restart, update).
- Typescript support for getSocket and listen.

## 0.0.6:

- Initial public release.
