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

Components often correspond to deployable units' of artifacts.  The level of granularity of a sub-system that constitutes a Component should lean towards a single deployable thing e.g. a Kubernetes Pod and not the individual containers, a container hosted in ECS, a combined web and application server (if co-hosted), a OS process but not its libraries etc.    

Start at a higher level and break apart Components as required.  When populating the threat model it often becomes apparent that it would be easier to express an authentication method, or an asset storage location, or threat or control, if a specific sub-system was called out as a Component, so it's unusual to get the list of Components complete on a first draft of a threat model, and the table becomes more complete as iterative work on the threat model happens.

Minimise infrastructure included as Components, especially if it makes sense for it to have its own threat model. It's typical to not include supporting infrastructure that is otherwise transparent to the systems containing the business logic or performing related tasks.  For instance we would not normally include; load balancers, proxies, DNS, etc., but if any of these implemented specific security controls for the system you may want to include them as Components (but often just listing them as a control in the Threats & Control Table is easier).  The threats related to this supporting infrastructure is usually best handled in it's own dedicated threat model (where the question 'What is a Component?' has a totally different answer), and usually it's a threat model that can specifically focus on infrastructure threats, and becomes a companion threat model for application-level threat models.

Practically speaking, if there is any kind of design documentation for a system then the various systems defined in that make an ideal starting point for a list of Components.

## Components Diagram

This should contain a diagram showing all, or at least the major components of the system being threat modelled.  Use an existing diagram if you have one, even if it is is not perfect or completely up to date (the [](./components.md#components-details-table) will be the accurate record of what the system comprises of).  If you have to create a new diagram, keep it simple to begin with, just trying to capture the major components.

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
It's a common mistake to state a `Purpose` that is really generic and doesn't help someone who is not familiar with the system to understand what the Component does.  For instance for a `Database` if you have a `Purpose` of `Stores data` then that doesn't help, so it would be better to say `Persistance storage for Service A that includes PII and password hashes`
:::

In-scope
:  Values must be `Yes` or `No` (this can be localised).  This is an important piece of information as threatware does not require threats to be listed for out-of-scope components.  A system is in-scope if the team completing the threat model:
:  - created the component e.g. wrote the source code, or defined it via configuration
:  - got the component provisioned (e.g a database), or got it on-boarded (e.g. a 3rd Party service or SaaS), and so are responsible for it
:  - they own or operate the component e.g. hosting infrastructure like Kubernetes clusters, cloud accounts, 3rd party services
:::{tip}
It's better to have many small threat models rather than a few large threat models.  Try to keep the number of components in-scope for a threat models to < 10 (and aim for ~5).  The more in-scope components the larger the threat model becomes and more time it takes to complete.
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

## Guidance on populating AuthN and AuthZ Table

There is a huge range of possible authentication and authorisation approaches in use today.  That makes it hard to accurately and consistently capture how a Component authenticates and authorises requests coming into it.  Below is some guidance on how to capture authentication and authorisation information for a Component.

To begin, you need to populate the AuthN and AuthZ Table with all the in-scope Components from the Components Details Table.  That would look something like:

:::{table}
:align: center
| Component (In-scope) | Identity | Authentication | Authorization |
| -------------------- | -------- | -------------- | ------------- |
| ComponentA | | | |
| ComponentB | | | |
| ComponentC | | | |
:::
Now, taking each Component one at a time, we need to populate the Identity, Authentication and Authorisation columns for that Component's row.

### Describe Identities

First we need to think about the identities that a Component knows about.  You can add additonal rows for each identity the Component accepts requests from.  Below is a flow-chart to help with determining what identities to add for a Component.

```{mermaid}
:align: center
flowchart TD
    classDef default fill:#aed6f1
    A[Start] --> Input{{"Does the component listen for external input i.e. requests"}}
    Input -->|Yes| Proxy{{"Does the component just proxy the requests?\n(aware of only transport layer (e.g. TCP/UDP)\ne.g. firewall, load balancer, gateway)"}}
    Input -->|No| InputN["A single row with #quot;n/a#quot; across all columns\nOptional: In Identity column: #quot;n/a (#lt;explanation>)#quot;"]
    Proxy -->|Yes| ProxyY["Add a generic description for the requests\ne.g. #quot;Network Traffic#quot;"]
    Proxy -->|No| Requests["Consider the range of request types\nthat come <b>INTO</b> the Component\n and who they are trying to serve.\n(Not including login)"]
    Requests -->|For each request type| IDs{{"Is there an identity present in the request?\n(explicitly or available via session information lookup)\nE.g. username, session ID, JWT, HTTP header with certificate CN"}}
    IDs -->|Yes| Many["Add a new Identity entry row for each\ngroup/explicit identity type/category/role/set,\npossible in the request type\n"]
    IDs -->|No| Single["A single Identity entry describing the\nimplicit/implied/assumed identity associated to the requests\ne.g. Internal Services, Anonymous Users,\nAuthenticated Users, #lt;component name>"]
    
```

Having done this for one Component row you could have a table like:

:::{table}
:align: center

| Component (In-scope) | Identity     | Authentication | Authorization |
| -------------------- | --------     | -------------- | ------------- |
| ComponentA           | Users        | | |
|                      | Admins       | | |
|                      | ComponentC   | | |
| ComponentB | | | |
| ComponentC | | | |

:::

::::{admonition} FAQ
Q: Why does the guidance say "Not including login" when considering different request types?
:  See Authentication FAQ question "**Should I add a row for an 'Anonymous' caller, for requests made before they login?**"
::::

### Describing Authentication

With a set of identities captured in different rows we now need to add authentication details to each row.  

We are going to capture 2 different aspects to authentication:
- **Login Authentication.**  This can happen when a Component receives an initial credential as part of a request, and can map that credential to a known user.  Not all Components handle login authentication themselves.  Some Components delegate this to other Components.  The login process can involve multiple steps, but we aren't looking to capture that complexity in this table.  Often a session token/identifier is the result of login authentication.
- **Session Authentication.**  This can happen when a Component receives a session token or identifier that they can use to determine the identity associated with a request.  The session token/identifier is usually validated in some way before the associated identity is trusted.  It's possible there is no session authentication e.g.
  - HTTP's 'Basic Auth' sends through a username and password on every request,
  - An API token given to a client and used on every request,
  - A client certificate used to establish a mutual-TLS connection

Continuing on from the flow chart for describing identity (the output of the below flow chart should be captured in the Authentication column for the corresponding Identity).

```{mermaid}
:align: center
flowchart TD
    classDef default fill:#f9e79f 
    classDef id fill:#aed6f1
    Many[Add a new Identity entry row for each\ngroup/explicit identity type/category/role/set,\npossible in the requests]:::id --> Login{{Does the component itself do\n'login' authentication?}}
    Single["A single Identity entry describing the\nimplicit/implied/assumed identity associated to the requests\ne.g. Internal Services, Anonymous Users,\nAuthenticated Users, #lt;component name>"]:::id --> IDN["#quot;None#quot;"]
    Login -->|Yes| LoginItself[Describe login authentication.\nGive description including\nprotocol and checks made]
    Login -->|No| LoginDelegate["#quot;Login authentication delegated to #lt;component name>#quot;"]
    LoginItself --> Session{{Does the component itself do\n'session' authentication?}}
    LoginDelegate --> Session
    Session ---->|Yes| SessionD[Describe session authentication.\nGive description including\nprotocol and checks made]
    Session -->|No, another component does| Delegate["#quot;Session authentication delegated to #lt;other component name>#quot;.\nOptional: Describe session authentication"]
    Delegate -->|Description guidance| DescGuid{{Is the other component\nin-scope?}}
    DescGuid -->|Yes| InScope["#quot;Session authentication delegated\nto #lt;other component name>#quot;."]
    DescGuid -->|No| NotInScope["#quot;Session authentication delegated\nto #lt;other component name>#quot;.\nGive protocol used."]
    Session ---->|No, there is no session token| Continue["Continue"]
```

In terms of what information about Authentication to capture, the goal here is to capture:
  - Whether authentication happens
  - Who does the authentication
  - What protocols/procedures for authentication are implemented
  - What validation is performed (if relevant)

It's also a good idea to link to more information if possible.

Having captured authentication for the various identities known to this Component, you could have a table like:

:::{table}
:align: center

| Component (In-scope) | Identity     | Authentication | Authorization |
| -------------------- | --------     | -------------- | ------------- |
| ComponentA           | Users        | Login authentication via user name and password.<br />Session authentication via opaque session token. | |
|                      | Admins       | Login authentication delegated to Corporate SSO.<br />Session authentication via JWTs.  JWT signature is validated. | |
|                      | ComponentC   | None | |
| ComponentB | | | |
| ComponentC | | | |

:::

:::{hint}
A common security issue is discovering that different Components in a system are applying different levels of validation when they authenticate a certain identity type.
:::

::::{admonition} FAQ
Q: Should I add a row for an 'Anonymous' caller, for requests made before they login?
:   You should only capture "Anonymous" callers to a Component if the Component is designed to take anonymous traffic (and we do not count the initial anonymous request for a user to login, that is just assumed).  So a website Component that is publicly browsable could have a row for an "Anonymous" Identity.  However, the same website that forces a user to immediately login wouldn't have an "Anonymous" row.  It is better to just capture Identities that the Component is expecting to deal with.  Otherwise every Component would have to have an "Anonymous" Identity row because every Component that can receive network traffic could in-theory recieve an anonymous request, but since it's always true it's just noise in the threat model document.

Q: The authentication protocol my Component uses involves multiple stages and multiple flows, do I need to capture this process as multiple rows?
:   No.  The purpose of the row is not capture detail on the authentication process (e.g. every OAuth2 redirect), but rather to capture the methods and protocols used for authentication, by the Component, for the different types of callers (i.e. identities) the Component receives, and any relevant validation done to confirm those identities.  Detailed information about authentication protocols can be captured (if beneficial) in the Diagrams section.

Q: How do I decide whether an authentication method is 'login' or 'session'?
:   A classic login authentication method is username and password.  However many systems enforce password expiry, meaning the password is only valid for a period of time.  So while a 'session' implies something valid for a period of time, 'time' is not the only factor to use to distinguish between login and session authentication, because passwords can be time limited, but are clearly not a session authentication method (the same applies to API keys and client certificates - in fact there should be few if any 'permanent' credentials).  In practice, a session token will usually also have a significantly shorter lifetime than login credentials (and so be wary of anyone trying to minimise security controls for so-called "session tokens" that live as long as login credentials).
:   Another factor to identify a session authentication method is whether the authentication information in the request used was obtained by the *exchange* of other credentials (i.e. login credentials).  This is still not definitive though, as some authentication methods effectively exchange login credentials for other login credentials e.g. OAuth2 refresh token.  

Q: What does "None" mean?
:   *None* can mean different things:
    - Requests to the Component are unauthenticated.  The Component does not know who the caller is, it does not associate any identity with the caller.
    - Even when another Component in the request path before this Component does authenticate the caller, if that identity is NOT passed to this Component, then "None" is still the approriate answer.  Whilst the larger system may have authenticated the caller, this component does not know the identity of the caller, and moreover an appropriately positioned attacker in the system can make arbitrary calls to the Component.
    - If the Component is sent an actual Identity but never consumes/processes that Identity (e.g. it's set in an HTTP header the Component doesn't read), then "None" is still the approriate answer. In this case not consuming/processing that Identity makes it equivlant to not knowing it in the first place.
      - If the Identity is logged then that's relevant from a repudiation perspective, but not an authentication perspective.
::::

### Describing Authorisation
One of the main reasons authentication is so important to security is that the resulting identity is often used to apply authorisation to the request coming from the caller.  Ultimately the point of trying to capture information about authorisation is to determine whether the component implements the concept that certain callers are allowed to perform certain actions, whilst other callers are prevented from performing certain actions.  In practice though a component itself isn't the only thing to consider when deciding what can invoke its functionality, that's why we consider the following (complimentary, not mutually exclusive) aspects of authorisation:
- **Access to the component.**  Some components don't implement authorisation themselves, but rely entirely on another component restricting access to them.  This other component "enforces" authorisation on behalf of the component.  It's common for the component to enforce some authorisation itself, in addition to the access restriction.
- **Access to the resources.**  This is traditional authorisation or access control.  A component implements actions on resources and needs to control who can do which action.  There are many different methods to achieve this.

Continuing on from the flow chart for describing authentication (the output of the below flow chart should be captured in the Authorisation column for the corresponding Identity).

```{mermaid}
:align: center
flowchart TD
    classDef default fill:#abebc6
    classDef auth fill:#f9e79f
    A[From authentication]:::auth --> Access{{"Is (e.g. network) access to the component\nrestricted by another (intermediary) component?"}}
    Access -->|Yes| AccessY["Provide description i.e. &quot;Access\ndelegated to #lt;other component name>&quot;.\nOptional: Describe conditions of access"]
    Access -->|No| Authz{{"Does this component itself decide on \nany kind of restrictions for any type of caller?"}}
    AccessY --> Authz
    Authz -->|No| PDP{{"Does this component completely outsource access\ndecisions to another component\ni.e. a Policy Decision Point (PDP)"}}
    PDP -->|Yes| PDPDelegate["&quot;Delegated to #lt;PDP component>&quot;"]
    PDPDelegate --> PDPY{{Is the PDP in-scope?}}
    PDPY --> |No| PDPinscopeN["Also describe (high level) what the identity can do,\nand what permissions(etc) are required.\nLink to config for brevity."]
    PDP -->|No| None["&quot;None&quot;"]
    Authz -->|Yes| Single{{Is there effectively a single account\nconfigured that can perform any action?}}
    Single -->|Yes| None
    Single -->|No| Perms{{"Are permissions/roles/policies/capabilities/scopes (etc)\nused to decide access?"}}
    Perms -->|Yes| PermsY["Describe (high level) what the identity can do,\nand what permissions(etc) are required.\nLink to config for brevity."]
    PermsY --> Own
    Perms -->|No| Own{{"Can the identity only perform some actions on resources they own?\n(e.g. UPDATE resource WHERE id == $username)"}}
    Own -->|Yes| OwnY["Add &quot;Actions restricted to owned resources&quot;"]
    Own -->|No| OwnN["Describe how component decides what identities can do.\nLink to config for brevity."]
    OwnY --> Finish["Finish"]
    OwnN --> Finish
    PDPY -->|Yes| Finish
    PDPinscopeN --> Finish
    None --> Finish
```

Having captured authentication for the various identities known to this Component, you could have a table like:

:::{table}
:align: center

| Component (In-scope) | Identity     | Authentication | Authorization |
| -------------------- | --------     | -------------- | ------------- |
| ComponentA           | Users        | Login authentication via user name and password.<br />Session authentication via opaque session token. | Actions restricted to owned resources |
|                      | Admins       | Login authentication delegated to Corporate SSO.<br />Session authentication via JWTs.  JWT signature is validated. | Access delegated to jumpbox<br />JWT scopes used to decide on allowed actions |
|                      | ComponentC   | None | Access delegated to service mesh policy |
| ComponentB | | | |
| ComponentC | | | |
:::

:::{hint}
A common security issue is discovering that an identity in a system has different levels of permission to act on the same type of resource because different Components have applied different access control policies/permissions (etc.) to the identity when it makes a request regarding the resource (as both Components have functionality for that resource.)
:::

::::{admonition} FAQ

Q: The authorisation decisions my Component makes are complicated, do I need to capture them in detail?
:   No.  The purpose of the row is to capture just enough detail on the authorisation controls to convey to the reader what controls are in place, and (ideally) provide them links to where they can get more detail if they want it.

Q: What does "None" mean?
:   *None* can mean different things:
    - The component doesn't implement any authorisation itself, nor does it rely on another component to implement authorisation for it.
    - Even when the Component has the capability to perform authorisation, if it has been configured with a single "admin" account (that has admin privileges), then we also capture "None" as this means component is not configured to restrict actions between different callers (because there is a single caller type), so isn't performing any authorisation.  The logic being that if a caller can authenticate to the component (using the single admin account configured) then they can do anything, so in essence the ability to authenticate is the authorisation control the component uses.
::::

### Examples

The below are imaginary examples showing what might end up being in the AuthN/Z table.  Do not copy these without doing the work to confirm they are appropriate for your system.

:::{table}
:align: center

| Component (In-scope) | Identity     | Authentication | Authorization |
| -------------------- | --------     | -------------- | ------------- |
| Web Application      | Users | Login authentication delegated to supported<br />Identity provider (e.g. Google) via OIDC<br />Session authentication via session cookies | Actions restricted to owned resources | 
| Database             | Web Application | Username and password | None |
| S3 Bucket            | User | Delegated to IAM via signed URL | S3 bucket resource policy |
|                      | Operations | Delegated to company SSO | S3 Ops IAM Policy associated with Ops IAM Role |
| API                  | Client | Login authentication via IdP<br />Session authentication via JWT | JWT scopes |
|                      | Different Client | API Key | Permissions assigned to API key |
| Internal Service     | Another Internal Service | None | Access delegated to K8 networking.<br />Only accessible to other K8 services. |
| Web service          | 3rd party service | mTLS client certificate | 3rd Party Role assigned to identity |
| AWS Service          | My Service running in AWS | AWS session token from EC2 metadata | Delegated to AWS IAM using policy. |
| Kubernetes           | Microservice (as a Service Account) | Delegated to Kubernetes admission controller<br />via deployment resource definition | Delegated to Kubernetes admission controller<br />via deployment resource definition |
| CSP Account          | Operations, Developers, Auditors | Delegated to company SSO | IAM Policy associated with IAM Role | 
| Firewall             | Network traffic | None | Source IP based ACLs |
| Cron job             | n/a (doesn't support incoming requests) | n/a | n/a |
| Notepad.exe          | Developer | None | None |
| sudo                 | Local User | Delegated to OS | sudoers file |
| Remote Workstation   | Remote user | SSH Key | OS permissions assigned to local group user is member of |
| Local Filesystem     | Web Service | Delegated to OS user authentication | Delegated to OS file system ACLs |

:::