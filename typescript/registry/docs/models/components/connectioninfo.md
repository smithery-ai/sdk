# ConnectionInfo

## Example Usage

```typescript
import { ConnectionInfo } from "@smithery/registry/models/components";

let value: ConnectionInfo = {
  type: "http",
  url: "https://api.smithery.ai/mcp/fetch",
  configSchema: {
    "type": "object",
    "properties": {
      "apiKey": {
        "type": "string",
        "description": "API key for authentication",
      },
    },
    "required": [
      "apiKey",
    ],
  },
};
```

## Fields

| Field                                                                                                                                         | Type                                                                                                                                          | Required                                                                                                                                      | Description                                                                                                                                   | Example                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                                                                                                                                        | [components.ConnectionInfoType](../../models/components/connectioninfotype.md)                                                                | :heavy_check_mark:                                                                                                                            | Connection type                                                                                                                               | http                                                                                                                                          |
| `url`                                                                                                                                         | *string*                                                                                                                                      | :heavy_minus_sign:                                                                                                                            | HTTP URL to connect to (for http type)                                                                                                        | https://api.smithery.ai/mcp/fetch                                                                                                             |
| `configSchema`                                                                                                                                | Record<string, *any*>                                                                                                                         | :heavy_check_mark:                                                                                                                            | JSON Schema defining required configuration options                                                                                           | {<br/>"type": "object",<br/>"properties": {<br/>"apiKey": {<br/>"type": "string",<br/>"description": "API key for authentication"<br/>}<br/>},<br/>"required": [<br/>"apiKey"<br/>]<br/>} |