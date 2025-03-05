# This code was obviously written by me. (i have no clue what is going on here)
from typing import Type, List, Callable, get_type_hints, get_origin, get_args
import inspect

class Signal:
    def __init__(self, *arg_types: Type):
        super().__init__()
        """
        Initialize a Signal with the expected argument types.
        Example: Signal(str) for a signal that emits strings.
        """
        self.arg_types = arg_types
        self.listeners: List[Callable] = []

    def emit(self, *args):
        """
        Emit the signal with the given arguments.
        Raises TypeError if the arguments don't match the expected types.
        """
        if len(args) != len(self.arg_types):
            raise TypeError(
                f"Expected {len(self.arg_types)} arguments, got {len(args)}"
            )

        for i, (arg, expected_type) in enumerate(zip(args, self.arg_types)):
            if not self._is_instance(arg, expected_type):
                raise TypeError(
                    f"Argument {i} must be of type {expected_type}, got {type(arg)}"
                )

        for listener in self.listeners:
            listener(*args)

    def connect(self, listener: Callable):
        """
        Register a listener to this signal.
        The listener must accept the same argument types as the signal.
        """
        # Validate listener signature
        sig = inspect.signature(listener)
        parameters = list(sig.parameters.values())

        # Adjust the expected number of arguments for methods
        expected_arg_count = len(self.arg_types)

        if len(parameters) != expected_arg_count:
            raise TypeError(
                f"Listener must accept {len(self.arg_types)} arguments, "
                f"but it accepts {len(parameters)}"
            )

        # Get the actual type hints for the listener
        type_hints = get_type_hints(listener)

        for i, (param, expected_type) in enumerate(zip(parameters, self.arg_types)):

            # Resolve the annotation to a type object
            annotation = type_hints.get(param.name, inspect.Parameter.empty)

            if annotation != inspect.Parameter.empty and not self._is_subtype(annotation, expected_type):
                raise TypeError(
                    f"Listener argument {i} must be of type {expected_type}, "
                    f"but it is annotated as {annotation}"
                )

        self.listeners.append(listener)

    def disconnect(self, listener: Callable):
        """
        Unregister a listener from this signal.
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

    def __call__(self, *args):
        """Allow the signal to be called like a function."""
        self.emit(*args)

    def _is_instance(self, obj, expected_type):
        """
        Check if `obj` is an instance of `expected_type`, handling subscripted generics.
        """
        origin = get_origin(expected_type)
        if origin is None:
            # Not a generic type, use isinstance directly
            return isinstance(obj, expected_type)
        else:
            # Handle generic types
            args = get_args(expected_type)
            return isinstance(obj, origin) and all(
                self._is_instance(item, arg) for item, arg in zip(obj, args)
            )

    def _is_subtype(self, subtype, supertype):
        """
        Check if `subtype` is a subtype of `supertype`, handling subscripted generics.
        """
        if subtype == supertype:
            return True

        origin = get_origin(supertype)
        if origin is None:
            # Not a generic type, use issubclass directly
            return issubclass(subtype, supertype)
        else:
            # Handle generic types
            args = get_args(supertype)
            return issubclass(subtype, origin) and all(
                self._is_subtype(sub_arg, super_arg) for sub_arg, super_arg in zip(get_args(subtype), args)
            )
