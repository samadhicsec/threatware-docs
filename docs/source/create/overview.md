# Overview

This page is going to start with the basics, but feel free to skip ahead to the [](./template.md) section to start populating the template.

If you are a threat modelling expert already, you might find it interesting to read this page, but it's not really aimed at you.

## What is Threat Modelling?

Threat Modelling is a process that helps you identify security threats to a system.  Beyond that simple statement everything else about threat modelling is opinion; there really isn't a right way of doing it (there probably are some wrong ways though).  Any threat modelling process you follow that enables you to identify security threats is legitimate, but not ever legitimate process will suit your requirements with respect to; output, effort, resources, time, abilities, coverage, technologies, automation, assurance, audit etc.

## An Opinionated Approach

The Threat Modelling Template and the process to populate it is the result of years of doing threat modelling and numerous refinements.  It has served as the basis for generating and updating hundreds of threat models in multiple businesses, and has held up to the scrutiny of numerous audits in some of the most demanding environments e.g. healthcare, finance, investor due diligence etc.

In order to be successful it has had to be opinionated:
- It focuses on architecture and design issues, but accomodates classes of specific vulnerabilities when relevant to the system being threat modelled.
- It takes a structured approach in the form of a template (as opposed to less structured approaches like brainstorming threats), that minimises the need for the author to be a 'security expert' or 'think like an attacker'.
- It captures existing controls for already mitigated threats, and considers these to be as, if not more, important as unmitigated threats (which also avoids threat models with 'no threats')
- It suits creating many small threat models as opposed to a few large threat models
- It creates tightly scoped threat models, scoped to just the systems a team owns or operates, which leads to threats specific to the team that they can actually do something about
- It prioritises capturing information about a system in order to create a model of the system where identifying security threats becomes easier (i.e. an information first, not threat first approach).
- It prioritises identification of threats, over analysis and remediation of threats
- It prefers to focuses on only 1 environment (e.g. production, CICD) at a time
- It promotes the reuse of existing design artifacts (e.g. diagrams, descriptions) to populate the threat model, and minimises the ask to create new artifacts 
- It sticks to the basics of Confidentiality and Integrity (and supports Availability) for authors to consider, and avoids security terms non-experts might struggle with (I'm looking at you "trust boundary"!)
- It aggregates threats so the resulting list of threats is more manageable and avoids asking authors to consider every permutation
- It promotes partially populated templates specific to orgs/teams/technologies to minimise effort to populate new threat models and drive consistent descriptions of shared systems and their controls
- It encourages a 'stack overflow' effect for threat models, where you can look at existing threats models, learn from them, and copy what you need
- It generates threat models that don't need to be updated often, only when integrating new components, dealing with new types of data, or intorducing new operational processes
- It treats versions of threat models as first class citizens and expects threat models will be updated, but recognises that previous versions should never be lost
- It supports an approval process for threat models to drive quality and consistency

The reason for taking these opinionated views on how to threat model is so the process is acceptable to the people who create threat models, and they percieve it as offering value.  These it turns out are actually more important than 'does the process find every threat?', because the process that finds every threat, isn't useful if no one uses it.

This approach also chooses to de-emphaise or leave out certain things other well-known threat modelling approaches use:
- If you have heard of or know about STRIDE then
    - this process minimises identifying Denial-of-Service threats (because these are usually handled at the infrastructure layer and common to multiple teams), 
    - it leaves out Non-Repudiation threats as these are very rarely relevant and difficult to explain (and as long as a system has centralised logging, the threat is usually satisfactorily mitigated), and
    - there is no real equalivalent of Elevation Of Privilege (EoP) as any EoP that isn't related to authentication/authorisation is usually the result of a coding/configuration vulneraiblity and usually there are automated tools that do a decent job of identifying these.
- If you are expecting to see a list of generated threats for a specific technology then that is not a focus for this process.  The focus is on architecture and design issues, and not on all possible threats associated with a specific technology.  By all means consult a list of threats for a technology and add them as threats, but usually it is better to aggregate these into a single threat about hardening a technology and reference a guide that focuses on it.

## The Threat Modelling Process

To create a new threat model the first thing to do is to make a copy of the threat model [template](./template.md).

As you look at your new, empty threat model, the whole threat modelling processes seems like a daunting task, and certainly starting from an empty template is tough.  Let's walk through some steps to get started (but remember that detailed information about sections/tables/fields is available in subsequent sections of this help, so read those as you go).

:::{admonition} Common Misconception
While the following list may seem you can just sit down and do it in one sitting, that is virtually never the case.  These steps are meant to be done over a series of 3-4 1-hour long meetings with the team that built the system.  The steps whilst numbered, are not atomic, you cannot complete one and expect to never go back it, you need to iterate and build the threat model pieces at a time.  Since fields on 1 section reference fields in other sections, as you populate any section you'll have to adjust other sections to match.  That's non-trivial, but the threatware `verify` action is what makes that practical.
:::

1. Hopefully you already have an existing diagram of your system.  It doesn't have to be perfect or even completely up to date.  Start by making a copy and putting it in the [](./components.md#components-diagram) section of the threat model.
2. Add a description to the [](./template.md#description) section.  Use existing executive summary paragraphs from other design documentation if you have them.  Try to list at least the major use cases for the system.
3. Using the diagram and use cases as a reference, start populating the [](./components.md#components-details-table) by adding rows with the Name and Purpose of components, and whether they are in-scope.
4. As you populate the [](./components.md#components-details-table) try to think about all the sources of requests into in-scope systems and the outbound requests made be in-scope systems.  Add new components for any you identify, deciding if they are in scope or not (no need to update the diagram if you don't want to).
:::{admonition} Tip
Are you thinking of existing controls whilst populating the threat model?  Capture them while you think about them!  Just put some text in the "Controls (Existing)" column in the [](./threats-controls.md#threats-and-controls-table) and worry about completing the rest of the row later.
:::
5.  For each in-scope component start adding rows to the [](./components.md#components-authn-and-authz-table) table by considering "who" is involved in each use cases and whether each component knows the identity of the requester, and then how the component authenticates and authorises that identity.
6. Start adding Functional Assets by considering the use cases captured, and the types of data required by those use cases.  Add rows for each in the [](./assets.md#functional-assets-table)], adding a Name, Description, Impact and Storage Location.  When capturing Storage Location, decide if there is an existing component that accurately represents the storage location, or whether you need to define a new component.  You can also start defining storage types (see [](./assets.md#functional-assets-table)) and adding them back to the template.
7. Start adding Technical Assets.  The best way to identify these is to look through configuration files for the different systems in-scope, looking for any configuration that seems related to security, credentials, secrets, locations etc.  When populating "Functional Assets Affected" consider whether an appropriate Functional Asset exists, and if one doesn't, consider creating one.
8. At this stage run the threatware `verify` action to see how consistant you have been with naming things and to spot any gaps where you haven't referenced things correctly.  There will likely be a lot of errors!  That's OK, it's still a work in progress.  Go through the errors and fix anything that seems like an easy win.  Resist the urge to put in fake values just to make errors go away.
9. Start populating the [](./threats-controls.md#threats-and-controls-table) by going through the list of Storage Locations for Functional and Technical Assets and populating a row for each type of Component, aggregating things together wherever possible.  Use "Unauthorised access to ..." as a basis for creating threats.
10. By now you have a partially populated threat model.  You should use the threatware `verify` action to identify and start filling in missing fields and references.
11. Sanity check the list of "Controls (Existing)" captured in the [](./threats-controls.md#threats-and-controls-table).  You probably know about some or most existing security controls that have been implemented in a system.  Are these present in this column?  If not, add the control to a new row, then add the threat that control protects against, and then decide what component(s) and asset(s) it relates to.  If you are struggling to identify the component or asset the threat relates to then consider adding new components and assets as appropriate.
12. Start thinking about context or technology specific threats that might be relevant (but don't be concerned if you can't).
13. Keep iterating until the threatware `verify` action says the threat model is valid.  When it is, submit it for approval.

Phew! That was a lot of work!  The first one is always the hardest though.

## Improving The Process

With a first threat model done (you may want to wait until the first 2-3 are done), make sure the work that has been done can benefit others.  Go over your threat model(s) and identify the components, assets, threats & controls that are common to other systems within your business (e.g. common Identity service, common logging/monitoring/observability, commmon artifact storage, common code repository etc.).  Populate the threat model template (or create a new template) with these common entries.  Other teams that need to create threat models can benefit from the threat modelling work that has happened already.

Make sure other teams can find any existing completed threat models.  Examples are **the best** way for teams to learn the process quickly (and they can steal anything that is relevant to make it even easier on them).  Examples are also the best way for threat modelling to gain momentum in your business - teams are less likely to complain about a new activity if they see other teams have done it already.

As you use the default template several times, you may wish there was the ability to capture information specific to your business.  The template format is customisable, but this requires creating a new `scheme`.  If it's adding a new column (or row) to a table, then this is not too much work, see [](../customise/overview.md#how-to-customise-a-threat-model-template).