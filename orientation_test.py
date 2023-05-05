#!/usr/bin/env python

import tf
import geometry_msgs


def main():
    rot = [-0.0249590815779, 0.999649402929, 0.00737916180073, 0.00486450832011]
    # [3.127081082946684, 0.010094131295008826, -3.0917405985240127]
    euler = [3.127081082946684, 0.010094131295008826, -23.0917405985240127]
    #euler = tf.transformations.euler_from_quaternion(rot)
    print(euler)
    quaternion = tf.transformations.quaternion_from_euler(euler[0], euler[1], euler[2])
    print(quaternion)

if __name__ == "__main__":
  main()
