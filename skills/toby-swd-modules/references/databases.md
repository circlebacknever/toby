# Databases and Data Access

## ORM in services

When services call the ORM directly, each one handles session scope, lazy loading, filter syntax, and objects that fail after their session closes. Switching ORMs or adding a read replica then means editing every service. Keep all of that ORM handling in the repository, which returns plain domain objects, so the service calls `orders.confirm(order_id)`.

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

This `User` struct is the database row, the JSON DTO, and the domain entity at once. Every consumer then depends on the schema, the wire format, and the hashing scheme. Give each audience its own type, and put each type in the package that makes that type's decisions. Here the row type goes in the store package, the domain type in `auth`, and the JSON type in the API package:

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

Use a separate type for reads only when a query returns data very different from the stored entity, such as a report or a dashboard. Otherwise use one type for reads and writes.
