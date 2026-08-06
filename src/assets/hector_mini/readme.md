## known issues

### hector_mini_body.urdf
1. self collision between leg thigh and calf, under convex hull approximation.

### hector_mini_body.xml

1. collision disabled for non-foot links.
2. `<equality>` constraints for `joint` costraint seem invalid, to be validated.

### hector_mini.py

1. missing `armature` value
2. missing actuator model for  gear transmission