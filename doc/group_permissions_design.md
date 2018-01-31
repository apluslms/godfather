# Group and Permissions Design

## Overview
A group can have many subgroups inside it, and at the same time a group can have only 1 parent group. It resembers a directory behavior or a nested items list:
* Group 1
  * Group 1.1
  * Group 1.2
    * Group 1.2.1
    * Group 1.2.2
    
In a real world example, imagine maintaining all courses in CS department:
* CS Department Group
  * DataBase Group
  * Distributed System Group
    * Cloud Computing Group
    
## Membership
* Administrator
  * Create a subgroup
  * Add and remove members
  * Assign course permissions to members
* Member

## Subgroups
With subgroups(aka nested groups or hierarchical groups) you can have up to * levels of nested groups, which among other things can help you to:
* Make it easier to manage people and control permissions to multiple courses.
* When you add a member to a subgroup, they inherit the membership and permission level from the parent group. This model allows access to nested groups if you have membership in one of its parents.
* The group permissions for a member can be changed only by Administrator and on the Members page of the group the member was added.
* You can tell a member's permissions by looking at the group's Members page.

## Course Permissions
* View all courses under control
* Edit course location (git)
* Create new course
* Course upload



