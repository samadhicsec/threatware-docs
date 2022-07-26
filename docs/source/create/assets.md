# Assets

In threat modelling when we talk about assets we are talking about 'things of value', things that we wish to ensure have the security properties of confidentiality, integrity and availability.  

## What is an asset?
The vast majority of assets that we capture in a threat model are data assets, pieces of data that have value, which could be:
- Personal Data, like names, addresses etc.
- Functional Data, which will be specific to the business purpose of the system being threat modelled, but could be; user's documents, product configurations, product prices, user history etc.
- Business Data, which could be; financial, legal, commercial, marketing, HR etc.

When populating (in the tables described below) data assets, they do not need to be populated as individual pieces of data, but can be a group of data (e.g. a row of data in a database, as `Profile` data instead of listing `name`, `address` etc., as `event data` instead of listing each field in an event).  The key thing to understand is that any data grouped should share the same required security properties and the same storage location.  Individual pieces of data can of course be called out separately, and that would be appropriate for particularly sensitive pieces of data, or data that your business otherwise commonly tracks.

We can also capture resource assets, which are consumable resources that have value (i.e. we want to ensure their confidentiality, integrity and availability), which could be:
- Compute resources, like; VMs, lambdas, OS, etc. - anything where an attacker might be able to run arbitrary code.
- Infastructure resources - any deployable infrastructure where the attacker may be able to influence what gets deployed.
- Network resources - any networking configuration where an attacker may be able to influence the configuration of a network.

These resource assets are only relevant to some systems, and wouldn't often appear in threat models related to business functionality (unless the purpose of the business was to deploy these kinds of resources).  These resource assets would likely appear in threat models related to infrastructure.

## Functional and Technical Assets

The threat model template has two tables used to capture assets within the system being threat modelled, to separately capture Functional Assets and Technical Assets.
- Functional Assets relate to the functionality implemented by the system being threat modelled, and are called out separately because they should represent the "end-goal" assets that an attacker is trying to compromise the security properties of.  If your business is using Domain Driven Design (DDD) to drive the design of your systems then the core data elements of that likely closely align to your Functional Assets
- Technical Assets relate to all the assets that have security properties you want to ensure, but aren't the "end-goal" for an attacker, and compromising one of these would then be used by the attacker to compromise a Functional Asset.

:::{admonition} Example
Imagine you have user data encrypted in a database.  This implies you have an encryption key used for the encryption.  That encryption key is an important asset from a security point of view and you want to ensure its confidentiality, because if it was disclosed to an attacker, they would have the means to decrypt user data in the database.  However, that encryption key should be considered a Technical Asset, because the "end-goal" of an attacker is not to find an encryption key (which by-itself has no value), their "end-goal" is to find an encryption key and then use it to decrypt encrypted user data.  The user data is the "end-goal", and so would be a Functional Asset.
:::

:::{note}
The term "end-goal" should be understood to mean the "end-goal within the scope of the system being threat modelled", so even if the ultimate end-goal of an attacker lay within an out-of-scope system, their "end-goal" with respect to the system being threat modelled should be used when identifying Functional Assets.
:::

## Functional Assets Table

The Functional Assets Table has the following columns:

Category
:  The category or type of the Functional Asset.  This can be any value you like, and is nothing more than a convenience identifier for a group of assets captured in this table.  It allows for threats to be identified that apply to a set of assets.  Since this is a reference name that can be used elsewhere, it must be unique outside of this table (i.e. it can't match a component name, an asset name, a Technical Asset category name).  An empty value means use the first non-empty value from a row above.

Name
:  A short unique name (amongst all names in this threat model) for the asset.  This is the name that will be used elsewhere in the threat model, so it must be unique, and for convienence it should be short.

Description
:  A brief description of the data, or set of data, and what role it plays in the system.  If the asset does represent a small set of data, it is helpful for this description to list the data in the set.

Confidentiality, Integrity and Availability Impact
:  The value for this column should be a sentence that captures the impact, if the Confidentiality, Integrity or Availability of the asset was compromised.  There should be seperate sentence per property and impact (i.e. you could have multiple sentences related to Confidentility).  This field has a special format, as sentences should be prepended with:
   - `Confidentiality:` or just `C:`
   - `Integrity:` or just `I:`
   - `Availability:` or just `A:`
   
   Here some example starts to the sentences you might want to use:
   - `C: An attacker that can read this asset could ...`
   - `I: An attacker that can write this asset could ...`
   
   The end of the sentence should just state a "bad thing" that could happen.  For instance if the asset was a secret key used to encrypt data in a database, the sentence could be `C: An attacker that can read this asset could decrypt data in the database`.  
   
   **At this stage we are totally ignoring the likelihood of the "bad thing" happen, we are totally ignoring any mitigating controls that might exist** (this will be captured in the [](./threats-controls.md#threats-and-controls-table)), we are only concerned with capturing impact.

   :::{admonition} Explanation
   *Why would I include impacts for assets that I know I have already mitigated that impact by controls I have in place?*
   
   Threats exist regardless of how many mitigating controls are in place.  The purpose here is to **acknowledge and convey** that the threat exists, regardless of the **current** risk (i.e. taking existing controls into account).  You can then explain in the [](./threats-controls.md#threats-and-controls-table) what the threat is and what existing controls are in place.  This means the threat model can be **explicit about why** the potential impact to this asset from the threat, has a mitigated risk.

   Consider the alternative: not listing the asset (because there are no possible ways for the assets confidentiality/integrity to be impacted due to existing controls), which also means not listing the controls.  Anyone trying to evaluate the security of your system via the threat model will not know about the asset or controls, so cannot evaluate for themselves if they agree that the risk is mitigated.  This would fail the goal of giving assurance about the security of the system since the author has evaluated and accepted (residual) risk without review.  This also misses the *opportunity* to promote the security of the system by listing existing security controls - listing security controls is important because it gives confidence to any reviewer that the system owners both understand and care about security.
   ::: 

   :::{admonition} Tip
   Novice threat modelling authors may be confused or unclear about what Confidentiality or Integrity mean, so it's often better to simplify this for them by saying: 
   
   "***Confidentiality** means you are concerned about an attacker being able  to **read** the asset*", and 
   
   "***Integrity** means you are concerned about an attacker being about to **write** or change the asset*"
   :::  
   :::{admonition} Common mistake
   :class: warning
   Authors will often feel like they should add an `Availability` impact to every asset, as of course if an asset was not available this would, for most systems, lead to the system failing.  Whilst that is true, it is very rarely the  "end-goal" of an attacker to affect `Availability` by deleting specific pieces of data, and moreover because it is an attack that usually applies to all assets, it would add a lot of noise (and effort) to the threat model to capture it.  Threat Models should liberally include `Availability` impacts (most will have none), as it should be a threat that is captured by a threat model at a lower level (one that handles infrastructure or deployment).
   :::

Storage Location
:  The location where the asset is stored.  This must reference a known location, which can be one of:
   - The Name of a Component from the [](./components.md#components-details-table)
   - A Storage Location listed in the Threat Model Template in either the Functional Assets Table or the Technical Assets Table (in the Storage Location column).

   :::{admonition} Tip
   The purpose of allowing values from the Threat Model Template is that some storage locations are not Components and are instead "storage types" where the security concerns relate to the type rather than the specific Component housing that location.  Some examples:
   - Environment Variables - the security concerns are usually independant of the particular machine
   - File System - the security concerns are usually independant of the particular machine
   - Kubernetes Secret - - the security concerns are usually independant of the specific cluster where they are stored

   Specifying storage types turns out to make specifying threats much more efficient, as threats can be called out that relate to ALL the assets stored in that storage type, which saves having to capture many threats for each asset individually.
   :::

## Technical Assets Table

The Technical Assets Table has the following columns:

Category
:  The category or type of the Technical Asset.  This can be any value you like, and is nothing more than a convenience identifier for a group of assets captured in this table.  It allows for threats to be identified that apply to a set of assets.  Since this is a reference name that can be used elsewhere, it must be unique outside of this table (i.e. it can't match a component name, an asset name, a Functional Asset category name).  An empty value means use the first non-empty value from a row above.

Name
:  A short unique name (amongst all names in this threat model) for the asset.  This is the name that will be used elsewhere in the threat model, so it must be unique, and for convienence it should be short.

Description
:  A brief description of the data, or set of data, and what role it plays in the system.  If the asset does represent a small set of data, it is helpful for this description to list the data in the set.

Confidentiality, Integrity and Availability Impact
:  See the entry for this field under the [](./assets.md#functional-assets-table) above.

Storage Location
:  See the entry for this field under the [](./assets.md#functional-assets-table) above.

Functional Asset(s) Affected
:  As described at the top of this page, Technical Assets are not the "end-goal" of an attacker, and so we use this column to reference the Functional Asset(s) that would be affected by a compromise of a security property of this asset.  The value for this column is a comma-separated list of `Name` or `Category` values from the [](./assets.md#functional-assets-table).

   :::{admonition} Tip
   But what if there is no Functional Asset affected?  When it's not clear which Functional Asset is affected, it usually means either:
   - You are missing a Functional Asset, and so need to add a row to the Functional Asset Table, or perhaps extend the description of an existing entry, or split an existing entry into more granular assets.
   - The Technical Asset you have captured is not an asset that has a security property with an impact that you need to mitigate i.e. there is no impact to a security compromise of the asset.  It's not unreasonable to say that a security compromise of **any** asset is a "bad thing", but if it truely does not affect the security of a Functional Asset, then it is just a "bad thing" with no (or extremely little) business impact, so it's better to exclude it from the threat model so the threat model can focused on the security of the things that do have business value.
   :::

## Non-tangible assets

The threat model template is not designed to capture threats against non-tangible assets such as; reputation, market position, perceived quality, etc.  You can express these as part of the impact for a tangible asset if you think it makes sense to do so (in the author's experience it rarely does).  These non-tangible assets tend to be cross-cutting concerns, not specific to a particular system within a business, and so whilst it may be appropriate to capture these threats somewhere, capturing them in threat models for individual systems tends to just be a burden that increases the effort of creating a threat model for that system, without providing any specific benefit to that system.