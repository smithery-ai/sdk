# Result

## Example Usage

```typescript
import { Result } from "@smithery/registry/models/components";

let value: Result = {
  command: "npx",
  args: [
    "@smithery/hello-world",
    "--config",
    "{}",
  ],
  env: {
    "NODE_ENV": "production",
  },
};
```

## Fields

| Field                                         | Type                                          | Required                                      | Description                                   | Example                                       |
| --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- | --------------------------------------------- |
| `command`                                     | *string*                                      | :heavy_check_mark:                            | N/A                                           | npx                                           |
| `args`                                        | *string*[]                                    | :heavy_check_mark:                            | N/A                                           | [<br/>"@smithery/hello-world",<br/>"--config",<br/>"{}"<br/>] |
| `env`                                         | Record<string, *string*>                      | :heavy_minus_sign:                            | N/A                                           | {<br/>"NODE_ENV": "production"<br/>}          |