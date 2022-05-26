# Diagrams

Diagrams can be an essential to conveying understanding of how a complex system works.  They can also be a needless chore to create something that is deemed "required" by a threat model yet offers little extra to help understand a system.

The threat modelling template captures a component diagram, a list of components, and a list of assets, but it is sometimes not obvous how those assets flow between the components.  Sometimes however, it is obvious how assets flow between components.  The template takes the approach that diagrams should be added if they are needed - if they serve to explain a complicated flow of assets between components.  Diagrams should not be added just for the sake of populating this section, or offer no particular insight e.g. a basic Client <-> Server REST API call.

:::{admonition} Tip
There are many possible tools to aid in drawing diagrams, but tools that use text to dynamically generate the diagram make it simple to both generate and change the diagram, which saves time in the long run.  

For Confluence Server the [Plant UML app](https://marketplace.atlassian.com/apps/41025/plantuml-for-confluence) can be used and is free.  For Confluence Cloud the [Mermaid Diagrams for Confluence](https://marketplace.atlassian.com/apps/1226567/mermaid-diagrams-for-confluence) may be an option (author has not used it) and is free.

For Google Docs the [Mermaid](https://workspace.google.com/marketplace/app/mermaid/636321283856) extension can be used and is free.

A less convenient, but still free, option is to use [www.plantuml.com](http://www.plantuml.com), and manually insert the diagram and embed the link that generates the diagram as a link in the document.
:::

The template has explicit sections for adding sequence and data-flow diagrams, but if adding other types of diagrams will help explain how a system works in ways that might expose security issues, then use whatever will work.

## Sequence Diagrams

Sequence diagrams are useful when the system has a complicated flow of assets that occur in a particular order and generally involve several different components.  As a rule of thumb, prefeence should be given to producing sequence diagrams over other types of diagrams.

## Data Flow Diagrams

Data Flow Diagrams are useful for showing state transitions or showing decision diagrams.

