# React Form Typing

Use `React.FormEvent<HTMLFormElement>` for submit handlers in TypeScript React.

Keep form parsing close to the submit handler, then pass validated values into a
small domain function. Avoid storing raw event objects outside the handler.
