# Databases and Data Access

## ORM in services

When services call the ORM directly, each one handles session scope, lazy loading, filter syntax, and objects that fail after their session closes. A switch of ORM or a new read replica then edits every service. Keep all of it in the repository, which returns plain domain objects, so the service calls `orders.confirm(order_id)`.

## One type for three audiences

```go
// auth/user.go
type User struct {
    ID              string `db:"id" json:"id"`
    HashedPassword  string `db:"hashed_password" json:"-"`
    LegacyMfaSecret string `db:"legacy_mfa_secret" json:"-"`
    // ...the struct has 25 more fields
}
```

This `User` struct is the database row, the JSON DTO, and the domain entity at once. Every consumer then depends on the schema, the wire format, and the hashing scheme. Give each audience its own type in the package that makes that decision:

```go
// auth/internal/store/user_row.go
type userRow struct { ... }   // matches the columns, package-private

// auth/user.go
type User struct { ID, Email string; Status UserStatus }

// auth/api/user_dto.go
type UserDTO struct { ... }   // the JSON format
```

A column change stays inside `internal/store`, and a JSON change needs no migration.

## Read models

Split a read model from the write model only when a query result differs sharply from the entity, such as a report or a dashboard. Otherwise keep one model.
