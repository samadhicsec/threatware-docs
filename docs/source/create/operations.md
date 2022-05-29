# Operational Security

Operational Security relates to the secuirty processes, procedures and governance activities that a team may be responsible for.  

Quite often a team will have no operational security responsibilities, in which case the table does not need to be populated.

:::{admonition}  Example
Imagine a team in a business that is responsible for an internal service that communicates with users via email, and the service takes an email address and a message and forwards it to a 3rd party email service provider.  If that team "own" the management responsibilities of that 3rd party email service provider, such as; 
- owning the administrative account, 
- provisioning and de-provisioning users (for instance members the marketing team that generate email templates using a UI provided by the 3rd party service), 
- configuring the security options of the 3rd party email service provider, etc., 

then that team has operational security responsibilities.  

They need to define; 
- who is allowed access and what roles will exist, 
- who is allowed to authorise access, 
- what access records will be kept, 
- how long will access records be kept, etc.  

They need to define these things because if the 3rd party email service provider contains assets of value, then an attacker may look to gain access to the 3rd party email service provider through non-technical methods, such as social engineering (and the team likely has a responsibility to meet the business' security policy requirements around access control).
:::

:::{admonition} Tip
Often a team with operational security responsibilities for granting other developers access to a system will use the most convenient communications channel (e.g. Slack) to support access requests, and are surprised when the threat model points out that the security of their systems now rely on the security of that channel.  This can often inspire a change towards a channel more commonly used for access requests within a business.
:::

## Operational Security Table

The purpose of the Operational Security Table is to provide a standard set of questions a team should answer in relation to any system where they have opertional security responsiblilities, which usually means that team is responsible for the access control to that system (this does not normally include systems that the team control access to, but no access is granted to people outside the team).

The questions in the template are meant to be a basic usuable list of questions, and should be customised in the template (by changing them or adding rows for more questions) to suit a particular business.

The table can accomodate multiple operational security responsibilities by adding new **columns** to the right of the last column (i.e. resulting in multiple `Answers` columns).

The table has the following columns:

Questions
:  The operational security questions a team should answer.  The question in the first row is usually to ask for a description of system the remaining operational security questions will relate to e.g. `What is the name of the system you team has operational responsibility for controlling access to?`.

Answers
:  Answer to the operational security question in the `Questions` column of that row.  If a team has no operational security responsibilities then all rows in this column should be left empty.