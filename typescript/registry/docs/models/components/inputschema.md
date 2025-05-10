# InputSchema

JSON Schema defining the required parameters for the tool

## Example Usage

```typescript
import { InputSchema } from "@smithery/registry/models/components";

let value: InputSchema = {
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
};
```

## Fields

| Field                                                                                                                                  | Type                                                                                                                                   | Required                                                                                                                               | Description                                                                                                                            | Example                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                                                                                                                                 | [components.ToolType](../../models/components/tooltype.md)                                                                             | :heavy_check_mark:                                                                                                                     | N/A                                                                                                                                    |                                                                                                                                        |
| `properties`                                                                                                                           | Record<string, *any*>                                                                                                                  | :heavy_minus_sign:                                                                                                                     | N/A                                                                                                                                    |                                                                                                                                        |
| `additionalProperties`                                                                                                                 | Record<string, *any*>                                                                                                                  | :heavy_minus_sign:                                                                                                                     | N/A                                                                                                                                    | {<br/>"type": "object",<br/>"properties": {<br/>"url": {<br/>"type": "string",<br/>"description": "URL to fetch content from"<br/>}<br/>},<br/>"required": [<br/>"url"<br/>]<br/>} |