# Topology validator

### Process and purpose

Please read the process and purpose at [https://confluence.int.net.nokia.com/display/5GUTE/%5BDRAFT%5D+Sanity+Checks]

Please note that topology validation is meant for testlines used by Cloud Manager. If your testline will not be cloudified use topology: `NON_CM`.

### Usage

#### Adding rules

Rules should be added in the [rules file](./rules.py).
They have specific syntax that has to be followed. Every rule is an instance:
*  of a rule type class (eg. `RequiredParam`), which specifies the type of the rule. Available base classes are listed below.
*  that passes in constructor `parameters` arg (mandatory) where data about specific rules are put. Supported data types are described in supported rules description. 

##### Supported rules:

*  `RequiredParam` is a rule that should contain a list of mandatory parameters. In checked tl config every parameter from list is verified- that it's present and not None.

    __Parameters for this rule:__
    *  `parameters`: list with mandatory parameters. List items should be path to param, including indexes in lists. Example: `tl.ues[0].l1.common_units[0].lmp_connection.password`. Paths should always start with `tl`.

#### Adding topologies

To run rules for topology, rules should be added to topologies in [topologies file](./topologies.py).

It contains rules class, where class variables are topologies with values of lists with required rules.

First, you need to import required rules from ./rules.py file. Then add rule to list in topology or create new topology key if it's not there already.


#### Examples

There already are examples of rules in both linked above files.
