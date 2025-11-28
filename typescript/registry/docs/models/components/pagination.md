# Pagination

## Example Usage

```typescript
import { Pagination } from "@smithery/registry/models/components";

let value: Pagination = {
  currentPage: 1,
  pageSize: 10,
  totalPages: 5,
  totalCount: 42,
};
```

## Fields

| Field              | Type               | Required           | Description        | Example            |
| ------------------ | ------------------ | ------------------ | ------------------ | ------------------ |
| `currentPage`      | *number*           | :heavy_check_mark: | N/A                | 1                  |
| `pageSize`         | *number*           | :heavy_check_mark: | N/A                | 10                 |
| `totalPages`       | *number*           | :heavy_check_mark: | N/A                | 5                  |
| `totalCount`       | *number*           | :heavy_check_mark: | N/A                | 42                 |