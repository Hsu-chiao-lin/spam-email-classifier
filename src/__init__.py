"""Top-level package marker for the `src` namespace.

Having an `__init__.py` here ensures `src` is treated as a regular
package (not only a namespace package). This makes relative imports
inside `src.spam_classifier` reliable on environments where implicit
namespace packages can lead to import resolution issues.
"""

__all__ = []
