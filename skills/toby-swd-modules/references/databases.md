# Databases and Data Access

In Django and Rails the model writes its own table, so an entry point or an operation calls model methods such as `order.confirm()`. Add a repository only when the repo already has repositories, as "Default structure" in `toby-swd-architecture` says.

## ORM in services

A service that calls SQLAlchemy or Hibernate directly handles session scope, lazy loading, filter syntax, and objects that fail after their session closes. Switching ORMs or adding a read replica then means editing every such service. When the repo already has repositories, keep that ORM handling in them. A service then calls `orders.confirm(order_id)` and gets plain domain objects back.

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

This `User` struct is the database row, the JSON DTO, and the domain entity at once. Every consumer then depends on the schema, the wire format, and the hashing scheme. Split the type only when one audience must not see a field, such as `HashedPassword`, or when the columns and the JSON already differ. Then put each audience's type in the package that makes that type's decisions. Here the row type goes in the store package, the domain type in `auth`, and the JSON type in the API package:

```go
// auth/internal/store/user_row.go
type userRow struct { ... }   // matches the columns, package-private

// auth/user.go
type User struct { ID, Email string; Status UserStatus }

// auth/api/user_dto.go
type UserDTO struct { ... }   // the JSON format
```

A column change stays inside `internal/store`, and a JSON change needs no migration. When all three types would hold the same fields, keep one struct with `db` and `json` tags.

In Django and Rails the model is the row type and the domain type. Add only the JSON type, such as a DRF serializer.

## Read models

Use a separate type for reads only when a query returns data very different from the stored entity, such as a report or a dashboard. Otherwise use one type for reads and writes.
