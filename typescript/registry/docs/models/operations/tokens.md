# Tokens

## Example Usage

```typescript
import { Tokens } from "@smithery/registry/models/operations";

let value: Tokens = {
  accessToken: "<value>",
  tokenType: "<value>",
};
```

## Fields

| Field              | Type               | Required           | Description        |
| ------------------ | ------------------ | ------------------ | ------------------ |
| `accessToken`      | *string*           | :heavy_check_mark: | N/A                |
| `idToken`          | *string*           | :heavy_minus_sign: | N/A                |
| `tokenType`        | *string*           | :heavy_check_mark: | N/A                |
| `expiresIn`        | *number*           | :heavy_minus_sign: | N/A                |
| `scope`            | *string*           | :heavy_minus_sign: | N/A                |
| `refreshToken`     | *string*           | :heavy_minus_sign: | N/A                |