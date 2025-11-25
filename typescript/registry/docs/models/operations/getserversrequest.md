# GetServersRequest

## Example Usage

```typescript
import { GetServersRequest } from "@smithery/registry/models/operations";

let value: GetServersRequest = {
  page: 1,
  pageSize: 10,
  q: "search term",
  profile: "my-profile",
};
```

## Fields

| Field              | Type               | Required           | Description        | Example            |
| ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| `page`             | *number*           | :heavy_minus_sign: | N/A                | 1                  |
| `pageSize`         | *number*           | :heavy_minus_sign: | N/A                | 10                 |
| `q`                | *string*           | :heavy_minus_sign: | N/A                | search term        |
| `profile`          | *string*           | :heavy_minus_sign: | N/A                | my-profile         |