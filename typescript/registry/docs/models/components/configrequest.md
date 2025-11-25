# ConfigRequest

## Example Usage

```typescript
import { ConfigRequest } from "@smithery/registry/models/components";

let value: ConfigRequest = {
  connectionType: "stdio",
  config: {
    "host": "localhost",
    "port": 8080,
  },
};
```

## Fields

| Field                                                                  | Type                                                                   | Required                                                               | Description                                                            | Example                                                                |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `userId`                                                               | *string*                                                               | :heavy_minus_sign:                                                     | User performing the request                                            |                                                                        |
| `connectionType`                                                       | [components.ConnectionType](../../models/components/connectiontype.md) | :heavy_check_mark:                                                     | The type of server to instantiate                                      | stdio                                                                  |
| `config`                                                               | Record<string, *any*>                                                  | :heavy_check_mark:                                                     | The configuration for the server                                       | {<br/>"host": "localhost",<br/>"port": 8080<br/>}                      |