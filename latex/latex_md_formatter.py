'''
rules: 
- single $ without new lines surrounding block of math text must have no white space
    - Wrong: Slope intercept form is $y = mx + b$.
    - Right: Slope intercept form is $y=mx+b$.
- single $ should have all instances of `}_(whatever)` turned into `_(whatever)}`. GitHub Latex interpreter interprets the former as italics.
- double $ must have new lines surrounding block of math text, but can have white space.
    - Wrong:
        Newton's Second Law is
        $$F_net = ma$$
        where $F_net$, $m$, and $a$ are the net force, mass, and acceleration respectively
    - Right:
        Newton's Second Law is

        $$F_net = ma$$

        where $F_net$, $m$, and $a$ are the net force, mass, and acceleration respectively
- When using `\\` as an indication of new line in something like `align*` or `bmatrix`, either have a newline after `\\` or us `\\\` instead.
'''