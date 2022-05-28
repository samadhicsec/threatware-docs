# Components

What is a component?  There is not a straight-forward answer to this unfortunately.  This is good in the sense it gives freedom to define this in a way that makes sense to your business, but bad in the sense it is not prescriptive and so may be challenging for people to understand what to capture.

It may help to understand how components are used:
- First and foremost they are a list of all the systems that make up the system being threat modelled, and the systems connected to the system being threat modelled.
- They allow scope to be defined.  The choice of Components should allow it to be categorised as either in-scope or out-of-scope.
- They allow authentication and authorization to be defined.  A system that implements authentication and/or authorisation is most likely a component.
- If the system itself has an identity given to it e.g. service account, OAuth2 Client ID, then it is likely a component.

For the Team that owns the threat model:
- any system they created should be considered a Component
- any system or service they got provisioned or on-boarded (e.g. a cloud database, SaaS service) should be considered a component
- any system they own or operate (e.g. Kubernetes cluster) should be considered a component

Components often correspond to deployable units' of artifacts.  The level of granularity of a sub-system that constitutes a Component should lean towards a single deployable thing e.g. a Kubernetes Pod and not the individual containers, a contrainer hosted in ECS, a combined web and application server (if co-hosted), a OS process but not its libraries etc.    

Start at a higher level and break apart Components as required.  When populating the threat model it often becomes apparent that it would be easier to express an authentication method, or an asset storage location, or threat or control, if a specific sub-system was called out as a Component, so it's unusual to get the list of Components complete on a first draft of a threat model, and the table becomes more complete as iterative work on the threat model happens.

Minimise infrastructure included as Components, especially if it makes sense for it to have its own threat model. It's typical to not include supporting infrastructure that is otherwise transparent to the systems containing the business logic or performing related tasks.  For instance we would not normally include; load balancers, proxies, DNS, etc., but if any of these implemented specific security controls for the system you may want to include them as Components (but often just listing them as a control in the Threats & Control Table is easier).  The threats related to this supporting infrastructure is usually best handled in it's own dedicated threat model (where the question 'What is a Component?' has a totally different answer), and usually it's a threat model that can specifically focus on infrastructure threats, and becomes a companion threat model for application-level threat models.

Practically speaking, if there is any kind of design documentation for a system then the various systems defined in that make an ideal starting point for a list of Components.

## Components Diagram

This should contain a diagram showing all, or at least the major components of the system being threat modelled.  Use an existing diagram if you have one, even if it is is not perfect or completely up to date (the [](./components.md#components-details-table)) will be the accurate record of what the system comprises of).  If you have to create a new diagram, keep it simple to begin with, just trying to capture the major components.

What is important for this diagram is that it shows which components connect to which other components.  The actual data being sent is less important, so this diagram does not need to be a Data Flow Diagram (DFD).  it's purpose is to visually display connectivity.  It can be helpful to group components by where they are deployed, but this is not required.  Some teams like to colour code which components are in and out of scope.

## Components Details Table

The Components Details Table must have a row per Component (and only one Component per row), and it contains the following columns:

Name
:  A short unique name (amongst all names in this threat model) for the component.  This is the name that will be used elsewhere in the threat model, so it must be unique, and for convienence it should be short.  If the Component is something that has an identity, then using that identity is often a good idea, but it depends on how human friendly the name is.

Location Stack
:  A comma separated list of the stack hosting the Component (the whole stack, up to the environment e.g. AWS account ID).  This is useful for understanding what Components are co-located, and which are not, and this directly informs threats related to communications (e.g. transport security, authentication, authorization, etc.).  For out-of-scope Components it's usually fine to only capture if it is Internet hosted, or shares the same location as in-scope Components.
:  The threatware `measure` action relies on some standardised values here; `3rd Party`, `SaaS`, `Internal Service` (but these are configurable in `measure/measure_config.yaml`)

Purpose
:  A brief description of the purpose of the Component in relation to the system being threat modelled.
:::{admonition} Common mistake
:class: warning
The `Purpose` given is really generic and doesn't help someone who is not familiar with the system to understand what the Component does.  For instance for a `Database` if you have a `Purpose` of `Stores data` then that doesn't help, so it would be better to say `Persistance storage for Service A that includes PII and password hashes`
:::

In-scope
:  Values must be `Yes` or `No` (this can be localised).  This is an important piece of information as threatware does not require threats to be listed for out-of-scope components.  A system is in-scope if the team completing the threat model:
:  - created the component e.g. wrote the source code, or defined it via configuration
:  - got the component provisioned (e.g a database), or got it on-boarded (e.g. a 3rd Party service or SaaS), and so are responsible for it
:  - they own or operate the component e.g. hosting infrastructure like Kubernetes clusters, cloud accounts, 3rd party services
:::{tip}
It's better to have many small threat models rather than few large threat models.  Try to keep the number of components in-scope for a threat models to < 10 (and aim for ~5).  The more in-scope components
:::

Tech Stack
:  **Only populate for in-scope Components.**  A brief comma-separated list of technologies used to create the Component.  For Components created by the team, usually language and framework is sufficient.  For 3rd Party Components listing the provider is usually sufficient.  This is useful as certain technologies give rise to specific threats, so detailing the stack allows a reviewer to decide if any relevant tech-specific threats should be added.

## Components AuthN and AuthZ Table

The Components Authentication (AuthN) and Authorization (AuthZ) Table captures how each in-scope component authenticates and authorizes requests from each of the different identities that make requests to it.

::::{admonition} Example
Imagine you have a client talking to a server, and the client has a user who authenticates to an Identity Provider via OAuth2, which results in a JWT that is passed to the Server on each request.  Perhaps also the client can talk to the server with an anonymous user for some functionality.  We would capture this with something like:

:::{list-table}
:header-rows: 1
* - Components (In-scope)
  - Identity
  - Authentication
  - Authorization 
* - Server
  - Authenticated Users
  - JWT verified and validated
  - Request evaluated against scopes in JWT
* - 
  - Anonymous Users
  - None
  - Restricted to anonymous functionality
:::
:::{admonition} Common mistake
:class: warning
What's important to hightlight is that the entries are for **requests coming into the Server** and **NOT how the Server authenticates to other components** (this is a common misunderstanding).
:::
::::

This table has the following columns:

Component (In-scope)
:  **Must match the name from the [](./components.md#components-details-table)**.  The name of the Component.  An empty value means use the first non-empty value from a row above i.e. for multiple entries for a Component the Component name only needs to be given once.

Identity
:  The Identity of the user/service/role etc., that initiates the request to the Component.  This will be the Identity given to the principal making the request if authentication succeeds.  It doesn't matter which other Component the request actually comes from, all that matters is what Identity will this Component associate to the request.  For each possible Identity that this Component understands, use a separate row.

Authentication
:  How will the Component authenticate the request e.g. validate a JWT, compare to a password hash, cient certificate, delegate to another Component (i.e. trust the Identity value directly), etc.  Also indicate where the value (i.e. identifier) used for the Identity will come from e.g. a scope in a JWT, username that was part of the request, etc.  If the component does not do authentication, by convention the value `None` is used.

:::{tip}
It can sometimes be difficult to decide if a Component is doing authentication or authorisation.  For instance, is an IP allowlist a form of authentication or a form of authorisation?  We'll let the scholars decide, but in the mean time this guidance might be helpful:
- Authentication will result in a Component assigning a request to a known and specific identifier for that Identity e.g. username, role, group.
- Authorization is a decision about whether or not a request will be executed, and that decision can depend on many different factors, with one of the most common being the Identity assigned to the request.

So what about that IP allowlist?  If it's a set of specific IPs that are supposed to correspond to specific servers, then it's probably authentication.  If it's a network range and any server in that range can make a request, then that doesn't seems like an Identity is being assigned to the request, so it's probably authorization.
:::

Authorization
:  How will the Component authorize the request e.g. check for a specific scope in the JWT, RBAC, delegate to IAM, look up permissions for a user/role, etc.  If the component does not do authorization, by convention the value `None` is used.  When no authorization is performed it means the Component will not place any restriction on whether it executes the request (notwithstanding it can still require an authenticated user).