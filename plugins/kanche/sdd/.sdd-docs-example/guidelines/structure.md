# Structure — Guidelines

<!-- written by /sdd:init -->

```
/api        Go services (module boundary = feature)
/web        React app
/db         migrations + schema
```

Feature code lives under `/api/{feature}` and `/web/src/features/{feature}`.
The module a feature maps to determines its `product/features/{module}/` slot.
