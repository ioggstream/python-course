# Writing with markdown

This files allow creating pdf with markdown via pandoc.

Further formatting is done with latex macros defined in partecstyle.tex.

Makefile compiles a main.pdf created concatenating
all the [0-9]*.md.tex files generated by pandoc.

# Columns
You can define columns like the following
 
\columnsbegin

\column[t]{.5\textwidth}
This is a top-aligned column

\column[t]{.5\textwidth}
Of a two-column page.

\columnsend