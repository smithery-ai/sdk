# Tool

## Example Usage

```typescript
import { Tool } from "@smithery/registry/models/components";

let value: Tool = {
  name: "fetch_url",
  description: "Fetches content from a URL",
  inputSchema: {
    type: "object",
    properties: {
      "url": {
        "type": "string",
        "description": "URL to fetch content from",
      },
    },
    additionalProperties: {
      "required": [
        "url",
      ],
    },
  },
};
```

## Fields

| Field                                                                                                                                  | Type                                                                                                                                   | Required                                                                                                                               | Description                                                                                                                            | Example                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                                                                                                                                 | *string*                                                                                                                               | :heavy_check_mark:                                                                                                                     | Name of the tool                                                                                                                       | fetch_url                                                                                                                              |
| `description`                                                                                                                          | *string*                                                                                                                               | :heavy_minus_sign:                                                                                                                     | Description of the tool                                                                                                                | Fetches content from a URL                                                                                                             |
| `inputSchema`                                                                                                                          | [components.InputSchema](../../models/components/inputschema.md)                                                                       | :heavy_check_mark:                                                                                                                     | JSON Schema defining the required parameters for the tool                                                                              | {<br/>"type": "object",<br/>"properties": {<br/>"url": {<br/>"type": "string",<br/>"description": "URL to fetch content from"<br/>}<br/>},<br/>"required": [<br/>"url"<br/>]<br/>} |