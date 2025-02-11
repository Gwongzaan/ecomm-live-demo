# Database Design in a Modular and maintainable Approach

## tools

- graphviz online
- https://django-extensions.readthedocs.io/en/latest/graph_models.html

```shell
sudo apt-get install python-dev-is-python3
sudo apt-get instal graphviz libgraphviz-dev graphviz-dev
pip install pygraphviz


python manage.py graph_models apps_list > er.dot
```

[top-level ER diagram](./top-level-er.svg)

[Account, Address](../account/models.py)

# WHYs & Reasoning of Database Design

## Why Textchoices, integerChoices, enum.Enum

The choice between `models.TextChoices`, `models.IntegerChoices`, and Python's `enum.Enum` depends on specific use case, readability preferences, and maintainability requirements.

```python
class ACCOUNT_TYPE(models.TextChoices):
    PERSONAL = 'personal', 'Personnal'
    MEMBER = 'member', 'Member'
    GUEST = 'guest', 'Guest'
    DEVELOPER = 'developer', 'Developer'

from enum import Enum
class ACCOUNT_TYPE(Enum):
    PERSONAL = 'Personal'
    MEMBER = 'Member'
    GUEST = 'Guest'
    DEVELOPER = 'Developer'

    # usage
    models.CharField(
        choices = [(tag.value, tag.name) for tag in ACCOUNT_TYPE]
        default = ACCOUNT_TYPE.PERSONAL.value
    )

class ACCOUNT_TYPE(models.IntegerChoices):
    PERSONAL = 0, 'Personal'
    MEMBER = 1, 'Member'
    GUEST = 2, 'Guest'
    DEVELOPER = 3, 'Developer' #

```

1. **TextChoices**

   Why Use:

   - Human-readable values: Ideal when you want meaningful, short text codes (e.g., 'P' for Pending) combined with descriptive labels.

   - Strings are flexible: Strings are easier to interpret when debugging or writing queries, as they directly represent the intended meaning (e.g., status='P' is clearer than status=1).

   - Built into Django: Provides a choices-ready interface without extra boilerplate.

   - Readable names in templates: The .label attribute gives human-readable values.

   When NOT to Use:

   - Performance-sensitive scenarios: Text storage is slightly less efficient than integers (e.g., for large datasets).

   - Complex logic: If you need advanced features like methods or attributes on the enum values.

2. **IntegerChoices**

   Why Use:

   - Space-efficient: Ideal for storing numeric data where space or indexing performance matters (e.g., large databases or highly queried fields).

   - Avoids ambiguity: Numbers (like 1 for Low, 2 for Medium) are less prone to misinterpretation when storing simple priority levels, etc.

   - Readable labels: Like TextChoices, it offers descriptive labels for template rendering or admin forms.

   When NOT to Use:

   - Readability in debugging: Numbers are less intuitive when debugging or querying the database (e.g., seeing priority=2 might require referring to documentation).

   - Custom behaviors: Less suitable if you need enum values with custom behavior.

3. **enum.Enum (or enum.IntEnum)**

   Why Use:

   - Flexibility: Enums allow you to define methods, properties, or custom behavior, which is great for complex logic.

   - Decoupled logic: Keeps business logic separate from Django, making enums reusable across non-Django parts of the app (e.g., APIs, services).

   - Pythonic structure: Gives you access to all the power of Python enums, like iteration and comparison.

   When NOT to Use:

   - Extra boilerplate: Requires manually converting enums into choices for model fields, which adds complexity.
   - Inconsistent conventions: Values stored in the database won't necessarily match the Enum's Python names unless you enforce it.

Key Questions to Ask

- Do I need the field to store strings or integers?

  - If strings: Use TextChoices for simplicity.
  - If integers: Use IntegerChoices for space efficiency.

- Do I need extra methods or behavior?

  - If yes, use enum.Enum or enum.IntEnum to define custom methods or attributes.
    How readable should my database be?

- If you want human-readable values in the database, use TextChoices. Numbers (IntegerChoices) require a reference to understand their meaning.

- Will this enum be reused outside Django models?

  - If yes, enum.Enum is more reusable and decoupled from Django.

- Simple cases: Use TextChoices (readability) or IntegerChoices (performance).

- Advanced/Reusable: Use enum.Enum for logic-heavy enums or non-Django reuse.
