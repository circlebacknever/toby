# Databases and Data Access

This file covers when to wrap ORM calls in a repository and when to split database row, domain, and API types.

## ORM in services

When a service calls SQLAlchemy or Hibernate directly, it manages session scope, lazy loading, and query syntax, so changing the query layer edits every caller. In repos that use repositories, keep ORM queries inside the repository and return domain objects. In Django and Rails, keep queries and table writes on the model (`toby-swd-architecture`).

## One type per audience

```go
// auth/user.go
type User struct {
    ID              string `db:"id" json:"id"`
    HashedPassword  string `db:"hashed_password" json:"-"`
    LegacyMfaSecret string `db:"legacy_mfa_secret" json:"-"`
}
```

When one struct serves as the database row, the domain object, and the JSON response, every caller depends on the table schema and secrets can leak if you miss a struct tag. Split the struct when callers must never receive a field (such as `HashedPassword`) or when the database columns and wire format differ:

```go
// auth/internal/store/user_row.go
type userRow struct { ... } // matches the columns, package-private

// auth/user.go
type User struct { ID, Email string; Status UserStatus }

// auth/api/user_dto.go
type UserDTO struct { ... } // the JSON wire format
```

When all three views share the same safe fields, keep one struct with `db` and `json` tags. In Django and Rails, the model serves as the row and domain type, and a serializer defines the JSON format.

## Read models

Define a separate read struct or query type only when a screen needs aggregated or pre-joined columns that don't match a single table.
